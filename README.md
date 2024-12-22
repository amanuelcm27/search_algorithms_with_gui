# Graph Search Visualizer Project

## Overview
This project is a GUI-based visualization tool for graph traversal algorithms. It allows users to explore the behavior of different search algorithms such as BFS, DFS, DLS, IDDFS, UCS, and BDS on a customizable graph structure. The tool uses NetworkX for graph representation and Matplotlib for visualization.

## Features
1. Visualizes graph traversal for various algorithms.
2. Interactive GUI built with Tkinter for selecting algorithms, start/goal nodes, and additional parameters.
3. Supports bidirectional graph representation.
4. Provides clear and dynamic visual feedback on the traversal path.

## Installation
1. Install Python (>=3.7).
2. Install required libraries:
   ```bash
   pip install matplotlib networkx
   ```

3. Run the script:
   ```bash
   python graph_visualizer.py
   ```

## Graph Representation
The graph is represented as a Python dictionary where keys are nodes and values are lists of neighboring nodes:

```python
{
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': ['F', 'H'],
    'F': [],
    'G': ['H'],
    'H': []
}
```

A helper function `make_bidirectional` ensures that edges are bidirectional.

## Algorithms
The following algorithms are implemented:

### Breadth-First Search (BFS)
- Explores all nodes at the current depth before moving deeper.
- Uses a queue for traversal.

### Depth-First Search (DFS)
- Explores as far as possible along a branch before backtracking.
- Uses a stack for traversal.

### Depth-Limited Search (DLS)
- A variant of DFS with a specified depth limit.

### Iterative Deepening Depth-First Search (IDDFS)
- Combines the benefits of BFS and DFS by incrementally increasing the depth limit.

### Uniform Cost Search (UCS)
- Explores nodes in order of cost (all edges are assumed to have equal weight).
- Uses a priority queue.

### Bidirectional Search (BDS)
- Simultaneously searches from the start and goal nodes until the two meet.

## Visualization
The `draw_graph` function:
1. Creates a directed graph using NetworkX.
2. Highlights the traversed path in red.
3. Uses a consistent layout across visualizations for better comparison.

```python
layout = nx.spring_layout(G)  # Default layout
```

## GUI Functionality
The GUI allows users to:
- Select a traversal algorithm.
- Specify start and goal nodes.
- Provide additional parameters for DLS and IDDFS (e.g., depth limit).

### Example Usage
1. Select "DFS" from the dropdown menu.
2. Enter "A" as the start node and "F" as the goal node.
3. Press "Submit" to visualize the DFS path.

## Code Highlights
### Bidirectional Graph Conversion
```python
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
```

### Running the Selected Algorithm
```python
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
```

### Graph Visualization
```python
def draw_graph(graph, path, title, layout=None):
    plt.ion()  # Turn on interactive mode
    plt.clf()  # Clear the current figure

    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = layout or nx.spring_layout(G)  # Default layout

    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", arrows=True)

    if path:
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)

    plt.title(title)
    plt.draw()
    plt.pause(0.001)  # Pause to update the plot
    return pos
```

## Future Improvements
1. Allow dynamic graph creation and modification through the GUI.
2. Support weighted edges for algorithms like UCS.
3. Enhance visualization with step-by-step traversal animations.

## Running the Project
To start the GUI application, run:
```bash
python graph_visualizer.py