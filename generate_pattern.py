import sys

COUNTER = 0

ALL_PATTERNS = []

def findPattern(pattern, pos, size):
    global COUNTER
    global ALL_PATTERNS
    if 0 not in pattern:
        COUNTER += 1
        print(pattern, COUNTER)
        ALL_PATTERNS.append(pattern)
    for i in range(pos, len(pattern)):
        if pattern[i] == 0:
            for char in [1, 2, 3, 4, 5, 6]:
                pattern[i] = char
                findPattern(pattern, i, size)
                pattern[i] = 0
            return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)

    pattern = list(map(int, sys.argv[1]))
    findPattern(pattern, 0, len(pattern))

    print(ALL_PATTERNS)
