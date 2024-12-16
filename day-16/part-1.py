# Using priority queue in Dijkstra's algorithm
import heapq

def get_weight_values(maze: list[str], cur_loc: tuple[int, int], prev_loc: tuple[int, int]) -> dict[tuple[int, int], int]:
    weights: dict[tuple[int, int], int] = {}
    direction = (cur_loc[0] - prev_loc[0], cur_loc[1] - prev_loc[1])
    for cur_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if maze[cur_loc[0] + cur_direction[0]][cur_loc[1] + cur_direction[1]] == ".":
            weights.update({(cur_loc[0] + cur_direction[0], cur_loc[1] + cur_direction[1]): 1001})
    if prev_loc in weights:
        weights[prev_loc] = 2001
    if (cur_loc[0] + direction[0], cur_loc[1] + direction[1]) in weights:
        weights[(cur_loc[0] + direction[0], cur_loc[1] + direction[1])] = 1
    return weights


def get_adjacent_coords(maze: list[str], cur_loc: tuple[int, int]) -> list[tuple[int, int]]:
    good_coords: list[tuple[int, int]] = []
    for cur_direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if maze[cur_loc[0] + cur_direction[0]][cur_loc[1] + cur_direction[1]] == ".":
            good_coords.append((cur_loc[0] + cur_direction[0], cur_loc[1] + cur_direction[1]))
    return good_coords


def get_start_coords(maze: list[str]) -> tuple[int, int]:
    """Gets the starting coordinates and replaces the character with a period"""
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == "S":
                maze[row] = line[:col] + "." + line[col + 1:]
                return row, col


def get_end_coords(maze: list[str]) -> tuple[int, int]:
    """Gets the starting coordinates and replaces the character with a period"""
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == "E":
                maze[row] = line[:col] + "." + line[col + 1:]
                return row, col


def dijkstra(maze: list[str], start_coords: tuple[int, int], end_coords: tuple[int, int]) -> int:
    """Uses Dijkstra's algorithm to find the shortest path between two points"""

    # Make the priority queue and add the starting coordinate
    pq: list[tuple[int, tuple[int, int]]] = [(0, start_coords)]
    # Make the distances hashmap and add the starting coordinate
    distances: dict[tuple[int, int], int] = {start_coords: 0}
    # Hashmap storing a list of all previous coordinates followed to get to this location
    prev_locs: dict[tuple[int, int], list[tuple[int, int]]] = {start_coords: [(start_coords[0], start_coords[1] - 1)]}

    while pq:
        # Get the shortest path vertex from the priority queue in (length, coord) format
        cur_vertex = heapq.heappop(pq)

        # Get all adjacent coordinates to this one
        adjacent_vertexes = get_adjacent_coords(maze, cur_vertex[1])

        # Get the weight of the adjacent coordinates going from the previous vertex to this one
        weights = get_weight_values(maze, cur_vertex[1], prev_locs[cur_vertex[1]][-1])

        # Go through all adjacent coordinates of the current coordinate
        for vertex in adjacent_vertexes:
            # Make alternate distance for this vertex using the distance to its prev and its weight
            alt_dist: int = distances[cur_vertex[1]] + weights[vertex]

            if vertex not in distances or alt_dist < distances[vertex]:
                distances.update({vertex: alt_dist})
                if vertex not in prev_locs:
                    prev_locs.update({vertex: []})
                prev_locs[vertex].append(cur_vertex[1])

                # Update the priority queue with the new distance to this vertex
                heapq.heappush(pq, (alt_dist, vertex))

    return distances[end_coords]


maze: list[str] = [line.strip() for line in open("input.txt")]

print(dijkstra(maze, get_start_coords(maze), get_end_coords(maze)))
