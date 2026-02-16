# 3D Spatial Reasoning (Nomad AI) — LLM + Geometry Engine for Collision-Free Placement

A practical approach to **reliable spatial reasoning**:  
instead of letting an LLM “guess” coordinates, we separate responsibilities:

- **LLM = intent + explanation** (what the user wants, constraints, natural language)
- **Geometry engine = feasibility** (where objects *can* go, collision-free, walkable)
- **Output = validated placement + human-readable reasoning** (with distances)

This project explores **room-aware object placement** inside a 3D scene (Blender-based), producing placements that are **physically valid** (no intersections / no blocked regions) and **explainable** (why this location was chosen).

---

## ✨ Key Features

- ✅ **Collision-free placement** using geometric checks (AABB / bounding volumes / spacing rules)
- ✅ **Constraint-aware** placement (walls, keep-out zones, minimum clearances, walkways)
- ✅ **LLM-driven intent parsing** (extract object type, size, preferences, constraints)
- ✅ **Explainable output** (distances, free-space justification, why alternatives were rejected)
- ✅ Works with a **Blender room scene** as the environment representation

---

## 🧠 Why this matters

Most LLMs understand intent but struggle with *physics/geometry*.  
This project avoids “coordinate hallucination” by making the LLM **never decide final coordinates**.

Instead:
1. The LLM converts the request into structured constraints (JSON-like plan)
2. A geometry engine computes candidate valid placements
3. The LLM explains the final choice using computed measurements

---

## 🏗️ System Overview

**Input:** “Place a chair near the desk, don’t block the doorway, keep 60cm clearance.”  
**Output:** position + rotation + explanation

**Pipeline**
1. **Scene parsing (Blender → usable geometry)**
   - room boundaries / floor plane
   - obstacles / existing furniture
   - door/walkway regions (optional)
2. **Candidate generation**
   - sample points on floor grid / free-space map
   - optional heuristic zones (near desk, against wall, etc.)
3. **Feasibility & collision checks**
   - reject collisions and violations
   - rank candidates by constraint satisfaction score
4. **LLM explanation**
   - “Chosen because it’s 0.8m from desk, 1.2m from doorway, no overlap…”

---

## 📦 Tech Stack

- **Python**
- **Blender** (scene / environment)
- **LLM API / Local LLM** for intent + explanation
- Basic geometry utilities (bounding boxes, distance checks, grid sampling)

---

3D to 2D With valid Candidate Placement Point:
<img width="775" height="545" alt="image" src="https://github.com/user-attachments/assets/524f4c1a-dee0-4c7f-812b-ed4f2071b2e0" />

