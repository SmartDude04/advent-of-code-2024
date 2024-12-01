input_file = [line.strip().split() for line in open("input.txt", "r")]

first_list = []
second_list = []

for line in input_file:
    first_list.append(int(line[0]))
    second_list.append(int(line[1]))

first_list.sort()
second_list.sort()

total = 0

for i in range(len(first_list)):
    total += abs(first_list[i] - second_list[i])

print(total)