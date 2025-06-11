import tkinter as tk
from GWFA_test import GWFA_test
from tqdm import tqdm

def flatten_path(path):
    coordinates = []
    x, y = 0, 0  # Starting position
    coordinates.append((x, y))

    for move in path:
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


def create_resizable_matrix_gui(rows, cols, gold_ans, gold_pos, path, final_ending_pos, breakpoints, gwfa_path):
    # Create the main window
    window = tk.Tk()
    window.title(f"Matrix: {rows}x{cols}")

    # Set the window size to be proportional to the matrix size
    window.geometry("410x410")  # You can adjust the default window size as needed

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


    print("Start generating GUI result.")
    print("-----------------------------")


    for row in tqdm(range(rows), desc="Processing"):
        for col in range(cols):
            
            score = gold_ans[row][col] 
            cell_color = "white"  
            
            
            if (row, col) in path: 
                cell_color = "red"  
            
            if (row, col) == final_ending_pos:
                cell_color = "yellow"
            
            if (row, col) in breakpoints:  
                cell_color = "green"  
            
            if (row, col) in gwfa_path: 
                cell_color = "blue" 
            
            if (row, col) == gold_pos:  
                cell_color = "gray"  
             
            
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
    check_golden_GWFA = False

    
    gold_ans, gold_pos, path, final_ending_pos, breakpoints, gwfa_score, gwfa_traceback, (gwfa_end_x, gwfa_end_y) = GWFA_test(check_golden_GWFA)

    rows = gold_ans.shape[0]
    cols = gold_ans.shape[1]

    # Flatten the path to convert directions into coordinates
    pos_path = flatten_path(path)
    gwfa_path = flatten_path(gwfa_traceback)

    # Call the function with the flattened path, gold_ans, breakpoints, and both final and gold positions
    create_resizable_matrix_gui(rows, cols, gold_ans, gold_pos, pos_path, final_ending_pos, breakpoints, gwfa_path)
