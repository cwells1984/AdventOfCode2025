import math
from copy import copy
import re


def get_input(path):
    l = []
    with open(path, 'r') as f:
        for line in f.readlines():
            l.append(Machine(line.strip()))
    return l

class GraphNode:
    def __init__(self, state:str, distance_from_start:float):
        self.state = state
        self.distance_from_start = distance_from_start
        self.neighbors = []

class Machine:
    def __init__(self, schematic):

        # Set up the indicator lights
        self.correct_indicator_lights = "".join(schematic[schematic.find("[")+1:schematic.find("]")])
        self.current_indicator_lights = "".join(["." for i in range(len(self.correct_indicator_lights))])

        # Set up the buttons
        self.buttons = []
        open_paren_i = [match.start() for match in re.finditer("\\(", schematic)]
        close_paren_i = [match.start() for match in re.finditer("\\)", schematic)]
        for i in range(len(open_paren_i)):
            button_lights = []
            for light_index in schematic[open_paren_i[i]+1:close_paren_i[i]].split(","):
                button_lights.append(int(light_index))
            self.buttons.append(button_lights)

        # Set up others
        self.graph = None
        self.start_node = None
        self.goal_node = None

    # Creates nodes for each possible state
    def build_graph(self):
        self.graph = {}
        s = None
        g = None
        for i in range(2 ** len(self.current_indicator_lights)):
            bin_digits = str(format(i, 'b'))
            diff_len = len(self.current_indicator_lights) - len(bin_digits)
            leading_str = "0" * diff_len
            bin_digits = leading_str + bin_digits

            bin_digits = bin_digits.replace("1", "#")
            bin_digits = bin_digits.replace("0", ".")
            if self.current_indicator_lights == bin_digits:
                distance = 0
            else:
                distance = math.inf
            self.graph[bin_digits] = GraphNode(bin_digits, distance)

            if bin_digits == self.current_indicator_lights:
                self.start_node = self.graph[bin_digits]
            if bin_digits == self.correct_indicator_lights:
                self.goal_node = self.graph[bin_digits]

    # Defines the neighbors of each node
    def connect_graph(self):
        for i, node in self.graph.items():
            node.neighbors = []
            for move in self.buttons:
                new_state = toggle(node.state, move)
                node.neighbors.append(self.graph[new_state])

    def calculate_distances(self):
        visited_nodes = set()

        while len(visited_nodes) < len(self.graph):
            # First, find the closest node to the start
            closest_to_start = None
            closest_distance = math.inf
            for i, node in self.graph.items():
                if node.state not in visited_nodes and node.distance_from_start < closest_distance:
                    closest_to_start = node
                    closest_distance = node.distance_from_start

            # If we have found the path to the target, then we're done
            if closest_to_start.state == self.goal_node.state:
                return

            # If the closest node is the goal, then terminate
            for neighbor in closest_to_start.neighbors:
                if neighbor.state not in visited_nodes:
                    new_closest_distance = closest_distance + 1
                    if new_closest_distance < neighbor.distance_from_start:
                        neighbor.distance_from_start = new_closest_distance
            visited_nodes.add(closest_to_start.state)

    def __str__(self):
        s = ""
        s += self.current_indicator_lights
        s += "\n"
        return s

def toggle(state:str, move:list):
    new_state = list(copy(state))
    for m in move:
        if new_state[m] == "#":
            new_state[m] = "."
        elif new_state[m] == ".":
            new_state[m] = "#"
    return "".join(new_state)


if __name__ == "__main__":

    # PART 1
    list_machines = get_input("Day10_Input.txt")
    sum_button_presses = 0
    for machine in list_machines:
        machine.build_graph()
        machine.connect_graph()
        machine.calculate_distances()
        sum_button_presses += machine.goal_node.distance_from_start
    print(f"Sum of button presses: {sum_button_presses}")
