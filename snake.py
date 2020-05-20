"""
Play the classic Snake game.

Classes:

    Game

Functions:

    reset()
    move(direction) -> boolean
    run()

"""

import pygame
import random


class Game:
    def __init__(self, graphics=True, starting_size=3):
        """
        This class is everything you need to run the game.

        If you wish to run the game programmatically, all you need to is create a
        Game object (e.g. game = snake.Game()) and call game.move(direction) to
        issue commands. game.snake is a dictionary that contains information
        about the snake, and game.board is a two-dimensional list that
        represents the current state of the game. You can check for a game-over
        by inspecting game.win and game.lose. When initializing the game for
        programmatic use, you can disable graphics by passing graphics=False,
        which will significantly decrease execution time.

        Snake directions:
        Stopped/neutral = -1
        Up = 0
        Right = 1
        Down = 2
        Left = 3

        Board legend:
        Empty = 0
        Tail = 1
        Head = 2
        Food = 3

            Parameters:
                graphics (bool): If false, will not initialize a game window
                starting_size (int): The starting size of the snake
        """
        self.COLUMNS = 16
        self.ROWS = 16
        self.MAX_SIZE = (self.COLUMNS * self.ROWS) - 1
        self.GRAPHICS = graphics
        self.STARTING_SIZE = starting_size

        self.running = True
        self.win = False
        self.lose = False
        self.collision = ''
        self.started = False
        self.eaten = False
        self.score = 0
        self.snake = {'head': {'x': random.randint(0, self.COLUMNS - 1),
                               'y': random.randint(0, self.ROWS - 1)},
                      'direction': -1,
                      'tail': [],
                      'size': self.STARTING_SIZE}
        self.board = [[0 for i in range(self.ROWS)]
                      for i in range(self.COLUMNS)]
        self.board[self.snake['head']['x']][self.snake['head']['y']] = 2
        self.food = {}
        self._place_food()

        if graphics:
            self.SPEED = 8  # ticks per second
            self.BLOCK_SIZE = 30  # pixels
            self.WIDTH = (self.COLUMNS + 2) * self.BLOCK_SIZE
            self.HEIGHT = (self.ROWS + 2) * self.BLOCK_SIZE
            self.SIZE = self.WIDTH, self.HEIGHT
            self.FONT = 'consolas'
            self.TEXT_COLOR = (20, 82, 204)
            
            pygame.init()
            pygame.display.set_caption("Snake")
            icon = pygame.image.load('snake_icon.png')
            pygame.display.set_icon(icon)
            # ensure held keys repeat at least once per frame
            pygame.key.set_repeat(int((1000 / self.SPEED) / 2))
            self.screen = pygame.display.set_mode(self.SIZE, pygame.HWSURFACE
                                                  | pygame.DOUBLEBUF)
            self.clock = pygame.time.Clock()
            self._render()

    def _place_food(self):
        """Places food in a random, unoccupied space."""
        food_placed = False
        while not food_placed and not self.win:
            self.food = {'x': random.randint(0, self.COLUMNS - 1),
                         'y': random.randint(0, self.ROWS - 1)}
            if self.board[self.food['x']][self.food['y']] == 0:
                self.board[self.food['x']][self.food['y']] = 3
                food_placed = True

    def _render(self):
        """Draws the current state of the board."""
        if not self.GRAPHICS:
            return False

        # set the background to gray
        self.screen.fill((50, 50, 50))

        # create board surface and I want it painted black ♫
        board_surf = pygame.Surface((self.BLOCK_SIZE * self.COLUMNS,
                                     self.BLOCK_SIZE * self.ROWS))
        board_surf.fill((0, 0, 0))
        # draw the food as a red square
        food_rect = ((self.food['x'] * self.BLOCK_SIZE),
                     (self.food['y'] * self.BLOCK_SIZE),
                     self.BLOCK_SIZE,
                     self.BLOCK_SIZE)
        pygame.draw.rect(board_surf, (255, 0, 0), food_rect)

        # draw the head as a green square
        head_rect = ((self.snake['head']['x'] * self.BLOCK_SIZE),
                     (self.snake['head']['y'] * self.BLOCK_SIZE),
                     self.BLOCK_SIZE,
                     self.BLOCK_SIZE)
        pygame.draw.rect(board_surf, (0, 255, 0), head_rect)
        # draw the body as a series of white squares
        for segment in self.snake['tail']:
            body_rect = ((segment['x'] * self.BLOCK_SIZE),
                         (segment['y'] * self.BLOCK_SIZE),
                         self.BLOCK_SIZE,
                         self.BLOCK_SIZE)
            pygame.draw.rect(board_surf, (255, 255, 255), body_rect)

        # blit all of the above to the screen
        self.screen.blit(board_surf, (self.BLOCK_SIZE, self.BLOCK_SIZE))

        # render the score and blit it to the screen
        score_font = pygame.font.SysFont(self.FONT, 25)
        score = score_font.render(str(self.score), True, self.TEXT_COLOR)
        self.screen.blit(score, (0, 0))

        if self.win:
            self._draw_text('WIN!')
        elif self.lose:
            self._draw_text('LOSE!')

            lose_text = 'You hit ' + self.collision + '!'
            self._draw_text(lose_text, 50, 30)

        if self.win or self.lose:
            reset_text = 'Press space to play again!'
            self._draw_text(reset_text, 66.6, 30)

        pygame.display.update()

    # center of text will be at 50% of the x plane and (pos)% of the y plane
    def _draw_text(self, text='', pos=33.3, size=100):
        """
        Draws text directly to the screen.

            Parameters:
                text (str): The string to be drawn the the screen
                pos (int/float): The y position represented by a percentage
                size (int): The font size measured in point
        """
        font = pygame.font.SysFont(self.FONT, size)
        img = font.render(text, True, self.TEXT_COLOR)
        x = int((self.WIDTH / 2) - (font.size(text)[0] / 2))
        y = int((self.HEIGHT * pos / 100) - (font.size(text)[1] / 2))
        self.screen.blit(img, (x, y))

    # decorator that checks/pumps events
    def _check_events(function):
        def wrapper(self, *args, **kwargs):
            if self.GRAPHICS:
                # check for any quit events and quit if there are any
                events = pygame.event.get(pygame.QUIT)
                if events:
                    pygame.quit()
                    exit()
            function(self, *args, **kwargs)
        return wrapper

    # decorator that calls _render() after the function has run
    # used when changes are made to the board
    def _render_after(function):
        def wrapper(self, *args, **kwargs):
            function(self, *args, **kwargs)
            self._render()
        return wrapper

    def _check_space(self, x, y):
        """
        Checks for collisions and returns False if there is one.

            Parameters:
                x (int): The x coordinate to be checked
                y (int): The y coordinate to be checked

            Returns:
                (bool): False if there is a collision, True otherwise
        """
        # checking for wall collisions first prevents IndexError exceptions
        if x < 0:
            self.collision = 'the left wall'
        elif x > self.COLUMNS - 1:
            self.collision = 'the right wall'
        elif y < 0:
            self.collision = 'the top wall'
        elif y > self.ROWS - 1:
            self.collision = 'the bottom wall'
        elif self.board[x][y] == 0:
            return True
        elif self.board[x][y] == 3:
            self.eaten = True
            return True
        elif self.board[x][y] == 1:
            self.collision = 'your tail'

        # any non-colliding move would have already returned True
        self.lose = True
        return False

    @_check_events
    @_render_after
    def move(self, direction=-1):
        """
        Moves the snake in the direction specified.

            Parameters:
                direction (int): An integer representing the direction to move

            Returns:
                (bool): True if the move was made, False otherwise
        """
        if self.lose:
            return False
        if self.win:
            return False
        if not self.started and direction == -1:
            return False

        # keep the snake from moving the opposite direction
        # also allow for the starting condition
        if (direction != -1
            and direction != self.snake['direction'] + 2
            and direction != self.snake['direction'] - 2)\
                or (self.snake['direction'] == -1 and direction != -1):
            self.snake['direction'] = direction
            self.started = True

        old_head = {'x': self.snake['head']['x'],
                    'y': self.snake['head']['y']}

        # move the head
        # up
        if self.snake['direction'] == 0:
            if self._check_space(self.snake['head']['x'],
                                 self.snake['head']['y'] - 1):
                self.snake['head']['y'] -= 1
        # right
        elif self.snake['direction'] == 1:
            if self._check_space(self.snake['head']['x'] + 1,
                                 self.snake['head']['y']):
                self.snake['head']['x'] += 1
        # down
        elif self.snake['direction'] == 2:
            if self._check_space(self.snake['head']['x'],
                                 self.snake['head']['y'] + 1):
                self.snake['head']['y'] += 1
        # left
        elif self.snake['direction'] == 3:
            if self._check_space(self.snake['head']['x'] - 1,
                                 self.snake['head']['y']):
                self.snake['head']['x'] -= 1

        if self.lose:
            return False
        else:
            self.board[self.snake['head']['x']][self.snake['head']['y']] = 2

        if self.eaten:
            self.eaten = False
            self.snake['size'] += 1
            self.score += 1
            if self.snake['size'] < self.MAX_SIZE:
                self._place_food()
            else:
                self.win = True

        # add a new tail segment where the head used to be
        self.snake['tail'].insert(0, {'x': old_head['x'],
                                      'y': old_head['y']})
        self.board[self.snake['tail'][0]['x']][self.snake['tail'][0]['y']] = 1
        # only remove the end of the tail if the snake is too big
        if self.snake['tail'] and len(self.snake['tail']) > self.snake['size']:
            # breaking it down to keep the line short
            last_tail_x = self.snake['tail'][-1]['x']
            last_tail_y = self.snake['tail'][-1]['y']
            self.board[last_tail_x][last_tail_y] = 0
            self.snake['tail'].pop(-1)

        return True

    @_render_after
    def reset(self):
        """Resets the game to a random starting state."""
        self.win = False
        self.lose = False
        self.collision = ''
        self.started = False
        self.eaten = False
        self.score = 0
        self.board = [[0 for i in range(self.ROWS)]
                      for i in range(self.COLUMNS)]
        self.snake = {'head': {'x': random.randint(0, self.COLUMNS - 1),
                               'y': random.randint(0, self.ROWS - 1)},
                      'direction': -1,
                      'tail': [],
                      'size': self.STARTING_SIZE}
        self.board[self.snake['head']['x']][self.snake['head']['y']] = 2
        self.food = {}
        self._place_food()

    def run(self):
        """Runs the game in user/interactive mode."""
        while self.running:
            self.clock.tick(self.SPEED)

            # get key-down events in FIFO order
            events = pygame.event.get(pygame.KEYDOWN)
            command = None
            # a list of the key values we are looking for
            # the index corresponds to that key's direction
            arrow_keys = (pygame.K_UP,
                          pygame.K_RIGHT,
                          pygame.K_DOWN,
                          pygame.K_LEFT)
            # end result should be the most recent valid keypress
            for event in events:
                if event.key in arrow_keys and not (self.win or self.lose):
                    direction = arrow_keys.index(event.key)
                    # check to see if the direction is valid
                    # this keeps from overwriting a valid command
                    if (direction != self.snake['direction'] + 2
                        and direction != self.snake['direction'] - 2)\
                            or self.snake['direction'] == -1:
                        command = direction
                elif (self.win or self.lose) and event.key == pygame.K_SPACE:
                    self.reset()

            if command is not None:
                self.move(command)
            else:
                self.move()


if __name__ == '__main__':
    game = Game()
    game.run()
