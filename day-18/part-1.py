import re
import sys


def find_path(memory_grid: list[list[str]], completed_path: list[tuple[int, int]]) -> int:
    # Base case
    if completed_path[-1] == (len(memory_grid) - 1, len(memory_grid[0]) - 1):
        print(len(memory_grid))
        return 0

    cur_row, cur_col = completed_path[-1]

    min_distance = sys.maxsize
    if cur_row > 0 and memory_grid[cur_row - 1][cur_col] == "." and (cur_row - 1, cur_col) not in completed_path:
        min_distance = min(min_distance, find_path(memory_grid, completed_path + [(cur_row - 1, cur_col)]))
    if cur_row + 1 < len(memory_grid) and memory_grid[cur_row + 1][cur_col] == "." and (cur_row + 1, cur_col) not in completed_path:
        min_distance = min(min_distance, find_path(memory_grid, completed_path + [(cur_row + 1, cur_col)]))
    if cur_col > 0 and memory_grid[cur_row][cur_col - 1] == "." and (cur_row, cur_col - 1) not in completed_path:
        min_distance = min(min_distance, find_path(memory_grid, completed_path + [(cur_row, cur_col - 1)]))
    if cur_col + 1 < len(memory_grid[0]) and memory_grid[cur_row][cur_col + 1] == "." and (cur_row, cur_col + 1) not in completed_path:
        min_distance = min(min_distance, find_path(memory_grid, completed_path + [(cur_row, cur_col + 1)]))

    return 1 + min_distance


size = 71
memory_grid: list[list[str]] = [["." for _ in range(size)] for _ in range(size)]

with open("input.txt") as f:
    counter = 0
    max_bytes = 1024
    while (line := f.readline().strip()) and counter < max_bytes:
        coords = re.findall(r"[0-9]+", line)
        memory_grid[int(coords[1])][int(coords[0])] = "#"
        counter += 1

print(find_path(memory_grid, [(0, 0)]))

