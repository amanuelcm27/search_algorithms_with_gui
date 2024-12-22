import matplotlib.pyplot as plt
import networkx as nx
from queue import PriorityQueue
import tkinter as tk
from tkinter import messagebox, simpledialog

def make_bidirectional(graph):
    bidirectional_graph = {}
    for node, neighbors in graph.items():
        if node not in bidirectional_graph:
            bidirectional_graph[node] = []
        for neighbor in neighbors:
            bidirectional_graph[node].append(neighbor)
            if neighbor not in bidirectional_graph:
                bidirectional_graph[neighbor] = []
            bidirectional_graph[neighbor].append(node)
    return bidirectional_graph

def draw_graph(graph, path, title, layout=None):
    plt.ion()
    plt.clf()
    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    pos = layout or nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", arrows=True)
    if path:
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)
    plt.title(title)
    plt.draw()
    plt.pause(0.001)
    return pos

def bfs(graph, start, goal):
    visited = set()
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

def dfs(graph, start, goal):
    visited = set()
    stack = [[start]]
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in reversed(graph.get(node, [])):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
    return None

def dls(graph, start, goal, limit):
    def recursive_dls(node, goal, limit, path, visited):
        if limit == 0:
            return None
        if node == goal:
            return path
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                result = recursive_dls(neighbor, goal, limit - 1, path + [neighbor], visited)
                if result:
                    return result
        return None
    return recursive_dls(start, goal, limit, [start], set())

def iddfs(graph, start, goal, max_depth):
    for depth in range(max_depth + 1):
        result = dls(graph, start, goal, depth)
        if result:
            return result
    return None

def ucs(graph, start, goal):
    visited = set()
    pq = PriorityQueue()
    pq.put((0, [start]))
    while not pq.empty():
        cost, path = pq.get()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                pq.put((cost + 1, new_path))
    return None

def bds(graph, start, goal):
    from_start = {start: [start]}
    from_goal = {goal: [goal]}
    visited_start, visited_goal = set(), set()
    while from_start and from_goal:
        current_start = list(from_start.keys())[0]
        path_start = from_start.pop(current_start)
        visited_start.add(current_start)
        if current_start in from_goal:
            return path_start + from_goal[current_start][::-1][1:]
        for neighbor in graph.get(current_start, []):
            if neighbor not in visited_start:
                from_start[neighbor] = path_start + [neighbor]
        current_goal = list(from_goal.keys())[0]
        path_goal = from_goal.pop(current_goal)
        visited_goal.add(current_goal)
        if current_goal in from_start:
            return from_start[current_goal] + path_goal[::-1][1:]
        for neighbor in graph.get(current_goal, []):
            if neighbor not in visited_goal:
                from_goal[neighbor] = path_goal + [neighbor]
    return None

def run_algorithm(graph, algorithm, start, goal, extra_input=None):
    if algorithm == "BFS":
        return bfs(graph, start, goal)
    elif algorithm == "DFS":
        return dfs(graph, start, goal)
    elif algorithm == "DLS":
        return dls(graph, start, goal, extra_input)
    elif algorithm == "IDDFS":
        return iddfs(graph, start, goal, extra_input)
    elif algorithm == "UCS":
        return ucs(graph, start, goal)
    elif algorithm == "BDS":
        return bds(graph, start, goal)
    else:
        return None

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': ['F', 'H'],
    'F': [],
    'G': ['H'],
    'H': []
}

graph = make_bidirectional(graph)
layout = None

def gui_app():
    def on_submit():
        global layout
        algorithm = algo_var.get()
        start = start_entry.get()
        goal = goal_entry.get()
        extra_input = None
        if algorithm in ["DLS", "IDDFS"]:
            extra_input = simpledialog.askinteger("Input", f"Enter the depth/limit for {algorithm}:")
        path = run_algorithm(graph, algorithm, start, goal, extra_input)
        if path:
            messagebox.showinfo("Path Found", f"Path: {path}")
            layout = draw_graph(graph, path, f"{algorithm} Traversal", layout)
        else:
            messagebox.showerror("No Path", "No path could be found!")
    root = tk.Tk()
    root.title("Graph Search Visualizer")
    tk.Label(root, text="Select Algorithm:").pack()
    algo_var = tk.StringVar(value="BFS")
    algo_menu = tk.OptionMenu(root, algo_var, "BFS", "DFS", "DLS", "IDDFS", "UCS", "BDS")
    algo_menu.pack()
    tk.Label(root, text="Start Node:").pack()
    start_entry = tk.Entry(root)
    start_entry.pack()
    tk.Label(root, text="Goal Node:").pack()
    goal_entry = tk.Entry(root)
    goal_entry.pack()
    tk.Button(root, text="Submit", command=on_submit).pack()
    root.mainloop()

if __name__ == "__main__":
    gui_app()
