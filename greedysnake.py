import tkinter as tk
from tkinter import Canvas
import time
from random import randint
from collections import deque
import numpy as np
import threading

# class CallbackThread(threading.Thread):
#     def __init__(self, queue):
        

class Application(tk.Frame):

    class Food(object):
        def __init__(self, mat, color='yellow'):
            self.color = color
            self.mat = mat
            self.coor = self.random()

        def random(self):
            return randint(0, len(self.mat[0]) - 1), randint(0, len(self.mat) - 1)

    def changedirection(self, event):
        print(event.keycode, event.keysym)
        self.directionq.appendleft(self.directiondict[event.keysym])

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.width, self.height = 800, 400
        self.unit = 20
        f = Canvas(master, width=self.width, height=self.height, bg='gray')
        f.bind('<Up>', self.changedirection)
        f.bind('<Down>', self.changedirection)
        f.bind('<Left>', self.changedirection)
        f.bind('<Right>', self.changedirection)
        f.focus_set()
        f.pack()
        for i in range(0, self.height, self.unit):
            f.create_line(0, i, self.width, i)
        for i in range(0, self.width, self.unit):
            f.create_line(i, 0, i, self.height)
        self.f = f
        self.mat = [[0] * (self.width // self.unit) for _ in range(self.height // self.unit)]
        print('canvas matrix', len(self.mat), len(self.mat[0]))

        # direction queue
        self.directiondict = {'Down': (0, 1), 'Up': (0, -1), 'Left': (-1, 0), 'Right': (1, 0)}
        self.directionq = deque([])

    def create_widgets(self):
        self.startgamebut = tk.Button(self)
        self.startgamebut["text"] = "Start Game"
        self.startgamebut["command"] = self.startgame
        self.startgamebut.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def startgame(self):
        print('start game!')
        # clear out the canvas
        if hasattr(self, 'snake'):
            self.clearsnake()
            self.f.delete('food')

        # create snake
        self.snake = [(0, 0), (1, 0)]
        # TODO need two direction
        self.direction = (1, 0)
        self.food = self.Food(self.mat)
        self.updatefood()

        # start game
        self.fillsnake()
        self.snakemove()

    def snakemove(self):
        print('new iter')
        head = self.snake[-1]
        while self.directionq:
            newdirection = self.directionq.pop()
            if np.inner(newdirection, self.direction) == 0:
                self.direction = newdirection
                break
        # newsnake = list(self.snake[1:]) + [(head[0] + self.direction[0], head[1] + self.direction[1])]
        newhead = (head[0] + self.direction[0], head[1] + self.direction[1])
        collide = self.check_collision(newhead)
        if not collide:
            print('game over')
            return
        elif collide == 'eat food':
            self.createrect(newhead[0], newhead[1])
            self.snake = self.snake + [newhead]
        else:
            self.updatesnake(self.snake[0], newhead)
            self.snake = self.snake[1:] + [newhead]
        print(self.snake)
        self.after(300, self.snakemove)

    def fillsnake(self):
        for i, j in self.snake:
            self.createrect(i, j)
        self.f.update()

    def clearsnake(self):
        for i, j in self.snake:
            self.f.delete('snake_{}_{}'.format(i, j))
        self.f.update()

    def updatesnake(self, tail, head):
        self.f.delete('snake_{}_{}'.format(tail[0], tail[1]))
        self.createrect(head[0], head[1])
        self.f.update()

    def updatefood(self):
        self.f.delete('food')
        while True:
            newcoor = self.food.random()
            print('new food {}'.format(newcoor))
            if newcoor not in self.snake:
                break
        self.createrect(newcoor[0], newcoor[1], color=self.food.color, t='food')
        self.food.coor = newcoor
        print('updated food at {}'.format(newcoor))
        self.f.update()

    def check_collision(self, head):
        # collide with boundary
        i1, j1 = head
        if i1 < 0 or i1 == len(self.mat[0]) or j1 < 0 or j1 == len(self.mat):
            print('hit boundary')
            return False

        # collide with food
        if (i1, j1) == self.food.coor:
            self.updatefood()
            return 'eat food'

        # collide with self
        if head in self.snake:
            print('hit self')
            return False
        return True

    def createrect(self, i, j, color='green', t='snake'):
        tag = 'snake_{}_{}'.format(i, j) if t == 'snake' else 'food'
        i *= self.unit
        j *= self.unit
        self.f.create_rectangle(i, j + self.unit, i + self.unit, j, fill=color, tags=tag)
        # self.f.update()


root = tk.Tk()
root.geometry('800x600')
app = Application(master=root)
app.master.maxsize(1000, 600)



app.mainloop()