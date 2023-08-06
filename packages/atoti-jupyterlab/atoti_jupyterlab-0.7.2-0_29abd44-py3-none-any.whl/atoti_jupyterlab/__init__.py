"""Plugin to interactively visualize atoti sessions in JupyterLab.

This package is required to use :meth:`atoti.Session.visualize` and :meth:`atoti_query.QuerySession.visualize`.
"""

import json
from pathlib import Path
from typing import Dict, List

_SOURCE_DIRECTORY = Path(__file__).parent

_LABEXTENSION_FOLDER = "labextension"


def _get_package_name() -> str:
    package_data = json.loads(
        (_SOURCE_DIRECTORY / _LABEXTENSION_FOLDER / "package.json").read_bytes()
    )
    name: str = package_data["name"]
    return name


def _jupyter_labextension_paths() -> List[  # pyright: ignore[reportUnusedFunction]
    Dict[str, str]
]:
    """Return the paths used by JupyterLab to load the extension assets."""
    return [{"src": _LABEXTENSION_FOLDER, "dest": _get_package_name()}]
