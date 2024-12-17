import re
import heapq


def execute_loop(a: int) -> int:
    # This is all that happens in each loop. Because b and c get overwritten each iteration, we don't even need them
    return ((a % 8) ^ 3 ^ (a // pow(2, (a % 8) ^ 5))) % 8


registers: list[int] = [0, 0, 0]
program: list[int] = []
with open("input.txt") as f:
    while line := f.readline():
        line = line.strip()
        if line.find("Register") != -1:
            if line.find("A") != -1:
                registers[0] = int(re.findall(r"[0-9]+", line)[0])
            elif line.find("B") != -1:
                registers[1] = int(re.findall(r"[0-9]+", line)[0])
            elif line.find("C") != -1:
                registers[2] = int(re.findall(r"[0-9]+", line)[0])
        elif len(line) > 0:
            program = [int(num) for num in re.findall(r"[0-9]+", line)]


def find_reg_for_output(output: list[int]) -> int:
    pq: list[tuple[int, int]] = []

    # Work backwards. If the program output is the same as the given, add it to the priority queue
    for i in range(8):
        if execute_loop(i) == output[-1]:
            # Append a pair of the index this output was and the input value to the program
            heapq.heappush(pq, (len(output) - 1, i))

    # Implement the dfs algorithm. It is greedy in the fact that it will first search the most promising result
    while pq:
        index, input = heapq.heappop(pq)
        # Base case: if the input index was 0, then return that input value
        if index == 0:
            return input

        new_required_output = output[index - 1]
        for i in range(8):
            # Now when executing the loop, you must multiply the exising value by 8 (<< 3) then add the extra number
            new_input = (input << 3) + i
            if execute_loop(new_input) == new_required_output:
                heapq.heappush(pq, (index - 1, new_input))

    # If we in fact get to the end and there is no element left, this means it is not possible to get this
    # output. Return -1
    return -1


#   Notes:
# - Program is a loop that runs floor(logbase8(start regA)) + 1 times meaning each time regA is divided by 8
# - Output is last 3 bits of register b

print(find_reg_for_output(program))

