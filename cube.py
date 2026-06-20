from OpenGL.GL import *
import math
import random
import time
from utils import set_normal_from_points

class Cube:
    """Represents a single tap-away cube in the puzzle grid."""
    def __init__(self, color_id, grid_pos, direction):
        self.color_id = color_id      # Unique ID for picking
        self.grid_pos = grid_pos      # (x, y, z) in grid coordinates
        self.direction = direction    # (dx, dy, dz) unit vector
        self.state = "IDLE"           # "IDLE", "FLYING", "BLOCKED_BUMP"
        self.anim_t = 0.0             # Flying animation time [0, 1]
        self.bump_t = 0.0             # Bump animation time [0, 1]
        self.assemble_offset = [random.uniform(-8, 8), random.uniform(8, 15), random.uniform(-8, 8)]
        self.assemble_rot_axis = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
        self.assemble_rot_speed = random.uniform(180, 540)
        self.is_hovered = False
        
    def update(self, dt):
        """Updates cube animation state."""
        if self.state == "FLYING":
            self.anim_t += dt * 1.5
            if self.anim_t > 1.0:
                self.anim_t = 1.0
        elif self.state == "BLOCKED_BUMP":
            self.bump_t += dt * 5.0
            if self.bump_t > 1.0:
                self.bump_t = 0.0
                self.state = "IDLE"

    def get_offset(self, assemble_t):
        """Calculates the current visual offset for animation."""
        if assemble_t < 1.0:
            s = (1.0 - assemble_t) ** 3
            return [self.assemble_offset[0] * s, self.assemble_offset[1] * s, self.assemble_offset[2] * s]
        if self.state == "FLYING":
            dist = (self.anim_t ** 3) * 18.0
            return [self.direction[0] * dist, self.direction[1] * dist, self.direction[2] * dist]
        if self.state == "BLOCKED_BUMP":
            dist = math.sin(self.bump_t * math.pi) * 0.18
            return [self.direction[0] * dist, self.direction[1] * dist, self.direction[2] * dist]
        return [0.0, 0.0, 0.0]

def draw_cube_faces(cube, for_picking):
    if for_picking:
        r = cube.color_id & 0xFF
        g = (cube.color_id >> 8) & 0xFF
        b = (cube.color_id >> 16) & 0xFF
        glColor3ub(r, g, b)
    else:
        if cube.is_hovered:
            pulse = (math.sin(time.time() * 8.0) * 0.5 + 0.5) * 0.15
            glColor4f(0.25 + pulse, 0.38 + pulse, 0.55 + pulse, 0.85)
        else:
            glColor4f(0.14, 0.20, 0.30, 0.65)
    s = 0.45
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-s, -s, s); glVertex3f(s, -s, s); glVertex3f(s, s, s); glVertex3f(-s, s, s)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-s, -s, -s); glVertex3f(-s, s, -s); glVertex3f(s, s, -s); glVertex3f(s, -s, -s)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-s, s, -s); glVertex3f(-s, s, s); glVertex3f(s, s, s); glVertex3f(s, s, -s)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-s, -s, -s); glVertex3f(s, -s, -s); glVertex3f(s, -s, s); glVertex3f(-s, -s, s)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(s, -s, -s); glVertex3f(s, s, -s); glVertex3f(s, s, s); glVertex3f(s, -s, s)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-s, -s, -s); glVertex3f(-s, -s, s); glVertex3f(-s, s, s); glVertex3f(-s, s, -s)
    glEnd()

def draw_cube_wireframe(cube, is_hovered):
    if is_hovered:
        pulse = math.sin(time.time() * 12.0) * 0.2 + 0.8
        glColor4f(1.0, 0.8 * pulse, 0.2 * pulse, 1.0)
    else:
        glColor4f(0.0, 0.8, 1.0, 0.85)
    s = 0.455
    glBegin(GL_LINES)
    glVertex3f(-s, -s, -s); glVertex3f(s, -s, -s)
    glVertex3f(s, -s, -s); glVertex3f(s, -s, s)
    glVertex3f(s, -s, s); glVertex3f(-s, -s, s)
    glVertex3f(-s, -s, s); glVertex3f(-s, -s, -s)
    glVertex3f(-s, s, -s); glVertex3f(s, s, -s)
    glVertex3f(s, s, -s); glVertex3f(s, s, s)
    glVertex3f(s, s, s); glVertex3f(-s, s, s)
    glVertex3f(-s, s, s); glVertex3f(-s, s, -s)
    glVertex3f(-s, -s, -s); glVertex3f(-s, s, -s)
    glVertex3f(s, -s, -s); glVertex3f(s, s, -s)
    glVertex3f(s, -s, s); glVertex3f(s, s, s)
    glVertex3f(-s, -s, s); glVertex3f(-s, s, s)
    glEnd()

def draw_standard_arrow(is_hovered):
    if is_hovered:
        pulse = math.sin(time.time() * 10.0) * 0.2 + 0.8
        glColor4f(1.0, 0.9 * pulse, 0.3 * pulse, 1.0)
    else:
        glColor4f(1.0, 0.5, 0.0, 1.0)
    sh = 0.045
    hh = 0.13
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-sh, -sh, 0.0); glVertex3f(sh, -sh, 0.0); glVertex3f(sh, sh, 0.0); glVertex3f(-sh, sh, 0.0)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-sh, -sh, -0.2); glVertex3f(-sh, sh, -0.2); glVertex3f(sh, sh, -0.2); glVertex3f(sh, -sh, -0.2)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-sh, sh, -0.2); glVertex3f(-sh, sh, 0.0); glVertex3f(sh, sh, 0.0); glVertex3f(sh, sh, -0.2)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-sh, -sh, -0.2); glVertex3f(sh, -sh, -0.2); glVertex3f(sh, -sh, 0.0); glVertex3f(-sh, -sh, 0.0)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(sh, -sh, -0.2); glVertex3f(sh, sh, -0.2); glVertex3f(sh, sh, 0.0); glVertex3f(sh, -sh, 0.0)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-sh, -sh, -0.2); glVertex3f(-sh, -sh, 0.0); glVertex3f(-sh, sh, 0.0); glVertex3f(-sh, sh, -0.2)
    glEnd()
    glBegin(GL_TRIANGLES)
    set_normal_from_points((-hh, -hh, 0.0), (hh, -hh, 0.0), (0.0, 0.0, 0.26))
    glVertex3f(-hh, -hh, 0.0); glVertex3f(hh, -hh, 0.0); glVertex3f(0.0, 0.0, 0.26)
    set_normal_from_points((hh, -hh, 0.0), (hh, hh, 0.0), (0.0, 0.0, 0.26))
    glVertex3f(hh, -hh, 0.0); glVertex3f(hh, hh, 0.0); glVertex3f(0.0, 0.0, 0.26)
    set_normal_from_points((hh, hh, 0.0), (-hh, hh, 0.0), (0.0, 0.0, 0.26))
    glVertex3f(hh, hh, 0.0); glVertex3f(-hh, hh, 0.0); glVertex3f(0.0, 0.0, 0.26)
    set_normal_from_points((-hh, hh, 0.0), (-hh, -hh, 0.0), (0.0, 0.0, 0.26))
    glVertex3f(-hh, hh, 0.0); glVertex3f(-hh, -hh, 0.0); glVertex3f(0.0, 0.0, 0.26)
    glEnd()
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-hh, -hh, 0.0); glVertex3f(-hh, hh, 0.0); glVertex3f(hh, hh, 0.0); glVertex3f(hh, -hh, 0.0)
    glEnd()
