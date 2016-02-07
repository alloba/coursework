from XMLParse import *
from tkinter import *
from tkinter.ttk import *


def window_setup():
    global window
    window = Tk()

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=2)

    window.grid_rowconfigure(0, weight=1)

    window.title("Project 1")
    window.geometry("500x300")


def treeview_setup():
    global window
    treeview_frame = Frame(window)

    scrollbar_x = Scrollbar(treeview_frame, orient=HORIZONTAL)
    scrollbar_y = Scrollbar(treeview_frame)

    text_tree_frame = Frame(treeview_frame)
    text_tree = Text(text_tree_frame, wrap=NONE, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    scrollbar_x.grid(row=1, column=0, sticky='nsew')
    scrollbar_y.grid(row=0, column=1, sticky='nsew')

    text_tree_frame.grid(row=0, column=0, sticky='nsew')
    text_tree_frame.grid_propagate(False)
    text_tree.grid(row=0, column=0, sticky='nsew')

    scrollbar_x.config(command=text_tree.xview)
    scrollbar_y.config(command=text_tree.yview)

    treeview_frame.grid(row=0, column=0, columnspan=2, sticky='nswe')

    treeview_frame.grid_rowconfigure(0, weight=1)
    treeview_frame.grid_columnconfigure(0, weight=1)

    text_tree.config(state=DISABLED)


def controlarea_setup():
    global window

    controlarea_frame = Frame(window)

    output_text_frame = Frame(controlarea_frame)
    output_text = Text(output_text_frame)

    input_entry = Entry(controlarea_frame)
    submitbutton_button = Button(controlarea_frame)

    output_text_frame.grid(row=0, column=0, sticky='nsew', columnspan=2)
    output_text_frame.grid_propagate(False)

    output_text.grid(row=0, column=0, sticky='nsew')
    input_entry.grid(row=1, column=0, sticky='w')
    submitbutton_button.grid(row=1, column=1, sticky='e')
    controlarea_frame.grid(row=0, column=1, sticky='nse')

    controlarea_frame.grid_columnconfigure(0, weight=1)
    controlarea_frame.grid_rowconfigure(0, weight=1)

#window_setup()
#treeview_setup()
#controlarea_setup()
#window.mainloop()



tree = XMLTree("C:/CourseWork/AI/Project 1/examplefile.xml")
#print(tree)
#print(tree.getresponse("Ranged"))
