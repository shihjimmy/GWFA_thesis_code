import tkinter as tk
import numpy as np
from GWFA_test import GWFA_test


def flatten_path(path):
    """
    Flatten the path and return the coordinates for each move.
    The path is a list of (move, direction) tuples like [(2, 'M'), (3, 'I'), ...]
    We convert it to a sequence of coordinates (x, y).
    """
    coordinates = []
    x, y = 0, 0  # Starting position
    coordinates.append((x, y))

    for seg in path:
        for move in seg:
            num = int(move[0])
            direction = move[1]  # 'M', 'I', 'D', 'U'

            if direction == 'M':  # Match
                x += 1
                y += num

            elif direction == 'I':  # Insert
                x += 1

            elif direction == 'D':  # Delete
                y += num

            elif direction == 'U':  # Mismatch
                x += 1
                y += num

            coordinates.append((x, y))
    
    return coordinates


def create_resizable_matrix_gui(rows, cols, gold_ans, gold_pos, path, final_ending_pos, breakpoints):
    # Create the main window
    window = tk.Tk()
    window.title(f"Matrix: {rows}x{cols}")

    # Set the window size to be proportional to the matrix size
    window.geometry("410x500")  # You can adjust the default window size as needed

    # Create a canvas for drawing the grid
    canvas = tk.Canvas(window, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Configure the canvas scroll region (this will allow the user to scroll if needed)
    canvas.config(scrollregion=(0, 0, cols * 20, rows * 20))  # Adjust the 20 to control cell size

    # Create a scrollable canvas (this will allow scrolling if the grid is large)
    x_scrollbar = tk.Scrollbar(window, orient="horizontal", command=canvas.xview)
    x_scrollbar.pack(side="bottom", fill="x")
    canvas.configure(xscrollcommand=x_scrollbar.set)

    y_scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    y_scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=y_scrollbar.set)

    # Draw the grid on the canvas
    for row in range(rows):
        for col in range(cols):
            score = gold_ans[row][col]  # Get the score from the gold_ans matrix
            cell_color = "white"  # Default color for cells
            
            if (row, col) in path:  # If this cell is part of the path
                cell_color = "red"  # Color the cell red
            
            if (row, col) in breakpoints:  # If this cell is part of breakpoints
                cell_color = "yellow"  # Color the cell yellow for breakpoints
            elif score == float('inf'):  # If the score is infinite (unreachable)
                cell_color = "gray"  # Color it gray to indicate unreachable
            
            
            if (row, col) == gold_pos:  
                cell_color = "blue"
            elif (row, col) == final_ending_pos:
                cell_color = "blue"    
             
            

            # Create the rectangle for each cell with color
            canvas.create_rectangle(
                col * 20, row * 20, (col + 1) * 20, (row + 1) * 20,  # Rectangle coordinates
                outline="black", width=1, fill=cell_color  # Cell border and background color
            )

            # Display the score in the cell
            canvas.create_text(
                col * 20 + 10, row * 20 + 10, text=str(score), font=("Arial", 8), fill="black"
            )


    # Run the window
    window.mainloop()


if __name__ == "__main__":
    # should be same as the setting in GWFA_test.py
    Block_Size = 5
    
    gold_ans, gold_pos, path, final_ending_pos, breakpoints = GWFA_test()

    rows = gold_ans.shape[0]
    cols = gold_ans.shape[1]

    # Flatten the path to convert directions into coordinates
    pos_path = flatten_path(path)


    # Call the function with the flattened path, gold_ans, breakpoints, and both final and gold positions
    create_resizable_matrix_gui(rows, cols, gold_ans, gold_pos, pos_path, final_ending_pos, breakpoints)
