import functools

@functools.cache
def valid_towel(cur_towel: str, towels: tuple[str, ...]) -> int:
    if len(cur_towel) == 0:
        return 1

    total = 0
    for towel in towels:
        if cur_towel.find(towel) == 0:
            total += valid_towel(cur_towel[len(towel):], towels)

    return total

towels: tuple[str, ...] = ()
designs: list[str]  = []

with open("input.txt") as f:
    while line := f.readline():
        if line.find(",") != -1:
            towels = tuple(line.strip().split(", "))
        elif len(line.strip()) > 0:
            designs.append(line.strip())


num_combinations = 0
num_towels = 0
for towel in designs:
    ret_val = valid_towel(towel, towels)
    num_combinations += ret_val
    if ret_val > 0:
        num_towels += 1


print(f"Part 1: {num_towels}")
print(f"Part 2: {num_combinations}")
