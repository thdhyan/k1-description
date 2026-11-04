"""k1_description resolver and model-file validity (stdlib + optional mujoco)."""
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

import k1_description as d

N_JOINTS = 22


@pytest.mark.parametrize("name", [d.URDF, d.URDF_ZED])
def test_urdf_has_22_revolute_joints(name):
    root = ET.parse(d.robot_file(name)).getroot()
    assert sum(j.get("type") == "revolute" for j in root.iter("joint")) == N_JOINTS


def test_robot_description_mesh_uris_exist():
    text = d.robot_description()
    uris = [u for u in text.split('filename="')[1:]]
    assert uris and all(u.startswith("file://") for u in uris)
    for u in uris:
        assert Path(u.split('"')[0][len("file://"):]).exists()


def test_xacro_sources_are_well_formed():
    for f in (Path(__file__).resolve().parents[1] / "urdf").glob("*.xacro"):
        ET.parse(f)


def test_env_override(tmp_path, monkeypatch):
    (tmp_path / "robots" / "K1").mkdir(parents=True)
    monkeypatch.setenv("K1_ASSETS_DIR", str(tmp_path))
    assert d.assets_dir() == tmp_path
    with pytest.raises(FileNotFoundError):
        d.robot_file(d.URDF)


@pytest.mark.parametrize("name", [d.MJCF, d.MJCF_MJLAB, d.MJCF_MJLAB_ARMS])
def test_mjcf_loads(name):
    mujoco = pytest.importorskip("mujoco")
    m = mujoco.MjModel.from_xml_path(str(d.robot_file(name)))
    assert m.nu == N_JOINTS
