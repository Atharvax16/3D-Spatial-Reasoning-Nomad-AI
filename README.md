# 3D-Spatial-Reasoning-Nomad-AI

A small end-to-end prototype for **3D spatial reasoning in an indoor room**:
1) take a Blender scene (`.blend`),  
2) export it to `.glb`,  
3) extract **object metadata + world-space transforms**,  
4) generate **collision-free placement candidates** for new objects,  
5) (optional) call an LLM (Mistral) to **choose / explain** placements in natural language.

---

## What this repo does (in plain words)

Given a room layout, we want to place an object (e.g., chair/table/plant) at a position that:
- does **not collide** with existing geometry,
- respects basic heuristics (near wall, not blocking walkable space, reasonable distance from other objects),
- can be explained like: *“Place the chair near the wall beside the desk, leaving clearance for movement.”*

This repo contains scripts + notebooks to:
- export and read a `.glb` version of the Blender scene,
- extract object transforms into JSON (world coordinates),
- generate candidate placements programmatically,
- optionally query an LLM to pick the best placement / provide reasoning.

---

## Repository contents

- `room_scene.blend`  
  Blender source scene (room layout).

- `room_scene.glb`  
  Exported GLB version of the scene.

- `extract_scene_glb.py` / `extract_scene_glb.ipynb`  
  Load the GLB and extract scene/object information.

- `extract_scenario_glb.py`  
  Variant script for scenario/object extraction (useful when you want a curated subset).

- `scene_objects_world.json`  
  Output: objects with **world-space** position/rotation/scale (and other metadata if available).

- `scene_state.json`  
  Output: scene-level information (bounds, floor estimate, etc.) used by placement logic.

- `placement_generator.py` / `placement_generator.ipynb`  
  Generates valid placement points (non-colliding) and ranks them with heuristics.

- `mistral_call.ipynb`  
  Optional: call a Mistral model/API to pick a placement and explain the reasoning.

---

## Requirements

### 1) Blender
Install Blender (recommended: **Blender 3.x / 4.x**) to open/edit the scene and export GLB.

You’ll use Blender for:
- opening `room_scene.blend`
- exporting to `room_scene.glb` (if you change the room)

### 2) Python
- Python **3.10+** recommended
- Works best in a virtual environment

### 3) Python packages
Exact packages depend on your local setup, but typically you’ll need:
- `numpy`
- `json` (built-in)
- GLB/mesh helpers (commonly: `trimesh`, `pygltflib`)
- geometry helpers (commonly: `shapely`, `scipy`) — if you use polygon/nearest-neighbor utilities

If you don’t have a `requirements.txt` yet, create one and pin what your scripts import.

---

## Setup

```bash
# 1) clone
git clone https://github.com/Atharvax16/3D-Spatial-Reasoning-Nomad-AI.git
cd 3D-Spatial-Reasoning-Nomad-AI

# 2) create venv
python -m venv .venv

# Windows:
# .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) install dependencies (add requirements.txt if you don’t have it yet)
pip install -U pip
pip install numpy trimesh pygltflib shapely scipy
