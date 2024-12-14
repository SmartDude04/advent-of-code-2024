import re

class Robot:
    def __init__(self, grid_width: int, grid_height: int, start_x: int, start_y: int, x_vel: int, y_vel: int):
        self.grid_width: int = grid_width
        self.grid_height: int = grid_height
        self.x: int = start_x
        self.y: int = start_y
        self.x_vel: int = x_vel
        self.y_vel: int = y_vel

    def move(self) -> None:
        self.x += self.x_vel
        self.y += self.y_vel
        self.x %= self.grid_width
        self.y %= self.grid_height

    def get_position(self) -> tuple[int, int]:
        return self.y, self.x


def print_robots(robots: list[Robot], grid_width: int, grid_height: int) -> None:
    assert grid_width > 0 and grid_height > 0
    grid = [[" " for _ in range(grid_width)] for _ in range(grid_height)]
    for robot in robots:
        if grid[robot.y][robot.x] == " ":
            grid[robot.y][robot.x] = 1
        else:
            grid[robot.y][robot.x] += 1
    for row in grid:
        print("".join(map(str, row)))


def move_robots(robots: list[Robot], moves: int, do_print: bool = False, width: int = -1, height: int = -1) -> None:
    for _ in range(moves):
        for robot in robots:
            robot.move()
        if do_print:
            print("-" * width)
            print_robots(robots, width, height)
            print("-" * width)


def compute_quadrents(robots: list[Robot], grid_width: int, grid_height: int) -> int:
    quadrants = [0, 0, 0, 0]

    for robot in robots:
        # First quadrant
        for row in range(grid_height // 2):
            for col in range(grid_width // 2):
                if robot.get_position() == (row, col):
                    quadrants[0] += 1

        # Second quadrant
        for row in range(grid_height // 2 + 1, grid_height):
            for col in range(grid_width // 2):
                if robot.get_position() == (row, col):
                    quadrants[1] += 1

        # Third quadrant
        for row in range(grid_height // 2):
            for col in range(grid_width // 2 + 1, grid_width):
                if robot.get_position() == (row, col):
                    quadrants[2] += 1

        # Fourth quadrant
        for row in range(grid_height // 2 + 1, grid_height):
            for col in range(grid_width // 2 + 1, grid_width):
                if robot.get_position() == (row, col):
                    quadrants[3] += 1

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


robots: list[Robot] = []
grid_width = 101
grid_height = 103

with open("input.txt") as f:
    # Didn't know := was allowed in python. This method is how files are regularly read in C as they allow
    # assignment inside loops with =, and this is Python's way of doing that since 3.8, I guess...
    while line := f.readline():
        str_nums = re.findall(r"-?[0-9]+", line)
        nums = [int(num) for num in str_nums]

        robots.append(Robot(grid_width, grid_height, nums[0], nums[1], nums[2], nums[3]))

move_robots(robots, 100, True , grid_width, grid_height)
print(compute_quadrents(robots, grid_width, grid_height))
