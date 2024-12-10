grid = [line.strip() for line in open("input.txt")]


# Class used to pass data by reference
class Location:
    def __init__(self, row: int, col: int, direction: str):
        self.direction = direction
        self.row = row
        self.col = col
        self.positions_visited = 0


loc = Location(-1, -1, "up")

for cur_row, line in enumerate(grid):
    if "^" in line:
        loc.row = cur_row
        loc.col = line.index("^")
        grid[loc.row] = grid[cur_row][:loc.col] + "." + grid[loc.row][loc.col + 1:]
        break


def advance_guard(cur_loc: Location) -> bool:
    # Helper function
    def increment_position() -> None:
        if grid[cur_loc.row][cur_loc.col] == ".":
            grid[cur_loc.row] = grid[cur_loc.row][:cur_loc.col] + "X" + grid[cur_loc.row][cur_loc.col + 1:]
            cur_loc.positions_visited += 1


    if cur_loc.direction == "up":
        if cur_loc.row == 0:
            return False
        if grid[cur_loc.row - 1][cur_loc.col] == "#":
            cur_loc.direction = "right"
            return True
        cur_loc.row -= 1
        increment_position()
        return True
    if cur_loc.direction == "right":
        if cur_loc.col + 1 == len(grid[0]):
            return False
        if grid[cur_loc.row][cur_loc.col + 1] == "#":
            cur_loc.direction = "down"
            return True
        cur_loc.col += 1
        increment_position()
        return True
    if cur_loc.direction == "down":
        if cur_loc.row + 1 == len(grid):
            return False
        if grid[cur_loc.row + 1][cur_loc.col] == "#":
            cur_loc.direction = "left"
            return True
        cur_loc.row += 1
        increment_position()
        return True
    if cur_loc.direction == "left":
        if cur_loc.col == 0:
            return False
        if grid[cur_loc.row][cur_loc.col - 1] == "#":
            cur_loc.direction = "up"
            return True
        cur_loc.col -= 1
        increment_position()
        return True

    # If we get here, something went wrong, so exit
    exit(1)


while True:
    if not advance_guard(loc):
        break

print(loc.positions_visited)
