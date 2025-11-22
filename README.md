# 🧭 Intro_algo_mini_project — A* Pathfinding Visualizer

This mini project demonstrates the **A\*** pathfinding algorithm using **Pygame**.
It allows users to interactively set start and end points, draw obstacles, and visualize how the A* algorithm finds the optimal path compared to naive methods.

---

## 🚀 Features

- Interactive **grid-based visualization** built with Pygame
- Supports **obstacle placement** and **random map generation**
- Uses **Octile distance** heuristic for realistic diagonal path cost
- Displays **open set**, **closed set**, and **final path** in real time
- Simple UI with on-screen **Reset** button and keyboard shortcuts

---

## 🧠 Algorithm Comparison: A* vs. Zigzag

To demonstrate the efficiency of intelligent search algorithms, this project includes a comparison between **A\*** (a heuristic-based search) and a **Strided Zigzag** (a naive coverage pattern).

### 📊 Experimental Results

The graph below visualizes the performance difference when attempting to reach 5 specific targets:

![Comparison Result](./comparison_result.png)
*(Make sure to add your image file to the repo and update this path)*

| Metric | A* (Straight-line) | Zigzag (Strided) | Analysis |
| :--- | :--- | :--- | :--- |
| **Total Distance** | **~59.33 m** | ~222.00 m | A* moves directly between points. Zigzag traverses the whole grid. |
| **Total Time** | **~46.49 s** | ~169.05 s | A* is **~3.6x faster** in this scenario. |
| **Behavior** | Calculates optimal path ($f = g + h$) | Fixed pattern blind coverage | A* is for **Navigation**; Zigzag is for **Coverage** (e.g., mowing). |

### 🧪 Try the Experiment
We have prepared a Google Colab notebook where you can run this simulation yourself and tweak parameters (like stride length or target locations).

👉 **[Open the Comparative Demo in Google Colab](https://colab.research.google.com/drive/1P6n2VuGFAJ6ldIFR-nYf70Rjf5kdfnLW?usp=sharing)**

---

## 🧰 Requirements

Ensure you have **Python 3.8+** installed.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/Intro_algo_mini_project.git](https://github.com/your-username/Intro_algo_mini_project.git)
   cd Intro_algo_mini_project
