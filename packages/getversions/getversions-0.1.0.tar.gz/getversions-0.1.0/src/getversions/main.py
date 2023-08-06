"""The main module of the getversions package.

This module parses arguments and dispatches them to functions in other modules. Its
``main`` function is the entrypoint for the console script that is installed with
the getversions package. Arguments can either be passed on the commannd line, or
they can be passed to the ``main`` function.

"""

import argparse
import sys
from typing import Optional

from getversions import (
    get_avail_versions,
    get_installed_version,
    print_versions,
    is_installed_in_avail_versions,
)

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse a list of arguments, or the command line arguments.

    Args:
        args: The arguments to parse. If None, then the command line arguments will
            be parsed.

    Returns:
        A namespace with the parsed arguments.

    """
    parser = argparse.ArgumentParser(
        prog="pygetversions",
        description=" ".join(
            (
                "Get versions of a package that are available in the repository,",
                "and installed for the current interpreter.",
            ),
        ),
    )
    parser.add_argument(
        "package", help="Name of the package for which to get version info"
    )
    parser.add_argument(
        "-i",
        "--installed-only",
        action="store_false",
        dest="print_avail",
        help="Print only the installed version",
    )
    parser.add_argument(
        "-e",
        "--exists-in-repo",
        action="store_true",
        dest="check_in_repo",
        help="Exit code 0 if the installed version is available in the repo",
    )
    return parser.parse_args(args)


def main(args: Optional[Sequence[str]] = None) -> int:
    """Parse arguments and dispatch them to the appropriate module function.

    Prints the available versions in the repo and the installed version, depending
    on the options passed.

    Args:
        args: The arguments to parse. If args is None, then the command line arguments
            will be parsed.

    Returns:
        0 to indicate success. 1 if the ``-e`` or ``--exists-in-repo`` option is
        passed and the installed version is in the repo.

    """
    options = parse_args(args)
    avail_versions = (
        get_avail_versions(options.package)
        if options.print_avail or options.check_in_repo
        else None
    )
    avail_versions_to_print = avail_versions if options.print_avail else None
    avail_versions_to_check = avail_versions if options.check_in_repo else None
    installed_version = get_installed_version(options.package)
    print_versions(avail_versions_to_print, installed_version)
    return (
        is_installed_in_avail_versions(avail_versions_to_check, installed_version)
        if options.check_in_repo
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
