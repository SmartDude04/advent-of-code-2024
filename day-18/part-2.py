import re
import heapq


def get_adjacent_vertices(memory_grid: list[list[str]], cur_coord: tuple[int, int]) -> list[tuple[int, int]]:
    coords: list[tuple[int, int]] = []
    cur_row, cur_col = cur_coord
    if cur_row > 0 and memory_grid[cur_row - 1][cur_col] == ".":
        coords.append((cur_row - 1, cur_col))
    if cur_row + 1 < len(memory_grid) and memory_grid[cur_row + 1][cur_col] == ".":
        coords.append((cur_row + 1, cur_col))
    if cur_col > 0 and memory_grid[cur_row][cur_col - 1] == ".":
        coords.append((cur_row, cur_col - 1))
    if cur_col + 1 < len(memory_grid) and memory_grid[cur_row][cur_col + 1] == ".":
        coords.append((cur_row, cur_col + 1))

    return coords


def find_path(memory_grid: list[list[str]], completed_path: list[tuple[int, int]]) -> int:
    """Find the shortest path using Dijkstra's algorithm. Code adapted from Day 16 Part 1"""

    # Priority queue storing distance from start to the point
    pq: list[tuple[int, tuple[int, int]]] = [(0, (0, 0))]
    # Distances from a location
    distances: dict[tuple[int, int], int] = {(0, 0): 0}
    # Previous coordinates from a path
    prev_coords: dict[tuple[int, int], tuple[int, int]] = {(0, 0): (0, 0)}

    while pq:
        cur_vertex = heapq.heappop(pq)

        adjacent_vertices = get_adjacent_vertices(memory_grid, cur_vertex[1])

        for vertex in adjacent_vertices:
            alt_distance = distances[cur_vertex[1]] + 1

            if vertex not in distances or alt_distance < distances[vertex]:
                distances.update({vertex: alt_distance})
                prev_coords.update({vertex: cur_vertex})

                # Add this vertex to the priority queue
                heapq.heappush(pq, (alt_distance, vertex))

    if (len(memory_grid) - 1, len(memory_grid[0]) - 1) not in distances.keys():
        return -1
    return distances[(len(memory_grid) - 1, len(memory_grid[0]) - 1)]


size = 71
memory_grid: list[list[str]] = [["." for _ in range(size)] for _ in range(size)]

with open("input.txt") as f:
    while (line := f.readline().strip()):
        coords = re.findall(r"[0-9]+", line)
        memory_grid[int(coords[1])][int(coords[0])] = "#"

        distance = find_path(memory_grid, coords)
        if distance == -1:
            print(coords)
            break


