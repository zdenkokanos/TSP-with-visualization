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
iteration_count = 0
best_path = []
shortest_distance = 99999999
tabu_list = []
end_count = 0

def clear_canvas():
    global iteration_count
    iteration_count += 1
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

def show_best_path():
    canvas.delete("all")
    canvas.create_text(200, 40, text=f"Best Path Length: {shortest_distance:.2f}", font=("Arial", 22), fill="black")
    for town in town_coordinates:
        canvas.create_oval(town[0] - 5, town[1] - 5, town[0] + 5, town[1] + 5, fill="red")
    for i in range(len(best_path) - 1):
        create_line(best_path[i][0], best_path[i][1], best_path[i + 1][0], best_path[i + 1][1], "black")
    create_line(best_path[len(best_path) - 1][0], best_path[len(best_path) - 1][1], best_path[0][0], best_path[0][1], "blue")

def create_connections(path):
    clear_canvas()
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
    max_tabu_size = 1000
    if len(tabu_list) >= max_tabu_size:
        tabu_list.pop(0)
    tabu_list.append(local_max)

def evaluation(total_distance, path):
    global shortest_distance
    global best_path
    global end_count
    if total_distance < shortest_distance:
        shortest_distance = total_distance
        best_path = path.copy()
        end_count = 0
        return 0
    return 1

def change_neighbours(arr):
    neighbour = arr.copy()
    while True:
        i = random.randint(0, len(neighbour) - 2)
        neighbour[i], neighbour[i + 1] = neighbour[i + 1], neighbour[i]
        if neighbour not in tabu_list:
            break
    update_tabu_list(neighbour)
    return neighbour

def tabu_search_alg(init_path):
    global best_path
    best_path = init_path
    global end_count
    max_iterations = 5000
    max_no_improvement = 1000
    for i in range(max_iterations):
        path = change_neighbours(best_path)
        total_distance = calculate_dist(path)
        result = evaluation(total_distance, path)
        end_count += result
        if end_count >= max_no_improvement:
            break
        create_connections(path)
    show_best_path()
    return shortest_distance


N = 10
town_coordinates = town_init(N)
# town_coordinates =[(60, 200), (180, 200), (100, 180), (140, 180),
#     (20, 160), (80, 160), (200, 160), (140, 140),
#     (40, 120), (120, 120), (180, 100), (60, 80),
#     (100, 80), (180, 60), (20, 40), (100, 40),
#     (200, 40), (20, 20), (60, 20), (160, 20)]
random.shuffle(town_coordinates)  # ensures first iteration is randomly created
print("Shortest distance: ", tabu_search_alg(town_coordinates))

root.mainloop()
