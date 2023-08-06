"""
Module that implements the core functionality of the package.
"""

from subprocess import check_output, run, CalledProcessError
import sys
from typing import Callable, Optional, Tuple

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Iterable
else:
    from typing import Iterable

_AvailVersionStrategy = Callable[[str], Optional[Iterable[str]]]
"""Available version strategy function type."""


def _get_pip_version() -> Tuple[int, ...]:
    """Get the version of pip for the current interpreter.

    Returns:
        The semantic version of pip for the current interpreter.

    """
    pip_version_out = check_output(
        [sys.executable, "-m", "pip", "--version"], text=True
    )
    version_str = pip_version_out.split()[1]
    version_str_parts = version_str.split(".")
    version_int_parts = map(int, version_str_parts)
    return tuple(version_int_parts)


def _index_versions_avail_versions_strategy(package: str) -> Optional[Iterable[str]]:
    """Call ``pip index versions`` to get available versions for a package.

    Args:
        package: The name of the package for which to get available versions for
            the current interpreter.

    Returns:
        The package versions available in the repo for the current interpreter.

    """
    try:
        compl_proc = run(
            [sys.executable, "-m", "pip", "index", "versions", package],
            capture_output=True,
            check=True,
            text=True,
        )
    except CalledProcessError as exc:
        if exc.output == f"ERROR: No matching distribution found for {package}\n":
            return None
        raise
    lines = compl_proc.stdout.splitlines()
    key = "Available versions:"
    idx = len(key)
    for version_line in filter(lambda line: line.startswith(key), lines):
        versions = version_line[idx:].strip().split(", ")
        return tuple(filter(lambda version: version.strip() != "", versions))
    return None


def _double_equal_avail_versions_strategy(package: str) -> Iterable[str]:
    """Call pip with an unspecifed version to get available versions for a package.

    Args:
        package: The name of the package for which to get available versions for
            the current interpreter.

    Returns:
        The package versions available in the repo for the currently interpreter.

    """
    raise NotImplementedError


def _legacy_resolver_avail_versions_strategy(package: str) -> Iterable[str]:
    """Call pip with an unspecified version and the legacy resolver flag to get
    available versions for a package.

    Args:
        package: The name of the package for which to get available versions for
            the current interpreter.

    Returns:
        The package versions available in the repo for the current interpreter.

    """
    raise NotImplementedError


def _not_implemented_avail_versions_strategy(package: str) -> Iterable[str]:
    """An unimplemented strategy that raises an exception when no other strategies
    are available.

    Args:
        package: The name of the package for which to get available versions for
            the current interpreter.

    Returns:
        Never returns, but always raises.

    Raises:
        NotImplementedError: Always raises this exception.

    """
    raise NotImplementedError


def _get_avail_versions_strategy(pip_version: Tuple[int, ...]) -> _AvailVersionStrategy:
    """Get the available version strategy to use based on the version of pip.

    Args:
        pip_version: The version of pip for the current interpreter.

    Returns:
        An _AvailVersionStrategy function that can be used with the ``pip_version``
        to get available versions for the current interpreter.

    """
    if pip_version >= (21, 2, 0):
        return _index_versions_avail_versions_strategy
    if pip_version >= (21, 1, 0):
        return _double_equal_avail_versions_strategy
    if pip_version >= (20, 3, 0):
        return _legacy_resolver_avail_versions_strategy
    if pip_version >= (9, 0, 0):
        return _double_equal_avail_versions_strategy
    return _not_implemented_avail_versions_strategy


def get_avail_versions(package: str) -> Optional[Iterable[str]]:
    """Get the available versions in the repo for the current interpreter.

    Args:
        package: The name of the package for which to check available versions.

    Returns:
        The package versions available in the repo for the current interpreter.

    """
    pip_version = _get_pip_version()
    strategy = _get_avail_versions_strategy(pip_version)
    return strategy(package)


def get_installed_version(package: str) -> Optional[str]:
    """Get the installed version of a package for the current interpreter.

    Args:
        package: The name of the package for which to check the installed version.

    Returns:
        The installed version of the package for the current interpreter. None if
        the package is not installed, or the version info isn't found.

    """
    try:
        compl_proc = run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            check=True,
            text=True,
        )
    except CalledProcessError as exc:
        if exc.output == f"WARNING: Package(s) not found: {package}\n":
            return None
        raise
    lines = compl_proc.stdout.splitlines()
    key = "Version:"
    idx = len(key)
    for version_line in filter(lambda line: line.startswith(key), lines):
        return version_line[idx:].strip()
    return None


def print_versions(
    avail_versions: Optional[Iterable[str]] = None,
    installed_version: Optional[str] = None,
) -> None:
    """Print a list of available and installed versions.

    If available versions are provided, add a mark to indicate the installed version,
    and whether or not it is in the available versions.

    Args:
        avail_versions: The list of available versions.
        installed_version: The installed version.

    """
    if avail_versions is not None:
        is_installed_in_available = False
        for version in avail_versions:
            if version != installed_version:
                print(version)
            else:
                print(f"*{version}")
                is_installed_in_available = True
        if installed_version and not is_installed_in_available:
            print(f"+{installed_version}")
    elif installed_version:
        print(installed_version)


def is_installed_in_avail_versions(
    avail_versions: Optional[Iterable[str]] = None,
    installed_version: Optional[str] = None,
) -> bool:
    """Check if the installed version is in the available versions.

    Args:
        avail_versions: The list of available versions.
        installed_version: The installed version.

    Returns:
        True if the installed version is ``None`` or in the available versions.

    """
    return (
        installed_version is None
        or avail_versions is not None
        and installed_version in avail_versions
    )
