import tkinter
from tkinter.ttk import *
import tkinter.filedialog
import Sarsa
import threading

def mainwindow_setup():
    global window

    window = tkinter.Tk()
    window.title("Project 1")
    #window.geometry('800x400')
    window.configure(background='grey')

    menubar = tkinter.Menu(window)
    menubar.add_command(label="Open File", command=openfile)
    menubar.add_command(label='Reset Q Table', command=reset_q)
    menubar.add_command(label='Create new Gridworld', command=new_gridworld)
    menubar.add_command(label='Save Gridworld', command=save_gridworld)

    menubar.add_command(label='Update', command=update_canvas)
    window.configure(menu=menubar)

    #window.bind('<Return>', submitinput)
    #window.bind('<Up>', previousinputentry)


def display_setup():
    global window, box_list, arrow_list
    #display_frame = Frame(window)

    #display_frame.pack()
    #label_list = [[Label(display_frame, text=0) for x in range(20)] for y in range(20)]
    #for x in range(len(label_list)):
    #    for y in range(len(label_list[x])):
    #        label_list[x][y].grid(row=x, column=y, sticky='nwse')

    global canvas, box_list
    canvas = tkinter.Canvas(window, width=800, height=800, bg='white')
    canvas.pack()

    size = 20

    box_list = []
    for i in range(size):
        for j in range(size):
            box_list.append(canvas.create_rectangle(i*40, j*40, i*40+40, j*40+40, fill='red', ))
    for box in box_list:
        canvas.itemconfig(box, fill='red')

    for box in box_list[1::3]:
        canvas.itemconfig(box, fill='blue')

    arrow_list=[]
    for i in range(size):
        for j in range(size):
            arrow_list.append(canvas.create_text(i*40+20, j*40+20, text='a'))
    for arrow in arrow_list:
        canvas.itemconfig(arrow, text='b')




def sarsa_tick():
    sarsa.episode(5)


def update_canvas():

    global canvas, box_list, arrow_list, sarsa, gridworld

    for x, y, z in zip(box_list, gridworld.Q, arrow_list):
        value = max(gridworld.Q[y])
        index = gridworld.Q[y].index(value)
        if index == 0:
            canvas.itemconfig(z, text='<')
        if index == 1:
            canvas.itemconfig(z, text='v')
        if index == 2:
            canvas.itemconfig(z, text='>')
        if index == 3:
            canvas.itemconfig(z, text='^')
        ######
        minimum = -0.5
        maximum = 0.5
        minimum, maximum = float(minimum), float(maximum)
        ratio = 2 * (value-minimum) / (maximum - minimum)
        b = int(max(0, 255*(1 - ratio)))
        r = int(max(0, 255*(ratio - 1)))
        g = 255 - b - r
        color = "#%02x%02x%02x" % (r, g, b)
        ######

        try:
            canvas.itemconfig(x, fill=color)
        except:
            canvas.itemconfig(x, fill='black')
    goal = gridworld.goal
    canvas.itemconfig(box_list[goal[0]*20 + goal[1]], fill='gold')

    t = threading.Thread(target=sarsa_tick)
    t.daemon = True
    t.start()

    canvas.after(50, update_canvas)



def reset_q():
    global gridworld
    gridworld.reset_q()


def new_gridworld():
    global gridworld
    gridworld = Sarsa.Gridworld(gridworld.size, gridworld.goal, gridworld.obstacles)


def save_gridworld():
    global gridworld
    Sarsa.save_csv(gridworld, 'gridworld.csv')


def openfile():
    global filename
    filename = tkinter.filedialog.askopenfilename(parent=window)

    try:
        gridworld = Sarsa.open_csv(filename)

    except SyntaxError as e:
        print("Improperly Formatted CSV File")


global gridworld, sarsa, t

import random
random.seed(0)

gridworld = Sarsa.Gridworld(obstacles=[(2,2), (3,3)], goal=(15,15))
sarsa = Sarsa.SARSA(gridworld=gridworld, alpha=0.7, gamma=0.4, lamb=0.5, epsilon=0.4)
mainwindow_setup()
display_setup()
window.after(1000, update_canvas)
window.mainloop()