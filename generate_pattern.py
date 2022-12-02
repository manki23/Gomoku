import sys

def findPattern(pattern, pos, size):
    if '.' not in pattern:
        print(f"'{''.join(pattern)}'", end=', ')
    for i in range(pos, len(pattern)):
        if pattern[i] == '.':
            for char in ['_', 'O', 'X']:
                pattern[i] = char
                findPattern(pattern, i, size)
                pattern[i] = '.'
            return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)

    pattern = list(sys.argv[1])
    findPattern(pattern, 0, len(pattern))

