import sys
import cv2
import time
from pprint import pprint


def begin_end_locs(maze):
    maze_length = len(maze)
    openings = []

    l_side = [[i, 0] for i in range(maze_length) if maze[i][0] == 1]
    top    = [[0, i] for i in range(maze_length) if maze[0][i] == 1]
    bottom = [[maze_length - 1, i] for i in range(maze_length) if maze[-1][i] == 1]
    r_side = [[i, maze_length - 1] for i in range(maze_length) if maze[i][-1] == 1]
    
    all_heads = [l_side, top, r_side, bottom, [[0, 0]]]
    
    for row in all_heads:
        for i in row:
            openings.append(i)
        if len(openings) == 2:
            break

    return openings


def next_possible_move(maze: list, loc):
    x = loc[0]
    r_x = x + 1
    l_x = x - 1
    
    y = loc[1]
    u_y = y + 1
    d_y = y - 1

    possible_moves = []

    if x == 0:
        possible_moves.extend([[r_x, y], [x, u_y], [x, d_y]])
    elif x == len(maze) - 1:
        possible_moves.extend([[l_x, y], [x, u_y], [x, d_y]])
    elif y == 0:
        possible_moves.extend([[r_x, y], [l_x, y], [x, u_y]])
    elif y == len(maze) - 1:
        possible_moves.extend([[r_x, y], [l_x, y], [x, d_y]])
    else:
        possible_moves.extend([[r_x, y], [l_x, y], [x, u_y], [x, d_y]])

    return [pos for pos in possible_moves if maze[pos[0]][pos[1]]]

def sorter(head, end):
    x = end[0]
    y = end[1]

    return [x for _,x in sorted(zip([abs(v[0] - x) + abs(v[1] - y) for v in head], head))]


def traverse(maze, loc, end, last):
    if loc == end:
        return [last]
    
    moves = next_possible_move(maze, loc)
    # sorted_moves = sorter(moves, end)

    for move in moves:
        if move == last:
            continue

        if (point := traverse(maze, move, end, loc)) != False:
            return point + [move]
    
    return False

if __name__ == "__main__":
    sys.setrecursionlimit(2147483647)
    for i in ["10", "20", "30", "50", "100", "200", "500", "900"]:
        name = f"maze_{i}"
        img_maze = cv2.imread(f"{name}.png")
        maze = []

        for row in img_maze.tolist():
            maze.append([1 if pixel == [255, 255, 255] else 0 for pixel in row])

        start, end = begin_end_locs(maze)
        path = traverse(maze, start, end, start)

        for k, move in enumerate(path):
            change = 255 / len(path) * k
            x = move[0]
            y = move[1]
            img_maze[x, y] = [0 + change, 0, 255 - change]

        cv2.imwrite(f"{name}_solved.png", img_maze)

        print(f"Name of Maze                   : {name}")
        print(f"Pixels needed to solve the maze: {len(path)}")
        # print(f"Time taken                     : {time.perf_counter()}")
