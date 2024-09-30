import random
import math
import tkinter

root = tkinter.Tk()
root.title("Town MAP")
# Set the window to always be on top
root.attributes("-topmost", True)
canvas = tkinter.Canvas(width=400, height=500, bg="white")
canvas.pack()

DELAY = 0
tabu_list = []

def clear_canvas(iteration_count):
    canvas.delete("all")
    canvas.create_text(200, 40, text=("Iteration: " + str(iteration_count)), font=("Arial", 22), fill="black")
    for town in town_coordinates:
        canvas.create_oval(town[0] - 5, town[1] - 5, town[0] + 5, town[1] + 5, fill="red")

# creates visible connections between cities
def create_line(x1, y1, x2, y2, color):
    global DELAY
    canvas.create_line(x1, y1, x2, y2, fill=color)
    canvas.after(DELAY)
    canvas.update()

def show_global_optimum(global_optimum, global_opt_dist):
    canvas.delete("all")
    canvas.create_text(200, 40, text=f"Best Path Length: {global_opt_dist:.2f}", font=("Arial", 22), fill="black")
    for town in town_coordinates:
        canvas.create_oval(town[0] - 5, town[1] - 5, town[0] + 5, town[1] + 5, fill="red")
    for i in range(len(global_optimum) - 1):
        create_line(global_optimum[i][0], global_optimum[i][1], global_optimum[i + 1][0], global_optimum[i + 1][1], "black")
    create_line(global_optimum[len(global_optimum) - 1][0], global_optimum[len(global_optimum) - 1][1], global_optimum[0][0], global_optimum[0][1], "blue")

def create_connections(path, i):
    clear_canvas(i)
    n = len(path)
    for i in range(n - 1):
        create_line(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1], "black")
    create_line(path[n - 1][0], path[n - 1][1], path[0][0], path[0][1], "blue")

# calculating distance using pythagorean theorem
def city_distance(town1, town2):
    x1, y1 = town1[0], town1[1]
    x2, y2 = town2[0], town2[1]

    a = (x1-x2) ** 2
    b = (y1-y2) ** 2
    c = math.sqrt(a+b)
    return c

# creates town coordinates and symbolizes towns on canvas as red dots
def town_init(n):
    town_coordinates = []
    # the map is big 400 x 400
    for i in range(n):
        x = random.randrange(10, 390)
        y = random.randrange(110, 390)
        # creates towns as dots on canvas
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        town_coordinates.append([x, y])
    return town_coordinates

# this is the fitnes function
def calculate_dist(path):
    total_distance = 0
    n = len(path)
    for i in range(n - 1):
        total_distance += city_distance(path[i], path[i + 1])
    total_distance += city_distance(path[n - 1], path[0])
    return total_distance

# this adds local maximum to tabu list
def update_tabu_list(local_max):
    max_tabu_size = 10000
    if len(tabu_list) >= max_tabu_size:
        tabu_list.pop(0)
    if local_max not in tabu_list:
        tabu_list.append(local_max)

def evaluation(total_distance, path, global_optimum, global_opt_dist):
    if total_distance < global_opt_dist:
        global_opt_dist = total_distance
        global_optimum = path.copy()
        return 0, global_optimum, global_opt_dist
    return 1, global_optimum, global_opt_dist

def change_neighbours(arr):
    neighbour = arr.copy()
    n = len(neighbour)
    while True:
        i, j = random.sample(range(n), 2)
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
        if neighbour not in tabu_list:
            break
    return neighbour

def tabu_search_alg(init_path, n):
    max_iterations = 15000
    max_no_improvement = 15000
    end_count = 0
    global_opt_dist = calculate_dist(init_path)
    local_opt_dist = calculate_dist(init_path)
    global_optimum = init_path.copy()
    local_optimum = init_path.copy()
    for i in range(max_iterations):
        for j in range(90):
            path = change_neighbours(local_optimum)
            total_distance = calculate_dist(path)
            if total_distance < local_opt_dist:
                local_opt_dist = total_distance
                local_optimum = path.copy()
        update_tabu_list(local_optimum)
        result, global_optimum, global_opt_dist = evaluation(local_opt_dist, local_optimum, global_optimum, global_opt_dist)
        print(local_opt_dist)
        if result == 0:
            end_count = 0
        else:
            end_count += result
        if end_count >= max_no_improvement:
            print("stopped")
            break
        if i % 500 == 0:
            create_connections(local_optimum, i)
    show_global_optimum(global_optimum, global_opt_dist)
    return global_opt_dist


N = 30
town_coordinates = town_init(N)
# town_coordinates =[(60, 200), (180, 200), (100, 180), (140, 180),
#     (20, 160), (80, 160), (200, 160), (140, 140),
#     (40, 120), (120, 120), (180, 100), (60, 80),
#     (100, 80), (180, 60), (20, 40), (100, 40),
#     (200, 40), (20, 20), (60, 20), (160, 20)]
random.shuffle(town_coordinates)  # ensures first iteration is randomly created
print("Shortest distance: ", tabu_search_alg(town_coordinates, N))

root.mainloop()
