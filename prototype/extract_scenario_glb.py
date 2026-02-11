#!/usr/bin/env python
# coding: utf-8

# In[5]:


pip install trimesh pygltflib numpy


# In[6]:


import json
import numpy as np
import trimesh
from pygltflib import GLTF2


# In[15]:


GLB_PATH = 'room_scene.glb'
OUT_JSON = 'scene_state.json'


# In[8]:


def mat4_from_trs(t, r, s):
    tx, ty, tz = t
    sx, sy, sz = s
    x, y, z, w = r

    R = np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - z*w),     2*(x*z + y*w)],
        [2*(x*y + z*w),     1 - 2*(x*x + z*z), 2*(y*z - x*w)],
        [2*(x*z - y*w),     2*(y*z + x*w),     1 - 2*(x*x + y*y)]
    ], dtype=np.float64)

    M = np.eye(4, dtype=np.float64)
    M[:3, :3] = R @ np.diag([sx, sy, sz])
    M[:3, 3] = [tx, ty, tz]
    return M


# In[10]:


def node_world_mats(gltf: GLTF2):
    children = {i: [] for i in range(len(gltf.nodes))}
    parents = {i: None for i in range(len(gltf.nodes))}
    for i, node in enumerate(gltf.nodes):
        if node.children:
            for c in node.children:
                children[i].append(c)
                parents[c] = i

    roots = []
    for scene in gltf.scenes:
        if scene.nodes:
            roots.extend(scene.nodes)

    local = []
    for node in gltf.nodes:
        if node.matrix and len(node.matrix) == 16:
            M = np.array(node.matrix, dtype=np.float64).reshape(4, 4).T
        else:
            t = node.translation or [0, 0, 0]
            r = node.rotation or [0, 0, 0, 1]
            s = node.scale or [1, 1, 1]
            M = mat4_from_trs(t, r, s)
        local.append(M)

    world = [np.eye(4, dtype=np.float64) for _ in gltf.nodes]
    def dfs(n, parentM):
        world[n] = parentM @ local[n]
        for c in children[n]:
            dfs(c, world[n])

    for r in roots:
        dfs(r, np.eye(4, dtype=np.float64))

    return world


# In[11]:


def transform_bounds(bounds, M):
    mn, mx = bounds
    corners = np.array([
        [mn[0], mn[1], mn[2], 1],
        [mn[0], mn[1], mx[2], 1],
        [mn[0], mx[1], mn[2], 1],
        [mn[0], mx[1], mx[2], 1],
        [mx[0], mn[1], mn[2], 1],
        [mx[0], mn[1], mx[2], 1],
        [mx[0], mx[1], mn[2], 1],
        [mx[0], mx[1], mx[2], 1],
    ], dtype=np.float64)

    wc = (M @ corners.T).T[:, :3]
    wmin = wc.min(axis=0)
    wmax = wc.max(axis=0)
    center = (wmin + wmax) / 2
    size = (wmax - wmin)
    return wmin, wmax, center, size


# In[13]:


def main():
    # Load GLB as trimesh scene (geometry) + gltf for node graph
    scene = trimesh.load(GLB_PATH, force="scene")
    gltf = GLTF2().load(GLB_PATH)
    world_mats = node_world_mats(gltf)

    # Map node->mesh name (best-effort)
    node_entries = []
    for i, node in enumerate(gltf.nodes):
        if node.mesh is None:
            continue

        node_name = node.name or f"node_{i}"
        mesh_index = node.mesh

        # Try to match geometry: trimesh names often differ, so we store node info anyway.
        node_entries.append({
            "node_index": i,
            "node_name": node_name,
            "mesh_index": int(mesh_index),
            "world_matrix": world_mats[i].round(6).tolist()
        })

    objects = []
    # Trimesh geometry holds actual vertices/bounds. We'll output per-geometry bounds too.
    for geom_name, geom in scene.geometry.items():
        bounds = geom.bounds  # local geom bounds
        objects.append({
            "geom_name": geom_name,
            "local_bbox_min": bounds[0].round(6).tolist(),
            "local_bbox_max": bounds[1].round(6).tolist(),
        })

    out = {
        "source": GLB_PATH,
        "num_geometries": len(scene.geometry),
        "geometries": objects,
        "nodes_with_mesh": node_entries
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"Saved {OUT_JSON}")
    print(f"Geometries: {len(scene.geometry)} | Nodes w/ mesh: {len(node_entries)}")


# In[16]:


if __name__ == '__main__':
    main()


# In[ ]:




