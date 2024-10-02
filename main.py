import random
import math
import tkinter
import matplotlib.pyplot as plt

root = tkinter.Tk()
root.title("Town MAP")
# Set the window to always be on top
root.attributes("-topmost", True)
canvas = tkinter.Canvas(width=400, height=500, bg="white")
canvas.pack()
graph_array = []  # To store total distances for plotting

DELAY = 0
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

def show_best_path(best_path):
    shortest_dist = fitness(best_path)
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
def fitness(path):
    total_distance = 0
    n = len(path)
    for i in range(n - 1):
        total_distance += city_distance(path[i], path[i + 1])
    total_distance += city_distance(path[n - 1], path[0])
    return total_distance

def change_neighbours(arr):
    neighbour = arr.copy()
    n = len(neighbour)
    i, j = sorted(random.sample(range(n), 2))  # i and j must be sorted, so we always start from left
    # I chose the mutation from lecture: "substring order inversion"
    neighbour[i:j + 1] = reversed(neighbour[i:j + 1])
    return neighbour

def probability(T, last_value, new_value):
    delta_E = new_value - last_value
    prob = math.exp(-delta_E / T)
    print("prob:", prob)
    if random.random() < prob:
        print("was here")
        return True
    return False

def cool(T, cooling):
    return T * cooling

def sim_annealing(init_path, n):
    i = 0
    final_path = init_path
    best_candidate = init_path
    best_path = init_path
    T = 90.00  # initialization
    cooling = 0.999
    T_min = 30.00
    while T > T_min:
        for j in range(5):  # I create n individuals
            path = change_neighbours(best_path)
            if fitness(path) < fitness(best_candidate):
                best_candidate = path.copy()  # this takes the best one created from neighbour-hood
        if fitness(final_path) < fitness(best_candidate):
            if probability(T, fitness(best_path), fitness(best_candidate)):
                best_path = best_candidate.copy()
                print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            final_path = best_path = best_candidate.copy()
        print(fitness(best_candidate))
        graph_array.append(fitness(best_candidate))
        if i % 200 == 0:
            create_connections(best_candidate, i)
        T = cool(T, cooling)
        i += 1
        best_candidate = init_path.copy()  # ma to byt nema to byt??
    show_best_path(final_path)
    return fitness(final_path)

def plot_graph():
    plt.plot(graph_array)
    plt.title('Total Distance over Iterations')
    plt.xlabel('Iterations')
    plt.ylabel('Total Distance')
    plt.grid(True)
    plt.show()


N = 40
town_coordinates = town_init(N)
# town_coordinates =[(60, 200), (180, 200), (100, 180), (140, 180),
#     (20, 160), (80, 160), (200, 160), (140, 140),
#     (40, 120), (120, 120), (180, 100), (60, 80),
#     (100, 80), (180, 60), (20, 40), (100, 40),
#     (200, 40), (20, 20), (60, 20), (160, 20)]
random.shuffle(town_coordinates)  # ensures first iteration is randomly created
print("Shortest distance: ", sim_annealing(town_coordinates, N))
plot_graph()
root.mainloop()
