class Robot:
    def __init__(self, cur_row: int, cur_col: int):
        self.row: int = cur_row
        self.col: int = cur_col

    def move(self, move_row: int, move_col: int) -> None:
        self.row += move_row
        self.col += move_col


def convert_direction(direction: str) -> tuple[int, int]:
    if direction == "<":
        return 0, -1
    elif direction == "^":
        return -1, 0
    elif direction == ">":
        return 0, 1
    elif direction == "v":
        return 1, 0
    else:
        raise ValueError(f"Invalid direction: {direction}")


def move_robot(robot: Robot, c_dir: tuple[int, int], walls: set[tuple[int, int]], boxes: set[tuple[int, int]]) -> None:

    # Check that the robot is able to move
    new_row, new_col = robot.row + c_dir[0], robot.col + c_dir[1]
    while (new_row, new_col) in boxes:
        new_row += c_dir[0]
        new_col += c_dir[1]
    if (new_row, new_col) in walls:
        return

    # Move the boxes then the robot once done with the while loop
    while (new_row - c_dir[0], new_col - c_dir[1]) != (robot.row, robot.col):
        boxes.remove((new_row - c_dir[0], new_col - c_dir[1]))
        boxes.add((new_row, new_col))
        new_row, new_col = new_row - c_dir[0], new_col - c_dir[1]

    # We are now on the robot's move; do that
    robot.move(c_dir[0], c_dir[1])
    assert new_row == robot.row and new_col == robot.col


def print_warehouse(robot: Robot, walls: set[tuple[int, int]], boxes: set[tuple[int, int]], width: int, height: int) -> None:
    for row in range(height):
        for col in range(width):
            if (row, col) in boxes:
                print("O", end="")
            elif (row, col) in walls:
                print("#", end="")
            elif (row, col) == (robot.row, robot.col):
                print("@", end="")
            else:
                print(".", end="")
        print("")
    print("\n")


robot = None
walls: set[tuple[int, int]] = set()
boxes: set[tuple[int, int]] = set()
directions = False
warehouse_width = 0
warehouse_height = 0
with open("input.txt") as f:
    input_file = f.readlines()
    for row, line in enumerate(input_file):
        for col, char in enumerate(line.strip()):
            if directions or char in ["^", ">", "V", "<"]:
                # print_warehouse(robot, walls, boxes, warehouse_width, warehouse_height)
                move_robot(robot, convert_direction(char), walls, boxes)
                directions = True
            elif char == "@":
                robot = Robot(row, col)
            elif char == "#":
                walls.add((row, col))
                warehouse_width = max(warehouse_width, col + 1)
                warehouse_height = max(warehouse_height, row + 1)
            elif char == "O":
                boxes.add((row, col))

total = 0
for box in boxes:
    total += (100 * box[0] + box[1])

print_warehouse(robot, walls, boxes, warehouse_width, warehouse_height)
print(total)
