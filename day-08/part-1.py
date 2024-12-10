grid = [line.strip() for line in open("input.txt")]


def draw_anti_node(first_row: int, first_col: int, second_row: int, second_col: int) -> None:
    assert grid[first_row][first_col] == grid[second_row][second_col] or grid[first_row][first_col] == "#" or grid[second_row][second_col] == "#"
    assert not (first_row == second_row and first_col == second_col)

    # Make sure the points are in order of where they appear on the grid
    if first_row > second_row:
        first_row, second_row = second_row, first_row
        first_col, second_col = second_col, first_col
    elif first_row == second_row and first_col > second_col:
        first_row, second_row = second_row, first_row
        first_col, second_col = second_col, first_col

    delta_y = second_row - first_row
    delta_x = second_col - first_col

    # If possible, draw the first anti-node
    if 0 <= first_row - delta_y < len(grid) and 0 <= first_col - delta_x < len(grid[0]):
        grid[first_row - delta_y] = (grid[first_row - delta_y][:first_col - delta_x] + "#" +
                                     grid[first_row - delta_y][first_col - delta_x + 1:])

    # If possible, draw the second anti-node
    if 0 <= second_row + delta_y < len(grid) and 0 <= second_col + delta_x < len(grid[0]):
        grid[second_row + delta_y] = (grid[second_row + delta_y][:second_col + delta_x] + "#" +
                                      grid[second_row + delta_y][second_col + delta_x + 1:])


def show_anti_nodes() -> None:
    # Collection of coordinates corresponding to a specific antenna frequency
    antenna_coords: dict[str, list[list[int]]] = {}

    # Make a hash table of antennas and all coordinates they are found on
    for row, line in enumerate(grid):
        for col, antenna in enumerate(line):
            if antenna == ".":
                continue

            if antenna not in antenna_coords.keys():
                antenna_coords[antenna] = [[row, col]]
            else:
                antenna_coords[antenna].append([row, col])

    # Go through the antenna locations and draw each combination for each antenna
    for antenna, coords in antenna_coords.items():
        # print(antenna, coords)
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                draw_anti_node(coords[i][0], coords[i][1], coords[j][0], coords[j][1])


def count_anti_nodes() -> int:
    count = 0
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == '#':
                count += 1

    return count


show_anti_nodes()
print(count_anti_nodes())
