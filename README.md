# k1-description

K1 URDF / MJCF / USD description (ROS 2 package); meshes come from the booster_assets submodule.

| | |
|---|---|
| Layer | **L0**: Contract (no heavy deps) |
| May import | nothing |
| Files / LOC | 9 files · 141 lines (py, sh, cpp) |
| Part of | [k1-workspace](https://github.com/thdhyan/k1-workspace) (architecture and layering rules live there) |

## Install

Not an installable library: clone it and run the scripts in place.
```bash
git clone https://github.com/thdhyan/k1-description
```

## Layout

```
CMakeLists.txt
README.md
config/  (2 files)
  k1_controllers.yaml
  ros2_control.yaml
launch/  (1 files)
  view_robot.launch.py
package.xml
pyproject.toml
scripts/  (1 files)
  generate_k1_urdf.py
urdf/  (2 files)
  k1.urdf.xacro
  k1_gz.urdf.xacro
```

## Dependencies

- Declared sibling libraries: none (see `pyproject.toml`, `[tool.uv.sources]`).
- PyPI: none detected.
- Provided by the environment (ROS 2, Isaac, mjlab, robot SDK) or unresolved: `ament_index_python`, `launch`, `launch_ros`.

## Assets

Meshes and MJCF live in a separate repo. Add them once:
```bash
git submodule add git@github.com:thdhyan/booster_assets.git assets
```

## Hard-coded paths into other repos

None.

## Origin

Extracted from `booster_ws` (branch `dev/push-training-wip`, working tree of 2026-11-03) by
`tools/build_workspace.py` in k1-workspace. Old path to new path for every file: [`docs/migration_map.tsv`](https://github.com/thdhyan/k1-workspace/blob/main/docs/migration_map.tsv) (filter on `k1-description`).
History was not carried over: the working tree was copied as is, including previously untracked files.
