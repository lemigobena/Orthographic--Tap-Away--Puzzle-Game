# Orthographic Tap-Away Puzzle Game

A 3D grid-based puzzle game implemented in Python using PyOpenGL and GLFW. The goal of the game is to clear all the blocks from the grid. Each block has an arrow indicating the direction it can fly off. If a block is blocked by another block in its direction of travel, it will perform a bump animation and remain in place until the path is cleared.

---

##  Gameplay & Features

- **3D Orthographic Rendering**: The game is rendered with a clean, hardware-accelerated orthographic projection.
- **Multiple Puzzle Levels**: Features 10 levels of increasing complexity and grid sizes.
- **Intelligent Obstruction Checking**: Blocks will not move if they are obstructed by another active block in their escape direction.
- **Procedural Particle Effects**: Dynamic particle animations triggered when successfully tapping blocks and during victory celebrations.
- **Interactive Camera Controls**: Rotate and zoom the entire grid dynamically using the mouse.
- **Custom Vector Font Engine**: Custom OpenGL line-drawing system for crisp HUD text and Victory displays without external font file dependencies.

---

## Tech Stack & Requirements

- **Language**: Python 3
- **Graphics Libraries**:
  - `glfw` for window management and input handling.
  - `PyOpenGL` & `PyOpenGL_accelerate` for hardware-accelerated 3D graphics rendering.

---

##  Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone <repo-url>
   cd Orthographic--Tap-Away--Puzzle-Game
   ```

2. **Set up Virtual Environment**:
   It is recommended to run the project in a dedicated virtual environment (`.venv`).
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install glfw PyOpenGL PyOpenGL_accelerate
   ```

3. **Run the Game**:
   You can start the game directly using the launcher script:
   ```bash
   ./run.sh
   ```
   Or run the main entry script directly from the virtual environment:
   ```bash
   source .venv/bin/activate
   python main.py
   ```
   If the virtual environment is not available, use the system Python interpreter:
   ```bash
   python3 main.py
   ```

---

##  Controls

* **Left Mouse Click**: Tap on a cube to launch it.
* **Right Mouse Click + Drag** (or **Left Click + Drag** on the empty background): Rotate the puzzle grid.
* **Scroll Wheel**: Zoom in/out.
* **Escape (ESC)**: Exit the game.

---

##  Project Structure

* **`main.py`**: Core entry point. Initializes GLFW window, OpenGL context, input callbacks, and runs the main render loop.
* **`game.py`**: Manages game logic, level generation (10 levels), taps, updates, and particle spawning.
* **`cube.py`**: Defines individual cube representation, visual states (`IDLE`, `FLYING`, `BLOCKED_BUMP`), and renders cube geometry and directions.
* **`particle.py`**: Manages 3D particle updates and physics for tap sparks and victory fireworks.
* **`vector_font.py`**: Renders custom vector characters and strings using pure OpenGL line primitives.
* **`utils.py`**: Contains geometric utility operations (e.g. surface normal calculation).
* **`run.sh`**: Bash script utility to easily execute the game using the `.venv` Python runtime.
