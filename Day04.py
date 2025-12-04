def get_input(path):
    l = []
    with open(path, 'r') as f:
        for line in f.readlines():
            grid_line = []
            for c in line.strip():
                grid_line.append(c)
            l.append(grid_line)
    return l

class ForkliftGrid:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.accessibility_grid = self.create_accessibility_grid()
        self.num_accessible = self.find_num_accessible()

    def remove_all_possible_rolls(self):
        removed_rolls_total = 0
        removed_roll_count = 1
        while removed_roll_count > 0:
            removed_roll_count = self.remove_accessible_rolls()
            removed_rolls_total += removed_roll_count
        print(f"{removed_rolls_total} rolls removed total")

    def remove_accessible_rolls(self):
        removed_roll_count = 0
        print(f"{self.num_accessible} rolls removed")
        for i in range(self.height):
            for j in range(self.width):
                if self.accessibility_grid[i][j]:
                    self.grid[i][j] = "."
                    removed_roll_count += 1
        self.accessibility_grid = self.create_accessibility_grid()
        self.num_accessible = self.find_num_accessible()
        return removed_roll_count

    def find_num_accessible(self):
        num_accessible = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.accessibility_grid[i][j]:
                    num_accessible += 1
        return num_accessible

    def create_accessibility_grid(self):
        accessibility_grid = []
        for i in range(self.height):
            accessability_grid_line = []
            for j in range(self.width):
                if self.is_accessible(i, j) and self.grid[i][j] == "@":
                    accessability_grid_line.append(True)
                else:
                    accessability_grid_line.append(False)
            accessibility_grid.append(accessability_grid_line)
        return accessibility_grid

    def is_accessible(self, i, j):
        num_adjacent_rolls = 0

        # check the 3 spots above
        if i > 0:
            if j > 0:
                if self.grid[i-1][j-1] == '@': num_adjacent_rolls += 1
            if self.grid[i-1][j] == '@': num_adjacent_rolls += 1
            if j < self.width-1:
                if self.grid[i-1][j+1] == '@': num_adjacent_rolls += 1

        # check the 2 spots beside
        if j > 0:
            if self.grid[i][j-1] == '@': num_adjacent_rolls += 1
        if j < self.width-1:
            if self.grid[i][j+1] == '@': num_adjacent_rolls += 1

        # check the 3 spots below
        if i < self.width - 1:
            if j > 0:
                if self.grid[i+1][j-1] == '@': num_adjacent_rolls += 1
            if self.grid[i+1][j] == '@': num_adjacent_rolls += 1
            if j < self.width-1:
                if self.grid[i+1][j + 1] == '@': num_adjacent_rolls += 1

        if num_adjacent_rolls < 4:
            return True
        else:
            return False

    def __str__(self):
        num_accessible = 0
        s = f"Grid: ({self.height}x{self.width})\n"
        s += f"Num accessible: {self.num_accessible}\n"
        for i in range(self.height):
            l = ""
            for j in range(self.width):
                if self.grid[i][j] == "@" and self.accessibility_grid[i][j]:
                    num_accessible += 1
                    l += "x"
                else:
                    l += self.grid[i][j]
            s += f"{l}\n"
        return s

if __name__ == "__main__":

    # PART 1
    forklift_grid = ForkliftGrid(get_input("Day04_Input.txt"))
    print(forklift_grid)

    # PART 2
    forklift_grid = ForkliftGrid(get_input("Day04_Input.txt"))
    forklift_grid.remove_all_possible_rolls()
