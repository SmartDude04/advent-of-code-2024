grid = [line.strip() for line in open("input.txt")]


def get_area_perimeter(grid: list[str], row: int, col: int) -> tuple[set[tuple[int, int]], tuple[int, int]]:
    def get_area_helper(grid: list[str], cur_row: int, cur_col: int, done: set[tuple[int, int]]) -> int:

        area = 1
        done.add((cur_row, cur_col))
        for i in [(cur_row - 1, cur_col), (cur_row + 1, cur_col), (cur_row, cur_col - 1), (cur_row, cur_col + 1)]:
            if 0 <= i[0] < len(grid) and 0 <= i[1] < len(grid[0]) and i not in done and \
                    grid[i[0]][i[1]] == grid[cur_row][cur_col]:
                area += get_area_helper(grid, i[0], i[1], done)

        return area

    def get_perimeter_helper(grid: list[str], cur_row: int, cur_col: int, done: set[tuple[int, int]]) -> int:

        perimeter = 0
        done.add((cur_row, cur_col))
        for i in [(cur_row - 1, cur_col), (cur_row + 1, cur_col), (cur_row, cur_col - 1), (cur_row, cur_col + 1)]:
            if i not in done:
                if 0 <= i[0] < len(grid) and 0 <= i[1] < len(grid[0]) and grid[i[0]][i[1]] == grid[cur_row][cur_col]:
                    perimeter += get_perimeter_helper(grid, i[0], i[1], done)
                else:
                    perimeter += 1

        return perimeter

    done_area_coords: set[tuple[int, int]] = set()
    area = get_area_helper(grid, row, col, done_area_coords)
    perimeter = get_perimeter_helper(grid, row, col, set())

    return done_area_coords, (area, perimeter)


done_coords: set[tuple[int, int]] = set()
total_area = 0
total_perimeter = 0
total = 0
for row, line in enumerate(grid):
    for col, char in enumerate(line):
        if (row, col) not in done_coords:
            ret_value: tuple[set[tuple[int, int]], tuple[int, int]] = get_area_perimeter(grid, row, col)
            done_coords.update(ret_value[0])
            total_area += ret_value[1][0]
            total_perimeter += ret_value[1][1]
            total += ret_value[1][0] * ret_value[1][1]

print(total)
