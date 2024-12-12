from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def turn_right(dir: Direction) -> Direction:
    if dir == Direction.UP:
        return Direction.RIGHT
    elif dir == Direction.RIGHT:
        return Direction.DOWN
    elif dir == Direction.DOWN:
        return Direction.LEFT
    elif dir == Direction.LEFT:
        return Direction.UP
    else:
        exit(1)


def turn_left(dir: Direction) -> Direction:
    if dir == Direction.UP:
        return Direction.LEFT
    elif dir == Direction.RIGHT:
        return Direction.UP
    elif dir == Direction.DOWN:
        return Direction.RIGHT
    elif dir == Direction.LEFT:
        return Direction.DOWN
    else:
        exit(1)


def turn_around(dir: Direction) -> Direction:
    if dir == Direction.UP:
        return Direction.DOWN
    elif dir == Direction.RIGHT:
        return Direction.LEFT
    elif dir == Direction.DOWN:
        return Direction.UP
    elif dir == Direction.LEFT:
        return Direction.RIGHT
    else:
        exit(1)


class Tracer:
    def __init__(self, row: int, col: int, dir: Direction = None, grid: list[str] = None):
        self.row: int = row
        self.col: int = col
        self.grid = grid
        self.num_sides = 0
        if dir is None:
            self.dir = Direction.DOWN
            self.start = Tracer(row, col, self.dir)
        else:
            self.dir = dir
            self.start = None

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.dir == other.dir

    def move(self) -> bool:
        if self.num_sides != 0 and self == self.start:
            return False

        # If we are good to turn right, we should do so to stay on the edge
        if 0 <= self.row + turn_right(self.dir).value[0] < len(self.grid) and \
                0 <= self.col + turn_right(self.dir).value[1] < len(self.grid[0]):
            if self.grid[self.row + turn_right(self.dir).value[0]][self.col + turn_right(self.dir).value[1]] == \
                    self.grid[self.row][self.col]:
                self.num_sides += 1
                self.dir = turn_right(self.dir)

                # Then move forward
                self.row += self.dir.value[0]
                self.col += self.dir.value[1]
                return True

        # Check if good to move in front
        if 0 <= self.row + self.dir.value[0] < len(self.grid) and \
                0 <= self.col + self.dir.value[1] < len(self.grid[0]):
            if self.grid[self.row + self.dir.value[0]][self.col + self.dir.value[1]] == self.grid[self.row][self.col]:
                # Good to move, so just advance
                self.row += self.dir.value[0]
                self.col += self.dir.value[1]
                return True

        # If we aren't able to move forward or turn right keep turning left until you are able to move, or you
        # get back to the beginning
        while (self != self.start or self.num_sides == 0) and \
                (not (0 <= self.row + self.dir.value[0] < len(self.grid)) or
                 not (0 <= self.col + self.dir.value[1] < len(self.grid[0])) or
                 self.grid[self.row + self.dir.value[0]][self.col + self.dir.value[1]] != self.grid[self.row][
                     self.col]):
            self.dir = turn_left(self.dir)
            self.num_sides += 1

        return True

def get_area_sides(grid: list[str], row: int, col: int) -> tuple[set[tuple[int, int]], tuple[int, int]]:
    def get_area_helper(grid: list[str], cur_row: int, cur_col: int, done: set[tuple[int, int]]) -> int:

        area = 1
        done.add((cur_row, cur_col))
        for i in [(cur_row - 1, cur_col), (cur_row + 1, cur_col), (cur_row, cur_col - 1), (cur_row, cur_col + 1)]:
            if 0 <= i[0] < len(grid) and 0 <= i[1] < len(grid[0]) and i not in done and \
                    grid[i[0]][i[1]] == grid[cur_row][cur_col]:
                area += get_area_helper(grid, i[0], i[1], done)

        return area

    def get_sides_helper(grid: list[str], cur_row: int, cur_col: int) -> int:
        cur_tracer = Tracer(cur_row, cur_col, grid=grid)
        while True:
            if not cur_tracer.move():
                break

        return cur_tracer.num_sides

    done_area_coords: set[tuple[int, int]] = set()
    area = get_area_helper(grid, row, col, done_area_coords)
    sides = get_sides_helper(grid, row, col)

    return done_area_coords, (area, sides)


grid = [line.strip() for line in open("input.txt")]
done_coords: set[tuple[int, int]] = set()
total = 0
for row, line in enumerate(grid):
    for col, char in enumerate(line):
        if (row, col) not in done_coords:
            ret_value: tuple[set[tuple[int, int]], tuple[int, int]] = get_area_sides(grid, row, col)
            done_coords.update(ret_value[0])
            total += ret_value[1][0] * ret_value[1][1]

print(total)
