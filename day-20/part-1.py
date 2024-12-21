import heapq


def find_start_end(maze: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
    start_coords: tuple[int, int] = (0, 0)
    end_coords: tuple[int, int] = (0, 0)

    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == "S":
                start_coords = (row, col)
                maze[row][col] = "."
            elif char == "E":
                end_coords = (row, col)
                maze[row][col] = "."

    return start_coords, end_coords


def get_adjacent_vertices(maze: list[list[str]], cur_coord: tuple[int, int]) -> list[tuple[int, int]]:
    adj_coords = []

    cur_row, cur_col = cur_coord
    if cur_row + 1 < len(maze) and maze[cur_row + 1][cur_col] == ".":
        adj_coords.append((cur_row + 1, cur_col))
    if cur_row > 0 and maze[cur_row - 1][cur_col] == ".":
        adj_coords.append((cur_row - 1, cur_col))
    if cur_col + 1 < len(maze[0]) and maze[cur_row][cur_col + 1] == ".":
        adj_coords.append((cur_row, cur_col + 1))
    if cur_col > 0 and maze[cur_row][cur_col - 1] == ".":
        adj_coords.append((cur_row, cur_col - 1))

    return adj_coords


def picoseconds_to_end(maze: list[list[str]], start_coords: tuple[int, int], end_coords: tuple[int, int]) -> int:
    # Use Dijkstra pathfinding algorithm
    pq: list[tuple[int, tuple[int, int]]] = [(0, start_coords)]
    distances: dict[tuple[int, int], int] = {start_coords: 0}
    prev_locs: dict[tuple[int, int], tuple[int, int]] = {start_coords: (0, 0)}

    while pq:
        cur_vertex = heapq.heappop(pq)

        adj_coords = get_adjacent_vertices(maze, cur_vertex[1])

        for adj in adj_coords:
            alt_distance = distances[cur_vertex[1]] + 1

            if adj not in distances or alt_distance < distances[adj]:
                distances[adj] = alt_distance
                prev_locs[adj] = cur_vertex[1]
                heapq.heappush(pq, (alt_distance, adj))

    return distances[end_coords]


maze: list[list[str]] = []
with open("input.txt") as f:
    while line := f.readline():
        maze.append(list(line.strip()))

start_coords, end_coords = find_start_end(maze)
base_time = picoseconds_to_end(maze, start_coords, end_coords)
time_savings: dict[int, int] = {}
num_good_cheats = 0
for row, line in enumerate(maze):
    for col, char in enumerate(line):
        if char == "#":
            # Remove a wall and replace it with a free spot, then try the pathfinding
            maze[row][col] = "."

            cheat_time = picoseconds_to_end(maze, start_coords, end_coords)
            if cheat_time < base_time:
                diff = base_time - cheat_time
                if diff not in time_savings:
                    time_savings.update({diff: 0})
                time_savings[diff] += 1
                if diff == 2:
                    print(row, col)
                if diff >= 100:
                    num_good_cheats += 1

            # Reset the maze
            maze[row][col] = "#"
    # print(f"Row {row + 1}")

print(time_savings)
print(f"Number of cheats that save at least 100 picoseconds: {num_good_cheats}")
