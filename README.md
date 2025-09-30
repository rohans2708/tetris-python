# tetris-python
A tetris game coded in python.

## How to play

Use python 3.9 or higher. (Tested on 3.9 and 3.11)

Install the dependencies with `pip install -r requirements.txt`.

Run the game with `python src/main.py`.


## Game Controls

Right arrow -> Move the piece to the right

Left arrow -> Move the piece to the left

Down arrow -> Drop the piece

Up arrow -> Rotate the piece clockwise

Shift -> Rotate the piece counterclockwise

R -> Restart

P -> Pause/Unpause

ESC -> Quit

Space -> Hard Drop (requires upgrade)

B -> Bomb (requires upgrade)

H -> Hold current piece (requires upgrade)

## Persistent Upgrades

Upgrades are stored per player in `upgrades.json` under `players[<name>]`.

| Key                           | Effect                                                     |
|-------------------------------|------------------------------------------------------------|
| `hard_drop`                   | Unlocks the Space-bar hard drop                            |
| `preview_plus`                | Adds additional next-piece previews (base is always one)   |
| `hold_unlocked`               | Unlocks the hold slot (press `H` to swap the active piece) |
| `bomb_unlocked & bomb_blocks` | Unlocks the bomb piece (press `B` to use)                  |
