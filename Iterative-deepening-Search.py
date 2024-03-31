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
BLUE = (0, 0, 255)  # Color for IDS exploration

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

def dfs_limit(map, start, destination, depth_limit, explored):
    if start == destination:
        return [start]
    if depth_limit <= 0:
        return None

    explored.add(start)
    for neighbor in find_neighbors(map, start):
        if neighbor not in explored:
            path = dfs_limit(map, neighbor, destination, depth_limit - 1, explored)
            if path is not None:
                return [start] + path
    return None

def iterative_deepening_search(map, start, destination):
    for depth_limit in range(1, len(map) * len(map[0])):
        explored = set()
        path = dfs_limit(map, start, destination, depth_limit, explored)
        if path is not None:
            return path

def draw_map(screen, map, explored=None, path=None):
    explored = explored or set()
    path = path or []
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 'X':
                pygame.draw.rect(screen, BLACK, rect)
            elif (x, y) in explored:
                pygame.draw.rect(screen, BLUE, rect)  # Explored tiles
            elif (x, y) in path:
                pygame.draw.rect(screen, RED, rect)  # Path tiles
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
    
    path = iterative_deepening_search(map, start, destination)
    
    if path is None:
        print("No path found.")
        sys.exit(1)

    explored = set(path[:-1])

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_map(screen, map, explored, path)
        pygame.display.flip()
        clock.tick(60)  # Refresh rate

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
