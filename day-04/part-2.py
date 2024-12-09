grid = [line.strip() for line in open("input.txt")]
letters = "MAS"


def check_xmas(cur_row: int, cur_col: int) -> bool:
    def wordsearch_helper(row: int, col: int, letters_remaining: int, horiz: int, vert: int) -> bool:
        # Base case
        if letters_remaining == 1:
            # Error checking, could be commented out for speed if needed
            assert grid[row][col] == letters[-1]
            return True

        # Make sure we are on a good slot, could be commented out for speed if needed
        assert grid[row][col] == letters[len(letters) - letters_remaining]

        # Check that we can keep going to look for the next letter
        if row + vert < 0 or row + vert >= len(grid) or col + horiz < 0 or col + horiz >= len(grid[0]):
            return False

        # Recurse if possible
        if grid[row + vert][col + horiz] == letters[len(letters) + 1 - letters_remaining]:
            return wordsearch_helper(row + vert, col + horiz, letters_remaining - 1, horiz, vert)

        # If recursion is not possible, return false
        return False

    # Error checking
    assert grid[cur_row][cur_col] == "A"

    # Confirm we are in bounds for the entire search
    if cur_row + 1 >= len(grid) or cur_col + 1 >= len(grid[0]) or cur_row - 1 < 0 or cur_col - 1 < 0:
        return False

    found = 0
    if grid[cur_row + 1][cur_col + 1] == "M":
        if wordsearch_helper(cur_row + 1, cur_col + 1, len(letters), -1, -1):
            found += 1
    if grid[cur_row - 1][cur_col + 1] == "M":
        if wordsearch_helper(cur_row - 1, cur_col + 1, len(letters), -1, 1):
            found += 1
    if grid[cur_row - 1][cur_col - 1] == "M":
        if wordsearch_helper(cur_row - 1, cur_col - 1, len(letters), 1, 1):
            found += 1
    if grid[cur_row + 1][cur_col - 1] == "M":
        if wordsearch_helper(cur_row + 1, cur_col - 1, len(letters), 1, -1):
            found += 1

    if found == 2:
        return True
    return False


total = 0

for i, line in enumerate(grid):
    for j, char in enumerate(line):
        if char == "A":
            if check_xmas(i, j):
                total += 1

print(total)
