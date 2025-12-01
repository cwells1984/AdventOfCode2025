import re


def get_input(path):
    list_a = []
    with open(path, 'r') as f:
        for line in f.readlines():
            t = re.findall(r"([R,L])(\d+)", line.strip())
            list_a.append(t[0])
        return list_a

class Dial:
    def __init__(self, lower, upper, pointer=0):
        self.lower = lower
        self.upper = upper
        self.pointer = pointer
        self.dial = list(range(self.lower, self.upper + 1))
        self.zero_count = 0

    def turn_left(self, rotations):
        self.pointer -= rotations % len(self.dial)
        self.pointer = self.dial[self.pointer]
        if self.pointer == 0:
            self.zero_count += 1

    def turn_right(self, rotations):
        self.pointer += rotations % len(self.dial)
        self.pointer = self.pointer % len(self.dial)
        if self.pointer == 0:
            self.zero_count += 1

    def turn_left_part2(self, rotations):
        complete_rotations = rotations // len(self.dial)
        self.zero_count += complete_rotations
        remaining_rotations = rotations % len(self.dial)

        started_at_zero = self.pointer == 0
        self.pointer -= remaining_rotations
        if self.pointer <= 0:
            self.pointer = self.dial[self.pointer]
            if not started_at_zero:
                self.zero_count += 1

    def turn_right_part2(self, rotations):
        complete_rotations = rotations // len(self.dial)
        self.zero_count += complete_rotations
        remaining_rotations = rotations % len(self.dial)

        started_at_zero = self.pointer == 0
        self.pointer += remaining_rotations
        if self.pointer > self.upper:
            self.pointer = self.pointer % len(self.dial)
            if not started_at_zero:
                self.zero_count += 1

    def __str__(self):
        s = f"Pointer is at {self.pointer}\n"
        s += f"Zero Count = {self.zero_count}\n"
        return s

if __name__ == "__main__":

    # PART 1
    list_rotations = get_input("Day01_input.txt")
    dial = Dial(lower=0, upper=99, pointer=50)

    for rotation_tuple in list_rotations:
        if rotation_tuple[0] == "L":
            dial.turn_left(int(rotation_tuple[1]))
        else:
            dial.turn_right(int(rotation_tuple[1]))
    print(f"Password: {dial.zero_count}")

    # PART 2
    list_rotations = get_input("Day01_input.txt")
    dial = Dial(lower=0, upper=99, pointer=50)

    for rotation_tuple in list_rotations:
        if rotation_tuple[0] == "L":
            dial.turn_left_part2(int(rotation_tuple[1]))
        else:
            dial.turn_right_part2(int(rotation_tuple[1]))
    print(f"Password: {dial.zero_count}")