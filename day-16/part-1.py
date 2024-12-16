import functools
import enum
import sys
import queue


class Direction(enum.Enum):
    UP: tuple[int, int] = (-1, 0)
    DOWN: tuple[int, int] = (1, 0)
    LEFT: tuple[int, int] = (0, -1)
    RIGHT: tuple[int, int] = (0, 1)


class Score:
    def __init__(self, score: int):
        self.score = score


grid: list[list[str]] = [list(line.strip()) for line in open("input.txt")]


def worker(task_queue, result_queue):
    while True:
        try:
            # Get task from queue
            data = task_queue.get(timeout=3)
        except queue.Empty:
            break

        # Base case
        if grid[data[1]][data[2]] == "E":
            # Process the base-case
            result_queue.put(data[4])
        else:
            # Rest of recursive function; process data then recurse
            completed_coords = data[0]
            cur_row = data[1]
            cur_col = data[2]
            cur_coords: tuple[tuple[int, int]] = ((cur_row, cur_col),)
            cur_dir = data[3]
            cur_score = data[4]
            new_completed = data[0] + cur_coords

            # Look around for free slots and recurse if found
            min_score: int = sys.maxsize
            turned = False


def get_lowest_score(completed_coords, cur_row: int, cur_col: int, cur_dir: Direction) -> int:
    # Base case
    if grid[cur_row][cur_col] == "E":
        print("Reached end")
        return 0

    cur_coords: tuple[tuple[int, int]] = ((cur_row, cur_col),)
    new_completed = completed_coords + cur_coords

    # Look around for free slots and recurse if found
    min_score: int = sys.maxsize
    turned = False

    if grid[cur_row + cur_dir.value[0]][cur_col + cur_dir.value[1]] in [".", "E"] and \
            (cur_row + cur_dir.value[0], cur_col + cur_dir.value[1]) not in completed_coords:
        score = get_lowest_score(new_completed, cur_row + cur_dir.value[0], cur_col + cur_dir.value[1], cur_dir)
        min_score = score
    if cur_dir != Direction.UP and \
            grid[cur_row + Direction.UP.value[0]][cur_col + Direction.UP.value[1]] in [".", "E"] and \
            (cur_row + Direction.UP.value[0], cur_col + Direction.UP.value[1]) not in completed_coords:
        score = get_lowest_score(new_completed, cur_row + Direction.UP.value[0], cur_col + Direction.UP.value[1], Direction.UP)
        if score < min_score:
            turned = True
            min_score = score
    if cur_dir != Direction.DOWN and \
            grid[cur_row + Direction.DOWN.value[0]][cur_col + Direction.DOWN.value[1]] in [".", "E"] and \
            (cur_row + Direction.DOWN.value[0], cur_col + Direction.DOWN.value[1]) not in completed_coords:
        score = get_lowest_score(new_completed, cur_row + Direction.DOWN.value[0], cur_col + Direction.DOWN.value[1], Direction.DOWN)
        if score < min_score:
            turned = True
            min_score = score
    if cur_dir != Direction.LEFT and \
            grid[cur_row + Direction.LEFT.value[0]][cur_col + Direction.LEFT.value[1]] in [".", "E"] and \
            (cur_row + Direction.LEFT.value[0], cur_col + Direction.LEFT.value[1]) not in completed_coords:
        score = get_lowest_score(new_completed, cur_row + Direction.LEFT.value[0], cur_col + Direction.LEFT.value[1], Direction.LEFT)
        if score < min_score:
            turned = True
            min_score = score
    if cur_dir != Direction.RIGHT and \
            grid[cur_row + Direction.RIGHT.value[0]][cur_col + Direction.RIGHT.value[1]] == '.' and \
            (cur_row + Direction.RIGHT.value[0], cur_col + Direction.RIGHT.value[1]) not in completed_coords:
        score = get_lowest_score(new_completed, cur_row + Direction.RIGHT.value[0], cur_col + Direction.RIGHT.value[1], Direction.RIGHT)
        if score < min_score:
            turned = True
            min_score = score

    # Turn back the square
    if turned:
        return 1001 + min_score
    return 1 + min_score

def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == "S":
                grid[row][col] = "."
                return row, col

    raise ValueError("Unable to find starting location")



start_row, start_col = find_start(grid)
print(get_lowest_score(tuple(), start_row, start_col, Direction.RIGHT))