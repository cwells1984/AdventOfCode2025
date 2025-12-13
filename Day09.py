from copy import copy
from shapely import Polygon

def get_input(path):

    # First get the coordinates
    l_x = []
    l_y = []
    with open(path, 'r') as f:
        for line in f.readlines():
            s = line.strip().split(",")
            l_x.append(int(s[0]))
            l_y.append(int(s[1]))

    # Now build the grid
    h = max(l_y)+2
    w = max(l_x)+2
    r_t = []
    map_h_l = {}
    map_v_l = {}
    for i in range(-1, len(l_x)-1):
        this_red_tile = tuple([l_x[i], l_y[i]])
        r_t.append(tuple([this_red_tile[0], this_red_tile[1]]))
        next_red_tile = tuple([l_x[i+1], l_y[i+1]])

        # if the next red tile has the same X coord, add a vertical edge to the amp
        if this_red_tile[0] == next_red_tile[0]:
            v_l = VerticalLine(x=this_red_tile[0])
            v_l_y = sorted([this_red_tile[1], next_red_tile[1]])
            v_l.y_min = v_l_y[0]
            v_l.y_max = v_l_y[1]
            if v_l.x in map_v_l:
                map_v_l[v_l.x].append(v_l)
            else:
                map_v_l[v_l.x] = [v_l]

        # if the next red tile has the same Y coord, add a horizontal edge to the amp
        if this_red_tile[1] == next_red_tile[1]:
            h_l = HorizontalLine(y=this_red_tile[1])
            h_l_x = sorted([this_red_tile[0], next_red_tile[0]])
            h_l.x_min = h_l_x[0]
            h_l.x_max = h_l_x[1]
            if h_l.y in map_h_l:
                map_h_l[h_l.y].append(h_l)
            else:
                map_h_l[h_l.y] = [h_l]

    return r_t, h, w, map_v_l, map_h_l


def calculate_area(a, b):
    test1 = abs(a[0] - b[0]) + 1
    test2 = abs(a[1] - b[1]) + 1
    return test1 * test2

def calculate_area_of_entry(e):
    return calculate_area(e[0], e[1])

# a = upper-left, b = lower-right
def calculate_area_part2(a, b):
    return (b[0]-a[0]+1) * (b[1] - a[1]+1)

class VerticalLine:
    def __init__(self, x, y_min=None, y_max=None):
        self.x = x
        self.y_min = y_min
        self.y_max = y_max

class HorizontalLine:
    def __init__(self, y, x_min=None, x_max=None):
        self.y = y
        self.x_min = x_min
        self.x_max = x_max

class TileFloor:
    def __init__(self, red_tiles, height, width):
        self.red_tiles = red_tiles
        self.height = height
        self.width = width

    def find_max_rectangle(self):
        max_area = -1
        max_r1 = (-1, -1)
        max_r2 = (-1, -1)

        for i in range(len(self.red_tiles)):
            for j in range(i+1, len(self.red_tiles)):
                area = calculate_area(self.red_tiles[i], self.red_tiles[j])
                if area > max_area:
                    max_area = area
                    max_r1 = self.red_tiles[i]
                    max_r2 = self.red_tiles[j]

        return max_area, max_r1, max_r2

    def find_all_rectangles(self):
        l = []

        for i in range(len(self.red_tiles)):
            for j in range(i+1, len(self.red_tiles)):
                tile1 = self.red_tiles[i]
                tile2 = self.red_tiles[j]
                l.append([tile1, tile2])


        l.sort(key=calculate_area_of_entry, reverse=True)
        return l

    def __str__(self):
        s = ""
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) in self.red_tiles:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        return s


def polygon_from_red_squares(red_squares):
    polygon_coords = copy(red_squares)
    polygon_coords.append(polygon_coords[0])
    return Polygon(polygon_coords)


def is_rectangle_in_polygon(p, r):
    low_x = min([r[0][0], r[1][0]])
    high_x = max([r[0][0], r[1][0]])
    low_y = min([r[0][1], r[1][1]])
    high_y = max([r[0][1], r[1][1]])
    rect_polygon = Polygon([[low_x, low_y], [high_x, low_y], [high_x, high_y], [low_x, high_y]])
    if rect_polygon.within(p):
        return True
    else:
        return False

if __name__ == "__main__":

    # PART 1
    red_squares, h, w, map_v_l, map_h_l = get_input("Day09_Input.txt")
    tile_floor = TileFloor(red_squares, h, w)
    area, r1, r2 = tile_floor.find_max_rectangle()
    print(f"Max Area: {area}")
    print(f"{r1}x{r2}")

    # PART 2
    polygon = polygon_from_red_squares(red_squares)
    all_rectangles = tile_floor.find_all_rectangles()
    max_rectangle = None
    for rectangle in all_rectangles:
        if is_rectangle_in_polygon(polygon, rectangle):
            max_rectangle = rectangle
            break
    print(f"Max Rectangle within Polygon: {max_rectangle}")
    print(f"Max Area: {calculate_area_of_entry(max_rectangle)}")