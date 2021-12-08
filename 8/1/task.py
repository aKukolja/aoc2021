
digit_to_segments = {
    0: {c for c in "abcefg"},
    1: {c for c in "cf"},
    2: {c for c in "acdeg"},
    3: {c for c in "acdfg"},
    4: {c for c in "bcdf"},
    5: {c for c in "abdfg"},
    6: {c for c in "abdefg"},
    7: {c for c in "acf"},
    8: {c for c in "abcdefg"},
    9: {c for c in "abcdfg"},
}

len_to_digit = {
    2: {1},
    3: {7},
    4: {4},
    5: {2, 3, 5},
    6: {0, 6, 9},
    7: {8},
}


if __name__ == "__main__":
    collection = []
    with open("data.txt", "r") as f:
        for line in f:
            left, right = line.strip().split("|")
            left = left.strip()
            right = right.strip()
            uniques = {x.strip() for x in left.split()}
            displayed = [x.strip() for x in right.split()]
            collection.append((uniques, displayed))

    sum = 0
    for _, displayed in collection:
        for val in displayed:
            possible = len_to_digit[len(val)]
            if len(possible) == 1:
                sum = sum + 1
    print(sum)

