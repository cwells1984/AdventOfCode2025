import math

def get_input(path):
    l = []
    with open(path, 'r') as f:
        for line in f.readlines():
            a = [int(s) for s in line.strip().split(",")]
            l.append(a)
    return l

def calculate_distance(b1, b2):
    d = math.sqrt(sum([math.pow(b2[0] - b1[0], 2),
                  math.pow(b2[1] - b1[1], 2),
                  math.pow(b2[2] - b1[2], 2)]))
    return d

def retrieve_sorted_distances(a):
    s_d = {}
    for i in range(len(a)):
        for j in range(len(a)):
            if i != j:
                s_d[tuple(sorted((i, j)))] = calculate_distance(a[i], a[j])
    s_d = list(s_d.items())
    s_d = sorted(s_d, key=lambda x: x[1])
    return s_d

def create_initial_circuits(a):
    l = []
    for i in range(len(a)):
        l.append({i})
    return l

def merge_sets(c, d):
    shortest_pair = d[0]
    box1 = shortest_pair[0][0]
    box2 = shortest_pair[0][1]
    del d[0]
    set1, set1_index = return_set_with_box(c, box1)
    set2, set2_index = return_set_with_box(c, box2)
    if set1_index != set2_index:
        c.append(set1.union(set2))
        if set1_index > set2_index:
            del c[set1_index]
            del c[set2_index]
        else:
            del c[set2_index]
            del c[set1_index]
    if len(c) == 1:
        l = [box1, box2]
    else:
        l = None
    return c, d, l

def return_set_with_box(c, b):
    for i in range(len(c)):
        if b in c[i]:
            return c[i], i

if __name__ == "__main__":

    # PART 1
    junction_boxes = get_input("Day08_Input.txt")
    sorted_distances = retrieve_sorted_distances(junction_boxes)
    circuit_sets = create_initial_circuits(junction_boxes)

    for i in range(1000):
        circuit_sets, sorted_distances, last_boxes_added = merge_sets(circuit_sets, sorted_distances)

    product_of_sets = 1
    for i in sorted(circuit_sets, key=len, reverse=True)[0:3]:
        product_of_sets *= len(i)
    print(f"Product of 3 Largest Circuit Sizes: {product_of_sets}")

    # PART 2
    junction_boxes = get_input("Day08_Input.txt")
    sorted_distances = retrieve_sorted_distances(junction_boxes)
    circuit_sets = create_initial_circuits(junction_boxes)
    box_add_history = []

    while len(circuit_sets) > 1:
        circuit_sets, sorted_distances, last_boxes_added = merge_sets(circuit_sets, sorted_distances)
        if last_boxes_added is not None:
            x1 = junction_boxes[last_boxes_added[0]][0]
            x2 = junction_boxes[last_boxes_added[1]][0]
            print(f"Product of last 2 boxes added: {x1 * x2}")
