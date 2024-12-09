import re

input_file = [line for line in open("input.txt")]

total = 0

do_mult = True

for line in input_file:
    good_input = re.findall(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", line)

    for cur_input in good_input:
        if cur_input == "do()":
            do_mult = True
        elif cur_input == "don't()":
            do_mult = False
        elif do_mult:
            nums = re.findall(r"[0-9]+", cur_input)
            total += int(nums[0]) * int(nums[1])

print(total)
