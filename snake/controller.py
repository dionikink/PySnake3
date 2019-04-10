from snake.model import SnakeModel, AppleModel


class SnakeController:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.snake = SnakeModel(grid_width, grid_height)
        self.game_over = False
        self.food = AppleModel(self.grid_width, self.grid_height, self.snake.head, self.snake.tail)

    def move(self, new_head):
        old_snake = self.snake.tail
        self.snake.tail = [self.snake.head]
        for i in range(1, len(old_snake)):
            self.snake.tail.append(old_snake[i - 1])

        self.snake.head = new_head

    def new_food(self):
        self.food = AppleModel(self.grid_width, self.grid_height, self.snake.head, self.snake.tail)

    def distance_to_food(self, new_head):
        return abs(self.food.x - new_head[0]) + abs(self.food.y - new_head[1])

    def reset(self):
        self.game_over = False
        self.food = AppleModel(self.grid_width, self.grid_height, self.snake.head, self.snake.tail)
        self.snake.reset()

    def run_rules(self):
        new_head = tuple([sum(x) for x in zip(self.snake.head, self.snake.direction[0])])

        # Check for collision with walls
        if new_head[0] <= 0 or new_head[0] >= self.grid_width - 1 or new_head[1] <= 0 or new_head[1] >= self.grid_height - 1:
            self.game_over = True
            return

        # Check for collision with tail
        if new_head in self.snake.tail[:-1]:
            self.game_over = True
            return

        # Check for food
        if new_head == self.food.get_coords():
            self.snake.tail = [self.snake.head] + self.snake.tail
            self.new_food()
            self.snake.eat()
        # else:
        #     # Update score
        #     current_dist = self.distance_to_food(new_head)
        #     new_dist = self.distance_to_food(new_head)
        #
        #     if new_dist < current_dist:
        #         self.snake.increase_score(1)
        #     else:
        #         self.snake.decrease_score(2)
        #
        # #
        # if self.snake.score <= -50:
        #     self.game_over = True
        #     return

        self.move(new_head)
