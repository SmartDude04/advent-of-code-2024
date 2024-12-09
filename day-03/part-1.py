import re

input_file = [line for line in open("input.txt")]

total = 0

do_mult = True

for line in input_file:
    good_input = re.findall(r"mul\([0-9]+,[0-9]+\)", line)

    for cur_input in good_input:
        nums = re.findall(r"[0-9]+", cur_input)
        total += int(nums[0]) * int(nums[1])

print(total)
