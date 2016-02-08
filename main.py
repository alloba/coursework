import tkinter

from XMLParse import *

from tkinter.ttk import *
import tkinter.scrolledtext
import tkinter.filedialog

def mainwindow_setup():
    global window

    window = tkinter.Tk()
    window.title("Project 1")
    window.geometry('600x400')

    menubar = tkinter.Menu(window)
    menubar.add_command(label="Open New XML File", command=openfile)

    window.configure(menu=menubar)

def treespace_setup():
    treespace_frame = Frame(window)
    treespace_frame.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.40)

    tree_scrolledtext = tkinter.scrolledtext.ScrolledText(treespace_frame)
    tree_scrolledtext.place(relx=0, rely=0, relheight=1, relwidth=1)
    tree_scrolledtext.configure(wrap=tkinter.NONE)


def inputarea_setup():
    global window

    input_entry = Entry(window)
    input_entry.place(relx=0.43, rely=0.92, relheight=0.08, relwidth=0.46)

    submit_button = Button(window)
    submit_button.place(relx=0.91, rely=0.92, relheight=0.09, relwidth=0.09)

    outputarea_text = tkinter.Text(window)
    outputarea_text.place(relx=0.43, rely=0.02, relheight=0.9, relwidth=0.55)


def openfile():
    filename = tkinter.filedialog.askopenfilename(parent=window)
    try:
        1+1
    except () as e:
        return

mainwindow_setup()
treespace_setup()
inputarea_setup()

window.mainloop()

tree = XMLTree("C:/CourseWork/AI/Project 1/examplefile.xml")
#print(tree)
#print(tree.getresponse("Ranged"))
