import random
import math
import tkinter as tk

root = tk.Tk()
root.title("Town MAP")
canvas = tk.Canvas(width=400, height=400, bg="white")
canvas.pack()


# calculating distance using pythagorean theorem
def cityDistance(x1, x2, y1, y2):
    a = abs(x1-x2) ** 2
    b = abs(y1-y2) ** 2
    c = math.sqrt(a+b)
    return c

def townInit(n):
    townCoordinates = []

    # the map is big 400 x 400
    for i in range(n):
        x = random.randrange(10, 390)
        y = random.randrange(10, 390)
        # creates towns as dots on canvas
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        townCoordinates.append([x, y, False])


# first random visit defining initial solution
def visitTownInit(n):
    town = random.randrange(n+1)
    cityDistance()


totalDistance = 0
townInit(20)

root.mainloop()
