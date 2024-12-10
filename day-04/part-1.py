grid = [line.strip() for line in open("input.txt")]
letters = "XMAS"


def wordsearch(cur_row: int, cur_col: int) -> int:
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

    wordsearch_total = 0
    if wordsearch_helper(cur_row, cur_col, len(letters), 0, -1):
        wordsearch_total += 1
    if wordsearch_helper(cur_row, cur_col, len(letters), 1, -1):
        wordsearch_total += 1
    if wordsearch_helper(cur_row, cur_col, len(letters), 1, 0):
        wordsearch_total += 1
    if wordsearch_helper(cur_row, cur_col, len(letters), 1, 1):
        wordsearch_total += 1
    if wordsearch_helper(cur_row, cur_col, len(letters), 0, 1):
        wordsearch_total += 1
    if wordsearch_helper(cur_row, cur_col, len(letters), -1, 1):
        wordsearch_total += 1
    if wordsearch_helper(cur_row, cur_col, len(letters), -1, 0):
        wordsearch_total += 1
    if wordsearch_helper(cur_row, cur_col, len(letters), -1, -1):
        wordsearch_total += 1

    return wordsearch_total


total = 0

for i, line in enumerate(grid):
    for j, char in enumerate(line):
        if char == letters[0]:
            total += wordsearch(i, j)

print(total)