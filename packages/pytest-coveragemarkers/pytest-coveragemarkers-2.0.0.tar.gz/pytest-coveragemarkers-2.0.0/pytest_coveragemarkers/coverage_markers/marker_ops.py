import json
from pathlib import Path

from ..utils import check_values_in_list, ensure_list, log
from ..utils.yml_processing import load_yaml

COVERAGEMARKERS_OFF_OPTION = "--disable-coveragemarkers"
COVERAGEMARKERS_OFF_HELP = "Flag to disable coveragemarkers functionality."
MARKERS_LOCATION_OPTION = "--markers-location"
MARKERS_LOCATION_HELP = "Yaml File location of marker specifications."
MARKERS_LOCATION_INI_KEY = "MarkersLocation"


class InvalidMarkerValue(AssertionError):
    pass


class MarkerLocationFileNotFound(Exception):
    pass


def coveragemarker_pytest_addoption(*, group, parser):
    group.addoption(
        COVERAGEMARKERS_OFF_OPTION,
        action="store_true",
        dest="coveragemarkers_disabled",
        default=False,
        help=COVERAGEMARKERS_OFF_HELP,
    )

    group.addoption(
        MARKERS_LOCATION_OPTION,
        action="store",
        dest="markerslocation",
        help=MARKERS_LOCATION_HELP,
    )
    parser.addini(
        MARKERS_LOCATION_INI_KEY,
        help=MARKERS_LOCATION_HELP,
    )


def coveragemarker_pytest_configure(*, config):
    coverage_markers_enabled(config=config)
    if not config.coverage_markers_enabled:
        return

    markers_spec = dict()

    markers_location = get_marker_path_from_location(config=config)
    if not markers_location:
        config.coverage_markers_enabled = False
        return

    config.coverage_markers_enabled = True
    log.debug(f"Master marker file: {markers_location}")
    load_yaml(markers_spec, markers_location)

    done = {}
    for marker in markers_spec.get("markers", []):
        done.update(include_coveragemarker(marker=marker, config=config))
    setattr(config, "cov_markers", done)


def include_coveragemarker(*, marker, config):
    if marker_name := marker.get("name", ""):
        log.debug(f"Adding marker name: {marker_name}")
        config.addinivalue_line("markers", marker_name)
        return {marker_name: marker}
    return {}


def coverage_markers_enabled(*, config):
    try:
        enabled = config.getoption(COVERAGEMARKERS_OFF_OPTION) or None
        if enabled is None:
            enabled = True
        else:
            enabled = not enabled
    except (KeyError, ValueError):
        enabled = True
    setattr(config, "coverage_markers_enabled", enabled)
    status = "enabled" if enabled else "disabled"
    log.debug(f"CoverageMarkers: {status}")


def get_supplied_marker_location(*, config):
    try:
        return (
            config.getoption(MARKERS_LOCATION_OPTION)
            or config.getini(MARKERS_LOCATION_INI_KEY)
            or None
        )
    except (KeyError, ValueError):
        return None


def get_marker_location_path(*, config, location):
    if not location:
        return

    # was absolute path provided
    location_file = Path(location)
    if location_file.is_file():
        return str(location_file)

    # no luck so far so lets try adding root_dir to location
    location_file = Path(config.rootdir) / location
    if location_file.is_file():
        return str(location_file)

    # third time lucky
    location_file = Path(config.rootdir) / "pytest_coveragemarkers" / location
    if location_file.is_file():
        return str(location_file)

    raise MarkerLocationFileNotFound(location)


def get_marker_path_from_location(*, config):
    location = get_supplied_marker_location(config=config)
    return get_marker_location_path(config=config, location=location)


def update_test_with_cov_markers(*, items):
    """
    Loop through all test items and update their metadata
    """

    for item in items:
        if not hasattr(item, "cov_markers"):
            item.cov_markers = {}
        for mark in item.iter_markers():
            if is_coverage_marker(mark, item.config):
                updates_ = reformat_cov_marker(mark)
                item.cov_markers.update(updates_)
        # output to json report
        content = json.dumps(item.cov_markers)
        log.debug(f"Adding markers to {item.nodeid}: {content}")
        item.add_report_section("setup", "_metadata", content)


def get_cov_markers_from_test(*, item):
    return {"cov_markers": item.cov_markers} if hasattr(item, "cov_markers") else {}


def is_coverage_marker(marker, config):
    if config.coverage_markers_enabled:
        if marker.name in list(config.cov_markers.keys()):
            return True
        log.debug(f"{marker.name} not in {list(config.cov_markers.keys())}")
        return False


def reformat_cov_marker(marker):
    arguments = {}
    for val in reformat_cov_marker_args(marker):
        arguments[val] = True
    return {marker.name: arguments}


def reformat_cov_marker_args(marker):
    """
    Processes the args supplied to a fixture in order to return a simplified
    list containing the args

    """
    simplified = []
    marker_args = ensure_list(marker.args)

    for arg in marker_args:
        if arg:
            if isinstance(arg, list):
                simplified.extend(arg)
            else:
                simplified.append(arg)
    if not isinstance(simplified, list):
        # single value so wrap in list
        simplified = [simplified]
    log.debug(f"Simplified {marker.args} to {simplified}")
    return simplified


def validate_marker_values(*, request):
    for mark in request.node.iter_markers():
        if not is_coverage_marker(mark, request.config):
            break

        allowed_values = request.config.cov_markers.get(mark.name, {}).get(
            "allowed", []
        )

        # no allowed_value so let everything through
        if not allowed_values:
            return

        marker_args = reformat_cov_marker_args(marker=mark)

        if not check_values_in_list(
            source_value=marker_args, allowed_values=allowed_values
        ):
            raise InvalidMarkerValue(
                "{} on {}: {} not in {}".format(
                    mark.name, request.node.name, marker_args, allowed_values
                )
            )


def coveragemarker_pytest_collectreport(report):
    """
    Record coverage marker details on each item in the collection report.
    This is so collect-only output shows cov markers too
    """
    for item in report.result:
        if not hasattr(item, "cov_markers"):
            item.cov_markers = {}
        for mark in item.iter_markers():
            if is_coverage_marker(mark, item.config):
                updates_ = reformat_cov_marker(mark)
                item.cov_markers.update(updates_)
