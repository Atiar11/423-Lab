import tkinter as tk
import random
import time

# Constants and point class
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = "black"
POINT_COLORS = ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "pink"]

class Point:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(x, y, x+10, y+10, fill=random.choice(POINT_COLORS))
        self.speed = random.randint(1, 5)
        self.direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])
        self.blinking = False

    def move(self):
        dx, dy = self.direction
        self.canvas.move(self.id, dx * self.speed, dy * self.speed)

    def blink(self):
        if self.blinking:
            current_color = self.canvas.itemcget(self.id, "fill")
            new_color = BACKGROUND_COLOR if current_color in POINT_COLORS else random.choice(POINT_COLORS)
            self.canvas.itemconfig(self.id, fill=new_color)
            self.canvas.update()
            self.canvas.after(500, self.blink)  # Blink every half second
#box class
class InteractiveBox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Atiar Osman CSE423 LAB1-TASK2")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()
        self.points = []
        self.frozen = False
        
        #movements
        self.bind("<Button-1>", self.add_point) 
        self.bind("<Button-3>", self.add_random_direction_point)
        self.bind("<Up>", self.increase_speed)
        self.bind("<Down>", self.decrease_speed)
        self.bind("<space>", self.toggle_freeze)

        self.update_points()
        
    #different angles
    def add_point(self, event):
        if not self.frozen:
            x, y = event.x, event.y
            point = Point(self.canvas, x, y)
            self.points.append(point)
    
    #direction for the points
    def add_random_direction_point(self, event):
        if not self.frozen:
            x, y = event.x, event.y
            point = Point(self.canvas, x, y)
            point.direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])
            self.points.append(point)
    #speed
    def increase_speed(self, event):
        for point in self.points:
            point.speed += 1

    def decrease_speed(self, event):
        for point in self.points:
            point.speed = max(1, point.speed - 1)

    def toggle_freeze(self, event):
        self.frozen = not self.frozen

    def update_points(self):
        for point in self.points:
            if not self.frozen:
                point.move()
            point.blink()
        self.after(30, self.update_points)

if __name__ == "__main__":
    app = InteractiveBox()
    app.mainloop()
