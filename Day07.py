def get_input(path):
    l = []
    with open(path, 'r') as f:
        for line in f.readlines():
            grid_line = []
            for c in line.strip():
                grid_line.append(c)
            l.append(grid_line)
    return l

class TachyonGrid:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.beams = [self.find_starting_pos()]
        self.weighted_beams = {self.find_starting_pos():1}
        self.beam_history = []
        self.split_count = 0
        self.possible_timelines = 0

    def find_starting_pos(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == 'S':
                    return (i, j)
        return (-1, -1)

    def travel(self):
        new_beams = []
        for beam in self.beams:

            if beam[0] < self.height - 1:

                # if the beam can, move it downward
                if self.grid[beam[0]+1][beam[1]] != '^':
                    self.beam_history.append(beam)
                    if (beam[0]+1, beam[1]) not in new_beams:
                        new_beams.append((beam[0]+1, beam[1]))

                # if the beam hits a splitter, split it
                else:
                    self.split_count += 1
                    self.beam_history.append(beam)
                    split_left = (beam[0]+1, beam[1]-1)
                    split_right = (beam[0]+1, beam[1]+1)

                    # there can only be one beam per space
                    if split_left not in new_beams:
                        new_beams.append(split_left)
                    if split_right not in new_beams:
                        new_beams.append(split_right)
            else:
                self.beam_history.append(beam)
        self.beams = new_beams

    def travel_part2(self):
        new_weighted_beams = {}
        for beam in self.weighted_beams.keys():
            weight = self.weighted_beams[beam]

            if beam[0] < self.height - 1:

                # if the beam can, move it downward
                if self.grid[beam[0]+1][beam[1]] != '^':
                    if (beam[0]+1, beam[1]) not in new_weighted_beams:
                        new_weighted_beams[(beam[0]+1, beam[1])] = weight
                    else:
                        new_weighted_beams[(beam[0] + 1, beam[1])] += weight

                # if the beam hits a splitter, split it
                else:
                    split_left = (beam[0]+1, beam[1]-1)
                    split_right = (beam[0]+1, beam[1]+1)

                    if split_left not in new_weighted_beams:
                        new_weighted_beams[split_left] = weight
                    else:
                        new_weighted_beams[split_left] += weight

                    if split_right not in new_weighted_beams:
                        new_weighted_beams[split_right] = weight
                    else:
                        new_weighted_beams[split_right] += weight
            else:
                self.possible_timelines += weight
        self.weighted_beams = new_weighted_beams

    def __str__(self):
        s = f"Grid: ({self.height}x{self.width})\n"
        s += f"# of Splits: {self.split_count}\n"
        for i in range(self.height):
            l = ""
            for j in range(self.width):
                if (i, j) in self.beams or (i, j) in self.beam_history:
                    l += "|"
                else:
                    l += self.grid[i][j]
            s += f"{l}\n"
        return s


if __name__ == "__main__":

    # PART 1
    tachyon_grid = TachyonGrid(get_input("Day07_Input.txt"))
    while len(tachyon_grid.beams) > 0:
        tachyon_grid.travel()
    print(f"Split count: {tachyon_grid.split_count}")

    # PART 2
    tachyon_grid = TachyonGrid(get_input("Day07_Input.txt"))
    while len(tachyon_grid.weighted_beams) > 0:
        tachyon_grid.travel_part2()
    print(f"Possible timelines: {tachyon_grid.possible_timelines}")
