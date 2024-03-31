import pygame
import sys
from collections import deque

# Constants for the game
TILE_SIZE = 10
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Color for BFS exploration

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

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(map, start, destination, on_explore):
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, destination)}
    
    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        on_explore(current, open_set)  # Callback for visualization
        
        if current == destination:
            break
        
        open_set.remove(current)
        
        for neighbor in find_neighbors(map, current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, destination)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def draw_map(screen, map, explored=None, frontier=None):
    explored = explored or set()
    frontier = frontier or []
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 'X':
                pygame.draw.rect(screen, BLACK, rect)
            elif (x, y) in explored:
                pygame.draw.rect(screen, BLUE, rect)  # Explored tiles
            elif (x, y) in frontier:
                pygame.draw.rect(screen, GREEN, rect)  # Frontier tiles
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
    def on_explore(current, frontier):
        nonlocal explored
        explored.add(current)
        draw_map(screen, map, explored, frontier)
        pygame.display.flip()
        pygame.time.delay(100)  # Delay to visualize A* exploration
    
    path = a_star(map, start, destination, on_explore)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw the final path
        draw_map(screen, map, explored)
        for point in path:
            pygame.draw.rect(screen, RED, (point[0]*TILE_SIZE, point[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        pygame.display.flip()
        clock.tick(60)  # Refresh rate

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
