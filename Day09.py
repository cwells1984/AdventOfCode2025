import math
import numpy as np

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

    return r_t, map_h_l, map_v_l, h, w


def calculate_area(a, b):
    return abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)

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
    def __init__(self, red_tiles, map_horiz_edges, map_vert_edges, height, width):
        self.red_tiles = red_tiles
        self.map_horiz_edges = map_horiz_edges
        self.map_vert_edges = map_vert_edges
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

    def is_edge_above(self, coords):
        for i in range(coords[1], -1, -1):
            if i in self.map_horiz_edges:
                for horiz_edge in self.map_horiz_edges[i]:
                    if horiz_edge.x_min <= coords[0] <= horiz_edge.x_max:
                        return True
        return False

    def is_edge_below(self, coords):
        for i in range(coords[1], self.height):
            if i in self.map_horiz_edges:
                for horiz_edge in self.map_horiz_edges[i]:
                    if horiz_edge.x_min <= coords[0] <= horiz_edge.x_max:
                        return True
        return False

    def is_edge_left(self, coords):
        for i in range(coords[0], -1, -1):
            if i in self.map_vert_edges:
                for vert_edge in self.map_vert_edges[i]:
                    if vert_edge.y_min <= coords[1] <= vert_edge.y_max:
                        return True
        return False

    def is_edge_right(self, coords):
        for i in range(coords[0], self.width):
            if i in self.map_vert_edges:
                for vert_edge in self.map_vert_edges[i]:
                    if vert_edge.y_min <= coords[1] <= vert_edge.y_max:
                        return True
        return False

    def is_within_polygon(self, coords):
        # First, is the coord a red tile?
        if coords in self.red_tiles:
            return True

        # Next, see if it is directly on a vertical  line:
        for v_edge in self.map_vert_edges[coords[0]]:
            if v_edge.y_min <= coords[1] <= v_edge.y_max:
                return True

        # Next, see if it is directly on a horizontal line:
        for h_edge in self.map_horiz_edges[coords[1]]:
            if h_edge.x_min <= coords[0] <= h_edge.x_max:
                return True

        # Finally, count the vertical and horizontal edges crossed. If both are odd, we are within the polygon
        vert_edges = 0
        if coords[1] in self.map_horiz_edges:
            for horiz_edge in self.map_horiz_edges[coords[1]]:
                if horiz_edge.x_max < coords[0]:
                    vert_edges += 1
                    break
        for i in range(coords[0]+1):
            if i in self.map_vert_edges:
                for vert_edge in self.map_vert_edges[i]:
                    if vert_edge.y_min < coords[1] < vert_edge.y_max:
                        vert_edges += 1
                        break

        horiz_edges = 0
        if coords[0] in self.map_vert_edges:
            for vert_edge in self.map_vert_edges[coords[0]]:
                if vert_edge.y_max < coords[1]:
                    horiz_edges += 1
                    break
        for i in range(coords[1]+1):
            if i in self.map_horiz_edges:
                for horiz_edge in self.map_horiz_edges[i]:
                    if horiz_edge.x_min < coords[0] < horiz_edge.x_max:
                        horiz_edges += 1
                        break

        return (vert_edges % 2 == 1) and (horiz_edges % 2 == 1)

    def find_max_rectangle_part2(self):
        max_area = -1
        max_r1 = (-1, -1)
        max_r2 = (-1, -1)

        for i in range(len(self.red_tiles)):
            for j in range(i+1, len(self.red_tiles)):

                if (self.red_tiles[i] == (7,1)) and (self.red_tiles[j] == (11,7)):
                    pass

                upper_left = None
                lower_left = None
                upper_right = None
                lower_right = None

                # Plot two of the corners
                if self.red_tiles[i][0] < self.red_tiles[j][0]:
                    if self.red_tiles[i][1] < self.red_tiles[j][1]:
                        upper_left = self.red_tiles[i]
                        lower_right = self.red_tiles[j]
                    else:
                        lower_left = self.red_tiles[i]
                        upper_right = self.red_tiles[j]
                else:
                    if self.red_tiles[i][1] < self.red_tiles[j][1]:
                        upper_right = self.red_tiles[i]
                        lower_left = self.red_tiles[j]
                    else:
                        lower_right = self.red_tiles[i]
                        upper_left = self.red_tiles[j]

                # Now plot the remaining corners
                if upper_left is None:
                    upper_left = tuple([lower_left[0], upper_right[1]])
                if lower_left is None:
                    lower_left = tuple([upper_left[0], lower_right[1]])
                if upper_right is None:
                    upper_right = tuple([lower_right[0], upper_left[1]])
                if lower_right is None:
                    lower_right = tuple([upper_right[0], lower_left[1]])

                # Now check the validity
                lower_left_valid = False
                upper_right_valid = False
                lower_right_valid = False
                upper_left_valid = self.is_within_polygon(upper_left)
                if upper_left_valid:
                    lower_left_valid = self.is_within_polygon(lower_left)
                    if lower_left_valid:
                        upper_right_valid = self.is_within_polygon(upper_right)
                        if upper_right_valid:
                            lower_right_valid = self.is_within_polygon(lower_right)

                if upper_left_valid and lower_left_valid and upper_right_valid and lower_right_valid:
                    area = calculate_area_part2(upper_left, lower_right)
                    if area > max_area:
                        max_area = area
                        max_r1 = self.red_tiles[i]
                        max_r2 = self.red_tiles[j]
                        print(max_area)

        return max_area, max_r1, max_r2

    def __str__(self):
        s = ""
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) in self.red_tiles:
                    s += "#"
                elif (j, i) in self.green_tiles:
                    s += "X"
                else:
                    s += "."
            s += "\n"
        return s


if __name__ == "__main__":

    # PART 1
    # red_squares, green_squares, h, w = get_input("Day09_InputTest.txt")
    # tile_floor = TileFloor(red_squares, green_squares, h, w)
    # area, r1, r2 = tile_floor.find_max_rectangle()
    # print(f"Max Area: {area}")
    # print(f"{r1}x{r2}")

    # PART 2
    red_squares, map_horiz_edges, map_vert_edges, h, w = get_input("Day09_Input.txt")
    tile_floor = TileFloor(red_squares, map_horiz_edges, map_vert_edges, h, w)
    area, r1, r2 = tile_floor.find_max_rectangle_part2()
    print(f"Max Area: {area}")
    print(f"{r1}x{r2}")