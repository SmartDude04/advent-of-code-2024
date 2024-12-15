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


def able_to_move(cur_pos: tuple[int, int], c_dir: tuple[int, int], boxes: set[tuple[tuple[int, int], tuple[int, int]]], walls: set[tuple[tuple[int, int], tuple[int, int]]]) -> bool:
    def move_dfs(cur_pos: tuple[int, int], vert: int, boxes: set[tuple[tuple[int, int], tuple[int, int]]], walls: set[tuple[tuple[int, int], tuple[int, int]]]) -> bool:
        new_pos = (cur_pos[0] + vert, cur_pos[1])
        for wall in walls:
            if new_pos == wall[0] or new_pos == wall[1]:
                return False
        for box in boxes:
            if new_pos == box[0] or new_pos == box[1]:
                return move_dfs(box[0], vert, boxes, walls) and move_dfs(box[1], vert, boxes, walls)

        return True

    # If we are trying to move horizontally, we can just go through
    # If we are trying to move vertically, we need to recurse with a helper function to check the expansion
    if c_dir[0] == 0:
        new_row, new_col = robot.row, robot.col + c_dir[1]
        found = True
        while found:
            found = False
            for box in boxes:
                if box[0] == (new_row, new_col) or box[1] == (new_row, new_col):
                    new_col += (c_dir[1] * 2)
                    found = True
                    break

        for wall in walls:
            if (new_row, new_col) == wall[0] or (new_row, new_col) == wall[1]:
                return False
        return True
    else:
        # Use the helper function to implement dfs search
        return move_dfs(cur_pos, c_dir[0], boxes, walls)


def move_box_vert(cur_box: tuple[tuple[int, int], tuple[int, int]], vert: int, boxes: set[tuple[tuple[int, int], tuple[int, int]]], walls: set[tuple[tuple[int, int], tuple[int, int]]]) -> None:
    assert cur_box in boxes

    new_box_first = (cur_box[0][0] + vert, cur_box[0][1])
    new_box_second = (cur_box[1][0] + vert, cur_box[1][1])
    # Move all boxes in front of this one
    for box in boxes:
        box_first = box[0]
        box_second = box[1]
        if box_first == new_box_first or box_first == new_box_second or box_second == new_box_first or box_second == new_box_second:
            move_box_vert(box, vert, boxes, walls)

    # Now we should have an empty space in front of this box. Move it
    boxes.remove(cur_box)
    boxes.add((new_box_first, new_box_second))


def move_robot(robot: Robot, c_dir: tuple[int, int], walls: set[tuple[tuple[int, int], tuple[int, int]]], boxes: set[tuple[tuple[int, int], tuple[int, int]]]) -> None:

    # Check that the robot is able to move
    if not able_to_move((robot.row, robot.col), c_dir, boxes, walls):
        return

    if c_dir[0] == 0:
        # Moving horizontally
        new_pos = (robot.row, robot.col + c_dir[1])
        found = True
        while found:
            found = False
            for box in boxes:
                # If we are skipping the right coord for each box, we only need to check its left coord
                # or right coord if moving to the right
                if c_dir[1] == -1:
                    if new_pos == box[1]:
                        new_pos = (new_pos[0], new_pos[1] - 2)
                        found = True
                        break
                elif c_dir[1] == 1:
                    if new_pos == box[0]:
                        new_pos = (new_pos[0], new_pos[1] + 2)
                        found = True
                        break

        # Move the blocks
        while (new_pos[0], new_pos[1] - c_dir[1]) != (robot.row, robot.col):
            if c_dir[1] == 1:
                boxes.remove(((new_pos[0], new_pos[1] - 2), (new_pos[0], new_pos[1] - 1)))
                boxes.add(((new_pos[0], new_pos[1] - 1), (new_pos[0], new_pos[1])))
                new_pos = (new_pos[0], new_pos[1] - 2)
            elif c_dir[1] == -1:
                boxes.remove(((new_pos[0], new_pos[1] + 1), (new_pos[0], new_pos[1] + 2)))
                boxes.add(((new_pos[0], new_pos[1]), (new_pos[0], new_pos[1] + 1)))
                new_pos = (new_pos[0], new_pos[1] + 2)
            else:
                raise ValueError(f"Invalid direction: {c_dir}")

        # Move the robot
        robot.move(c_dir[0], c_dir[1])
        assert (robot.row, robot.col) == new_pos
    elif c_dir[1] == 0:
        new_pos = (robot.row + c_dir[0], robot.col)
        # If there is a box in front of the robot, then we need to move it first
        for box in boxes:
            if new_pos == box[0] or new_pos == box[1]:
                move_box_vert(box, c_dir[0], boxes, walls)

        # Then move the robot
        robot.move(c_dir[0], c_dir[1])
        assert (robot.row, robot.col) == new_pos


def print_warehouse(robot: Robot, walls: set[tuple[tuple[int, int], tuple[int, int]]], boxes: set[tuple[tuple[int, int], tuple[int, int]]], width: int, height: int) -> None:
    printed_robot = False
    for row in range(height):
        for col in range(0, width):
            done = False
            # A lot slower than the first part as you can't leverage the O(1) speed of hashing and instead
            # need to go through each element
            for box in boxes:
                if (row, col) == box[0]:
                    print("[", end="")
                    done = True
                    break
                if (row, col) == box[1]:
                    print("]", end="")
                    done = True
                    break

            if not done:
                for wall in walls:
                    if (row, col) == wall[0] or (row, col) == wall[1]:
                        print("#", end="")
                        done = True
                        break

            if not done and (row, col) == (robot.row, robot.col):
                print("@", end="")
                printed_robot = True
                done = True

            if not done:
                print(".", end="")

        print("")
    print("\n")


robot = None
walls: set[tuple[tuple[int, int], tuple[int, int]]] = set()
boxes: set[tuple[tuple[int, int], tuple[int, int]]] = set()
directions = False
warehouse_width = 0
warehouse_height = 0
with open("input.txt") as f:
    input_file = f.readlines()
    for row, line in enumerate(input_file):
        for col, char in enumerate(line.strip()):
            if directions or char in ["^", ">", "V", "<"]:
                # print(f"Moving: {char}")
                # print_warehouse(robot, walls, boxes, warehouse_width, warehouse_height)
                move_robot(robot, convert_direction(char), walls, boxes)
                directions = True
            elif char == "@":
                robot = Robot(row, col * 2)
            elif char == "#":
                walls.add(((row, col * 2), (row, col * 2 + 1)))
                warehouse_width = max(warehouse_width, col * 2 + 2)
                warehouse_height = max(warehouse_height, row + 1)
            elif char == "O":
                boxes.add(((row, col * 2), (row, col * 2 + 1)))

total = 0
for box in boxes:
    total += (100 * box[0][0] + box[0][1])

print_warehouse(robot, walls, boxes, warehouse_width, warehouse_height)
print(total)
