hiking_grid = []
with open("input.txt") as f:
    lines = f.readlines()
    for line in lines:
        hiking_grid.append([int(num) for num in line.strip()])


def find_trailheads(grid: list[list[int]], row: int, col: int, trailheads: set[tuple[int, int]]) -> None:
    # Base case
    if grid[row][col] == 9:
        trailheads.add((row, col))
        return

    cur_height = grid[row][col]

    # Check around and recurse
    if row > 0 and grid[row - 1][col] == cur_height + 1:
        find_trailheads(grid, row - 1, col, trailheads)
    if col + 1 < len(grid[0]) and grid[row][col + 1] == cur_height + 1:
        find_trailheads(grid, row, col + 1, trailheads)
    if row + 1 < len(grid) and grid[row + 1][col] == cur_height + 1:
        find_trailheads(grid, row + 1, col, trailheads)
    if col > 0 and grid[row][col - 1] == cur_height + 1:
        find_trailheads(grid, row, col - 1, trailheads)


def find_ratings(grid: list[list[int]], row: int, col: int) -> int:
    # Base case
    if grid[row][col] == 9:
        return 1

    cur_height = grid[row][col]

    total = 0
    if row > 0 and grid[row - 1][col] == cur_height + 1:
        total += find_ratings(grid, row - 1, col)
    if col + 1 < len(grid[0]) and grid[row][col + 1] == cur_height + 1:
        total += find_ratings(grid, row, col + 1)
    if row + 1 < len(grid) and grid[row + 1][col] == cur_height + 1:
        total += find_ratings(grid, row + 1, col)
    if col > 0 and grid[row][col - 1] == cur_height + 1:
        total += find_ratings(grid, row, col - 1)

    return total


num_trailheads = 0
sum_ratings = 0
for row, _ in enumerate(hiking_grid):
    for col, height in enumerate(_):
        if height == 0:
            trailheads = set()
            find_trailheads(hiking_grid, row, col, trailheads)
            num_trailheads += len(trailheads)
            sum_ratings += find_ratings(hiking_grid, row, col)

print(f"Number of trailheads (Part 1): {num_trailheads}")
print(f"Sum of the ratings of all trailheads (Part 2): {sum_ratings}")
