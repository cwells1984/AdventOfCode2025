import math
import re


def get_input(path):
    l = []
    with open(path, 'r') as f:
        input_ranges = f.readline().split(",")
    for input_range in input_ranges:
        input_range_split = input_range.split("-")
        l += list(range(int(input_range_split[0]),
                        int(input_range_split[1])+1))
    return l


def is_repeated_sequence(id):
    s = str(id)
    l = len(s)
    lower_half = s[:math.ceil(l/2)]
    upper_half = s[math.ceil(l/2):]
    if lower_half == upper_half:
        return True
    else:
        return False

def is_repeated_sequence_part2(id):
    s = str(id)
    l = len(s)

    for i in range(1, (l//2)+1):
        search_for = s[0:i]
        test = f"^{search_for}{{2,}}$"
        if re.search(f"^({search_for}){{2,}}$", s):
            return True
    return False


if __name__ == "__main__":

    # PART 1
    list_idranges = get_input("Day02_Input.txt")
    sum_invalid_ids = 0
    for idrange in list_idranges:
        if is_repeated_sequence(idrange):
            sum_invalid_ids += idrange
    print(f"Sum of invalid ids: {sum_invalid_ids}")

    # PART 2
    list_idranges = get_input("Day02_Input.txt")
    sum_invalid_ids = 0
    for idrange in list_idranges:
        if is_repeated_sequence_part2(idrange):
            sum_invalid_ids += idrange
    print(f"Sum of invalid ids: {sum_invalid_ids}")
    # print(is_repeated_sequence_part2(1188511885))
