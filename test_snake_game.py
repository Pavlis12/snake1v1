
import unittest
import tkinter as tk
from Main import Snake, WIDTH, HEIGHT, STEP
"""
Unit tests for the Snake game logic using the tkinter canvas.

This test suite validates the core behavior of the `Snake` class, including movement,
growth, direction control, and collision logic.

Modules:
    unittest -- Python's standard unit testing framework
    tkinter -- Used to create a canvas for drawing the snake
    Main -- Contains the Snake class and constants like WIDTH, HEIGHT, STEP

Classes:
    TestSnakeGame(unittest.TestCase)
        Unit test case for testing the Snake class

Tested Features:
    - Initial position of the snake
    - Setting direction
    - Moving the snake
    - Growing the snake
    - Simulated self-collision
    - Collision with another snake
"""


class TestSnakeGame(unittest.TestCase):
    """
      Unit tests for the Snake game classes and core logic.
      """
    def setUp(self):
        """
               Creates a hidden tkinter window and canvas for drawing the snake.
               Initializes a Snake object at position (10, 10).
               Called before each test.
               """
        self.root = tk.Tk()
        self.root.withdraw()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.snake = Snake(self.canvas, 10, 10, "blue", (1, 0))

    def tearDown(self):
        """
              Cleans up the tkinter canvas and window after each test.
              Prevents resource leakage between tests.
              """
        self.canvas.destroy()
        self.root.destroy()

    def test_initial_position(self):
        """
                Test if the snake's head is placed at the correct initial position (10, 10).
                """
        pos = self.snake.get_positions()
        self.assertEqual(pos[0], (10, 10))

    def test_set_direction(self):
        """
                Test that the snake's direction updates correctly using set_direction().
                """
        self.snake.set_direction(0, -1)
        self.assertEqual(self.snake.direction, (0, -1))

    def test_move(self):
        """
               Test that the snake moves in its current direction (initially right).
               Validates the new head position after one move.
               """
        self.snake.move()
        new_pos = self.snake.get_positions()[0]
        self.assertEqual(new_pos, (10 + STEP, 10))

    def test_grow(self):
        """
                Test that grow() adds one segment to the snake's body.
                Also checks if get_positions() returns the correct number of segments.
                """
        self.snake.grow()
        self.assertEqual(len(self.snake.body), 1)
        self.assertEqual(len(self.snake.get_positions()), 2)

    def test_self_collision_simulation(self):
        """
                Simulates a scenario where the snake turns into itself (U-turn).
                Asserts that the snake's head collides with one of its own body segments.
                """
        for _ in range(5):
            self.snake.grow()

        for _ in range(3):
            self.snake.move()

        self.snake.set_direction(0, -1)
        self.snake.move()
        self.snake.set_direction(-1, 0)
        self.snake.move()
        self.snake.set_direction(0, 1)
        self.snake.move()
        self.snake.set_direction(1, 0)
        self.snake.move()

        head_pos = self.snake.get_positions()[0]
        body = self.snake.get_positions()[1:]
        self.assertIn(head_pos, body)

    def test_collision_with_other_snake(self):
        """
                Creates two snakes at the same position and checks that a collision is detected
                based on overlapping positions.
                """
        other_snake = Snake(self.canvas, 50, 10, "yellow", (0, 0))
        other_snake.grow()
        snake = Snake(self.canvas, 50, 10, "blue", (0, 0))
        head_pos = snake.get_positions()[0]
        other_positions = other_snake.get_positions()
        self.assertIn(head_pos, other_positions)


if __name__ == "__main__":
    unittest.main()
