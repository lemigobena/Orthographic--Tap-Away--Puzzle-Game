"""
Utility functions for the Orthographic Tap-Away Puzzle Game.
"""
from OpenGL.GL import *
from typing import Tuple

def set_normal_from_points(p1: Tuple[float, float, float], p2: Tuple[float, float, float], p3: Tuple[float, float, float]) -> None:
    """Calculates surface normal for a triangle (CCW winding order)."""
    ux, uy, uz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    vx, vy, vz = p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    length: float = (nx*nx + ny*ny + nz*nz) ** 0.5
    if length > 0.0001:
        glNormal3f(nx/length, ny/length, nz/length)


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value to a bounded range."""
    return max(minimum, min(value, maximum))
