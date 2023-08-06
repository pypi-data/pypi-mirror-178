"""
if cli/ini stores data supplied then is it stored in one attrib on config?

"""

import json
from pathlib import Path

import pytest

from ..utils import log
from .filter_engine import check_rules

FILTER_OPTION = "--marker-filter"
FILTER_LOCATION_OPTION = "--filter-location"
FILTER_LOCATION_INI_KEY = "FilterLocation"


class FilterLocationFileNotFound(Exception):
    pass


class BadJSONFormat(Exception):
    pass


def get_supplied_filter(*, config):
    return config.getoption(FILTER_OPTION) or None


def get_supplied_filter_location(*, config):
    try:
        return (
            config.getoption(FILTER_LOCATION_OPTION)
            or config.getini(FILTER_LOCATION_INI_KEY)
            or None
        )
    except (KeyError, ValueError):
        return None


def get_marker_filter_path(*, config, location):
    if not location:
        return

    # was absolute path provided
    filter_file = Path(location)
    if filter_file.is_file():
        return str(filter_file)

    # no luck so far so lets try adding root_dir to location
    filter_file = Path(config.rootdir) / location
    if filter_file.is_file():
        return str(filter_file)

    # third time lucky
    filter_file = Path(config.rootdir) / "pytest_coveragemarkers" / location
    if filter_file.is_file():
        return str(filter_file)

    raise FilterLocationFileNotFound(location)


def get_marker_filter_from_location(*, config, location):
    filter_location = get_marker_filter_path(config=config, location=location)
    with Path(filter_location).open(encoding="UTF-8") as source:
        try:
            return json.load(source)
        except json.decoder.JSONDecodeError as exc:
            raise BadJSONFormat(f"Failed to load JSON from: {location}") from exc


def get_marker_filter(config):
    if marker_filter := get_supplied_filter(config=config):
        return json.loads(marker_filter)
    if filter_location := get_supplied_filter_location(config=config):
        return get_marker_filter_from_location(config=config, location=filter_location)


def filtering_pytest_addoption(*, group, parser):

    # Filter section
    group.addoption(
        FILTER_OPTION,
        action="store",
        dest="markerfilter",
        help="Filtering of tests by coverage marker.",
    )

    filter_location_help = "JSON File location of filter specifications."
    group.addoption(
        FILTER_LOCATION_OPTION,
        action="store",
        dest="filterlocation",
        help=filter_location_help,
    )
    parser.addini(
        FILTER_LOCATION_INI_KEY,
        help=filter_location_help,
    )


def filtering_pytest_report_header(config):
    if marker_filter := get_supplied_filter(config=config):
        return f"Marker Filter: {marker_filter}"


def apply_filter_rule(*, config, items):
    if not config.coverage_markers_enabled:
        return

    not_in_group = pytest.mark.skip(reason="Test failed to meet filter rule criteria")

    if filter_spec := get_marker_filter(config=config):
        log.debug(f"Applying filter: {filter_spec}")
        for item in items:
            if not check_rules(rules=[filter_spec], data=item.cov_markers):
                item.add_marker(not_in_group)
