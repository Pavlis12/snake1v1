import tkinter as tk
import random


WIDTH = 400
HEIGHT = 300
STEP = 10
DELAY = 400


class Snake:
    """
      Represents a single snake on the game canvas.

      Attributes:
          canvas (tk.Canvas): The canvas where the snake is drawn.
          head (int): The canvas object representing the snake's head.
          body (list): List of canvas objects representing the snake's body.
          dx (int): Horizontal movement direction.
          dy (int): Vertical movement direction.
          speed_boost (bool): Flag for speed boost (activated by perks).
      """
    def __init__(self, canvas, x, y, color, direction):
        """
              Initializes a Snake instance.

              Args:
                  canvas (tk.Canvas): The canvas on which to draw the snake.
                  x (int): Initial x-coordinate.
                  y (int): Initial y-coordinate.
                  color (str): Color of the snake.
                  direction (tuple): Initial direction as (dx, dy).
              """
        self.canvas = canvas
        self.color = color
        self.direction = direction
        self.body = []
        self.speed_boost = False
        self.food_count = 0
        self.head = canvas.create_rectangle(x, y, x + STEP, y + STEP, fill=color, outline="black")

    def move(self):
        """
              Moves the snake one step forward in its current direction.
              Shifts body segments to follow the head.
              """
        dx = self.direction[0] * STEP
        dy = self.direction[1] * STEP
        coords = self.canvas.coords(self.head)
        x1, y1 = coords[0], coords[1]
        old_positions = [(x1, y1)]

        for part in self.body:
            part_coords = self.canvas.coords(part)
            old_positions.append((part_coords[0], part_coords[1]))

        for i, part in enumerate(self.body):
            ox, oy = old_positions[i]
            self.canvas.coords(part, ox, oy, ox + STEP, oy + STEP)

        self.canvas.move(self.head, dx, dy)

    def grow(self):
        """
               Adds a new segment to the snake at the current head position.
               """
        coords = self.canvas.coords(self.head)
        x1, y1 = coords[0], coords[1]
        new_part = self.canvas.create_rectangle(x1, y1, x1 + STEP, y1 + STEP, fill="green", outline="black")
        self.body.append(new_part)

    def get_positions(self):
        """
             Returns a list of all (x, y) positions of the snake (head + body).

             Returns:
                 list: A list of (x, y) coordinate tuples.
             """
        positions = []
        coords = self.canvas.coords(self.head)
        positions.append((int(coords[0]), int(coords[1])))
        for part in self.body:
            coords = self.canvas.coords(part)
            positions.append((int(coords[0]), int(coords[1])))
        return positions

    def set_direction(self, dx, dy):
        """
               Updates the direction of the snake's movement.

               Args:
                   dx (int): New horizontal direction.
                   dy (int): New vertical direction.
               """
        self.direction = (dx, dy)


class Game:
    """
      Main game controller class. Manages snakes, food, perks, and game state.

      Attributes:
          canvas (tk.Canvas): Game drawing area.
          snake1 (Snake): First player snake.
          snake2 (Snake): Second player snake.
          food (list): List of canvas food items.
          food_count (int): Number of foods eaten.
          perks (list): List of perk canvas items.
      """
    def __init__(self, root):
        """
            Initializes the game, sets up canvas and starts the loop.

            Args:
                root (tk.Tk): The main Tkinter window.
            """
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.snake1 = Snake(self.canvas, 10, 10, "blue", (1, 0))
        self.snake2 = Snake(self.canvas, WIDTH - 20, HEIGHT - 20, "yellow", (-1, 0))
        self.foods = []
        self.food_pos = self.spawn_food()
        self.perks = []
        self.running = True
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<Return>", self.restart)
        self.game_loop()

    def spawn_food(self):
        """
              Randomly spawns up to 3 food items on unoccupied positions.
              """
        while len(self.foods) < 3:
            while True:
                x = random.randint(0, (WIDTH - STEP) // STEP) * STEP
                y = random.randint(0, (HEIGHT - STEP) // STEP) * STEP
                occupied_positions = self.snake1.get_positions() + self.snake2.get_positions() + [(fx, fy) for _, fx, fy in self.foods]
                if (x, y) not in occupied_positions:
                    break
            food = self.canvas.create_oval(x, y, x + STEP, y + STEP, fill="red", outline="")
            self.foods.append((food, x, y))

    def key_press(self, event):
        """
              Handles key presses for both snakes' movement.

              Args:
                  event (tk.Event): The key press event.
              """
        key = event.keysym.lower()

        if key == "w":
            self.snake1.set_direction(0, -1)
        elif key == "a":
            self.snake1.set_direction(-1, 0)
        elif key == "s":
            self.snake1.set_direction(0, 1)
        elif key == "d":
            self.snake1.set_direction(1, 0)

        elif key == "up":
            self.snake2.set_direction(0, -1)
        elif key == "left":
            self.snake2.set_direction(-1, 0)
        elif key == "down":
            self.snake2.set_direction(0, 1)
        elif key == "right":
            self.snake2.set_direction(1, 0)

    def game_loop(self):
        """
             The main game loop. Updates game state and restarts itself.
             """
        if self.running:
            self.check_food_collision(self.snake1)
            self.check_food_collision(self.snake2)
            self.check_perk_collision(self.snake1)
            self.check_perk_collision(self.snake2)

            if not self.snake1.speed_boost:
                self.snake1.move()
            if not self.snake2.speed_boost:
                self.snake2.move()

            self.check_collisions()
            self.root.after(DELAY, self.game_loop)

    def check_food_collision(self, snake):
        """
               Checks if a snake collides with food.

               Args:
                   snake (Snake): The snake to check.
               """
        head_x, head_y = snake.get_positions()[0]
        for food, fx, fy in self.foods:
            if abs(head_x - fx) < STEP and abs(head_y - fy) < STEP:
                self.canvas.delete(food)
                self.foods.remove((food, fx, fy))
                snake.grow()
                snake.food_count += 1
                self.spawn_food()
                self.check_perk_spawn(snake)
                break

    def check_perk_spawn(self, snake):
        """
                Spawns a perk every 2 eaten foods.

                Args:
                    snake (Snake): The snake that ate the food.
                """
        if snake.food_count % 2 == 0:
            while True:
                x = random.randint(0, (WIDTH - STEP) // STEP) * STEP
                y = random.randint(0, (HEIGHT - STEP) // STEP) * STEP
                if (x, y) not in self.snake1.get_positions() and (x, y) not in self.snake2.get_positions():
                    break

            triangle = self.canvas.create_polygon(
                x, y,
                x + STEP, y + STEP,
                x, y + STEP,
                fill="cyan", outline="white", tags="perk"
            )
            self.perks.append((triangle, x, y))
            self.root.after(10000, lambda: self.remove_perk(triangle))

    def remove_perk(self, triangle):
        """
               Removes a perk item from the canvas.

               Args:
                   triangle (int): Canvas object ID of the perk.
               """
        for perk in self.perks:
            if perk[0] == triangle:
                self.canvas.delete(triangle)
                self.perks.remove(perk)
                break

    def check_perk_collision(self, snake):
        """
               Checks if a snake collides with a perk.

               Args:
                   snake (Snake): The snake to check.
               """
        head_x, head_y = snake.get_positions()[0]
        for triangle, x, y in self.perks:
            if abs(head_x - x) < STEP and abs(head_y - y) < STEP:
                self.activate_perk(snake)
                self.canvas.delete(triangle)
                self.perks.remove((triangle, x, y))
                break

    def activate_perk(self, snake):
        """
                Activates a speed boost perk for a given snake.

                Args:
                    snake (Snake): The snake that collected the perk.
                """
        if snake.speed_boost:
            return
        snake.speed_boost = True
        boosted_delay = DELAY // 2

        def boosted_loop():
            if self.running and snake.speed_boost:
                self.check_food_collision(snake)
                snake.move()
                self.check_collisions()
                self.check_perk_collision(snake)
                self.root.after(boosted_delay, boosted_loop)

        boosted_loop()
        self.root.after(5000, lambda: setattr(snake, "speed_boost", False))

    def check_collisions(self):
        """
               Checks for collisions with walls, self, and other snake.

               Returns:
                   bool: True if a collision occurred.
               """
        for snake in [self.snake1, self.snake2]:
            head_x, head_y = snake.get_positions()[0]

            if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
                self.game_over()
                return

            if (head_x, head_y) in snake.get_positions()[1:]:
                self.game_over()
                return

        head1 = self.snake1.get_positions()[0]
        if head1 in self.snake2.get_positions():
            self.game_over()
            return

        head2 = self.snake2.get_positions()[0]
        if head2 in self.snake1.get_positions():
            self.game_over()
            return

    def game_over(self):
        """
               Ends the game and shows 'Game Over' message.
               """
        self.running = False
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over\nPress Enter to Restart", fill="white", font=("Arial", 16))

    def restart(self, event=None):
        """
              Restarts the game when Enter is pressed.

              Args:
                  event (tk.Event, optional): Key press event.
              """
        self.canvas.delete("all")
        self.snake1 = Snake(self.canvas, 10, 10, "blue", (1, 0))
        self.snake2 = Snake(self.canvas, WIDTH - 20, HEIGHT - 20, "yellow", (-1, 0))
        self.foods = []
        self.food_pos = self.spawn_food()
        self.perks = []
        self.running = True
        self.game_loop()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
