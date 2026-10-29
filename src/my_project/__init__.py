"""My Project."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("my-project")
except PackageNotFoundError:  # package not installed (e.g. running from the source tree)
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
