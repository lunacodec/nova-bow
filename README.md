# Nova Bow 🏹🌌

A 2D top-down exploration, archery, and puzzle game built in Python (`Pygame`) for my OCR A-Level Computer Science NEA project[span_6](start_span)[span_6](end_span)[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span). Designed to pair accessible archery physics with logic and mathematics challenges, persistent player profiles, and a competitive leaderboard[span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span)[span_11](start_span)[span_11](end_span).

## Core Gameplay & Features
* **2D Exploration World:** Navigate across a 9-screen interconnected space environment (`1280x720` resolution) featuring boundary detection, room transitions, and patrolling enemy classes (`EnemyH`, `EnemyV`)[span_12](start_span)[span_12](end_span)[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span)[span_15](start_span)[span_15](end_span).
* **Trigonometric & Kinematic Archery Mechanics:** Toggle into archery mode (`E`) to aim a 360° dynamic target line with the mouse[span_16](start_span)[span_16](end_span). Arrow launch angles are calculated using quadrant-aware `arctan` trigonometry, while flight trajectories simulate initial draw velocity and gravitational acceleration ($s = ut + \frac{1}{2}at^2$)[span_17](start_span)[span_17](end_span)[span_18](start_span)[span_18](end_span)[span_19](start_span)[span_19](end_span).
* **Interactive Puzzle System:** Touching randomly spawned puzzle boxes pauses combat and opens a dedicated problem-solving interface—complete with a rough-work scratchpad (`Working Box`), answer entry, and dynamic scoring loaded from `puzzles.csv`[span_20](start_span)[span_20](end_span)[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span)[span_23](start_span)[span_23](end_span).
* **User Accounts, Save States & Leaderboard:**
  * Full sign-up and login validation enforcing username uniqueness and NIST-inspired password rules[span_24](start_span)[span_24](end_span)[span_25](start_span)[span_25](end_span)[span_26](start_span)[span_26](end_span).
  * Deterministic password hashing and persistent state storage in `players.csv` (saving current area, health, elapsed time, score, and `(x, y)` coordinates)[span_27](start_span)[span_27](end_span)[span_28](start_span)[span_28](end_span)[span_29](start_span)[span_29](end_span).
  * Top-10 High Score Leaderboard sorted in descending order[span_30](start_span)[span_30](end_span)[span_31](start_span)[span_31](end_span).

## Tech Stack & Architecture
* **Language & Libraries:** Python 3, `Pygame` (rendering, sprite groups, event loop, audio mixer), `Pandas` / `csv` (file persistence), `math`, `random`[span_32](start_span)[span_32](end_span)[span_33](start_span)[span_33](end_span)[span_34](start_span)[span_34](end_span)[span_35](start_span)[span_35](end_span).
* **Object-Oriented Structure:** Modular classes for `Player`, `Arrow`, `Enemy` (with horizontal/vertical inheritance subclasses), `puzzleBox`, and interactive UI components (`Button`, `textBox`)[span_36](start_span)[span_36](end_span)[span_37](start_span)[span_37](end_span)[span_38](start_span)[span_38](end_span)[span_39](start_span)[span_39](end_span).

## Screenshots
![Nova Bow Main Menu](mainMenu.png)
![Nova Bow Gameplay](area1.png)
