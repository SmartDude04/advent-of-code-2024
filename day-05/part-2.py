from functools import update_wrapper

# Using a hash table can increase speed, although for this example an array would work well too
ordering_rules: dict[int, list[int]] = {}
update_numbers = []

with open("input.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if "|" in line:
            if int(line[0:line.find("|")]) not in ordering_rules.keys():
                ordering_rules[int(line[0:line.find("|")])] = []
            ordering_rules[int(line[0:line.find("|")])].append(int(line[line.find("|") + 1:]))
        elif "," in line:
            update_numbers.append([int(num) for num in line.split(",")])
        else:
            # Something went wrong. Print the line then exit
            print(line)
            exit(1)


def valid_update(cur_update: list[int]) -> bool:
    good_update = True
    for i, first in enumerate(cur_update):
        for j, second in enumerate(cur_update[i + 1:]):
            # print(cur_update[i], cur_update[j])
            if first not in ordering_rules.keys() or second not in ordering_rules[first]:
                good_update = False
                break

        if not good_update:
            break

    return good_update


total = 0
for update in update_numbers:

    # Go through each update from the second number onward. If that number belongs before any
    # that come before it, do a swap
    if not valid_update(update):
        # print(update)
        good = True
        for i, first in enumerate(update[1:]):
            for j, second in enumerate(update[0:i + 1]):
                if first in ordering_rules.keys() and second in ordering_rules[first]:
                    temp = update[i + 1]
                    update[i + 1] = update[j]
                    update[j] = temp

        total += update[int(len(update) / 2)]

print(total)
