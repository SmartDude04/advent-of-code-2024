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


def move_robots(robots: list[Robot], num_moves: int) -> None:
    for _ in range(num_moves):
        for robot in robots:
            robot.move()


def low_varience(robots: list[Robot], grid_width: int, grid_height: int) -> bool:
    x_coords: dict[int, int] = {}
    y_coords: dict[int, int] = {}
    for robot in robots:
        if robot.x in x_coords:
            x_coords[robot.x] += 1
        else:
            x_coords[robot.x] = 1

        if robot.y in y_coords:
            y_coords[robot.y] += 1
        else:
            y_coords[robot.y] = 1

    variance = 4
    x_threshold = grid_width // variance
    y_threshold = grid_height // variance

    if max(x_coords.values()) >= x_threshold and max(y_coords.values()) >= y_threshold:
        return True
    else:
        return False


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

iteration = 0

while not low_varience(robots, grid_width, grid_height):
    move_robots(robots, 1)
    iteration += 1

print_robots(robots, grid_width, grid_height)
print(iteration)