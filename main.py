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

def show_best_path(best_path, shortest_dist):
    canvas.delete("all")
    canvas.create_text(200, 40, text=f"Best Path Length: {shortest_dist:.2f}", font=("Arial", 22), fill="black")
    for town in town_coordinates:
        canvas.create_oval(town[0] - 5, town[1] - 5, town[0] + 5, town[1] + 5, fill="red")
    for i in range(len(best_path) - 1):
        create_line(best_path[i][0], best_path[i][1], best_path[i + 1][0], best_path[i + 1][1], "black")
    create_line(best_path[len(best_path) - 1][0], best_path[len(best_path) - 1][1], best_path[0][0], best_path[0][1], "blue")

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

# -------------------------ALGORITHM PART------------------------------- #
# this is the fitnes function
def calculate_dist(path):
    total_distance = 0
    n = len(path)
    for i in range(n - 1):
        total_distance += city_distance(path[i], path[i + 1])
    total_distance += city_distance(path[n - 1], path[0])
    return total_distance

def evaluation(total_distance, path, best_path, shortest_dist, T, final_dist, final_path):
    probability = T / 100
    if total_distance < final_path:
        final_dist = total_distance
        final_path = path.copy()
        return final_path, final_dist
    else:

        return best_path, shortest_dist

def change_neighbours(arr):
    neighbour = arr.copy()
    n = len(neighbour)
    while True:
        i, j = random.sample(range(n), 2)
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
        if neighbour not in tabu_list:
            break
    return neighbour

def probability(T):
    percentage = T/100
    if random.random() < percentage:
        return 0
    return 1

def cool(T, cooling):
    return T * cooling

def sim_annealing(init_path, n):
    maximum = 999999999
    i = 0
    shortest_dist = maximum
    best_local_dist = maximum
    best_path = init_path
    final_dist = maximum  # final shortest distance
    final_path = init_path
    best_local_path = []
    T = 90.00  # initialization
    cooling = 0.995
    T_min = 20.00
    while T > T_min:
        for j in range(n):
            path = change_neighbours(best_path)
            total_distance = calculate_dist(path)
            if total_distance < best_local_dist:
                best_local_dist = total_distance
                best_local_path = path.copy()
        if final_dist < best_local_dist:
            if probability(T):
                best_path = best_local_path.copy()
                shortest_dist = best_local_dist
        else:
            final_path = best_path = best_local_path.copy()
            final_dist = shortest_dist = best_local_dist
        print(best_local_dist)
        best_local_dist = maximum
        create_connections(best_local_path, i)
        T = cool(T, cooling)
        i += 1
    show_best_path(final_path, final_dist)
    return shortest_dist


N = 30
town_coordinates = town_init(N)
# town_coordinates =[(60, 200), (180, 200), (100, 180), (140, 180),
#     (20, 160), (80, 160), (200, 160), (140, 140),
#     (40, 120), (120, 120), (180, 100), (60, 80),
#     (100, 80), (180, 60), (20, 40), (100, 40),
#     (200, 40), (20, 20), (60, 20), (160, 20)]
random.shuffle(town_coordinates)  # ensures first iteration is randomly created
print("Shortest distance: ", sim_annealing(town_coordinates, N))

root.mainloop()
