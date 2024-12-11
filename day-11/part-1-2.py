import math
import functools

stones = [int(stone) for stone in open("input.txt").read().split()]


@functools.cache
def blink(num: int, blinks_left: int) -> int:
    # Base case
    if blinks_left == 0:
        return 1

    # Rule 1: If the number is 0, set it to 1
    if num == 0:
        return blink(1, blinks_left - 1)

    # Rule 2: If the number of digits in the number is even, split it
    num_digits = int(math.log10(num)) + 1
    if num_digits % 2 == 0:
        second_num = num % pow(10, num_digits // 2)
        first_num = num // pow(10, num_digits // 2)
        return blink(first_num, blinks_left - 1) + blink(second_num, blinks_left - 1)

    # Rule 3: If the number of digits is odd, multiply by 2024
    return blink(num * 2024, blinks_left - 1)


total = 0
for stone in stones:
    total += blink(stone, 75)

print(f"\nTotal: {total}")
print(blink.cache_info())
