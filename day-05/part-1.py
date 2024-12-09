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


total = 0
for update in update_numbers:

    good = True
    for i, first in enumerate(update):
        for j, second in enumerate(update[i + 1:]):
            print(update[i], update[j])
            if first not in ordering_rules.keys() or second not in ordering_rules[first]:
                good = False
                break

        if not good:
            break

    if good:
        # print(update)
        total += update[int(len(update) / 2)]

print(total)

