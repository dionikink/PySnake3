import pyglet

from snake.controller import SnakeController


class SnakeView(pyglet.window.Window):
    def __init__(self, window_width=720, window_height=720, controller=None, framerate=1/60, cell_size=20):
        super(SnakeView, self).__init__(width=window_width, height=window_height)

        self.grid_width = int(window_width / cell_size)
        self.grid_height = int(window_height / cell_size)
        self.cell_size = cell_size
        self.framerate=framerate

        if controller:
            self.controller = controller
        else:
            self.controller = SnakeController(self.grid_width, self.grid_height)

        pyglet.gl.glClearColor(255, 255, 255, 255)

    def start(self):
        pyglet.clock.schedule_interval(self.update, self.framerate)
        pyglet.app.run()

    def update(self, dt):
        if not self.controller.game_over:
            self.controller.run_rules()
        else:
            self.controller.reset()

    def on_draw(self):
        self.clear()
        self.draw()
        self.draw_grid()

    def draw_grid(self):
        main_batch = pyglet.graphics.Batch()

        for row in range(self.grid_height):
            line_coords = [0, row * self.cell_size,
                           self.grid_width * self.cell_size, row * self.cell_size]

            main_batch.add(2, pyglet.gl.GL_LINES, None,
                           ('v2i', line_coords),
                           ('c3B', [0, 0, 0, 0, 0, 0]))

        for col in range(self.grid_width):
            line_coords = [col * self.cell_size, 0,
                           col * self.cell_size, self.grid_height * self.cell_size]

            main_batch.add(2, pyglet.gl.GL_LINES, None,
                           ('v2i', line_coords),
                           ('c3B', [0, 0, 0, 0, 0, 0]))

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if row == 0 or row == self.grid_height - 1 or col == 0 or col == self.grid_width - 1:
                    square_coords = [row * self.cell_size, col * self.cell_size,
                                     row * self.cell_size, col * self.cell_size + self.cell_size,
                                     row * self.cell_size + self.cell_size, col * self.cell_size,
                                     row * self.cell_size + self.cell_size, col * self.cell_size + self.cell_size]

                    main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                                           [0, 1, 2, 1, 2, 3],
                                           ('v2i', square_coords),
                                           ('c3B', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

        main_batch.draw()

    def draw(self):
        main_batch = pyglet.graphics.Batch()

        square_coords = [self.controller.snake.head_x * self.cell_size, self.controller.snake.head_y * self.cell_size,
                         self.controller.snake.head_x * self.cell_size, self.controller.snake.head_y * self.cell_size + self.cell_size,
                         self.controller.snake.head_x * self.cell_size + self.cell_size, self.controller.snake.head_y * self.cell_size,
                         self.controller.snake.head_x * self.cell_size + self.cell_size, self.controller.snake.head_y * self.cell_size + self.cell_size]

        main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                               [0, 1, 2, 1, 2, 3],
                               ('v2i', square_coords),
                               ('c3B', [0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255]))

        for (row, col) in self.controller.snake.tail:
            square_coords = [row * self.cell_size, col * self.cell_size,
                             row * self.cell_size, col * self.cell_size + self.cell_size,
                             row * self.cell_size + self.cell_size, col * self.cell_size,
                             row * self.cell_size + self.cell_size, col * self.cell_size + self.cell_size]

            main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                                   [0, 1, 2, 1, 2, 3],
                                   ('v2i', square_coords),
                                   ('c3B', [0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0]))

        square_coords = [self.controller.food.x * self.cell_size, self.controller.food.y * self.cell_size,
                         self.controller.food.x * self.cell_size, self.controller.food.y * self.cell_size + self.cell_size,
                         self.controller.food.x * self.cell_size + self.cell_size, self.controller.food.y * self.cell_size,
                         self.controller.food.x * self.cell_size + self.cell_size, self.controller.food.y * self.cell_size + self.cell_size]

        main_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                               [0, 1, 2, 1, 2, 3],
                               ('v2i', square_coords),
                               ('c3B', [255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0]))

        main_batch.draw()


if __name__ == '__main__':
    view = SnakeView()

