"""Single owner of the K1 robot model files (URDF / MJCF / USD / meshes).

Every library asks this package for model paths instead of computing them
relative to its own source file. Resolution order for the asset root:

1. ``$K1_ASSETS_DIR`` (a ``booster_assets`` checkout: contains ``robots/K1``)
2. assets bundled inside an installed ``k1-description`` wheel
3. the ``assets/`` submodule of a ``k1-description`` source checkout

Stdlib only: this is an L0 contract package.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

__all__ = ["assets_dir", "robot_file", "robot_description",
           "URDF", "URDF_ZED", "MJCF", "MJCF_MJLAB", "MJCF_MJLAB_ARMS",
           "USD_MJLAB", "USD_MJLAB_ARMS", "USD_MJLAB_SOLID"]

# Canonical file names under robots/K1/.
URDF = "K1_22dof.urdf"
URDF_ZED = "K1_22dof-ZED.urdf"
MJCF = "K1_22dof.xml"
MJCF_MJLAB = "K1_22dof_mjlab.xml"
MJCF_MJLAB_ARMS = "K1_22dof_mjlab_arms.xml"
# Isaac Lab conversions of the mjlab MJCFs (soft-gain K1 for the Isaac tasks).
USD_MJLAB = "usd_mjlab/K1_22dof_mjlab/K1_22dof_mjlab.usda"
USD_MJLAB_ARMS = "usd_mjlab/K1_22dof_mjlab_arms/K1_22dof_mjlab_arms.usda"
USD_MJLAB_SOLID = "usd_mjlab/K1_22dof_mjlab_solid/K1_22dof_mjlab_solid/K1_22dof_mjlab_solid.usda"

_PKG = Path(__file__).resolve().parent


def assets_dir() -> Path:
    """Root of the booster_assets tree (the directory holding ``robots/``)."""
    env = os.environ.get("K1_ASSETS_DIR")
    if env:
        return Path(env).expanduser().resolve()
    for cand in (_PKG / "assets", _PKG.parents[1] / "assets"):
        if (cand / "robots" / "K1").is_dir():
            return cand
    raise FileNotFoundError(
        "K1 assets not found. Run `git submodule update --init --recursive` in "
        "k1-description, install the k1-description wheel, or set K1_ASSETS_DIR "
        "to a booster_assets checkout.")


def robot_file(name: str = URDF) -> Path:
    """Path to a file under ``robots/K1/`` (e.g. ``robot_file(MJCF)``)."""
    p = assets_dir() / "robots" / "K1" / name
    if not p.exists():
        raise FileNotFoundError(f"K1 asset missing: {p}")
    return p


def robot_description(name: str = URDF) -> str:
    """URDF text with relative ``meshes/`` paths made absolute ``file://`` URIs.

    Suitable as the ``robot_description`` parameter of robot_state_publisher.
    """
    path = robot_file(name)
    mesh_dir = path.parent / "meshes"
    return re.sub(r'filename="meshes/', f'filename="file://{mesh_dir}/',
                  path.read_text())
