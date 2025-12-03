import copy


def get_input(path):
    l = []
    with open(path, 'r') as f:
        for line in f.readlines():
            s = list(line.strip())
            for i in range(len(s)):
                s[i] = int(s[i])
            l.append(s)
    return l

def find_max_combo(a):
    max_combo = -1
    max_loc = (-1, -1)
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            x = int(str(f"{a[i]}{a[j]}"))
            if x > max_combo:
                max_combo = x
                max_loc = (i, j)
    return max_combo, max_loc

def find_max_combo_part2(a):
    # Remove any number whose next number is larger, starting from the left and stopping if the length of the array
    # gets to 12
    mod_a = copy.copy(a)
    digit_removed = True
    while digit_removed and len(mod_a) > 12:
        digit_removed = False
        for i in range(len(mod_a)-1):
            if mod_a[i] < mod_a[i+1]:
                del mod_a[i]
                digit_removed = True
                break

    # If the array is still larger than 12, just trim the remaining numbers off
    if len(mod_a) > 12:
        mod_a = mod_a[0:12]

    return int("".join(str(s) for s in mod_a))


if __name__ == "__main__":

    # PART 1
    sum_joltage = 0
    list_banks = get_input("Day03_Input.txt")
    for bank in list_banks:
        sum_joltage += find_max_combo(bank)[0]
    print(f"Sum Joltage: {sum_joltage}")

    # PART 2
    sum_joltage = 0
    list_banks = get_input("Day03_Input.txt")
    counter = 0
    for bank in list_banks:
        sum_joltage += find_max_combo_part2(bank)
    print(f"Sum Joltage: {sum_joltage}")
