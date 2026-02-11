3D Spatial Reasoning – Project Execution Plan
🎯 Project Goal

Build a room-agnostic 3D object placement system that:

Accepts any 3D room layout (.glb)

Extracts geometric structure automatically

Computes valid placement locations

Uses an LLM to generate geometry-grounded explanations

Works across multiple room layouts (generalization proof)

SYSTEM FLOW
Room (.glb)
      ↓
Scene Graph Extraction (Phase 1)
      ↓
Free-Space & Collision Engine (Phase 2)
      ↓
Placement Scoring System (Phase 3)
      ↓
LLM Explanation Layer (Phase 4)
      ↓
Evaluation Across Multiple Rooms

**Phase 1 – Scene Understanding (Room-Agnostic Core)**
Objective

Convert any .glb file into a structured scene representation.

Extracted Information

Room bounds

Floor height (robust percentile-based estimation)

Object bounding boxes (AABB in world coordinates)

2D occupancy grid (top-down projection)


Phase 2 – Collision & Free-Space Engine
Objective

Generate physically valid placement candidates.

Checks

No collision with existing objects

Inside room bounds

Clearance radius satisfied

Does not block walkable free space


Phase 3 – Placement Optimization
Objective

Select the best placement using spatial scoring.

Example Scoring Criteria

Distance to nearest wall

Distance to target object (e.g., chair near desk)

Maximum clearance

Walkability preservation


Phase 4 – Geometry-Grounded LLM Explanation

The LLM does not hallucinate placement.

Instead, it receives structured geometric facts:

Distance to nearest wall

Clearance value

Collision checks

Walkability impact

Candidate ranking

It generates:

Final placement decision

Explanation referencing measured geometry

Optional rejection reasoning for alternatives

Multi-Room Generalization

To prove room-agnostic behavior:

Multiple room layouts are placed in /data/rooms

A batch runner processes all rooms

Evaluation metrics are computed per room

Metrics

Collision-free rate

Average clearance

Walkability impact

Runtime per scene

Novelty

This system is novel because:

It is fully room-agnostic

No scene-specific hardcoding

Converts arbitrary 3D layouts into structured scene graphs

Combines geometric reasoning with LLM-based explanation

Produces measurable evaluation metrics

Supports multi-room generalization

👥 Team Responsibilities
Geometry & Core Engine

Scene extraction

Bounding box computation

Occupancy grid

Optimization

Collision detection

Candidate scoring

Constraint modeling

LLM & Explainability

Prompt design

Structured input formatting

Explanation generation

Evaluation & Demo

Batch runner

Metrics

Visualization

Documentation
