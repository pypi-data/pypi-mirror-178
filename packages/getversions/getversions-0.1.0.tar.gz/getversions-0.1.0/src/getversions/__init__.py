"""Initialize the get_versions package."""

from getversions.getversions import (
    get_avail_versions,
    get_installed_version,
    print_versions,
    is_installed_in_avail_versions,
)

__version__ = "0.1.0"

__all__ = (
    "get_avail_versions",
    "get_installed_version",
    "print_versions",
    "is_installed_in_avail_versions",
)
