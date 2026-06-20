import random
import math
import time
from cube import Cube
from particle import Particle

class Game:
    """
    Game manager that handles game loop state, loading level layout designs,
    checking block tap obstructions, and managing visual particles.
    """
    def __init__(self):
        self.level_idx = 0
        self.cubes = {}
        self.particles = []
        
        self.rot_x = 20.0
        self.rot_y = -45.0
        self.target_rot_x = 20.0
        self.target_rot_y = -45.0
        
        self.zoom = 1.0
        self.target_zoom = 1.0
        
        self.grid_size = 3
        self.grid_center = [0.0, 0.0, 0.0]
        
        self.hovered_cube_id = 0
        self.assemble_t = 0.0
        
        self.level_complete_timer = None
        self.celebration_spin = 0.0
        self.game_state = "PLAYING"
        self.hovered_button = 0
        
        self.load_level(self.level_idx)

    def load_level(self, idx):
        self.level_idx = idx
        self.cubes.clear()
        self.particles.clear()
        self.assemble_t = 0.0
        self.hovered_cube_id = 0
        self.level_complete_timer = None
        self.celebration_spin = 0.0
        self.game_state = "PLAYING"
        self.hovered_button = 0
        
        self.target_rot_x = 25.0
        self.target_rot_y = -45.0
        self.target_zoom = 1.0
        
        shape = []
        if idx == 0:
            self.grid_size = 2
            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        shape.append((x, y, z))
        elif idx == 1:
            self.grid_size = 3
            for x in range(3):
                for z in range(3):
                    shape.append((x, 0, z))
            for x in range(1, 3):
                for z in range(1, 3):
                    shape.append((x, 1, z))
            shape.append((2, 2, 2))
        elif idx == 2:
            self.grid_size = 3
            for x in range(3):
                for z in range(3):
                    if not (x == 1 and z == 1):
                        shape.append((x, 1, z))
            shape.append((1, 0, 1))
            shape.append((1, 2, 1))
        elif idx == 3:
            self.grid_size = 3
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        axes_count = 0
                        if x == 1: axes_count += 1
                        if y == 1: axes_count += 1
                        if z == 1: axes_count += 1
                        if axes_count >= 2:
                            shape.append((x, y, z))
        elif idx == 4:
            self.grid_size = 3
            for x in range(3):
                for z in range(3):
                    shape.append((x, 0, z))
                    shape.append((x, 2, z))
            shape.append((1, 1, 1))
        elif idx == 5:
            self.grid_size = 3
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        if not (x == 1 and y == 1 and z == 1):
                            shape.append((x, y, z))
        elif idx == 6:
            self.grid_size = 3
            for y in range(3):
                shape.extend([(0, y, 0), (0, y, 2), (2, y, 0), (2, y, 2)])
            shape.extend([(1, 1, 0), (1, 1, 2)])
        elif idx == 7:
            self.grid_size = 3
            shape.extend([(0,0,0), (1,0,0), (2,0,0), (2,0,1), (2,0,2)])
            shape.extend([(2,1,2), (1,1,2), (0,1,2), (0,1,1), (0,1,0)])
            shape.extend([(0,2,0), (1,2,0), (2,2,0), (2,2,1), (2,2,2)])
        elif idx == 8:
            self.grid_size = 3
            for y in range(3):
                shape.extend([(0,y,0), (2,y,2), (2,y,0), (0,y,2), (1,y,1)])
        else:
            self.grid_size = 3
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        shape.append((x, y, z))
                        
        self.grid_center = [(self.grid_size - 1) / 2.0] * 3
        
        C = self.grid_center[0]
        shape_sorted = list(shape)
        shape_sorted.sort(key=lambda p: ((p[0]-C)**2 + (p[1]-C)**2 + (p[2]-C)**2) + random.uniform(-1.5, 1.5))
        
        placed_positions = set()
        cubes_to_add = []
        
        directions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
        
        for pos in shape_sorted:
            valid_dirs = []
            for d in directions:
                x, y, z = pos
                obstructed = False
                while True:
                    x += d[0]
                    y += d[1]
                    z += d[2]
                    if x < -1 or x > self.grid_size or y < -1 or y > self.grid_size or z < -1 or z > self.grid_size:
                        break
                    if (x, y, z) in placed_positions:
                        obstructed = True
                        break
                if not obstructed:
                    block_count = 0
                    rx, ry, rz = pos
                    while True:
                        rx += d[0]
                        ry += d[1]
                        rz += d[2]
                        if rx < -1 or rx > self.grid_size or ry < -1 or ry > self.grid_size or rz < -1 or rz > self.grid_size:
                            break
                        if (rx, ry, rz) in shape and (rx, ry, rz) not in placed_positions:
                            block_count += 1
                    valid_dirs.append((d, block_count))
                    
            if valid_dirs:
                valid_dirs.sort(key=lambda item: item[1], reverse=True)
                max_count = valid_dirs[0][1]
                best_dirs = [item[0] for item in valid_dirs if item[1] == max_count]
                direction = random.choice(best_dirs)
            else:
                direction = random.choice(directions)
                
            placed_positions.add(pos)
            cubes_to_add.append((pos, direction))
            
        color_id_counter = 1
        for pos, direction in cubes_to_add:
            cube = Cube(color_id_counter, pos, direction)
            self.cubes[color_id_counter] = cube
            color_id_counter += 1

    def check_obstruction(self, cube):
        d = cube.direction
        x, y, z = cube.grid_pos
        while True:
            x += d[0]
            y += d[1]
            z += d[2]
            if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size or z < 0 or z >= self.grid_size:
                return False
            for c in self.cubes.values():
                if c.state != "FLYING" and c.grid_pos == (x, y, z):
                    return True

    def attempt_tap(self, color_id):
        if color_id not in self.cubes:
            return
        cube = self.cubes[color_id]
        if cube.state != "IDLE" or self.assemble_t < 1.0:
            return
        blocked = self.check_obstruction(cube)
        if not blocked:
            cube.state = "FLYING"
            self.spawn_tap_sparks(cube)
        else:
            cube.state = "BLOCKED_BUMP"
            cube.bump_t = 0.0

    def spawn_tap_sparks(self, cube):
        cx = cube.grid_pos[0] - self.grid_center[0]
        cy = cube.grid_pos[1] - self.grid_center[1]
        cz = cube.grid_pos[2] - self.grid_center[2]
        base_color = (0.0, 0.8, 1.0)
        highlight_color = (1.0, 0.9, 0.2)
        for _ in range(30):
            rx = cube.direction[0] * 4.0 + random.uniform(-2.5, 2.5)
            ry = cube.direction[1] * 4.0 + random.uniform(-2.5, 2.5)
            rz = cube.direction[2] * 4.0 + random.uniform(-2.5, 2.5)
            color = random.choice([base_color, base_color, highlight_color])
            gravity = random.uniform(1.0, 3.5)
            self.particles.append(Particle((cx, cy, cz), (rx, ry, rz), color, gravity=gravity))

    def spawn_victory_fireworks(self):
        for _ in range(150):
            rx = random.uniform(-6, 6)
            ry = random.uniform(-2, 8)
            rz = random.uniform(-6, 6)
            color = random.choice([
                (1.0, 0.2, 0.6), (0.0, 0.9, 1.0), (1.0, 0.8, 0.0), (0.2, 1.0, 0.4), (0.9, 0.5, 1.0)
            ])
            gravity = random.uniform(0.5, 2.0)
            self.particles.append(Particle((0, 0, 0), (rx, ry, rz), color, gravity=gravity))

    def update(self, dt):
        if self.assemble_t < 1.0:
            self.assemble_t += dt * 1.5
            if self.assemble_t > 1.0:
                self.assemble_t = 1.0
                
        self.rot_x += (self.target_rot_x - self.rot_x) * 10.0 * dt
        self.rot_y += (self.target_rot_y - self.rot_y) * 10.0 * dt
        self.zoom += (self.target_zoom - self.zoom) * 10.0 * dt
        
        active_count = sum(1 for c in self.cubes.values() if c.state != "FLYING")
        if active_count == 0 and self.level_complete_timer is None:
            self.level_complete_timer = 2.0
            self.spawn_victory_fireworks()
            
        if self.level_complete_timer is not None:
            self.level_complete_timer -= dt
            self.celebration_spin += dt * 150.0
            if self.level_complete_timer <= 0.0:
                self.level_complete_timer = None
                next_lvl = (self.level_idx + 1)
                if next_lvl < 10:
                    self.load_level(next_lvl)
                else:
                    self.game_state = "VICTORY_SCREEN"
                    
        dead_cubes = []
        for cid, cube in self.cubes.items():
            cube.update(dt)
            if cube.state == "FLYING" and cube.anim_t >= 1.0:
                dead_cubes.append(cid)
                
        for cid in dead_cubes:
            del self.cubes[cid]
            
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0.0]
