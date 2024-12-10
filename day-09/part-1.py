input_line = open("input.txt", "r").readline().strip()
filesystem = [int(num) for num in input_line]
expanded = []


# Side note: I considered performing the refactor in the compressed version of the string for
# efficiency, but considering the expanded version of the string won't actually be crazy long
# (computers have lots of memory and each char is 1 byte) I decided to expand it first.
# Although, if this was going to be used for anything other than a month-long challenge, it
# would be best to work in the compacted form

def expand_filesystem() -> None:
    global filesystem
    global expanded

    for i, num in enumerate(filesystem):
        for _ in range(num):
            if i % 2 == 0:
                expanded.append(i // 2)  # I completely forgot about operator//
            else:
                expanded.append(-1)


def refactor_filesystem() -> None:
    global expanded

    empty_space = expanded.index(-1)
    file_space = len(expanded) - 1
    while expanded[file_space] == -1:
        file_space -= 1

    while empty_space < file_space:
        expanded[empty_space] = expanded[file_space]
        expanded[file_space] = -1

        empty_space += 1
        while expanded[empty_space] != -1:
            empty_space += 1
        file_space -= 1
        while expanded[file_space] == -1:
            file_space -= 1

    expanded = expanded[:empty_space]


def calc_checksum() -> int:
    total = 0
    for file_id, num in enumerate(expanded):
        total += (file_id * num)
    return total


expand_filesystem()
refactor_filesystem()
print(calc_checksum())
