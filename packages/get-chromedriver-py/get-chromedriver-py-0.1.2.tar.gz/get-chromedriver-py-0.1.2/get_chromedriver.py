"""
Get chromedriver-py version most suitable for your system.
"""
import argparse
import json
import logging
import os
import re
from shlex import split
from subprocess import check_output
from typing import Any, Dict, Union
from urllib.error import HTTPError
from urllib.request import urlopen

__title__ = "get_chromedriver.py"
__version__ = "0.1.2"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2022 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "get_chromium_version",
    "get_closest_version",
    "get_releases_tree",
    "run",
    "run_cli",
)


LOGGER = logging.getLogger(__name__)


def get_chromium_version() -> Union[str, None]:
    """Get chromium version."""

    res = check_output(split("chromium --version"))

    pattern = re.compile(r".*chromium\s([0-9]+(\.[0-9]+)+)\s.*", re.IGNORECASE)
    version = pattern.match(res.decode()).groups()[0]
    LOGGER.debug(f"version={version}")
    return version


def get_releases_tree() -> Dict[str, Any]:
    """Get releases tree."""

    try:
        response = urlopen("https://pypi.org/pypi/chromedriver-py/json")
    except HTTPError as err:
        LOGGER.exception(err)
        return {}

    data = json.loads(response.read())
    releases = list(data["releases"].keys())
    LOGGER.debug(f"releases={json.dumps(releases, indent=2)}")

    releases_tree = {}
    for __version in releases:
        __t = releases_tree  # noqa
        for part in __version.split("."):
            __t = __t.setdefault(part, {"version": __version})

    LOGGER.debug(f"tree={json.dumps(releases_tree, indent=2)}")

    return releases_tree


def get_closest_version(
    try_version: str, tree: Dict[str, Any]
) -> Union[str, None]:
    """Get closest version."""

    if not try_version:
        LOGGER.error("Exhausted trying to get closest version. Quitting.")
        return None

    LOGGER.debug(f"try_version={try_version}")
    _try_version = try_version.split(".")
    if _try_version[0] in tree:
        return get_closest_version(
            ".".join(_try_version[1:]), tree[_try_version[0]]
        )
    else:
        return tree.get("version", None)


def run() -> bool:
    """Entrypoint."""

    version = get_chromium_version()
    releases_tree = get_releases_tree()
    closest_version = get_closest_version(version, releases_tree)

    if closest_version:
        LOGGER.info(f"closest_version={closest_version}")
        LOGGER.info(f"installing chromedriver-py=={closest_version}")
        return not bool(
            os.system(f"pip install chromedriver-py=={closest_version}")
        )
    return False


def run_cli() -> int:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser(
        description="Get chromedriver-py version most suitable for your system"
    )
    parser.add_argument(
        "-v", "--verbose", help="Verbosity", action="count", default=0
    )

    log_levels = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
    }

    args = parser.parse_args()
    level = logging.ERROR

    if args.verbose is not None:
        level = int(args.verbose)
        level = log_levels.get(level, logging.CRITICAL)

    logging.basicConfig(level=level)
    return int(not run())
