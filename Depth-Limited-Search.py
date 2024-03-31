import pygame
import sys

# Constants for the game
TILE_SIZE = 10
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Color for DLS exploration

def read_map(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def find_neighbors(map, node):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < len(map[0]) and 0 <= ny < len(map) and map[ny][nx] in ('.', 'D'):
            neighbors.append((nx, ny))
    return neighbors

def dls(map, start, destination, limit, explored, on_explore):
    if start == destination:
        return [start]

    if limit <= 0:
        return None

    explored.add(start)
    on_explore(start)

    for neighbor in find_neighbors(map, start):
        if neighbor not in explored:
            result = dls(map, neighbor, destination, limit - 1, explored, on_explore)
            if result is not None:
                return [start] + result

    return None

def draw_map(screen, map, explored=None):
    explored = explored or set()
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 'X':
                pygame.draw.rect(screen, BLACK, rect)
            elif (x, y) in explored:
                pygame.draw.rect(screen, BLUE, rect)  # Explored tiles
            else:
                pygame.draw.rect(screen, WHITE, rect, 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Map Explorer')

    map = read_map('map.txt')
    start = None
    destination = None

    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == 'S':
                start = (x, y)
            elif tile == 'D':
                destination = (x, y)
    
    if start is None or destination is None:
        print("Map must have a start (S) and a destination (D)")
        sys.exit(1)
    
    explored = set()

    def on_explore(current):
        nonlocal explored
        explored.add(current)
        draw_map(screen, map, explored)
        pygame.display.flip()
        pygame.time.delay(100)  # Delay to visualize DLS exploration

    limit = 10  # Depth limit
    path = dls(map, start, destination, limit, explored, on_explore)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw the final path
        draw_map(screen, map, explored)
        if path is not None:
            for point in path:
                pygame.draw.rect(screen, RED, (point[0]*TILE_SIZE, point[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        pygame.display.flip()
        clock.tick(60)  # Refresh rate

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
