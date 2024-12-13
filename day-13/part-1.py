import numpy as np
import re


def solve_equation(cur_equation: np.array, cur_prize: np.array) -> np.array:
    return np.linalg.solve(cur_equation, cur_prize)


systems = []
with open("input.txt") as f:
    file_input = f.readlines()

    for i in range(0, len(file_input), 4):
        button_a = [int(num) for num in re.findall(r"[0-9]+", file_input[i])]
        button_b = [int(num) for num in re.findall(r"[0-9]+", file_input[i + 1])]
        prize = np.array([int(num) for num in re.findall(r"[0-9]+", file_input[i + 2])])
        equations = np.array([[button_a[0], button_b[0]], [button_a[1], button_b[1]]])

        systems.append((equations, prize))

total = 0
for system in systems:
    result = solve_equation(system[0], system[1])
    epsilon = 0.01
    if abs(result[0] - round(result[0], 0)) <= epsilon and abs(result[1] - round(result[1], 0)) <= epsilon:
        if int(result[0] + 0.1) <= 100 and int(result[1] + 0.1) <= 100:
            total += int(result[0] + 0.1) * 3 + int(result[1] + 0.1)

print(total)
