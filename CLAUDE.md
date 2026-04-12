# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Arkanoid, a classic brick-breaker game built with Python and pygame. The repository contains two game versions:
- `arkanoid.py` - Basic version with core gameplay
- `arkanoid_enhanced.py` - Enhanced version with 36 levels, power-ups, particles, and advanced visual effects

## Running the Game

```bash
# Enhanced version (recommended)
python arkanoid_enhanced.py

# Basic version
python arkanoid.py

# Using the launch script
run_game.bat
```

## Key Architecture

### Main Game Loop
The `Game` class (arkanoid_enhanced.py) is the central controller. Its `run()` method implements the standard game loop pattern:
1. `handle_events()` - Process input
2. `update()` - Update game state
3. `draw()` - Render to screen
4. `clock.tick(60)` - Maintain 60 FPS

### Game States
The game uses a state machine with four states: `menu`, `playing`, `game_over`, `victory`. State transitions are triggered in `handle_events()` and `update()`.

### Collision System
- Uses pygame's `Rect.colliderect()` for detection
- Ball-paddle collision uses angle-based physics: `angle = (hit_pos - 0.5) * math.pi / 3`
- Collision cooldown prevents multi-hit issues: 30 frames (0.5 seconds)

### Level System
Levels are defined as 10x8 matrices in `ORIGINAL_LEVELS` where:
- 0 = empty space
- 1-8 = brick type (index into `BRICK_COLORS`)

36 unique patterns are defined in `LEVEL_NAMES`. Levels cycle when completed.

### Brick Resistance
Simplified system mapping colors to hits: RED=3, YELLOW=2, BLUE=1. Resistance decreases color brightness progressively via `update_color_by_damage()`.

### Power-up System
Five types stored in `active_power_ups` dict with frame-based timers:
- `expand` - Increases paddle width
- `multi_ball` - Adds 2 balls (max 5)
- `slow_ball` - Reduces ball speed by 30%
- `destroyer_ball` - Instant brick destruction
- `laser_shoot` - Enables paddle laser cannons

Power-ups spawn with 15% probability when bricks are destroyed.

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

## Constants

Key game constants are at the top of arkanoid_enhanced.py:
- `WINDOW_WIDTH`, `WINDOW_HEIGHT` - 800x600
- `BALL_SPEED` - 3 (global, modified by level progression)
- `PADDLE_SPEED` - 8
- `BRICK_WIDTH`, `BRICK_HEIGHT` - 75x20

## High Score Persistence

Scores are saved to `high_score.txt` using simple file I/O in `load_high_score()` and `save_high_score()`.

## Important Notes

- The game captures mouse input by default (ESC to toggle)
- `BALL_SPEED` is a global modified during level progression
- Ball speeds are synchronized across all balls in `sync_ball_speeds()`
- Screen shake is managed via `screen_shake` counter in Game class
