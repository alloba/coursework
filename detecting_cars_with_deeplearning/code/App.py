import random
import sys, os, shutil
import threading
import time

import PIL.Image

import Tkinter as tk
import tkFileDialog
from PIL import ImageTk

import CustomizedInterfaceElements as ui
from ParkingLot import *

import ConfigParser


class RoleSelect(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, master=self.parent)
        self.lot_origin, self.lot_source, self.stats_file = self.load_config()

        # check if all the folders that need to exist actually do.
        if not os.path.isdir('cropped_images/'):
            os.makedirs('cropped_images/')
        if not os.path.isdir('resources/lot_origin/'):
            os.makedirs('resources/lot_origin/')
        if not os.path.isdir('resources/lot_source/'):
            os.makedirs('resources/lot_source/')

        # add a label with the project logo
        # separate operations on loading the image because anti aliasing didn't work otherwise
        pilimage = PIL.Image.open('resources/Logo-WhiteBG.png')
        resized = pilimage.resize([784, 412], PIL.Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized)
        self.panel = tk.Label(self, image=self.img)
        self.panel.pack(side=tk.TOP, fill='both')

        self.selectSetupButton = tk.Button(self, text="Open Operator", command=self.start_setup)
        self.selectMonitorButton = tk.Button(self, text="Open Monitor", command=self.start_monitor)
        self.selectSetupButton.pack(side=tk.RIGHT)
        self.selectMonitorButton.pack(side=tk.RIGHT)

        # directory paths for image source and image origin
        self.source_label = tk.Label(self, text='Enter Image Source: ')
        self.source_var = tk.StringVar()
        self.source_var.set(self.lot_source)
        self.source_entry = tk.Entry(self, textvariable=self.source_var)
        self.source_label.pack(side=tk.LEFT)
        self.source_entry.pack(side=tk.LEFT)

        self.origin_label = tk.Label(self, text='Enter Image Origin: ')
        self.origin_var = tk.StringVar()
        self.origin_var.set(self.lot_origin)
        self.origin_entry = tk.Entry(self, textvariable=self.origin_var)
        self.origin_label.pack(side=tk.LEFT)
        self.origin_entry.pack(side=tk.LEFT)

        self.pack()

    def start_setup(self):
        origin = os.path.normpath(os.getcwd() + self.origin_var.get()) + '/'
        source = os.path.normpath(os.getcwd() + self.source_var.get()) + '/'
        if os.path.isdir(origin) and os.path.isdir(source):
            self.destroy()
            app = SetupApp(self.parent, "resources/init.jpg", ParkingLot(), source, origin, self.stats_file)
        else:
            print "Invalid Directories"

    def start_monitor(self):
        origin = os.path.normpath(os.getcwd() + self.origin_var.get())
        source = os.path.normpath(os.getcwd() + self.source_var.get())
        print origin
        print source
        if os.path.isdir(origin) and os.path.isdir(source):
            self.destroy()
            app = MonitorApp(self.parent, "resources/init.jpg", ParkingLot(), source, origin, self.stats_file)
        else:
            print "Invalid Directories"

    def load_config(self, filepath='/resources/config.ini'):
        cwd = os.getcwd()
        path = os.path.normpath(os.getcwd()) + os.path.normpath(filepath)
        print path
        if not os.path.isfile(path):
            print "Creating Config File...",
            f = open(path, 'w')
            f.write('[Settings]\nimage_source : /resources/lot_source/\nimage_origin : /resources/lot_origin/\nstats_file : resources/lot_stats/\n')
            f.close()
            print 'Done.'
        configparser = ConfigParser.ConfigParser()
        configparser.read(path)

        image_source = configparser.get('Settings', 'image_source')
        image_origin = configparser.get('Settings', 'image_origin')
        stats_file = configparser.get('Settings', 'stats_file')

        return image_origin, image_source, stats_file


class SetupApp(tk.Frame):
    def __init__(self, parent, image_path, PKLot, img_src_dir, img_origin_dir, stats_file='resources/lot_stats/'):
        self.parent = parent
        self.parkinglot = PKLot
        self.cv2_img = cv2.imread(image_path)
        self.stats_file = stats_file

        tk.Frame.__init__(self, master=self.parent)

        self.winfo_toplevel().title('Setup')
        self.winfo_toplevel().configure(background='grey')

        self.canvas = ui.CanvasArea(self, self.parkinglot, self.cv2_img)
        self.canvas.grid(row=0, column=0, columnspan=10, sticky=tk.N)

        # Parking Spot List
        # currently an issue with scrolling on the list. it will scroll and then immediately be set back to to 0.
        self.parkingspot_listbox = ui.SpotList(self, self.parkinglot, width=20, height=34)
        self.parkingspot_listbox.grid(row=0, column=10, sticky='N')

        # MenuBar
        self.menubar = ui.MenuBar(self)
        self.parent.configure(menu=self.menubar)

        # ##Buttons
        # Image Processor/Parking lot update button
        tk.Grid.rowconfigure(self, 1, weight=1)
        self.lotupdate_button = tk.Button(self, text='Update Lot', command=self.update_lot)
        self.lotupdate_button.grid(row=1, column=10, sticky='EW')
        # delete spot button
        self.deleteSpotButton = tk.Button(self, text='Delete Selected', command=self.delete_selection)
        self.deleteSpotButton.grid(row=2, column=10, sticky='EW')
        # single image load Button
        self.loadImageButton = tk.Button(self, text="load image", command=self.manual_set_image)
        self.loadImageButton.grid(row=3, column=10, sticky='EW')
        # toggle update button
        self.toggleUpdateButton = tk.Button(self, text="toggle update", command=self.update_toggle)
        self.toggleUpdateButton.grid(row=4, column=10, sticky='EW')
        # ###

        # ##Labels
        self.occupied_label = tk.Label(self, text='Occupied')
        self.occupied_count_var = tk.StringVar()
        self.occupied_count_label = tk.Label(self, textvariable=self.occupied_count_var)

        self.occupied_label.grid(row=1, column=0, sticky='W')
        self.occupied_count_label.grid(row=1, column=1, sticky='W')

        self.vacant_label = tk.Label(self, text='Vacant')
        self.vacant_count_var = tk.StringVar()
        self.vacant_count_label = tk.Label(self, textvariable=self.vacant_count_var)

        self.vacant_label.grid(row=2, column=0, sticky='W')
        self.vacant_count_label.grid(row=2, column=1, sticky='W')

        self.status_label = tk.Label(self, text="Not Processing")
        self.status_label.grid(row=3, column=0, sticky='W')

        # bind events
        self.parent.bind('c', self.window_exit)

        self.pack()

        self.timestamp = time.time() - 20

        self.update_toggle_bool = False

        self.image_source_directory = img_src_dir
        self.img_origin_directory = img_origin_dir

        # image swapping thread setup
        t = threading.Thread(target=image_swapper, args=[self.img_origin_directory, self.image_source_directory])
        t.daemon = True
        t.start()

        self.update_all()  # this kicks off the main root calling updates ever 100 ms

    def manual_set_image(self, events=None):
        filename = tkFileDialog.askopenfilename(parent=self.parent)
        if filename is not None:
            try:
                self.parkinglot.currentLotImage = cv2.imread(filename)
                self.canvas.update_image(self.parkinglot.currentLotImage)
            except (SyntaxError, AttributeError) as e:
                print "Improper File"
                print filename
                pass
        else:
            pass

    def update_lot(self):
        # i realized that this is surrounded on all sides by dependencies. for now this function will not be used,
        # everything will be serial. (because it was so tied to everything else, speedup was barely there anyways)

        # currently switching back and forth between threading and not. currently not.
        #if threading.activeCount() > 3:
        #    print 'Warning: Images have not finished processing from the last iteration'
        #    print 'Active Threads: ' + str(threading.activeCount())
        #    pass
        #else:
        #    threading.Thread(target=self.parkinglot.update, args=[]).start()
        self.status_label.config(text="Processing")
        self.status_label.update_idletasks()
        self.parkinglot.update()
        self.status_label.config(text="Not Processing")

    def delete_selection(self):
        self.parkinglot.removeSpot(self.parkingspot_listbox.get_selection_id())

    def window_exit(self, event=None):
        self.parent.destroy()

    def return_roleselect(self):
        self.destroy()
        app=RoleSelect(self.parent)

    def update_toggle(self):
        self.update_toggle_bool = not self.update_toggle_bool
        if self.update_toggle_bool:
            self.toggleUpdateButton.config(bg='red')
            self.toggleUpdateButton.update_idletasks()
        else:
            self.toggleUpdateButton.config(bg='#D9D9D9')

    def update_current_image(self):
        # take the image, or the first, image from the image_source_directory.
        # currently going to try just deleting the image when done with it.

        # this function relies on something else in the background supplying images to the folder.

        image = os.listdir(self.image_source_directory)
        if image:
            image = image[0]
            self.parkinglot.currentLotImage = cv2.imread(self.image_source_directory + image)
            self.canvas.update_image(self.parkinglot.currentLotImage)
            os.remove(self.image_source_directory + image)
            print "Image " + image + " Removed"
            self.update_lot()

    def update_all(self, event=None):
        if time.time() - self.timestamp > 10 and self.update_toggle_bool:
            self.timestamp = time.time()
            self.update_current_image()
            self.update_lot()
            self.parkinglot.saveUsage(os.getcwd() + '/' + self.stats_file + self.parkinglot.name + '.txt')

        self.parkingspot_listbox.update_parkingspot_list()

        id_number = self.parkingspot_listbox.get_selection_id()
        try:  # try to set the highlighted spot, unless it doesnt exist
            self.canvas.highlightedSpot = self.parkinglot.getSingleSpot(id_number)
        except (IndexError, AttributeError) as e:
            pass

        self.vacant_count_var.set(len(self.parkinglot.getEmpty()))
        self.occupied_count_var.set(len(self.parkinglot.getOccupied()))

        self.canvas.update_all()
        self.parent.after(100, self.update_all)


class MonitorApp(SetupApp):
    # since this is just a version of SetupApp with functionality removed, then it can just inherit directly from it ez.
    def __init__(self, parent, image_path, PKLot, img_src_dir, img_origin_dir, stats_file='/resources/lot_stats/'):
        SetupApp.__init__(self, parent, image_path, PKLot, img_src_dir, img_origin_dir, stats_file='/resources/lot_stats/')

        # remove the ability for users to draw things in monitor mode
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

        # remove delete button
        self.deleteSpotButton.grid_forget()
        # remove save lot menu item
        self.menubar.delete(2)


def image_swapper(source_directory, populate_directory):
    # Meant to run in separate thread. DO NOT run in main thread.
    time.sleep(1)
    while True:
        population_images = os.listdir(populate_directory)
        if not population_images:
            options = os.listdir(source_directory)
            choice = random.choice(options)
            shutil.copy(source_directory + choice, populate_directory + choice)
        time.sleep(10)


if __name__ == "__main__":
    try:
        import caffe
    except ImportError:
        print "Warning: Could not locate installed Caffe, images will not be analyzed."

    root = tk.Tk()
    tk.Grid.columnconfigure(root, 0, weight=1)
    root.resizable(0, 0)

    app = RoleSelect(root)

    root.mainloop()
