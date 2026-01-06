# Introduction

**Meow Adventure** is a 2D platform adventure game developed using **Python** and the **Pygame** framework.  
This project was created as a course final assignment and aims to demonstrate fundamental concepts of game development, including character control, collision detection, camera systems, and interactive dialogue.

---

In the game, players control a small cat exploring a horizontally scrolling world. By moving, jumping, and interacting with the environment, players can trigger dialogues and narrative events that gradually reveal the background story of the game.

- Genre: 2D Platformer / Exploration  
- Language: Python  
- Framework: Pygame  
- Project Type: Course Project / Student Work  

---

##  Gameplay

Players navigate the game world by:
- Moving left and right across platforms  
- Jumping over obstacles  
- Interacting with specific areas or objects  
- Triggering dialogue boxes or fullscreen story scenes  

The current version focuses on implementing core mechanics and a basic narrative framework, providing a foundation for future expansion.

---

##  Controls

| Key | Action |
|----|------|
| W / A / S / D | Move character |
| Space | Jump |
| E | Interact |
| ESC | Exit dialogue / Quit game |

---

##  Project Structure

- `main.py` – Game entry point and main loop  
- `constants.py` – Global configuration and parameters  
- `entities/` – Game entities such as the cat and platforms  
- `world/` – Background, foreground, and camera system  
- `ui/` – Dialogue boxes and interaction UI  
- `assets/` – Images, fonts, and other resources  

---

##  Key Features

- **Collision Detection**: Implemented using Axis-Aligned Bounding Box (AABB) rectangles  
