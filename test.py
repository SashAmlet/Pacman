### ПОИСК В ШИРИНУ ###

from collections import deque
import pygame
import config as g

pygame.init()


def draw_board(lvl):
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1: # Wall
                pygame.draw.rect(g.screen, g.color, (j * g.pixel_w, i * g.pixel_h, g.pixel_w, g.pixel_h))
            if lvl[i][j] == 2: # Little treat
                pygame.draw.circle(g.screen, 'white', (j * g.pixel_w + (0.5 * g.pixel_w), i * g.pixel_h + (0.5 * g.pixel_h)), 4)
            if lvl[i][j] == 3: # Big treat
                pygame.draw.circle(g.screen, 'white', (j * g.pixel_w + (0.5 * g.pixel_w), i * g.pixel_h + (0.5 * g.pixel_h)), 10)

def draw_path(path):
    for coord in path:
        pygame.draw.circle(g.screen, 'red', (coord[0] * g.pixel_w + (0.5 * g.pixel_w), coord[1] * g.pixel_h + (0.5 * g.pixel_h)), 2)

def is_valid_move(matrix, x, y):
    rows, cols = len(matrix), len(matrix[0])
    return 0 <= x < rows and 0 <= y < cols and matrix[y][x] in {0, 2, 3, 4}

def bfs_shortest_path(matrix, start, end):    
    # R, L, U, D
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    paths = []
    
    # Очередь для BFS: каждый элемент - это (x, y, путь_до_этой_точки)
    queue = deque([(start[0], start[1], [])])
    visited = set()  # множество посещенных клеток
    visited.add((start[0], start[1]))
    
    while queue:
        x, y, path = queue.popleft()
        
        # Если достигли конечной точки, возвращаем путь
        if (x, y) == end:
            paths.append(path + [(x, y)])
        
        # Проверяем всех соседей
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if is_valid_move(matrix, nx, ny) and (nx, ny) not in visited:
                queue.append((nx, ny, path + [(x, y)]))
                visited.add((nx, ny))
    
    return paths

# Пример использования
matrix = [
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

start = (0, 0)  # Начальная точка
end = (19, 19)  # Конечная точка

paths = bfs_shortest_path(matrix, start, end)

path =  min(paths, key=len)

print("The minimum path:", path)


fps = 60
timer = pygame.time.Clock()
run = True

while run:
    timer.tick(fps)
    g.screen.fill('black')
    draw_board(matrix)
    draw_path(path)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    pygame.display.flip() 


pygame.quit()
