test_values = []
numbers = []

with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        test_values.append(int(line[0:line.find(":")]))
        numbers.append([int(num) for num in line[line.find(":") + 2:].split(" ")])


def good_test_value(test_value: int, numbers: list[int]) -> bool:
    # Recursive function to generate permutations for the test value
    def test_value_helper(test_value: int, numbers: list[int], cur_value: int, add: bool, multiply: bool, concatenate: bool) -> bool:
        # Make sure we are adding or multiplying and not doing both
        assert add ^ multiply ^ concatenate

        # Base case
        if len(numbers) == 0:
            return cur_value == test_value

        if add:
            return test_value_helper(test_value, numbers[1:], cur_value + numbers[0], True, False, False) or \
                test_value_helper(test_value, numbers[1:], cur_value + numbers[0], False, True, False) or \
                test_value_helper(test_value, numbers[1:], cur_value + numbers[0], False, False, True)
        elif multiply:
            return test_value_helper(test_value, numbers[1:], cur_value * numbers[0], True, False, False) or \
                test_value_helper(test_value, numbers[1:], cur_value * numbers[0], False, True, False) or \
                test_value_helper(test_value, numbers[1:], cur_value * numbers[0], False, False, True)
        elif concatenate:
            new_value = int(str(cur_value) + str(numbers[0]))
            return test_value_helper(test_value, numbers[1:], new_value, True, False, False) or \
                test_value_helper(test_value, numbers[1:], new_value, False, True, False) or \
                test_value_helper(test_value, numbers[1:], new_value, False, False, True)

    return test_value_helper(test_value, numbers, 0, True, False, False) or \
        test_value_helper(test_value, numbers, 1, False, True, False) or \
        test_value_helper(test_value, numbers, 0, False, False, True)


total = 0
for i, test_value in enumerate(test_values):
    if good_test_value(test_value, numbers[i]):
        total += test_value

print(total)