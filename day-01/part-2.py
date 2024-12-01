input_file = [line.strip().split() for line in open("input.txt", "r")]

first_list = []
second_list = []

for line in input_file:
    first_list.append(int(line[0]))
    second_list.append(int(line[1]))

score = 0

for num in first_list:
    score += num * second_list.count(num)

print(score)