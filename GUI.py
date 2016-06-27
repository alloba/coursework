import tkinter
import tkinter.filedialog
from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
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

        self.canvas_height = 800
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

        if len(self.point_list) == 2:
            self.point_list.append(self.point_list[0])
            self.point_list.append(self.point_list[1])

        self.canvas.create_line(self.point_list, tags='theline', width=20)
        self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, tags='theline', fill='black')

        self.draw.line(self.point_list, 'black', width=20)

        self.point_list = self.point_list[-2:]

    def clear_canvas(self, event):
        self.canvas.delete('theline')
        self.point_list = []

        self.draw.rectangle([0, 0, self.canvas_width, self.canvas_height], 'white')

    def save(self):
        im = self.trim(self.image1)
        #dont do resizing here like this. it cuts out the black entirely and messed up the answer
        resized = im.resize([8,8])
        resized.save('C:/test/tsst.jpg')
        print(self.convert_img_array(resized))
        print('test')

        out = self.network.getoutput(self.convert_img_array(resized))
        answer = self.convert_to_answer(out)
        print(answer)

    def trim(self, image):
        bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return self.image1.crop(bbox)

    def convert_img_array(self, img):
        # work needs to be done here to compress images correctly.
        # needs to take the image and shrink it to an array using the original method
        # (take groups of pixels and compress into squares)
        arr = img.getdata()
        new_arr = []
        for i in arr:
            if sum(i) == 0:
                new_arr.append(15)
            else:
                new_arr.append(0)
        return new_arr

    def convert_to_answer(self, output_list):
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
