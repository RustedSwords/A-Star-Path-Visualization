# 🗺️ A* Path Finding Visualization

A stunning, **interactive visualization** of the A* pathfinding algorithm with a cyberpunk aesthetic. Watch in real-time as the algorithm explores a grid, finds the optimal path, and lights it up in neon yellow.

## ✨ Demo

![A* Pathfinding Algorithm in Action](astar.gif)

## 🎮 Features

- **Interactive Grid**: Click and drag to draw walls and obstacles
- **Colorful UI**: Eye-catching neon colors (cyan, magenta, purple, orange)
- **Real-Time Visualization**: Watch the algorithm explore nodes in real-time
- **Optimal Pathfinding**: Uses A* heuristic to find the shortest path
- **Responsive Controls**: Simple mouse controls for easy interaction

## 🎨 Color Legend

| Color | Meaning |
|-------|---------|
| 🟣 Purple | Start node |
| 🟠 Orange | End node |
| 🟦 Cyan | Open nodes (being considered) |
| 🟥 Magenta | Closed nodes (already evaluated) |
| 🟨 Yellow | Final shortest path |
| ⬛ Dark | Barriers/walls |

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pygame

### Installation

```bash
pip install pygame
```

### Usage

```bash
python astar.py
```

**Controls:**
- **Left Click**: Set start point (first click), end point (second click), or draw walls (hold and drag)
- **Right Click**: Remove walls
- **SPACE**: Start the A* algorithm
- **C**: Clear the grid
- **Q**: Quit

## 🧠 How It Works

The A* algorithm combines the benefits of Dijkstra's algorithm and greedy best-first search:

1. Maintains a priority queue of nodes to explore
2. Calculates cost as: `f(n) = g(n) + h(n)`
   - `g(n)`: distance from start node
   - `h(n)`: heuristic estimate to end node (Manhattan distance)
3. Always explores the most promising node first
4. Guarantees the shortest path if one exists
