import random
from typing import Tuple, List

class Particle:
    """Represents a simple visual particle for explosion effects."""
    def __init__(self, pos: Tuple[float, float, float], vel: Tuple[float, float, float], color: Tuple[float, float, float], gravity: float = 2.0):
        self.pos: List[float] = list(pos)
        self.vel: List[float] = list(vel)
        self.color: Tuple[float, float, float] = color
        self.gravity: float = gravity
        self.life: float = 1.0
        self.decay: float = random.uniform(1.0, 2.5)
        self.size: float = random.uniform(3.0, 8.0)

    def update(self, dt: float) -> None:
        """Updates particle position and lifetime over time dt."""
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt
        self.vel[0] *= 0.95
        self.vel[1] *= 0.95
        self.vel[2] *= 0.95
        self.vel[1] -= self.gravity * dt
        self.life -= dt * self.decay
        if self.life < 0:
            self.life = 0.0
