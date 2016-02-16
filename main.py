import tkinter

from XMLParse import *

from tkinter.ttk import *
import tkinter.scrolledtext
import tkinter.filedialog


def mainwindow_setup():
    global window

    window = tkinter.Tk()
    window.title("Project 1")
    window.geometry('700x400')
    window.configure(background='medium spring green')

    menubar = tkinter.Menu(window)
    menubar.add_command(label="Open New XML File", command=openfile)
    window.configure(menu=menubar)

    window.bind('<Return>', submitinput)
    window.bind('<Up>', previousinputentry)


def treespace_setup():
    global tree_scrolledtext, tree
    treespace_frame = Frame(window)
    treespace_frame.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.60)

    tree_scrolledtext = tkinter.scrolledtext.ScrolledText(treespace_frame)
    tree_scrolledtext.place(relx=0, rely=0, relheight=1, relwidth=1)
    tree_scrolledtext.configure(wrap=tkinter.NONE)

    tree_scrolledtext.config(state=tkinter.DISABLED)
    try:
        tree = XMLTree('examplefile.xml')
    except FileNotFoundError:
        return


def inputarea_setup():
    global window, input_entry, outputarea_text, previousinput

    input_entry = Entry(window)
    input_entry.place(relx=0.62, rely=0.91, relheight=0.08, relwidth=0.295)
    input_entry.focus_set()

    submit_button = Button(window, text="Submit", command=submitinput)
    submit_button.place(relx=0.92, rely=0.91, relheight=0.08, relwidth=0.075)

    outputarea_text = tkinter.Text(window)
    outputarea_text.place(relx=0.62, rely=0.01, relheight=0.89, relwidth=0.375)

    previousinput=""

def submitinput(junk=0):
    global input_entry, outputarea_text, previousinput
    text = input_entry.get()

    if len(text) > 0:
        try:
            text = '>>> ' + input_entry.get() + '\n' + tree.getresponse(input_entry.get()) + '\n\n'
            previousinput=input_entry.get()
            input_entry.delete(0, tkinter.END)
            outputarea_text.insert(tkinter.END, text)
        except NameError:
            outputarea_text.insert(tkinter.END, "*No XML File Loaded*" + '\n\n')
            input_entry.delete(0, tkinter.END)
        outputarea_text.see(tkinter.END)


def previousinputentry(junk=0):
    global previousinput, input_entry
    input_entry.delete(0, tkinter.END)
    input_entry.insert(0,previousinput)

    
def openfile():
    global filename, tree, outputarea_text
    filename = tkinter.filedialog.askopenfilename(parent=window)
    if '.xml' in filename.lower():
        try:
            tree = XMLTree(filename)
            updatetree()
        except () as e:
            return
    else:
        outputarea_text.insert(tkinter.END, "Not a valid file" + '\n\n')


def updatetree():
    global tree_scrolledtext, outputarea_text
    tree_scrolledtext.config(state=tkinter.NORMAL)
    tree_scrolledtext.delete(1.0, tkinter.END)
    tree_scrolledtext.insert(1.0, str(tree))
    tree_scrolledtext.config(state=tkinter.DISABLED)
    outputarea_text.delete(1.0, tkinter.END)

mainwindow_setup()
treespace_setup()
inputarea_setup()

try:
    updatetree()
except NameError:
    None

window.mainloop()
