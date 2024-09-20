import random
import math
import tkinter as tk

root = tk.Tk()
root.title("Town MAP")
canvas = tk.Canvas(width=400, height=500, bg="white")
canvas.pack()

iteration_count = 0
iteration_text = canvas.create_text(200, 40, text=("Iterations: " + str(iteration_count)), font=("Arial", 22), fill="black")

tabu_list = []
def update_iteration():
    global iteration_count
    iteration_count += 1
    canvas.itemconfig(iteration_text, text=("Iterations: " + str(iteration_count)))

# calculating distance using pythagorean theorem
def city_distance(town1, town2):
    x1, y1 = town1[0], town1[1]
    x2, y2 = town2[0], town2[1]

    a = abs(x1-x2) ** 2
    b = abs(y1-y2) ** 2
    c = math.sqrt(a+b)
    return c

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


# creates visible connections between cities
def create_line(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, fill="black")
    canvas.after(300)
    canvas.update()

# def objective_function():

def change_neighbours(arr):
    while True:
        neighbor = arr[:]
        random.shuffle(neighbor)
        if neighbor not in tabu_list:
            tabu_list.append(neighbor)
            return neighbor

# first random visit defining initial solution
def initial_path(townArray, n):
    random.shuffle(townArray)  # defines first random solution
    total_distance = 0
    for i in range(len(townArray) - 1):
        total_distance += city_distance(townArray[i], townArray[i + 1])
        create_line(townArray[i][0], townArray[i][1], townArray[i + 1][0], townArray[i + 1][1])

    total_distance += city_distance(townArray[n - 1], townArray[0])
    create_line(townArray[n - 1][0], townArray[n - 1][1], townArray[0][0], townArray[0][1])
    print("Total distance: ", total_distance)
    return total_distance

def tabu_search_alg(recent_path, n):
    for i in range(10):
        path = change_neighbours(recent_path)
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += city_distance(path[i], path[i + 1])
            create_line(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])

        total_distance += city_distance(path[n - 1], path[0])
        create_line(path[n - 1][0], path[n - 1][1], path[0][0], path[0][1])
        print("Total distance: ", total_distance)
        update_iteration()


N = 20
town_coordinates = town_init(N)
distance = initial_path(town_coordinates, N)
best_path = town_coordinates
tabu_search_alg(town_coordinates, N)

root.mainloop()
