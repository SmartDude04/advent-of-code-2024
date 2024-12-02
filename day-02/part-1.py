input_file = [line.strip().split() for line in open("input.txt", "r")]

total = 0

for line in input_file:
    good_line = True
    increasing = int(line[0]) < int(line[1])
    for i in range(1, len(line)):
        if abs(int(line[i]) - int(line[i - 1])) > 3 or int(line[i]) == int(line[i - 1]):
            good_line = False
            break
        if increasing and int(line[i]) < int(line[i - 1]):
            good_line = False
            break
        if not increasing and int(line[i]) > int(line[i - 1]):
            good_line = False
            break
    if good_line:
        total += 1


print(total)