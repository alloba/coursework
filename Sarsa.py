import random
import itertools
import csv

import time

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

        self.greed_decay = .001

    def episode(self):
        self.gridworld.reset_e()
        state = (random.randint(0, self.gridworld.size-1), random.randint(0, self.gridworld.size-1))
        action = self.get_action(state)

        visited_list = [state]

        reward = self.gridworld.get_reward(state)
        while reward is not 1 and reward is not -1:
            state_prime = self.take_action(state, action)

            #if state_prime == state:
            #    #if a wall is hit, do this code or reward wont send back right
            #    reward = -1
            #    self.gridworld.e[state][action] += 1
            #    derivate = reward + self.gamma * self.gridworld.Q[state_prime][action]
            #    for s in self.gridworld.Q:
            #        for a in range(4):
            #            self.gridworld.Q[s][a] += self.alpha * self.gridworld.e[s][a] * derivate
            #            self.gridworld.e[s][a] *= self.lamb * self.gamma
            #            if math.isnan(self.gridworld.Q[s][a]):
            #                print("nan")
            #    break
            ####

            reward = self.gridworld.get_reward(state_prime)
            action_prime = self.get_action(state_prime)

            derivate = reward + self.gamma * self.gridworld.Q[state_prime][action_prime] - self.gridworld.Q[state][action]
            self.gridworld.e[state][action] += 1

            for s in self.gridworld.Q:
                for a in range(4):
                    self.gridworld.Q[s][a] += self.alpha * self.gridworld.e[s][a] * derivate
                    self.gridworld.e[s][a] *= self.lamb * self.gamma
                    if math.isnan(self.gridworld.Q[s][a]):
                        print("nan")

            action = action_prime
            state = state_prime
            visited_list.append(state)

        if self.epsilon < .95:
            self.epsilon *= 1+self.greed_decay


        if state == self.gridworld.goal:
            return visited_list

    def get_action(self, state):
        if random.random() > self.epsilon:
            return random.randint(0, 3)
        else:
            return self.gridworld.Q[state].index(max(self.gridworld.Q[state]))

    def take_action(self, position, move):

        if move % 2 == 0:
            new_state = (position[0] + (move-1), position[1])
        else:
            new_state = (position[0], position[1] + (move-2))

        if new_state[0] < 0 or new_state[0] > self.gridworld.size - 1 or new_state[1] < 0 or new_state[1] > self.gridworld.size - 1:
            return (-1, -1)

        return new_state


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
    c = Gridworld(obstacles=[(7, 3)], goal=(10, 10))
    sarsa = SARSA(gridworld=c, alpha=.9, epsilon=.9, gamma=.9, lamb=.9)

    for i in range(100):
        print(i)
        sarsa.episode()
        #time.sleep(0.001)


