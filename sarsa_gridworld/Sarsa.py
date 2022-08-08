import random
import itertools
import csv

import math


class Gridworld:
    def __init__(self, size=20, goal=None, obstacles=[]):
        self.size = size
        # obstacle input should be a list of tuples for coordinates of walls
        self.obstacles = obstacles

        if goal is None:
            self.goal = (random.randint(0, size-1), random.randint(0, size-1))
        else:
            self.goal = goal

        self.Q = {x: [(random.random()-.5)/10 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}
        self.e = {x: [0 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}

        self.rewards = {x: 0.0 for x in itertools.product(range(self.size), repeat=2)}
        for wall in obstacles:
            self.rewards[wall] = -1
        self.rewards[self.goal] = 1


        self.Q[(-1,-1)] = [.01,.01,.01,.01]
        self.rewards[(-1,-1)] = -1

    def get_reward(self, position):
        if tuple(position) not in self.rewards:
            return -1
        else:
            return self.rewards[tuple(position)]

    def reset_e(self):
        self.e = {x: [0 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}
        self.e[(-1,-1)] = [0,0,0,0]

    def reset_q(self):
        self.Q = {x: [(random.random()-0.5)/10 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}
        self.Q[(-1,-1)] = [.01,.01,.01,.01]

    pass


class SARSA:
    def __init__(self, gridworld, alpha, epsilon, gamma, lamb):
        self.gridworld = gridworld
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.lamb = lamb

        self.greed_decay = .0004 # increases epsilon by ___ ever 200 iterations. which may or may not be a good value

        self.episode_count = 0  # for use in recording things. keep track of the number of times it's ran total.
        self.successful_trail_lengths = []  # for use in finding average path length. not used for much, but nice to see

    def episode(self):
        # goes through the algorithm until either the goal or a wall is hit.
        # if it successfully navigates a path to the goal, will return a list of visited locations.
        # otherwise nothing is returned, although the algorithm still plays out the same.

        self.gridworld.reset_e()

        state = (random.randint(0, self.gridworld.size-1), random.randint(0, self.gridworld.size-1))
        #state = (0, 0)
        action = self.get_action(state)

        self.episode_count += 1

        visited_list = [state]

        reward = self.gridworld.get_reward(state)
        while reward is not 1 and reward is not -1:
            # the reward being not 0 is indicative of a terminal state. pretty much keep doing this until the path ends,
            # one way or the other.
            # from here on out it's straight up just follow the algorithm that was provided.
            state_prime = self.take_action(state, action)

            reward = self.gridworld.get_reward(state_prime)
            action_prime = self.get_action(state_prime)

            if len(visited_list) > 400:
                # terminated paths that were stuck. removed from the final version.
                #reward = -1
                #print("broken")
                pass


            derivate = reward + self.gamma * self.gridworld.Q[state_prime][action_prime] - self.gridworld.Q[state][action]
            self.gridworld.e[state][action] += 1

            for s in self.gridworld.Q:
                for a in range(4):
                    self.gridworld.Q[s][a] += self.alpha * self.gridworld.e[s][a] * derivate
                    self.gridworld.e[s][a] *= self.lamb * self.gamma


            action = action_prime
            state = state_prime
            visited_list.append(state)
        # slowly increase the greed of the algorithm. early exploration, late exploitation.
        # no idea what a good number for the cap or increase is though, mostly guessing.
        if self.epsilon < .90:
            self.epsilon += self.greed_decay

        # for the sake of recording results for a report
        if self.episode_count % 200 == 0:
            print("Total number of episodes: " + str(self.episode_count))
            print("Percentage of hits over the last 200 episodes: " + str(len(self.successful_trail_lengths) / 200 * 100) + "%")
            try:
                print("Average length of successful paths: " + str(sum(self.successful_trail_lengths) / len(self.successful_trail_lengths)))
            except ZeroDivisionError:
                print("Average length of successful paths: " + str(0))
            print(self.epsilon)
            print("_____________________________________________________\n")
            self.successful_trail_lengths = []

        # returning this list is pretty much just for the use of the GUI. I wanted to be able to show successful paths.
        if state == self.gridworld.goal:
            self.successful_trail_lengths.append(len(visited_list))
            return visited_list

    def get_action(self, state):
        if random.random() > self.epsilon:  # for some reason choosing < or > messed with my brain so much here.
            return random.randint(0, 3)
        else:
            return self.gridworld.Q[state].index(max(self.gridworld.Q[state]))

    def take_action(self, position, move):
        # this assumes that actions are represented in the order of left, right, up, down
        # this allows for easy math to figure out how to shift coordinates based on the index of the highest value found
        if move % 2 == 0:
            new_state = (position[0] + (move-1), position[1])
        else:
            new_state = (position[0], position[1] + (move-2))

        if new_state[0] < 0 or new_state[0] > self.gridworld.size - 1 or new_state[1] < 0 or new_state[1] > self.gridworld.size - 1:
            return (-1, -1)

        return new_state

# save and write to a file. for use in the GUI bit of the program, it is always saved under "gridworld.csv"
# looks a mess inside the file itself, but it works out pretty well.
def save_csv(gridworld, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(str(gridworld.size))

        writer.writerow(gridworld.obstacles)

        writer.writerow(gridworld.goal)

        writer.writerow(str(len(gridworld.rewards)))

        for val in gridworld.rewards:
            writer.writerow(str(val) + ':' + str(gridworld.rewards[val]))

        for val in gridworld.Q:
            writer.writerow(str(val) + ':' + str(gridworld.Q[val]))


def open_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar = '|')
        q = {}
        r = {}
        size = next(reader)
        size = int(''.join(size))

        obstacles = next(reader)
        for i in range(len(obstacles)):
            obstacles[i] = eval(obstacles[i])

        goal = next(reader)
        goal[0] = int(goal[1])
        goal[1] = int(goal[1])
        goal = tuple(goal)

        i = int(''.join(next(reader)))
        for x in range(i):
            val = ''.join(next(reader)).split(':')
            r[eval(val[0])] = eval(val[1])

        for row in reader:
            val = ''.join(row).split(':')
            q[eval(val[0])] = eval(val[1])

        gridworld = Gridworld(size, goal, obstacles)
        gridworld.Q = q
        return gridworld

if __name__ == "__main__":
    gridworld = Gridworld(obstacles=[(5, 6), (5, 7), (5, 8), (5, 9),
                                           (12, 10), (12, 9), (12, 8), (12, 11),
                                           (13, 9), (14, 9),
                                           (8, 13), (9, 13), (7, 13),
                                           (8, 5), (9, 5), (10, 5), (11, 5),
                                           (2, 17), (17, 17), (19, 16), (18, 1)],
                                goal=(10, 10))
    sarsa = SARSA(gridworld=gridworld, alpha=.5, gamma=.5, epsilon=0.50, lamb=.5)

    for i in range(100000):
        #print(i)
        sarsa.episode()
    save_csv(gridworld, 'gridworld_half_everything.csv')

