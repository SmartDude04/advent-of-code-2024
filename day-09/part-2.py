input_line = open("input.txt", "r").readline().strip()
filesystem = [int(num) for num in input_line]
expanded: list[int] = []


def expand_filesystem() -> None:
    global filesystem
    global expanded

    for i, num in enumerate(filesystem):
        for _ in range(num):
            if i % 2 == 0:
                expanded.append(i // 2)  # I completely forgot about operator//
            else:
                expanded.append(-1)


# def refactor_filesystem() -> None:
#     global expanded
#
#     empty_space = expanded.index(-1)
#     file_space = len(expanded) - 1
#     while expanded[file_space] == -1:
#         file_space -= 1
#
#     while empty_space < file_space:
#         empty_space = expanded.index(-1)
#         empty_size = 1
#         while expanded[empty_space + empty_size] == -1:
#             empty_size += 1
#         file_size = 1
#         while expanded[file_space - file_size] == expanded[file_space]:
#             file_size += 1
#
#         while empty_size < file_size:
#             empty_space += empty_size
#             while expanded[empty_space] != -1:
#                 empty_space += 1
#             empty_size = 1
#             while empty_space + empty_size < len(expanded) and expanded[empty_space + empty_size] == -1:
#                 empty_size += 1
#
#         # If the space is big enough to move, then do so
#         if empty_size >= file_size:
#             for elem in range(file_size):
#                 expanded[empty_space + elem] = expanded[file_space - file_size + 1 + elem]
#                 # Set the now-empty space to show that
#                 expanded[file_space - file_size + 1 + elem] = -1
#         else:
#             # Move file_space to the previous id
#             cur_elem_id = expanded[file_space]
#             while expanded[file_space] == cur_elem_id:
#                 file_space -= 1
#
#         # Move both the empty space and file space variables to their next respective locations
#         while empty_space < len(expanded) and expanded[empty_space] != -1:
#             empty_space += 1
#         while file_size >= 0 and expanded[file_space] == -1:
#             file_space -= 1

def move_file(empty_start: int, file_start: int) -> None:
    global expanded

    assert expanded[empty_start] == -1
    assert expanded[file_start] != -1

    cur_index = 0
    file_num = expanded[file_start]
    while file_start + cur_index < len(expanded) and expanded[file_start + cur_index] == file_num:
        expanded[empty_start + cur_index] = expanded[file_start + cur_index]
        expanded[file_start + cur_index] = -1
        cur_index += 1


def refactor_filesystem() -> None:
    global expanded

    cur_file = len(expanded) - 1
    while expanded[cur_file] == -1:
        cur_file -= 1

    while True:
        cur_open = expanded.index(-1)
        if cur_open == ValueError:
            return

        file_len = 1
        while expanded[cur_file - file_len] == expanded[cur_file]:
            file_len += 1

        # Search for an open space big enough to store this file
        while cur_open < cur_file:
            open_len = 1
            while expanded[cur_open + open_len] == -1:
                open_len += 1

            # Space is big enough, move the file
            if open_len >= file_len:
                move_file(cur_open, cur_file - file_len + 1)
                break
            else:
                # If not, move up a space and see if that will work
                cur_open += open_len
                while expanded[cur_open] != -1:
                    cur_open += 1

        # We were either able or unable to move the file. Either way, move down to the next file and loop
        cur_file -= file_len
        while cur_file >= 0 and expanded[cur_file] == -1:
            cur_file -= 1

        # We are out of options for files, so return
        if cur_file < 0 or expanded[cur_file] == -1:
            return


def calc_checksum() -> int:
    total = 0
    for file_id, num in enumerate(expanded):
        if num != -1:
            total += (file_id * num)
    return total


expand_filesystem()
refactor_filesystem()
print(calc_checksum())
