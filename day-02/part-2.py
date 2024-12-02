input_file = [line.strip().split() for line in open("input.txt", "r")]

def safe_level(report: list[str]) -> bool:
    increasing = int(report[0]) < int(report[1])
    for i in range(1, len(report)):
        if abs(int(report[i]) - int(report[i - 1])) > 3 or int(report[i]) == int(report[i - 1]):
            return False
        if increasing and int(report[i]) < int(report[i - 1]):
            return False
        if not increasing and int(report[i]) > int(report[i - 1]):
            return False
    return True

total = 0
for line in input_file:
    safe = safe_level(line)
    if safe:
        total += 1
    else:
        # If this level was found to not be safe, then try removing individual elements and
        # plug the new list into the function

        # Not nearly the fastest way, but it works...
        for index in range(len(line)):
            new_line = line.copy()
            new_line.pop(index)
            if safe_level(new_line):
                total += 1
                break



print(total)