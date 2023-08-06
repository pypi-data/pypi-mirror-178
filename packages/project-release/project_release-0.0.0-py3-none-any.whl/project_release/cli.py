"""The command line module."""
import argparse
import logging
from typing import List
from typing import Optional

from . import __version__

logger = logging.getLogger(__name__)


def project_release_cli(args: Optional[List[str]] = None) -> int:
    """Entry point for the command line.

    Returns
    -------
    int
        The value to be returned by the CLI executable.
    """
    parser = argparse.ArgumentParser(
        prog="project-release", description="A tool to help releasing projects."
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="show debug logs")

    parsed_args = parser.parse_args(args)

    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.DEBUG if parsed_args.verbose else logging.INFO,
    )

    return 0
