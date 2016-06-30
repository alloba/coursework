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
        im = self.trim(self.image1)
        im.save('tsst.jpg')
        out = self.network.getoutput(self.convert_img_array(im))
        answer = self.convert_to_answer(out)
        print(answer)

    def trim(self, image):
        #bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
        #diff = ImageChops.difference(image, bg)
        #diff = ImageChops.add(diff, diff, 2.0, -100)
        #bbox = diff.getbbox()

        #image = self.image1.crop(bbox)

        size = (32, 32)
        #image.thumbnail(size)
        #background = Image.new('RGBA', size, (255, 255, 255, 0))
        #background.paste(
        #    image,
        #    ((size[0] - image.size[0]) // 2, (size[1] - image.size[1]) // 2))

        thumb = ImageOps.fit(image,size,Image.ANTIALIAS)
        return thumb

    def convert_img_array(self, img):
        # work needs to be done here to compress images correctly.
        # needs to take the image and shrink it to an array using the original method
        # (take groups of pixels and compress into squares)

        #put all pixels into a dictionary that organizes everything into boxes
        box_dict = {}
        for i in range(8):
            for j in range(8):
                box_dict[(i,j)] = []

        for value, i in zip(img.getdata(), range(len(img.getdata()))):
            box_row = i // 32 // 4
            box_column = i % 32 // 4
            box_dict[(box_row, box_column)].append(value)

        out_array = []
        box_sum_list = []
        for i in range(8):
            for j in range(8):
                box_sum = 0
                for item in box_dict[i, j]:
                    box_sum += sum(item[:-1])
                box_sum_list.append(box_sum)

        for val in box_sum_list:
            out_array.append(val//510)

        #invert numbers. black needs to be max val, not white
        for i in range(len(out_array)):
            out_array[i] = -(out_array[i] - 8) + 8

        return out_array

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
