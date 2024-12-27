import tkinter as tk
from tkinter import messagebox
from random_maze_solver import MazeGenerator, Maze
import threading

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Generator and Solver")

        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()

        self.label = tk.Label(root, text="Enter Maze Size:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.generate_button = tk.Button(root, text="Generate Maze", command=self.generate_maze)
        self.generate_button.pack()

        self.solve_button = tk.Button(root, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack()

        self.maze = None
        self.solution_steps = []

    def generate_maze(self):
        try:
            size = int(self.entry.get())
            if size <= 0:
                raise ValueError()
            
            # Ensure size is odd
            if size % 2 == 0:
                size += 1  # Adjust to the next odd number
                self.show_error(f"Maze size adjusted to {size} (must be odd).")
            
        except ValueError:
            self.show_error("Please enter a valid positive integer.")
            return

        # Generate the maze in a thread
        def generate():
            maze_generator = MazeGenerator(size, size)
            self.maze, self.start_point, self.end_point = maze_generator.maze, maze_generator.start, maze_generator.end
            self.root.after(0, self.draw_maze)  # Update the GUI after generation

        threading.Thread(target=generate).start()



    def solve_maze(self):
        if self.maze is None:
            self.show_error("Please generate a maze first.")
            return

        # Create the Maze object and solve it
        maze_obj = Maze(self.maze, self.start_point, self.end_point)
        try:
            maze_obj.solve()
        except Exception as e:
            self.show_error(str(e))
            return

        self.solution_steps = maze_obj.solution[1]
        self.explored_paths = maze_obj.explored
        self.draw_solution(maze_obj)

    def draw_maze(self):
        self.canvas.delete("all")
        cell_size = max(800 // len(self.maze), 5)  # Dynamically adjust cell size
        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = (j + 1) * cell_size, (i + 1) * cell_size
                fill_color = "black" if col == '#' else "blue" if (i, j) == self.start_point else "orange" if (i, j) == self.end_point else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")


    def draw_solution(self, maze_obj):
        self.canvas.delete("all")
        cell_size = max(800 // len(self.maze), 5)  # Dynamically adjust cell size

        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = (j + 1) * cell_size, (i + 1) * cell_size

                # Draw walls, start, goal, and solution
                if col == '#':
                    fill_color = "black"
                elif (i, j) == self.start_point:
                    fill_color = "blue"
                elif (i, j) == self.end_point:
                    fill_color = "orange"
                elif (i, j) in self.solution_steps:
                    fill_color = "green"
                elif (i, j) in maze_obj.explored:
                    fill_color = "yellow"  # Explored paths
                else:
                    fill_color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")



    def show_error(self, message):
        messagebox.showerror("Error", message)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    app.run()