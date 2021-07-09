# Snake
This a rendition of the classic Snake game that can be played normally or controlled programmatically.
My intent is for this to be used to experiment with AIs, both hard-coded and machine-learned.
To this end, I've written [simple_bot.py](simple_bot.py), which acts as a rudimentary example of how you can control the game.

[![Total alerts](https://img.shields.io/lgtm/alerts/g/ajbrining/snake.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ajbrining/snake/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ajbrining/snake.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ajbrining/snake/context:python)

## Requirements
The only things you need to run this are [Python3](https://www.python.org/downloads/) and [PyGame](https://www.pygame.org/news).

## Running
If you just want to play the game, all you need to do is run [snake.py](snake.py). It can be controlled using the arrow keys.

If you wish to write a script to play the game, you can get up and running quickly with the following:
```
import snake

game = snake.Game()
```
From there, you can start scripting movements with `game.move()` and passing it `0` to move up, `1` to move right, `2` to move down, or `3` to move left.
When running the game like this, the game will not tick on its own; it will only progress when you call `game.move()`.

All of the information about the game's running state is available in the [second paragraph of the Game class's `__init__` function](https://github.com/ajbrining/snake/blob/master/snake.py#L57).
The most notable of these are `game.snake` (a dictionary containing all data directly relating to the snake) and `game.board` (a two dimensional list that contains the state of every cell).

You may also find it useful to run the game without any graphics.
If this is the case, you can disable graphics by passing `graphics=False` when creating the game object.
Doing this will *significantly* decrease execution time.
