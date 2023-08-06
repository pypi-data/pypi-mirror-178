import contextlib
from distutils.version import StrictVersion as V

from pip import __version__
from pip._internal.operations.prepare import RequirementPreparer
from pip._internal.req import parse_requirements as pip_parse_requirements


try:
    from pip._internal.index.package_finder import PackageFinder
except ImportError:
    from pip._internal.index import PackageFinder


__all__ = ["get_requirement_tracker"]

PIP_VERSION = V(__version__)


class CompatRequirementTracker:
    def __enter__(self):
        return None

    def __exit__(self, *args):
        return None


class CompatBuildTracker:
    def track(self, req):
        return CompatRequirementTracker()


def get_requirement_tracker():
    if PIP_VERSION < V("22.1"):
        from pip._internal.req.req_tracker import get_requirement_tracker

        return get_requirement_tracker()
    else:
        return CompatRequirementTracker()


def is_dir_url(link):
    return link.is_existing_dir()


def is_file_url(link):
    return link.is_file


def is_vcs_url(link):
    return link.is_vcs


def get_dist_from_abstract_dist(abstract_dist):
    if PIP_VERSION >= V("20.3"):
        return abstract_dist
    else:
        return abstract_dist.get_pkg_resources_distribution()


def get_package_finder(session):
    from pip._internal.index.collector import LinkCollector
    from pip._internal.models.search_scope import SearchScope
    from pip._internal.models.selection_prefs import SelectionPreferences

    kwargs = {}
    if PIP_VERSION > V("22.3"):
        kwargs["no_index"] = True

    search_scope = SearchScope.create(find_links=[], index_urls=[], **kwargs)

    kwargs = {
        "link_collector": LinkCollector(
            session=session, search_scope=search_scope
        )
    }

    if PIP_VERSION >= V("22.0") and PIP_VERSION < V("22.2"):
        kwargs["use_deprecated_html5lib"] = False

    return PackageFinder.create(
        selection_prefs=SelectionPreferences(allow_yanked=False), **kwargs
    )


def get_requirement_preparer(finder, session, req_tracker):
    kwargs = {
        "require_hashes": False,
        "finder": finder,
        "use_user_site": False,
    }
    if PIP_VERSION < V("20.3"):
        from pip._internal.network.download import Downloader

        kwargs["downloader"] = Downloader(session, progress_bar=None)

    if PIP_VERSION >= V("20.3"):
        kwargs.update(
            {
                "session": session,
                "progress_bar": None,
                "lazy_wheel": False,
            }
        )
        if PIP_VERSION >= V("21.1") and PIP_VERSION < V("22.1"):
            kwargs["in_tree_build"] = False
    else:
        kwargs["wheel_download_dir"] = None

    if PIP_VERSION >= V("22.0"):
        kwargs["verbosity"] = 1

    if PIP_VERSION >= V("22.1"):
        kwargs["check_build_deps"] = True
        kwargs["build_tracker"] = CompatBuildTracker()
    else:
        kwargs["req_tracker"] = req_tracker

    preparer = RequirementPreparer(
        build_dir=None,
        download_dir=None,
        src_dir=None,
        build_isolation=True,
        **kwargs
    )

    def prepare_editable_reqs(req):
        return preparer.prepare_editable_requirement(req)

    return prepare_editable_reqs


def parse_requirements(*args, **kwargs):
    reqs = pip_parse_requirements(*args, **kwargs)
    if PIP_VERSION >= V("20.1"):
        from pip._internal.req.constructors import (
            install_req_from_parsed_requirement,
        )

        reqs = (install_req_from_parsed_requirement(r) for r in reqs)

    return reqs


@contextlib.contextmanager
def setup_global_pip_state():
    if PIP_VERSION < V("20.1"):
        yield
    else:
        from pip._internal.utils import temp_dir

        with contextlib.ExitStack() as exit_stack:
            exit_stack.enter_context(temp_dir.tempdir_registry())
            exit_stack.enter_context(temp_dir.global_tempdir_manager())
            yield


def get_deps_from_dist(dist, extras):
    if PIP_VERSION >= V("21.3"):
        return dist.iter_dependencies(extras)
    else:
        return dist.requires(extras)
