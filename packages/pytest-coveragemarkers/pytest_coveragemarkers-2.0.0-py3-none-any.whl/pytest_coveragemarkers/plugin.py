import pytest

from .coverage_markers import (
    coveragemarker_pytest_addoption,
    coveragemarker_pytest_collectreport,
    coveragemarker_pytest_configure,
    get_cov_markers_from_test,
    update_test_with_cov_markers,
    validate_marker_values,
)
from .filtering import apply_filter_rule, filtering_pytest_addoption

PLUGIN_GROUP = "coveragemarkers"


def pytest_addoption(parser):
    group = parser.getgroup(PLUGIN_GROUP)

    filtering_pytest_addoption(group=group, parser=parser)
    coveragemarker_pytest_addoption(group=group, parser=parser)


def pytest_configure(config):
    coveragemarker_pytest_configure(config=config)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    if config.coverage_markers_enabled:
        update_test_with_cov_markers(items=items)
        apply_filter_rule(config=config, items=items)


@pytest.hookimpl(tryfirst=True)
def pytest_collectreport(report):
    """
    Record coverage marker details on each item in the collection report.
    This is so collect-only output shows cov markers too
    """
    coveragemarker_pytest_collectreport(report)


@pytest.mark.optionalhook
def pytest_json_runtest_metadata(item):
    return get_cov_markers_from_test(item=item)


@pytest.fixture(autouse=True)
def cov_markers(request):
    """fixture for setting gs_applicaton in test metadata"""
    # TODO: Need to pass in name and allowed_args into this fixture
    if request.config.coverage_markers_enabled:
        validate_marker_values(request=request)
