import random
import math
import tkinter as tk

root = tk.Tk()
root.title("Town MAP")
canvas = tk.Canvas(width=400, height=400, bg="white")
canvas.pack()


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
        y = random.randrange(10, 390)
        # creates towns as dots on canvas
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        town_coordinates.append([x, y])
    return town_coordinates


# creates visible connections between cities
def create_line(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, fill="black")
    canvas.after(300)
    canvas.update()


# first random visit defining initial solution
def visitTownInit(townArray, n):
    random.shuffle(townArray)  # defines first random solution
    totalDistance = 0
    for i in range(len(townArray) - 1):
        totalDistance += city_distance(townArray[i], townArray[i + 1])
        create_line(townArray[i][0], townArray[i][1], townArray[i + 1][0], townArray[i + 1][1])

    totalDistance += city_distance(townArray[n - 1], townArray[0])
    create_line(townArray[n - 1][0], townArray[n - 1][1], townArray[0][0], townArray[0][1])
    print("Total distance: ", totalDistance)


town_coordinates = town_init(20)
visitedTowns = []
visitTownInit(town_coordinates, 20)

root.mainloop()
