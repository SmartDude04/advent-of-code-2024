import copy

grid_input = [line.strip() for line in open("input.txt")]


# Class used to pass data by reference
class Location:
    def __init__(self, row: int, col: int, direction: str):
        self.direction: str = direction
        self.row: int = row
        self.col: int = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.direction == other.direction


class GridLocation:
    def __init__(self, row: int, col: int, marking: str):
        self.row: int = row
        self.col: int = col
        self.marking: str = marking
        self.visited: bool = False
        self.visited_orientation: str = "NA"


loc = Location(-1, -1, "up")

for cur_row, line in enumerate(grid_input):
    if "^" in line:
        loc.row = cur_row
        loc.col = line.index("^")
        grid_input[loc.row] = grid_input[cur_row][:loc.col] + "." + grid_input[loc.row][loc.col + 1:]
        break

# Convert the grid into GridLocation objects
grid: list[list[GridLocation]] = []

for i, line in enumerate(grid_input):
    grid.append([])
    for j, char in enumerate(line):
        grid[i].append(GridLocation(i, j, char))


def advance_guard(cur_loc: Location) -> bool:
    if cur_loc.direction == "up":
        if cur_loc.row == 0:
            return False
        if grid[cur_loc.row - 1][cur_loc.col].marking == "#":
            cur_loc.direction = "right"
            return True
        # Update the grid
        grid[cur_loc.row][cur_loc.col].visited = True
        grid[cur_loc.row][cur_loc.col].visited_orientation = cur_loc.direction
        cur_loc.row -= 1
    elif cur_loc.direction == "right":
        if cur_loc.col + 1 == len(grid[0]):
            return False
        if grid[cur_loc.row][cur_loc.col + 1].marking == "#":
            cur_loc.direction = "down"
            return True
        # Update the grid
        grid[cur_loc.row][cur_loc.col].visited = True
        grid[cur_loc.row][cur_loc.col].visited_orientation = cur_loc.direction
        cur_loc.col += 1
    elif cur_loc.direction == "down":
        if cur_loc.row + 1 == len(grid):
            return False
        if grid[cur_loc.row + 1][cur_loc.col].marking == "#":
            cur_loc.direction = "left"
            return True
        # Update the grid
        grid[cur_loc.row][cur_loc.col].visited = True
        grid[cur_loc.row][cur_loc.col].visited_orientation = cur_loc.direction
        cur_loc.row += 1
    elif cur_loc.direction == "left":
        if cur_loc.col == 0:
            return False
        if grid[cur_loc.row][cur_loc.col - 1].marking == "#":
            cur_loc.direction = "up"
            return True
        # Update the grid
        grid[cur_loc.row][cur_loc.col].visited = True
        grid[cur_loc.row][cur_loc.col].visited_orientation = cur_loc.direction
        cur_loc.col -= 1
    else:
        # If we get here, something went wrong, so exit
        exit(1)

    return True


def reset_visited() -> None:
    for row in grid:
        for col in row:
            col.visited = False
            col.visited_orientation = "NA"


def valid_obstacle(obstacle_row: int, obstacle_col: int, starting_loc: Location) -> bool:
    # Change the obstacle square in the grid
    assert grid[obstacle_row][obstacle_col].marking == "."
    grid[obstacle_row][obstacle_col].marking = "#"

    # Make a copy of starting_loc that doesn't reference back to the starting_loc
    cur_loc = copy.deepcopy(starting_loc)

    # Advance the guard until the function returns false, or we are at a location where our location
    # is identical to the visited grids location
    while advance_guard(cur_loc):
        if grid[cur_loc.row][cur_loc.col].visited and grid[cur_loc.row][
                cur_loc.col].visited_orientation == cur_loc.direction:
            # Set back the grid to what it was before and return success
            grid[obstacle_row][obstacle_col].marking = "."
            reset_visited()
            return True

    # Guard has left the screen, so it is not a loop; return false
    grid[obstacle_row][obstacle_col].marking = "."
    reset_visited()
    return False


total = 0
for i in range(len(grid_input)):
    for j in range(len(grid_input[i])):
        if grid_input[i][j] == ".":
            if valid_obstacle(i, j, loc):
                total += 1
                # print(f"Valid: {i}, {j} - Total: {total}")
            # else:
            #     print(f"Invalid: {i}, {j}")

# Wow, my code is incredibly inefficient, who would've guessed

# The problem lies in the fact that reset_visited() has to get called each time, which is
# horrible for performance. The rest isn't too bad

print(total)
