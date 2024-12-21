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


def distance_between(first: tuple[int, int], second: tuple[int, int]) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def valid_shortcut(maze: list[list[str]], shortcut_start: tuple[int, int], shortcut_end: tuple[int, int]) -> bool:
    # Check bounds first
    if not (0 <= shortcut_end[0] < len(maze) and 0 <= shortcut_end[1] < len(maze[0])):
        return False

    # Verify the shortcut starts and ends on good parts of the maze
    start_row, start_col = shortcut_start
    end_row, end_col = shortcut_end
    return maze[start_row][start_col] == "." and maze[end_row][end_col] == "."


def dijkstra(maze: list[list[str]], start_coords: tuple[int, int]) -> (
        tuple)[dict[tuple[int, int], int], dict[tuple[int, int], tuple[int, int]]]:
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

    return distances, prev_locs


maze: list[list[str]] = []
with open("input.txt") as f:
    while line := f.readline():
        maze.append(list(line.strip()))

start_coords, end_coords = find_start_end(maze)

from_start: dict[tuple[int, int], int] = dijkstra(maze, start_coords)[0]
from_end: dict[tuple[int, int], int] = dijkstra(maze, end_coords)[0]
base_time = from_start[end_coords]

original_paths: dict[tuple[int, int], tuple[int, int]] = dijkstra(maze, start_coords)[1]
path: list[tuple[int, int]] = [end_coords]
while path[-1] != start_coords:
    path.append(original_paths[path[-1]])
path = path[1:]
completed_shortcuts: set[tuple[tuple[int, int], tuple[int, int]]] = set()
cheats: dict[int, int] = {}

for coord in path:
    # Look around this coordinate for shortcuts that can be made
    for diff_row in range(-20, 21):
        for diff_col in range(-20 + abs(diff_row), 21 - abs(diff_row)):
            end_coord = (coord[0] + diff_row, coord[1] + diff_col)
            if valid_shortcut(maze, coord, end_coord):
                # Valid shortcut, determine how much the shortcut saves in time
                if end_coord in from_end:
                    start_to_first = from_start[coord]
                    end_to_second = from_end[end_coord]
                    shortcut_distance = distance_between(coord, end_coord)
                    total_distance = start_to_first + shortcut_distance + end_to_second
                    if total_distance < base_time and (base_time - total_distance) >= 100:
                        # Good shortcut, add it to the completed shortcuts set
                        completed_shortcuts.add((coord, end_coord))

                        if (base_time - total_distance) not in cheats:
                            cheats.update({base_time - total_distance: 0})
                        cheats[base_time - total_distance] += 1

print(sum(cheats.values()))