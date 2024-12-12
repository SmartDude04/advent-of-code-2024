def in_bounds(row: int, col: int, grid: list[str]) -> bool:
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


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
        def get_shape_coords(grid: list[str], cur_row: int, cur_col: int, coords: set[tuple[int, int]]) -> None:
            coords.add((cur_row, cur_col))

            for i in [(cur_row - 1, cur_col), (cur_row + 1, cur_col), (cur_row, cur_col - 1), (cur_row, cur_col + 1)]:
                if 0 <= i[0] < len(grid) and 0 <= i[1] < len(grid[0]) and \
                        grid[i[0]][i[1]] == grid[cur_row][cur_col] and i not in coords:
                    get_shape_coords(grid, i[0], i[1], coords)

        shape_coords: set[tuple[int, int]] = set()
        get_shape_coords(grid, cur_row, cur_col, shape_coords)
        num_sides = 0

        # Depending on the pieces surrounding the coordinate, add a certain amount of sides
        check = [((-1, 0), (0, 1)), ((0, 1), (1, 0)), ((1, 0), (0, -1)), ((0, -1), (-1, 0))]
        cur_shape = grid[cur_row][cur_col]
        for coord in shape_coords:
            for diff in check:
                first_diff = diff[0]
                second_diff = diff[1]
                third_diff = (first_diff[0] + second_diff[0], first_diff[1] + second_diff[1])

                # Check bounds first
                if 0 <= coord[0] + first_diff[0] < len(grid) and 0 <= coord[1] + first_diff[1] < len(grid[0]) and \
                        0 <= coord[0] + second_diff[0] < len(grid) and 0 <= coord[1] + second_diff[1] < len(grid[0]):
                    if grid[coord[0] + first_diff[0]][coord[1] + first_diff[1]] == cur_shape and \
                            grid[coord[0] + second_diff[0]][coord[1] + second_diff[1]] == cur_shape:
                        if grid[coord[0] + third_diff[0]][coord[1] + third_diff[1]] != cur_shape:
                            num_sides += 1
                    elif grid[coord[0] + first_diff[0]][coord[1] + first_diff[1]] != cur_shape and \
                            grid[coord[0] + second_diff[0]][coord[1] + second_diff[1]] != cur_shape:
                        num_sides += 1
                elif not in_bounds(coord[0] + first_diff[0], coord[1] + first_diff[1], grid) and \
                        in_bounds(coord[0] + second_diff[0], coord[1] + second_diff[1], grid):
                    if grid[coord[0] + second_diff[0]][coord[1] + second_diff[1]] != cur_shape:
                        num_sides += 1
                elif not in_bounds(coord[0] + second_diff[0], coord[1] + second_diff[1], grid) and \
                        in_bounds(coord[0] + first_diff[0], coord[1] + first_diff[1], grid):
                    if grid[coord[0] + first_diff[0]][coord[1] + first_diff[1]] != cur_shape:
                        num_sides += 1
                else:
                    num_sides += 1

        return num_sides

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
