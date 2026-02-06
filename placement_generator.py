#!/usr/bin/env python
# coding: utf-8

# In[20]:


import json
import numpy as np


# In[21]:


SCENE_JSON = "scene_objects_world.json"


# In[31]:


def aabb_overlap(a_min, a_max, b_min, b_max):
    return (
        a_min[0] <= b_max[0] and a_max[0] >= b_min[0] and
        a_min[1] <= b_max[1] and a_max[1] >= b_min[1] and
        a_min[2] <= b_max[2] and a_max[2] >= b_min[2]
    )


# In[32]:


def inflate_aabb_xy(bmin, bmax, margin_xy):
    bmin = np.array(bmin, dtype=float)
    bmax = np.array(bmax, dtype=float)
    bmin[:2] -= margin_xy
    bmax[:2] += margin_xy
    return bmin.tolist(), bmax.tolist()


# In[33]:


def placement_aabb(center, size):
    c = np.array(center, dtype=float)
    s = np.array(size, dtype=float)
    half = s / 2.0
    return (c - half).tolist(), (c + half).tolist()


# In[34]:


def safe_center(o):
    # Some jsons have bbox_center, some don't. Compute if missing.
    if "bbox_center" in o:
        return np.array(o["bbox_center"], dtype=float)
    mn = np.array(o["bbox_min"], dtype=float)
    mx = np.array(o["bbox_max"], dtype=float)
    return (mn + mx) / 2.0


# In[35]:


def is_floor_like(o):
    sx, sy, sz = o["bbox_size"]
    return (sx > 3.0 and sy > 3.0 and sz < 0.25)

def is_wall_like(o):
    sx, sy, sz = o["bbox_size"]
    return (sz > 2.0 and (sx < 0.35 or sy < 0.35) and (sx > 2.0 or sy > 2.0))


# In[36]:


with open(SCENE_JSON, "r", encoding="utf-8") as f:
    scene = json.load(f)

objs = scene["objects"]

all_mins = np.array([o["bbox_min"] for o in objs], dtype=float)
all_maxs = np.array([o["bbox_max"] for o in objs], dtype=float)
scene_min = all_mins.min(axis=0)
scene_max = all_maxs.max(axis=0)

floor_z = float(scene_min[2])

print("Scene bounds:", scene_min.round(3), "to", scene_max.round(3))
print("Estimated floor_z:", round(floor_z, 3))


# In[37]:


def collides(candidate_center, candidate_size, clearance_xy=0.25):
    cand_min, cand_max = placement_aabb(candidate_center, candidate_size)
    cand_min, cand_max = inflate_aabb_xy(cand_min, cand_max, clearance_xy)

    for o in objs:
        if is_floor_like(o) or is_wall_like(o):
            continue
        if aabb_overlap(cand_min, cand_max, o["bbox_min"], o["bbox_max"]):
            return True
    return False


# In[38]:


def distance_to_nearest_object(center):
    c = np.array(center, dtype=float)
    dmin = 1e9
    for o in objs:
        if is_floor_like(o) or is_wall_like(o):
            continue
        oc = safe_center(o)
        d = np.linalg.norm(c[:2] - oc[:2])
        dmin = min(dmin, d)
    return float(dmin)


# In[39]:


def generate_candidates(obj_size, grid_step=0.25, clearance_xy=0.25, margin=0.3, top_k=10):
    L, W, H = obj_size
    z_center = floor_z + (H / 2.0) + 0.02

    x_min = scene_min[0] + margin + L/2
    x_max = scene_max[0] - margin - L/2
    y_min = scene_min[1] + margin + W/2
    y_max = scene_max[1] - margin - W/2

    valid = []
    xs = np.arange(x_min, x_max, grid_step)
    ys = np.arange(y_min, y_max, grid_step)

    for x in xs:
        for y in ys:
            center = [float(x), float(y), float(z_center)]
            if not collides(center, obj_size, clearance_xy=clearance_xy):
                near_wall = min(abs(x - scene_min[0]), abs(x - scene_max[0]),
                                abs(y - scene_min[1]), abs(y - scene_max[1]))
                space_from_objects = distance_to_nearest_object(center)

                # want: close to wall (small) and far from objects (large)
                score = (0.6 * near_wall) - (0.4 * space_from_objects)

                valid.append((score, center, near_wall, space_from_objects))

    valid.sort(key=lambda t: t[0])

    picked = []
    min_sep = 0.8
    for score, c, nw, dmin in valid:
        if all(np.linalg.norm(np.array(c[:2]) - np.array(p[:2])) >= min_sep for p in picked):
            picked.append(c)
        if len(picked) >= top_k:
            break

    return picked, len(valid), valid[:10]

# ---------- RUN ----------
new_object = {"name": "cabinet", "size": [1.0, 0.5, 2.0]}

cands, total, top10_debug = generate_candidates(
    obj_size=new_object["size"],
    grid_step=0.25,
    clearance_xy=0.25,
    margin=0.3,
    top_k=10
)

print(f"\nTotal valid placements found: {total}")
print("\nTop 10 (debug): score | near_wall | d_to_nearest | center")
for s, c, nw, dmin in top10_debug:
    print(round(s, 3), "|", round(nw, 3), "|", round(dmin, 3), "|", [round(x, 3) for x in c])

print("\nChosen diverse top candidates:")
for i, c in enumerate(cands, 1):
    print(i, [round(x, 3) for x in c])


# In[ ]:





# In[ ]:





# In[ ]:




