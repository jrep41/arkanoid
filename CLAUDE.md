# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Arkanoid, a classic brick-breaker game built with Python and pygame. The repository contains two game versions:
- `arkanoid.py` - Basic version with core gameplay
- `arkanoid_enhanced.py` - Enhanced version with 36 levels, power-ups, particles, and advanced visual effects

## Running the Game

```bash
# Using the pre-configured virtual environment (recommended)
.venv/Scripts/python.exe arkanoid_enhanced.py

# Or activate venv first
.venv/Scripts/activate
python arkanoid_enhanced.py

# Basic version
python arkanoid.py

# Using the launch script (Windows)
run_game.bat
```

## Dependencies

- Python 3.7+
- pygame>=2.0.0 (already in .venv, also listed in `requirements.txt`)

## Controls

| Input | Action |
|-------|--------|
| Mouse | Move paddle (captured by default) |
| Arrow keys / A/D | Alternative paddle movement |
| Left click / Space | Launch ball / Fire laser |
| Hold left click | Continuous laser fire |
| B | Add extra ball (max 5) |
| ESC | Toggle mouse capture |
| P | Pause game |
| Space | Start/Restart/Next level |

## Key Architecture

### Main Game Loop
The `Game` class (arkanoid_enhanced.py) is the central controller. Its `run()` method implements the standard game loop pattern:
1. `handle_events()` - Process input
2. `update()` - Update game state
3. `draw()` - Render to screen
4. `clock.tick(60)` - Maintain 60 FPS

### Game States
The game uses a state machine with four states: `menu`, `playing`, `game_over`, `victory`. State transitions are triggered in `handle_events()` and `update()`.

### Sticky Ball
At the start of each life, the ball sticks to the paddle and must be launched with Space/click. This provides a moment to position before launching.

### Collision System
- Uses pygame's `Rect.colliderect()` for detection
- Ball-paddle collision uses angle-based physics: `angle = (hit_pos - 0.5) * math.pi / 3`
- Collision cooldown prevents multi-hit issues: 30 frames (0.5 seconds)

### Level System
Levels are defined as 8×10 matrices (8 rows, 10 cols) in `ORIGINAL_LEVELS` where:
- 0 = empty space
- 1-8 = brick type (index into `BRICK_COLORS`)

36 unique patterns (Rectangle, Pyramid, Diamond, Castle, Heart, etc.) defined in `LEVEL_NAMES`. Levels cycle when completed.

### Brick Resistance
Simplified system mapping colors to hits:
- Red/Orange: 3 hits (highest resistance)
- Yellow/Magenta/Cyan/Green: 2 hits (medium)
- Blue/Gray: 1 hit (low)

Resistance decreases color brightness progressively via `update_color_by_damage()`.

### Power-up System
Five types stored in `active_power_ups` dict with frame-based timers:
- `expand` (E) - Increases paddle width
- `multi_ball` (M) - Adds 2 balls (max 5 total)
- `slow_ball` (S) - Reduces ball speed by 30%
- `destroyer_ball` (D) - Instant brick destruction (10 seconds)
- `laser_shoot` (L) - Enables dual laser cannons (10 seconds)

Power-ups spawn with 15% probability when bricks are destroyed.

### Sounds System
The `sounds.py` module generates all audio effects procedurally using pygame's mixer - no external audio files or numpy required (only stdlib `math` and `struct`). Key components:
- `SoundManager` class manages all sound effects
- `generate_tone()`, `generate_sweep()`, `generate_noise_burst()`, `generate_arpeggio()` create synthetic sounds
- Use `get_sound_manager()` to get the global instance
- Sounds: paddle_hit, brick_hit, brick_destroy, power_up, life_lost, game_over, victory, laser, level_complete, multi_ball

### Visual Effects
The game uses neon colors for glow effects: `NEON_CYAN`, `NEON_PINK`, `NEON_PURPLE`, `NEON_ORANGE`, `NEON_GREEN`, `NEON_YELLOW`, `NEON_RED`.

## Key Classes

| Class | File | Responsibility |
|-------|------|----------------|
| `Game` | arkanoid_enhanced.py | Main controller, state machine, game loop |
| `Paddle` | arkanoid_enhanced.py | Player movement, laser activation, expansion |
| `Ball` | arkanoid_enhanced.py | Physics, trail effect, destroyer mode |
| `Brick` | arkanoid_enhanced.py | Hit tracking, damage color, visual effects |
| `PowerUp` | arkanoid_enhanced.py | Falling collectibles with rotation animation |
| `Laser` | arkanoid_enhanced.py | Projectile with trail effect |
| `Particle` | arkanoid_enhanced.py | Explosion effects on brick destruction |
| `SoundManager` | sounds.py | Centralized synthetic sound generation |

## Constants

Key game constants are at the top of arkanoid_enhanced.py:
- `WINDOW_WIDTH`, `WINDOW_HEIGHT` - 1000x700
- `BALL_SPEED` - 3 (global, modified by level progression)
- `INITIAL_BALL_SPEED` - 3 (constant reference for resets)
- `MIN_BALL_SPEED` - 2 (lower bound when `slow_ball` power-up is active)
- `PADDLE_SPEED` - 8
- `BRICK_WIDTH`, `BRICK_HEIGHT` - 90x25
- `BRICK_ROWS`, `BRICK_COLS` - 8x10 grid
- Starting lives: 10

## High Score Persistence

Scores are saved to `high_score.txt` using simple file I/O in `load_high_score()` and `save_high_score()`.

## Important Notes

- The game captures mouse input by default (ESC to toggle)
- `BALL_SPEED` is a global modified during level progression
- Ball speeds are synchronized across all balls in `sync_ball_speeds()`
- Screen shake is managed via `screen_shake` counter in Game class
