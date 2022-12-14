import solution14a

import tkinter as tk

# initialize the window
def init_window():
    window = tk.Tk()
    window.title("Display 14")
    window.geometry("600x400")
    return window

# draw the picture from the data in map solution14a.cave_map
def draw_grid(window, cave_map):
    window = init_window()
    # find the min and max x and y coordinates
    min_x = min(cave_map.keys(), key=lambda x: x[0])[0]
    max_x = max(cave_map.keys(), key=lambda x: x[0])[0]
    min_y = min(cave_map.keys(), key=lambda x: x[1])[1]
    max_y = max(cave_map.keys(), key=lambda x: x[1])[1]
    # draw the grid
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # create a label
            label = tk.Label(window, text=cave_map.get((x, y), '.'))
            # place the label
            label.grid(column=x, row=y)
    window.mainloop()




# Create a new tkinter window
window = tk.Tk()

# Set the window title
window.title("Map")

# Create a new tkinter frame to hold the map
frame = tk.Frame(window)
frame.pack()

# Create a new tkinter canvas to draw the map on
canvas = tk.Canvas(frame, width=600, height=600)
canvas.pack()

# Define the size of each cell in the map
cell_size = 50

# Create a 2D array to hold the map data
map_data = [
    [4, 5, 5],
    [9, 0, 0],
    [4, 0, 3]
]

# Loop through the map data and draw each cell
for row in range(len(map_data)):
    for col in range(len(map_data[row])):
        value = map_data[row][col]
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        if value == 0:
            color = "white"
        elif value == 1:
            color = "black"
        elif value == 2:
            color = "red"
        elif value == 3:
            color = "green"
        elif value == 4:
            color = "blue"
        elif value == 5:
            color = "yellow"
        elif value == 6:
            color = "orange"
        elif value == 7:
            color = "purple"
        elif value == 8:
            color = "brown"
        elif value == 9:
            color = "gray"
        canvas.create_rectangle(x1, y1, x2, y2, fill=color) # , outline="black")
# Start the tkinter main loop
window.mainloop()

# update the mapq
