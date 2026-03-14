def draw_snake(surface, snake_segments, color):
    for segment in snake_segments:
        pygame.draw.rect(surface, color, pygame.Rect(segment[0], segment[1], 10, 10))

def draw_food(surface, position, color):
    pygame.draw.rect(surface, color, pygame.Rect(position[0], position[1], 10, 10))

def generate_random_position(width, height):
    x = random.randint(0, (width // 10) - 1) * 10
    y = random.randint(0, (height // 10) - 1) * 10
    return (x, y)