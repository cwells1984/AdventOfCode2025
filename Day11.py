from copy import copy
import math
import re

def get_input(path):
    l = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            line_split = line.strip().split(":")
            name = line_split[0]
            outputs_str = line_split[1].strip()
            l[name] = GraphNode(name, outputs_str)
    l["you"].distance_from_start = 0
    return l


def connect_nodes(dict_nodes:dict):
    start = dict_nodes["you"]
    goal = GraphNode("out", "")
    for i, node in dict_nodes.items():
        if i == "you":
            pass
        neighbors_str_list = node.outputs_str.split(" ")
        for s in neighbors_str_list:
            if s == "you":
                start.inputs.append(node)
                node.outputs.append(start)
            elif s == "out":
                goal.inputs.append(node)
                node.outputs.append(goal)
            else:
                node.outputs.append(dict_nodes[s])
                dict_nodes[s].inputs.append(node)
    dict_nodes["out"] = goal
    return start, goal


class GraphNode:
    def __init__(self, name:str, outputs_str:str):
        self.name = name
        self.outputs_str = outputs_str
        self.outputs = []
        self.inputs = []
        self.distance_from_start = math.inf


def calculate_distances(dict_nodes:dict):
    visited_nodes = set()

    while len(visited_nodes) < len(dict_nodes):

        # First, find the closest node to the start
        closest_to_start = None
        closest_distance = math.inf
        for i, node in dict_nodes.items():
            if node.name not in visited_nodes and node.distance_from_start < closest_distance:
                closest_to_start = node
                closest_distance = node.distance_from_start

        if not closest_to_start:
            return

        # Now update the distances of all neighbors
        for neighbor in closest_to_start.outputs:
            if neighbor.name not in visited_nodes:
                new_closest_distance = closest_distance + 1
                if new_closest_distance < neighbor.distance_from_start:
                    neighbor.distance_from_start = new_closest_distance

        visited_nodes.add(closest_to_start.name)


def find_paths_to_goal(goal:GraphNode, dict_nodes:dict):
    paths = []
    node_stack = [(goal, [])]

    while len(node_stack) > 0:
        node_path = node_stack.pop()
        node = node_path[0]
        path = node_path[1]

        updated_path = copy(path)
        updated_path.append(node.name)

        if node.name == "you":
            paths.append(updated_path)
        else:
            for neighbor in node.inputs:
                if neighbor.distance_from_start <= node.distance_from_start:
                    node_stack.append((neighbor, updated_path))
    return paths


if __name__ == "__main__":

    # PART 1
    # graph = get_input("Day11_Input.txt")
    # start_node, goal_node = connect_nodes(graph)
    # calculate_distances(graph)
    # paths = find_paths_to_goal(goal_node, graph)
    # print(f"Unique paths to goal {len(paths)}")

    # PART 2
    graph = get_input("Day11_Input.txt")
    start_node, goal_node = connect_nodes(graph)