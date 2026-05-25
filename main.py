#!/usr/bin/env python3
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time

from game import Game
import vector_font
import cube

# Global instances
game = Game()
window_width = 1024
window_height = 768

mouse_pressed = False
last_mouse_x = 0.0
last_mouse_y = 0.0
is_dragging = False

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_pos = [5.0, 10.0, 8.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    ambient = [0.3, 0.3, 0.4, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    diffuse = [0.8, 0.8, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    specular = [0.6, 0.6, 0.6, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.15, 0.15, 0.2, 1.0])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)

def draw_scene(for_picking=False):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    aspect = window_width / max(1, window_height)
    ortho_base = 3.6
    ortho_w = ortho_base * game.zoom
    ortho_h = ortho_base * game.zoom
    
    if aspect >= 1.0:
        ortho_w *= aspect
    else:
        ortho_h /= aspect
        
    glOrtho(-ortho_w, ortho_w, -ortho_h, ortho_h, -15.0, 15.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if not for_picking:
        draw_background(ortho_w, ortho_h)
        
    glRotatef(game.rot_x, 1, 0, 0)
    total_rot_y = game.rot_y
    if game.level_complete_timer is not None:
        total_rot_y += game.celebration_spin
    glRotatef(total_rot_y, 0, 1, 0)
    
    if not for_picking:
        glEnable(GL_DEPTH_TEST)
        
    for c in game.cubes.values():
        glPushMatrix()
        offset = c.get_offset(game.assemble_t)
        glTranslatef(
            c.grid_pos[0] - game.grid_center[0] + offset[0],
            c.grid_pos[1] - game.grid_center[1] + offset[1],
            c.grid_pos[2] - game.grid_center[2] + offset[2]
        )
        
        if game.assemble_t < 1.0:
            angle = (1.0 - game.assemble_t) * c.assemble_rot_speed
            glRotatef(angle, c.assemble_rot_axis[0], c.assemble_rot_axis[1], c.assemble_rot_axis[2])
            
        c.is_hovered = (c.color_id == game.hovered_cube_id)
        
        if for_picking:
            cube.draw_cube_faces(c, for_picking=True)
        else:
            glEnable(GL_LIGHTING)
            glPushMatrix()
            d = c.direction
            if d == (0, 0, -1):
                glRotatef(180, 0, 1, 0)
            elif d == (1, 0, 0):
                glRotatef(90, 0, 1, 0)
            elif d == (-1, 0, 0):
                glRotatef(-90, 0, 1, 0)
            elif d == (0, 1, 0):
                glRotatef(-90, 1, 0, 0)
            elif d == (0, -1, 0):
                glRotatef(90, 1, 0, 0)
            cube.draw_standard_arrow(c.is_hovered)
            glPopMatrix()
            
            glEnable(GL_POLYGON_OFFSET_FILL)
            glPolygonOffset(1.0, 1.0)
            glEnable(GL_LIGHTING)
            cube.draw_cube_faces(c, for_picking=False)
            glDisable(GL_POLYGON_OFFSET_FILL)
            
            glDisable(GL_LIGHTING)
            cube.draw_cube_wireframe(c, c.is_hovered)
            
        glPopMatrix()
        
    if not for_picking:
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glDepthMask(GL_FALSE)
        for p in game.particles:
            glColor4f(p.color[0], p.color[1], p.color[2], p.life)
            glPointSize(p.size)
            glBegin(GL_POINTS)
            glVertex3f(p.pos[0], p.pos[1], p.pos[2])
            glEnd()
        glDepthMask(GL_TRUE)

def draw_background(ow, oh):
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glBegin(GL_QUADS)
    glColor3f(0.04, 0.05, 0.08)
    glVertex3f(-ow * 1.5, -oh * 1.5, -12.0)
    glVertex3f(ow * 1.5, -oh * 1.5, -12.0)
    glColor3f(0.12, 0.14, 0.24)
    glVertex3f(ow * 1.5, oh * 1.5, -12.0)
    glVertex3f(-ow * 1.5, oh * 1.5, -12.0)
    glEnd()
    glEnable(GL_DEPTH_TEST)

def draw_hud():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window_width, window_height, 0, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    
    glLineWidth(2.0)
    glEnable(GL_LINE_SMOOTH)
    
    glColor3f(0.0, 0.8, 1.0)
    vector_font.draw_text(f"LEVEL {game.level_idx + 1}", 20, 35, scale=12.0, spacing=1.2)
    
    active_count = sum(1 for c in game.cubes.values() if c.state != "FLYING")
    glColor3f(1.0, 0.8, 0.0)
    vector_font.draw_text(f"CUBES: {active_count}", 20, 65, scale=10.0, spacing=1.2)
    
    level_names = ["INTRO CLUSTER", "PYRAMID STACK", "THE 3D CROSS", "THE GIANT CORE"]
    glColor3f(0.6, 0.7, 0.8)
    vector_font.draw_text(level_names[game.level_idx], 20, 95, scale=8.0, spacing=1.2)
    
    glColor3f(0.4, 0.5, 0.6)
    vector_font.draw_text("MOUSE LEFT DRAG: ROTATE BLOCK", 20, window_height - 90, scale=7.0, spacing=1.2)
    vector_font.draw_text("MOUSE WHEEL: ZOOM IN / OUT", 20, window_height - 65, scale=7.0, spacing=1.2)
    vector_font.draw_text("R: RESTART LEVEL   N: NEXT LEVEL   ESC: QUIT", 20, window_height - 40, scale=7.0, spacing=1.2)
    
    if game.level_complete_timer is not None:
        glDisable(GL_BLEND)
        glEnable(GL_BLEND)
        glColor4f(0.08, 0.09, 0.16, 0.85)
        glBegin(GL_QUADS)
        glVertex2f(0, window_height/2 - 70)
        glVertex2f(window_width, window_height/2 - 70)
        glVertex2f(window_width, window_height/2 + 50)
        glVertex2f(0, window_height/2 + 50)
        glEnd()
        
        pulse = math.sin(time.time() * 12.0) * 0.1 + 0.9
        glColor3f(pulse, pulse * 0.8, pulse * 0.2)
        
        msg = "VICTORY!" if game.level_idx < 3 else "ALL LEVELS CLEAR!"
        char_w = 20.0 * 1.2
        text_w = len(msg) * char_w
        tx = (window_width - text_w) / 2
        vector_font.draw_text(msg, tx, window_height/2 - 30, scale=20.0, spacing=1.2)
        
        sub = "LOADING NEXT STAGE..." if game.level_idx < 3 else "CONGRATULATIONS!"
        sub_char_w = 9.0 * 1.2
        sub_text_w = len(sub) * sub_char_w
        sx = (window_width - sub_text_w) / 2
        glColor3f(0.8, 0.8, 0.9)
        vector_font.draw_text(sub, sx, window_height/2 + 15, scale=9.0, spacing=1.2)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def perform_picking(mx, my):
    glDisable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glDisable(GL_LINE_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    draw_scene(for_picking=True)
    
    viewport_y = window_height - my
    pixel = glReadPixels(int(mx), int(viewport_y), 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
    
    glClearColor(0.08, 0.09, 0.16, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    
    if len(pixel) >= 3:
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        picked_id = r + (g << 8) + (b << 16)
        return picked_id
    return 0

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_R:
            game.load_level(game.level_idx)
        elif key == glfw.KEY_N:
            next_lvl = (game.level_idx + 1) % 4
            game.load_level(next_lvl)

def scroll_callback(window, xoffset, yoffset):
    game.target_zoom -= yoffset * 0.08
    game.target_zoom = max(0.4, min(2.5, game.target_zoom))

def resize_callback(window, width, height):
    global window_width, window_height
    window_width = max(1, width)
    window_height = max(1, height)
    glViewport(0, 0, window_width, window_height)

def main():
    global window_width, window_height, mouse_pressed, last_mouse_x, last_mouse_y, is_dragging
    
    if not glfw.init():
        print("Failed to initialize GLFW")
        return
        
    glfw.window_hint(glfw.SAMPLES, 4)
    window = glfw.create_window(window_width, window_height, "Orthographic Tap Away Puzzle Game", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        return
        
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_framebuffer_size_callback(window, resize_callback)
    
    width, height = glfw.get_framebuffer_size(window)
    resize_callback(window, width, height)
    
    glClearColor(0.08, 0.09, 0.16, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(2.0)
    
    setup_lighting()
    last_time = glfw.get_time()
    
    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        dt = current_time - last_time
        last_time = current_time
        
        game.update(min(0.1, dt))
        mx, my = glfw.get_cursor_pos(window)
        
        if game.assemble_t >= 1.0 and game.level_complete_timer is None:
            game.hovered_cube_id = perform_picking(mx, my)
        else:
            game.hovered_cube_id = 0
            
        left_state = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT)
        if left_state == glfw.PRESS:
            if not mouse_pressed:
                mouse_pressed = True
                last_mouse_x = mx
                last_mouse_y = my
                is_dragging = False
            else:
                dx = mx - last_mouse_x
                dy = my - last_mouse_y
                if abs(dx) > 1.0 or abs(dy) > 1.0:
                    is_dragging = True
                    game.target_rot_y += dx * 0.28
                    game.target_rot_x += dy * 0.28
                    game.target_rot_x = max(-80.0, min(80.0, game.target_rot_x))
                    last_mouse_x = mx
                    last_mouse_y = my
        else:
            if mouse_pressed:
                mouse_pressed = False
                if not is_dragging:
                    clicked_id = perform_picking(mx, my)
                    game.attempt_tap(clicked_id)
                is_dragging = False
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_scene(for_picking=False)
        draw_hud()
        glfw.swap_buffers(window)
        glfw.poll_events()
        
    glfw.terminate()

if __name__ == "__main__":
    main()
