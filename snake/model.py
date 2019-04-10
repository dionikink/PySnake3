import operator
import random

# Directions consist of tuple (coordinate_mutation, angle)
LEFT = ((-1, 0), 180)
UP = ((0, 1), 90)
RIGHT = ((1, 0), 0)
DOWN = ((0, -1), 270)

DIRECTIONS = [LEFT, UP, RIGHT, DOWN]


# Returns opposite direction
def opposite(direction):
    opposite_angle = (direction[1] - 180) % 360
    return [x for x in DIRECTIONS if x[1] == opposite_angle][0]


# Adds up two tuples (element-wise)
def tuple_add(tuple1, tuple2):
    return tuple(map(operator.add, tuple1, tuple2))


# Multiplies tuple by a factor (element-wise)
def tuple_mul(tuple1, factor):
    return tuple(map(operator.mul, tuple1, (factor, factor)))


class SnakeModel:
    def __init__(self, grid_width, grid_height, initial_length=4):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.initial_length = initial_length

        self.head = None
        self.direction = None
        self.tail = None
        self.score = None
        self.food = None

        self.reset()

    def reset(self):
        random_x = random.randint(self.initial_length - 1, self.grid_width - 1 - self.initial_length)
        random_y = random.randint(self.initial_length - 1, self.grid_height - 1 - self.initial_length)

        self.head = (random_x, random_y)
        self.direction = random.choice(DIRECTIONS)

        tail_direction = opposite(self.direction)
        self.tail = [tuple_add(self.head, tuple_mul(tail_direction[0], i)) for i in range(1, self.initial_length)]

        self.score = 0
        self.food = 0

    def eat(self):
        self.score += 100
        self.food += 1

    def increase_score(self, amount):
        self.score += amount

    def decrease_score(self, amount):
        self.score -= amount

    @property
    def head_x(self):
        return self.head[0]

    @property
    def head_y(self):
        return self.head[1]


class AppleModel:
    def __init__(self, grid_width, grid_height, snake_head, snake_tail):
        self.x = random.randint(2, grid_width - 2)
        self.y = random.randint(2, grid_height - 2)

        while (self.x, self.y) in snake_head or (self.x, self.y) in snake_tail:
            self.x = random.randint(2, grid_width - 2)
            self.y = random.randint(2, grid_height - 2)

    def get_coords(self):
        return self.x, self.y

