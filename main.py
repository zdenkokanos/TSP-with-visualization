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

DELAY = 0
tabu_list = []
graph_array = []  # To store total distances for plotting

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
def show_best_overall(best_overall):
    shortest_dist = fitness(best_overall)
    canvas.delete("all")
    canvas.create_text(200, 40, text=f"Best Path Length: {shortest_dist:.2f}", font=("Arial", 22), fill="black")
    for town in town_coordinates:
        canvas.create_oval(town[0] - 5, town[1] - 5, town[0] + 5, town[1] + 5, fill="red")
    for i in range(len(best_overall) - 1):
        create_line(best_overall[i][0], best_overall[i][1], best_overall[i + 1][0], best_overall[i + 1][1], "black")
    create_line(best_overall[len(best_overall) - 1][0], best_overall[len(best_overall) - 1][1], best_overall[0][0], best_overall[0][1], "blue")

# this function creates lines between nodes (cities), last line is blue to be sure it came back to starting point
def create_connections(path, i):
    clear_canvas(i)
    n = len(path)
    for i in range(n - 1):
        create_line(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1], "black")
    create_line(path[n - 1][0], path[n - 1][1], path[0][0], path[0][1], "blue")

# -------------------------ALGORITHM PART------------------------------- #

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

def fitness(path):
    total_distance = 0
    n = len(path)
    for i in range(n - 1):
        total_distance += city_distance(path[i], path[i + 1])
    total_distance += city_distance(path[n - 1], path[0])
    return total_distance

# this adds values to the tabu list and ensures that if it is full the oldest value is popped
def update_tabu_list(local_max):
    max_tabu_size = 10
    if len(tabu_list) >= max_tabu_size:
        tabu_list.pop(0)
    tabu_list.append(local_max)

def evaluation(path, best_overall):
    if fitness(path) < fitness(best_overall):
        best_overall = path.copy()
        return 0, best_overall
    return 1, best_overall

# this function switches the order of towns in which they are visited, I use substring order inversion for this task
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

# this is the main part of the algorithm
def tabu_search_alg(init_path, n):
    max_iterations = 1000
    max_no_improvement = 100
    end_count = 0
    best_overall = init_path.copy()
    candidate = init_path.copy()
    best_candidate = init_path.copy()
    update_tabu_list(best_candidate)
    for i in range(max_iterations):
        for j in range(n):  # I create n individuals, which are not in tabu list
            path = change_neighbours(best_candidate)
            if fitness(path) < fitness(candidate):  # choose the best one
                candidate = path.copy()
        if fitness(candidate) < fitness(best_candidate):    # if the individual from the chosen is
            best_candidate = candidate.copy()               # better than actual I start to search in it
        result, best_overall = evaluation(best_candidate, best_overall)  # I check if the value is best from all so far
        print(fitness(candidate))
        graph_array.append(fitness(best_candidate))
        update_tabu_list(best_candidate)
        if result == 0:  # this is just to keep track of not improving anymore
            end_count = 0
        else:
            end_count += result
        if end_count == max_no_improvement:
            break
        if i % 100 == 0:  # creates visualisation of every 100th path
            create_connections(best_candidate, i)
        candidate = init_path.copy()  # this achieves reset of the value in the next generation
    show_best_overall(best_overall)
    return fitness(best_overall)

# this function just creates graph to better visualise the correct solution
def plot_graph():
    plt.plot(graph_array)
    plt.title('Total Distance over Iterations')
    plt.xlabel('Iterations')
    plt.ylabel('Total Distance')
    plt.grid(True)
    plt.show()


N = 100   # this value can be changed (this is the number of towns)
town_coordinates = town_init(N)
random.shuffle(town_coordinates)  # ensures first iteration is randomly created
print("Shortest distance: ", tabu_search_alg(town_coordinates, N))
plot_graph()
root.mainloop()
