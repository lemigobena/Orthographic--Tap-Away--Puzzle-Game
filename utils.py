from OpenGL.GL import *

def set_normal_from_points(p1, p2, p3):
    """Calculates surface normal for a triangle (CCW winding order)."""
    ux, uy, uz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    vx, vy, vz = p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    length = (nx*nx + ny*ny + nz*nz) ** 0.5
    if length > 0.0001:
        glNormal3f(nx/length, ny/length, nz/length)
