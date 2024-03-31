import pygame
import sys
from collections import deque

# Constants for the game
TILE_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

def bfs(map, start, destination):
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        current = queue.popleft()
        if current == destination:
            break
        for neighbor in find_neighbors(map, current):
            if neighbor not in visited:
                queue.append(neighbor)
                visited[neighbor] = current
    
    path = []
    while current is not None:
        path.append(current)
        current = visited[current]
    path.reverse()
    return path

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
    
    path = bfs(map, start, destination)
    
    clock = pygame.time.Clock()
    index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Draw the map
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 'X':
                    pygame.draw.rect(screen, BLACK, rect)
                elif tile == '.' or tile == 'S' or tile == 'D':
                    pygame.draw.rect(screen, WHITE, rect, 1)
        
        # Draw the path
        for point in path:
            pygame.draw.rect(screen, GREEN, (point[0]*TILE_SIZE, point[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Draw the character
        if index < len(path):
            char_pos = path[index]
            pygame.draw.rect(screen, RED, (char_pos[0]*TILE_SIZE, char_pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            index += 1

        pygame.display.flip()
        clock.tick(5) # Move the character at 5 tiles per second

if __name__ == '__main__':
    main()
