""" Handlers for an RPM dependency chain model.

The idea here is that these are two of what will eventually be many handlers
that build and maintain a dependency chain in PDC.

There are two handlers here.  They both respond to koji 'tag' events. One of
them figures out what the build required at *build* time, and updates PDC with
that. The other figures out what the build requires at *run* time, and updates
PDC with that.

"""

import collections
import logging
import multiprocessing.pool
import time

import pdcupdater.handlers
import pdcupdater.services
from pdcupdater.utils import (
    tag2release,
    interesting_tags,
)


log = logging.getLogger(__name__)


class BaseRPMDepChainHandler(pdcupdater.handlers.BaseHandler):
    """ Abstract base class. """

    # A list of the types of relationships this thing manages.
    # This needs to be overridden by subclasses of this base class.
    managed_types = None

    def _yield_koji_relationships_from_build(self, koji_url, build_id, rpms=None):
        raise NotImplementedError("Subclasses must implement this.")

    def __init__(self, *args, **kwargs):
        super(BaseRPMDepChainHandler, self).__init__(*args, **kwargs)
        self.koji_url = self.config['pdcupdater.koji_url']
        self.io_threads = self.config.get('pdcupdater.koji_io_threads', 8)

    @property
    def topic_suffixes(self):
        return ['buildsys.tag']

    def can_handle(self, msg):
        if not any([msg['topic'].endswith(suffix)
                    for suffix in self.topic_suffixes]):
            return False

        # Ignore secondary arches for now
        if msg['msg']['instance'] != 'primary':
            log.debug("From %r.  Skipping." % (msg['msg']['instance']))
            return False

        interesting = interesting_tags()
        tag = msg['msg']['tag']

        if tag not in interesting:
            log.debug("%r not in %r.  Skipping."  % (tag, interesting))
            return False

        return True

    def _yield_managed_pdc_relationships_from_release(self, pdc, release_id):
        for relationship_type in self.managed_types:
            entries = pdc.get_paged(
                pdc['release-component-relationships']._,
                from_component_release=release_id,
                type=relationship_type,
            )
            for entry in entries:
                # Filter out any irrelevant relationships (those of some type
                # managed by a different pdc updater Handler).
                relationship_type = entry['type']
                if relationship_type not in self.managed_types:
                    continue

                # Construct and yield a three-tuple result.
                keys = ('name', 'release')
                parent = dict(zip(keys, [entry['from_component'][key] for key in keys]))
                child = dict(zip(keys, [entry['to_component'][key] for key in keys]))
                yield parent, relationship_type, child

    def _yield_koji_relationships_from_tag(self, pdc, tag):

        release_id, release = tag2release(tag)
        # TODO -- this tag <-> release agreement is going to break down with modularity.

        pdcupdater.utils.ensure_release_exists(pdc, release_id, release)

        builds = pdcupdater.services.koji_builds_in_tag(self.koji_url, tag)

        working_build_id = None
        rpms = []
        for i, build in enumerate(builds):
            if not working_build_id:
                working_build_id = build['build_id']

            if working_build_id == build['build_id']:
                rpms.append(build)
                if i != len(builds) - 1:
                    continue

            def _format_rpm_filename(build):
                # XXX - do we need to handle epoch here?  I don't think so.
                return "{name}-{version}-{release}.{arch}.rpm".format(**build)

            rpms = [_format_rpm_filename(rpm) for rpm in rpms]
            log.info("Considering build idx=%r, (%i of %i) with %r" % (
                build['build_id'], i, len(builds), rpms))

            relationships = list(self._yield_koji_relationships_from_build(
                self.koji_url, build['build_id'], rpms=rpms))

            # Reset our loop variables.
            rpms = []
            working_build_id = build['build_id']

            for parent_name, relationship_type, child_name in relationships:
                parent = {
                    'name': parent_name,
                    'release': release_id,
                    #'global_component': build['srpm_name'],  # ideally.
                }
                child = {
                    'name': child_name,
                    'release': release_id,
                }
                yield parent, relationship_type, child

    def handle(self, pdc, msg):
        tag = msg['msg']['tag']
        release_id, release = tag2release(tag)

        # TODO -- this tag <-> release agreement is going to break down with modularity.
        pdcupdater.utils.ensure_release_exists(pdc, release_id, release)

        build_id = msg['msg']['build_id']

        # Go to sleep due to a race condition that is koji's fault.
        # It publishes a fedmsg message before the task is actually done and
        # committed to their database.  In the next step, we try to query
        # them -- but if the task isn't done, we get an exception.
        #
        # Here's the koji branch that has some code which will ultimately let
        # us get rid of this sleep statement:
        # https://github.com/mikem23/koji-playground/commits/post-commit-callback
        time.sleep(1)

        # We're going to do things in terms of bulk operations, so first find
        # all the relationships from koji, then find all the relationships from
        # pdc.  We'll study the intersection between the two sets and act on
        # the discrepancies.
        log.info("Gathering relationships from koji for %r" % build_id)
        koji_relationships = set(self._yield_koji_relationships_from_build(
            self.koji_url, build_id))

        # Consolidate those by the parent/from_component
        by_parent = collections.defaultdict(set)
        for parent_name, relationship, child_name in koji_relationships:
            by_parent[parent_name].add((relationship, child_name,))

        # Finally, iterate over all those, now grouped by parent_name
        for parent_name, koji_relationships in by_parent.items():
            # TODO -- pass in global_component_name to this function?
            parent = pdcupdater.utils.ensure_release_component_exists(pdc, release_id, parent_name)

            log.info("Gathering from pdc for %s/%s" % (parent_name, release_id))
            pdc_relationships = set(self._yield_pdc_relationships_from_build(
                pdc, parent['name'], release_id))

            to_be_created = koji_relationships - pdc_relationships
            to_be_deleted = pdc_relationships - koji_relationships

            log.info("Issuing bulk create for %i entries" % len(to_be_created))
            pdcupdater.utils.ensure_bulk_release_component_relationships_exists(
                pdc, parent, to_be_created, component_type='rpm')

            log.info("Issuing bulk delete for %i entries" % len(to_be_deleted))
            pdcupdater.utils.delete_bulk_release_component_relationships(
                pdc, parent, to_be_deleted)

    def audit(self, pdc):
        present, absent = set(), set()
        tags = interesting_tags()

        for tag in tags:
            log.info("Starting audit of tag %r of %r." % (tag, tags))
            release_id, release = tag2release(tag)

            # Query Koji and PDC to figure out their respective opinions
            koji_relationships = list(self._yield_koji_relationships_from_tag(pdc, tag))
            pdc_relationships = list(self._yield_managed_pdc_relationships_from_release(pdc, release_id))

            # normalize the two lists, and smash items into hashable strings.
            def _format(parent, relationship_type, child):
                return "%s/%s %s %s/%s" % (
                    parent['name'], parent['release'],
                    relationship_type,
                    child['name'], child['release'],
                )
            koji_relationships = set([_format(*x) for x in koji_relationships])
            pdc_relationships = set([_format(*x) for x in pdc_relationships])

            # use set operators to determine the difference
            present = present.union(pdc_relationships - koji_relationships)
            absent = absent.union(koji_relationships - pdc_relationships)

        return present, absent

    def initialize(self, pdc):
        tags = interesting_tags()
        tags.reverse()

        for tag in tags:
            log.info("Starting initialize of tag %r of %r." % (tag, tags))
            release_id, release = tag2release(tag)
            pdcupdater.utils.ensure_release_exists(pdc, release_id, release)

            # Figure out everything that koji knows about this tag.
            koji_relationships = self._yield_koji_relationships_from_tag(pdc, tag)

            # Consolidate those by the parent/from_component
            children = []
            old_parent = None
            for parent, relationship, child in koji_relationships:
                # This only gets triggered the first time through the loop.
                if not old_parent:
                    old_parent = parent

                # If switching to a new parent key, then issue bulk create
                # statements for each parent
                if parent != old_parent:
                    pdcupdater.utils.ensure_bulk_release_component_relationships_exists(
                        pdc, parent, children, component_type='rpm')
                    # Reset things...
                    children = []
                    old_parent = parent

                children.append((relationship, child['name'],))

    def _yield_pdc_relationships_from_build(self, pdc, name, release):
        for relationship_type in self.managed_types:
            entries = pdc.get_paged(
                pdc['release-component-relationships']._,
                from_component_name=name,
                from_component_release=release,
                type=relationship_type,
            )
            for entry in entries:
                # Filter out unmanaged types (just to be sure..)
                if entry['type'] not in self.managed_types:
                    continue
                yield entry['type'], entry['to_component']['name']


class NewRPMBuildTimeDepChainHandler(BaseRPMDepChainHandler):
    """ When a build gets tagged, update PDC with buildroot info. """

    # A list of the types of relationships this thing manages.
    managed_types = ('RPMBuildRequires', 'RPMBuildRoot')

    def _yield_koji_relationships_from_build(self, koji_url, build_id, rpms=None):

        # Get all RPMs for a build... only if they're not supplied.
        if not rpms:
            build, rpms = pdcupdater.services.koji_rpms_from_build(
                koji_url, build_id)

        # https://pdc.fedoraproject.org/rest_api/v1/rpms/
        results = collections.defaultdict(set)

        def _get_buildroot(filename):
            log.debug("Looking up buildtime deps in koji for %r" % filename)
            return filename, pdcupdater.services.koji_list_buildroot_for(
                self.koji_url, filename)

        # Look up the *build time* deps, in parallel.  Lots of I/O wait..
        pool = multiprocessing.pool.ThreadPool(self.io_threads)
        buildroots = pool.map(_get_buildroot, rpms)
        pool.close()

        for filename, buildroot in buildroots:
            parent = filename.rsplit('-', 2)[0]

            for entry in buildroot:
                child = entry['name']

                if entry['is_update']:
                    relationship_type = 'RPMBuildRequires'
                else:
                    relationship_type = 'RPMBuildRoot'

                results[parent].add((relationship_type, child,))

        for parent in results:
            for relationship_type, child in results[parent]:
                yield parent, relationship_type, child


class NewRPMRunTimeDepChainHandler(BaseRPMDepChainHandler):
    """ When a build gets tagged, update PDC with rpm dep info. """

    # A list of the types of relationships this thing manages.
    managed_types = ('RPMRequires',)

    def _yield_koji_relationships_from_build(self, koji_url, build_id, rpms=None):

        # Get all RPMs for a build... only if they're not supplied.
        if not rpms:
            build, rpms = pdcupdater.services.koji_rpms_from_build(
                koji_url, build_id)

        results = collections.defaultdict(set)

        def _get_requirements(filename):
            log.debug("Looking up installtime deps in koji for %r" % filename)
            return filename, pdcupdater.services.koji_yield_rpm_requires(
                self.koji_url, filename)

        # Look up the *build time* deps, in parallel.  Lots of I/O wait..
        # Look up the *install time* deps, in parallel.  Lots of I/O wait..
        pool = multiprocessing.pool.ThreadPool(self.io_threads)
        requirements = pool.map(_get_requirements, rpms)
        pool.close()

        for filename, requirements in requirements:
            parent = filename.rsplit('-', 2)[0]

            for name, qualifier, version in requirements:
                # XXX - we're dropping any >= or <= information here, which is
                # OK for now.  All we need to know is that there is a
                # dependency.
                results[parent].add(('RPMRequires', name,))

        for parent in results:
            for relationship_type, child in results[parent]:
                yield parent, relationship_type, child
