# Using priority queue in Dijkstra's algorithm
import heapq
import copy

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


def dijkstra(maze: list[str], start_coords: tuple[int, int], end_coords: tuple[int, int]) -> (
        tuple[dict[tuple[int, int], int], dict[tuple[int, int], list[tuple[int, int]]]]):
    """
    Uses Dijkstra's algorithm to find the shortest path between two points
    Returns: Tuple of (coord -> length of shortest path, coord -> list of previous coordinates)
    """

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

    return distances, prev_locs


def update_list(cur: list[...], merge: list[...], skip=None) -> None:
    copy_merge = copy.deepcopy(merge)
    if skip is None:
        skip = []
    while copy_merge:
        item = copy_merge.pop()
        if item not in cur and item not in skip:
            cur.append(item)


def print_paths(maze: list[str], path: list[tuple[int, int]]) -> None:
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if (row, col) in path:
                print("X", end="")
            else:
                print(char, end="")
        print("")


def calc_tiles_for_optimal_path(maze: list[str], start_coords: tuple[int, int], end_coords: tuple[int, int]) -> list[tuple[int, int]]:
    # This algorithm works by first generating the first min-valid path. It then iterates over the path and
    # as it does so blocks different maze parts to generate different min paths. When it comes across one that
    # has the same path length as the min, it will add its coordinates to the good_tiles list and to the block_coords
    # list to be removed to possibly generate new paths

    # First return value; this will serve as baseline for all operations
    ret = dijkstra(maze, start_coords, end_coords)

    # Coordinates that will eventually be blocked out in the while loop
    block_coords: list[tuple[int, int]] = ret[1][end_coords]
    # Add all coordinates from the end to the start to block_coords
    cur = block_coords[0]
    while cur != start_coords:
        block_coords.append(ret[1][cur][0])
        cur = block_coords[-1]

    # Tiles that produce paths that are valid/lowest in value
    good_tiles: list[tuple[int, int]] = block_coords

    # Erase the starting coordinate from block_coords
    block_coords = block_coords[:-1]

    # Shortest path with unblocked maze
    shortest_path: int = ret[0][end_coords]

    # Keep blocking coordinates and rechecking the path
    while block_coords:
        # Block the current coordinate
        cur_block = block_coords.pop()
        maze[cur_block[0]] = maze[cur_block[0]][:cur_block[1]] + "#" + maze[cur_block[0]][cur_block[1] + 1:]

        # Check the result of running dijkstra on this new map
        res = dijkstra(maze, start_coords, end_coords)
        if end_coords in res[0] and res[0][end_coords] == shortest_path:
            # # If this path is also the same distance as the shortest, then add its coordinates to block_coords
            # ret_coords = res[1][end_coords]
            # cur = ret_coords[0]
            # while cur != start_coords:
            #     ret_coords.append(res[1][cur][0])
            #     cur = ret_coords[-1]
            #
            # # Make sure to block good_tiles so the starting coords don't appear again
            # update_list(block_coords, ret_coords, good_tiles)
            #
            # # Update good_tiles

            print("Recursing...")
            update_list(good_tiles, calc_tiles_for_optimal_path(maze, start_coords, end_coords))

        # Change back the blocked coordinate
        maze[cur_block[0]] = maze[cur_block[0]][:cur_block[1]] + "." + maze[cur_block[0]][cur_block[1] + 1:]

    if end_coords not in good_tiles:
        good_tiles.append(end_coords)
    # print_paths(maze, good_tiles)

    return good_tiles



maze: list[str] = [line.strip() for line in open("input.txt")]

print(len(calc_tiles_for_optimal_path(maze, get_start_coords(maze), get_end_coords(maze))))
