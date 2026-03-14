class Snake:
    def __init__(self):
        self.body = [(0, 0)]
        self.direction = (1, 0)  # Initially moving right
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        # Prevent the snake from reversing
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow_snake(self):
        self.grow = True

    def check_collision(self, width, height):
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= width or
                head_y < 0 or head_y >= height or
                len(self.body) != len(set(self.body)))  # Check for self-collision

    def get_head_position(self):
        return self.body[0]

    def get_body(self):
        return self.body