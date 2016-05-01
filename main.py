import tkinter
import tkinter.filedialog

import Sarsa


class TKApp:
    def __init__(self, window, gridworld, sarsa):

        # main window setup
        # mostly menu bar stuff
        self.window = window
        window.title("Project 3")
        window.configure(background='grey')
        menubar = tkinter.Menu(window)
        menubar.add_command(label="Open File", command=self.open_file)
        menubar.add_command(label='Reset Q Table', command=self.reset_q)
        menubar.add_command(label='Save Gridworld', command=self.save_gridworld)
        menubar.add_command(label='Update Toggle', command=self.update_canvas_toggle)
        window.configure(menu=menubar)

        # display canvas setup
        self.canvas = tkinter.Canvas(window, width=800, height=800, bg='white')
        self.canvas.pack()

        # class variables that dont bind so neatly to tkinter modules
        self.update_switch = False
        self.gridworld = gridworld
        self.sarsa = sarsa
        self.previous_visited = []

        self.box_list = []
        for i in range(20):
            for j in reversed(range(20)):
                self.box_list.append(self.canvas.create_rectangle(i * 40, j * 40, i * 40 + 40, j * 40 + 40, fill='red'))
        for box in self.box_list:
            self.canvas.itemconfig(box, fill='white')

        # i feel like there should be a nice way to combine this with box_list, since they are really the same thing
        # with different content, but i couldn't find a way to do it really online.
        self.arrow_list = []
        for i in range(20):
            for j in reversed(range(20)):
                self.arrow_list.append(self.canvas.create_text(i * 40 + 20, j * 40 + 20))
        for arrow in self.arrow_list:
            self.canvas.itemconfig(arrow, text='b')

    def display(self):
        # aka the slowest part of the program and the reason for much sadness
        for i in range(20):
            for j in reversed(range(20)):
                # for the sake of trying to speed up canvas draws,
                # this compares the text at every position and only changes it if needed.
                # not sure how much time this actually saves, but at least i tried.

                value = max(self.gridworld.Q[(i, j)])
                index = self.gridworld.Q[(i, j)].index(value)
                draw_value = ''
                if index == 0:
                    draw_value = '<'
                elif index == 1:
                    draw_value = 'v'
                elif index == 2:
                    draw_value = '>'
                elif index == 3:
                    draw_value = '^'
                if draw_value is not self.canvas.itemcget(self.arrow_list[i * 20 + j], 'text'):
                    self.canvas.itemconfig(self.arrow_list[i * 20 + j], text=draw_value)

        visited_list = self.sarsa.episode()
        if visited_list:
            cval = 640
            # fill in previous colored cells with white so the entire thing doesnt fill up with previous paths
            if self.previous_visited:
                for val in self.previous_visited:
                    position = val[0] * 20 + val[1]
                    self.canvas.itemconfig(self.box_list[position], fill='white')
            self.previous_visited = visited_list
            # mark the path taken to the goal in (poorly varying) colors
            for cell in visited_list:
                if cell != (-1, -1):
                    color = "#%02d%02d%02d" % (100, max(cval, 200), max(cval, 200))
                    position = cell[0] * 20 + cell[1]
                    self.canvas.itemconfig(self.box_list[position], fill=color)
                    cval -= 5
            position = visited_list[0][0] * 20 + visited_list[0][1]
            color = "#%02d%02d%02d" % (255, 500, 255)
            self.canvas.itemconfig(self.box_list[position], fill=color)

        goal = self.gridworld.goal
        self.canvas.itemconfig(self.box_list[goal[0] * 20 + goal[1]], fill='gold')

        obstacles = [key for key in self.gridworld.obstacles]
        for item in obstacles:
            self.canvas.itemconfig(self.box_list[item[0] * 20 + item[1]], fill='lime')

        if self.update_switch:
            self.window.after(5, self.display)

    def reset_q(self):
        # not exactly the ideal total reset, but it works.
        # really the main problem is that it doesnt allow you to change the initial conditions as a user.
        # it relies on good values from the outset of the program running
        self.gridworld.reset_q()
        self.sarsa.gridworld = self.gridworld
        self.sarsa.epsilon = .1

        self.display()

    def update_canvas_toggle(self):
        self.update_switch = not self.update_switch
        if self.update_switch:
            self.window.after(5, self.display)

    def save_gridworld(self):
        Sarsa.save_csv(self.gridworld, 'gridworld.csv')

    def open_file(self):
        filename = tkinter.filedialog.askopenfilename(parent=self.window)

        try:
            self.gridworld = Sarsa.open_csv(filename)
            self.sarsa.gridworld = self.gridworld

        except SyntaxError as e:
            print("Improperly Formatted CSV File")

        self.sarsa.epsilon = 1.0
        self.sarsa.episode_count = 0
        self.display()


if __name__ == '__main__':
    gridworld = Sarsa.Gridworld(obstacles=[(5, 6), (5, 7), (5, 8), (5, 9),
                                           (12, 10), (12, 9), (12, 11),
                                           (13, 9), (14, 9),
                                           (8, 13), (9, 13), (7, 13),
                                           (8, 5), (9, 5), (10, 5), (11, 5),
                                           (2, 17), (17, 17), (19, 16), (18, 1)],
                                goal=(10, 10))
    sarsa = Sarsa.SARSA(gridworld=gridworld, alpha=.1, gamma=.9, epsilon=.4, lamb=.5)

    root = tkinter.Tk()
    app = TKApp(root, gridworld, sarsa)

    root.mainloop()
