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
    canvas.create_line(x1, y1, x2, y2, fill=color)
    canvas.after(DELAY)
    canvas.update()

# this function shows visualization of the best path found during the algorithm search
def show_best_path(best_path):
    shortest_dist = fitness(best_path)
    canvas.delete("all")
    canvas.create_text(200, 40, text=f"Best Path Length: {shortest_dist:.2f}", font=("Arial", 22), fill="black")
    for town in town_coordinates:
        canvas.create_oval(town[0] - 5, town[1] - 5, town[0] + 5, town[1] + 5, fill="red")
    for i in range(len(best_path) - 1):
        create_line(best_path[i][0], best_path[i][1], best_path[i + 1][0], best_path[i + 1][1], "black")
    create_line(best_path[len(best_path) - 1][0], best_path[len(best_path) - 1][1], best_path[0][0], best_path[0][1], "blue")

# this function creates lines between nodes (cities), last line is blue to be sure it came back to starting point
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

# this is the fitness function
def fitness(path):
    total_distance = 0
    n = len(path)
    for i in range(n - 1):
        total_distance += city_distance(path[i], path[i + 1])
    total_distance += city_distance(path[n - 1], path[0])
    return total_distance

# this adds local maximum to tabu list
def update_tabu_list(local_max):
    max_tabu_size = 20
    if len(tabu_list) >= max_tabu_size:
        tabu_list.pop(0)
    tabu_list.append(local_max)

def evaluation(path, best_path):
    if fitness(path) < fitness(best_path):
        best_path = path.copy()
        return 0, best_path
    return 1, best_path

# this function makes mutations of the path
def change_neighbours(arr):
    neighbour = arr.copy()
    n = len(neighbour)
    while True:
        i, j = sorted(random.sample(range(n), 2))  # i and j must be sorted, so we always start from left
        # I chose the mutation from lecture: "substring order inversion"
        neighbour[i:j + 1] = reversed(neighbour[i:j + 1])

        if neighbour not in tabu_list:
            break
    return neighbour

def tabu_search_alg(init_path, n):
    max_iterations = 200
    max_no_improvement = 20
    end_count = 0
    best_path = init_path
    best_candidate = init_path
    update_tabu_list(best_candidate)
    for i in range(max_iterations):
        for j in range(n):
            path = change_neighbours(best_candidate)
            if fitness(path) < fitness(best_candidate):
                best_candidate = path.copy()
        result, best_path = evaluation(best_candidate, best_path)
        print(fitness(best_candidate))
        update_tabu_list(best_candidate)
        if result == 0:
            end_count = 0
        else:
            end_count += result
        if end_count >= max_no_improvement:
            break
        if i % 20 == 0:  # creates visualisation of every 200th path
            create_connections(best_candidate, i)
        print("i = ", i)
    show_best_path(best_path)
    return fitness(best_path)


N = 30
town_coordinates = town_init(N)
# town_coordinates = [(94, 390), (348, 390), (179, 359), (263, 359),
#     (10, 328), (137, 328), (390, 328), (263, 297),
#     (52, 266), (221, 266), (348, 234), (94, 203),
#     (179, 203), (348, 172), (10, 141), (179, 141),
#     (390, 141), (10, 110), (94, 110), (306, 110)]
random.shuffle(town_coordinates)  # ensures first iteration is randomly created
print("Shortest distance: ", tabu_search_alg(town_coordinates, N))

root.mainloop()
