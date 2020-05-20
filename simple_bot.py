"""
A simple snake game bot.

This bot serves as an an example of how to control the snake game
programmatically. It's just a quick-and-dirty script used to test
win conditions, and only works if the number of columns and rows
are both even and greater than 4 or thereabout.
"""
import snake


game = snake.Game()


def loop():
    while not game.win and not game.lose:
        while game.snake['head']['x'] != game.COLUMNS - 1\
                and not game.win and not game.lose:
            game.move(1)
        while game.snake['head']['y'] != game.ROWS - 1\
                and not game.win and not game.lose:
            game.move(2)
        while game.snake['head']['x'] != 1\
                and not game.win and not game.lose:
            game.move(3)
            while game.snake['head']['y'] != 1\
                    and not game.win and not game.lose:
                game.move(0)
            game.move(3)
            while game.snake['head']['y'] != game.ROWS - 1\
                    and not game.win and not game.lose:
                game.move(2)
        game.move(3)
        while game.snake['head']['y'] != 0\
                and not game.win and not game.lose:
            game.move(0)


def run():
    if game.snake['head']['y'] == 0:
        if game.snake['head']['x'] == 0:
            loop()
        for i in range(1, 4):
            game.move(2)
    while game.snake['head']['x'] != 0:
        game.move(3)
    while game.snake['head']['y'] != 0:
        game.move(0)
    loop()


run()

if game.win:
    print('win!')
if game.lose:
    print('lose!')
