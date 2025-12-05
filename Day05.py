from copy import copy

def get_input(path):
    a = list()
    l = list()
    with open(path, 'r') as f:
        line = f.readline().strip()
        while len(line) > 0:
            s = line.split("-")
            a.append((int(s[0]), int(s[1])+1))
            line = f.readline().strip()
        for line in f.readlines():
            l.append(int(line.strip()))
    return a, l


def is_ingredient_fresh(fresh_ranges, id):
    for fresh_range in fresh_ranges:
        if fresh_range[0] <= id <= fresh_range[1]:
            return True
    return False


def merge_fresh_ingredient_ranges(fresh_ranges):
    new_fresh_ranges = copy(fresh_ranges)

    # Find if any two ranges can be merged together, return True if so and False if not and also return the merged list
    for i in range(len(fresh_ranges)):
        for j in range(len(fresh_ranges)):
            if i != j:
                # First see if the range i is completely enclosed in j and merge them if so
                if (fresh_ranges[j][0] <= fresh_ranges[i][0] <= fresh_ranges[j][1]) and (fresh_ranges[j][0] <= fresh_ranges[i][1] <= fresh_ranges[j][1]):
                    del(new_fresh_ranges[i])
                    return True, new_fresh_ranges
                # Next, see if the lower i is within j, use j's lower if so
                elif fresh_ranges[j][0] <= fresh_ranges[i][0] <= fresh_ranges[j][1]:
                    new_fresh_ranges[i] = (fresh_ranges[j][0], fresh_ranges[i][1])
                    del(new_fresh_ranges[j])
                    return True, new_fresh_ranges
                # Next, see if the upper i is within j, use j's upper if so
                elif fresh_ranges[j][0] <= fresh_ranges[i][1] <= fresh_ranges[j][1]:
                    new_fresh_ranges[i] = (fresh_ranges[i][0], fresh_ranges[j][1])
                    del (new_fresh_ranges[j])
                    return True, new_fresh_ranges
    return False, new_fresh_ranges

if __name__ == "__main__":

    # PART 1
    fresh_ingredient_ranges, ingredient_ids = get_input("Day05_Input.txt")
    count_fresh_ingreeints = 0
    for i in ingredient_ids:
        is_fresh = is_ingredient_fresh(fresh_ingredient_ranges, i)
        if is_fresh:
            count_fresh_ingreeints += 1
    print(f"Fresh Ingrendients Count: {count_fresh_ingreeints}")

    # PART 2
    fresh_ingredient_ranges, ingredient_ids = get_input("Day05_Input.txt")
    keep_merging = True
    num_fresh_ingredient_ids = 0
    while keep_merging:
        keep_merging, fresh_ingredient_ranges = merge_fresh_ingredient_ranges(fresh_ingredient_ranges)
    for range in fresh_ingredient_ranges:
        num_fresh_ingredient_ids += range[1] - range[0]
    print(f"# of Fresh Ingredient IDs: {num_fresh_ingredient_ids}")
