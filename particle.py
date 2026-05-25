import random

class Particle:
    def __init__(self, pos, vel, color):
        self.pos = list(pos)
        self.vel = list(vel)
        self.color = color
        self.life = 1.0
        self.decay = random.uniform(1.0, 2.5)
        self.size = random.uniform(3.0, 7.0)

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt
        self.vel[0] *= 0.95
        self.vel[1] *= 0.95
        self.vel[2] *= 0.95
        self.vel[1] -= 2.0 * dt
        self.life -= dt * self.decay
        if self.life < 0:
            self.life = 0.0
