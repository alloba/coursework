import tkinter
import tkinter.filedialog
from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
from PIL import ImageOps
import pickle

from Network import Network

class TKApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Draw")
        self.window.configure(background="white")

        self.menubar = tkinter.Menu(self.window)
        self.menubar.add_command(label="save", command=self.save)

        self.window.configure(menu=self.menubar)

        self.canvas_height = 600
        self.canvas_width = 600
        self.canvas_center = self.canvas_height//2

        self.canvas = tkinter.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.image1 = Image.new('RGB', (self.canvas_width, self.canvas_height), 'white')
        self.draw = ImageDraw.Draw(self.image1)

        self.point_list = []
        self.line_tag = 'theline'

        self.canvas.bind('<B1-Motion>', self.draw_line)
        self.canvas.bind('<Button-3>', self.clear_canvas)

        self.network = pickle.load(open('best_net.p', 'rb'))

    def draw_line(self, event):
        self.point_list.append(event.x)
        self.point_list.append(event.y)

        # this is just to make it stop complaining that it cant draw lines when there is only one point
        # when the line first starts
        if len(self.point_list) == 2:
            self.point_list.append(self.point_list[0])
            self.point_list.append(self.point_list[1])

        self.canvas.create_line(self.point_list, tags='theline', width=80)
        self.canvas.create_oval(event.x-40, event.y-40, event.x+40, event.y+40, tags='theline', fill='black')

        self.draw.line(self.point_list, 'black', width=80)
        self.point_list = self.point_list[-2:]

    def clear_canvas(self, event):
        self.canvas.delete('theline')
        self.point_list = []

        self.draw.rectangle([0, 0, self.canvas_width, self.canvas_height], 'white')

    def save(self):
        resized_image = ImageOps.fit(self.image1, (32, 32), Image.ANTIALIAS)
        resized_image.save('tsst.jpg')
        out = self.network.getoutput(self.convertImageToArray(resized_image))

        # displaying the answer should be done better, but i am super lazy and not worried about it
        answer = self.convert_to_answer(out)
        print(answer)

    def convertImageToArray(self, img):
        # takes the given image and changes it into an array matching the format of the optdigits training set.
        # this expects that the image given will be a 32x32 sized, black and white image.
        # the image is divided into 4x4 sectors and the amount of color is summed up, and used for the final array

        # put all pixels into a dictionary that organizes everything into boxes
        # thank you very much sudoku project, because dividing arrays into boxes is annoying for my brain
        box_dict = {}
        # why isn't there a better way to do this?
        for i in range(8):
            for j in range(8):
                box_dict[(i, j)] = []  # making a dictionary referring to coordinates made it easier to sort into boxes

        for value, i in zip(img.getdata(), range(len(img.getdata()))):
            # 32 is the picture size, 4 is because there will be 4x4 boxes
            box_row = i // 32 // 4
            box_column = i % 32 // 4
            box_dict[(box_row, box_column)].append(value)

        box_sum_list = []
        for i in range(8):
            for j in range(8):
                box_sum = 0
                for item in box_dict[i, j]:
                    box_sum += sum(item[:-1])
                box_sum_list.append(box_sum//510)  # 510 is the max color value/16. this is to scale the values to 0-16

        # the original training set treated black as max value, and white or transparency as 0.
        # so this bit flips the values around, since the current list's values are backwards (white is 16)
        # (another bit of simple math that took way too long to figure out
        # (to invert a number around an axis that isn't 0, just subtract the center point (8), make the number negative,
        # (and add the axis back in. it's dead simple, which makes it sad that it took like 15 minutes to think of)
        for i in range(len(box_sum_list)):
            box_sum_list[i] = -(box_sum_list[i] - 8) + 8

        return box_sum_list

    def convert_to_answer(self, output_list):
        # this function should be put in the network class probably, but whatever.
        # takes an outputted list from the network and decides what the actual answer is as an integer
        most_confident = -1
        amount = 0.0
        for i in range(len(output_list)):
            if output_list[i] > amount:
                most_confident = i
                amount = output_list[i]
        return most_confident

root = tkinter.Tk()
app = TKApp(root)

root.mainloop()
