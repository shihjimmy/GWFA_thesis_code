import tkinter as tk

def create_resizable_matrix_gui(rows, cols):
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
            # Draw a rectangle for each cell, starting at the given row, col position
            canvas.create_rectangle(
                col * 20, row * 20, (col + 1) * 20, (row + 1) * 20,  # Rectangle coordinates
                outline="black", width=1  # Cell borders
            )

    # Run the window
    window.mainloop()

# Example: 50x50 matrix
rows = 20
cols = 20
create_resizable_matrix_gui(rows, cols)

