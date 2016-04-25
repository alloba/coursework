import random
import itertools
import csv


class Gridworld:
    def __init__(self, size=20, goal=None, obstacles=[]):
        self.size = size
        self.obstacles = obstacles

        if goal is None:
            self.goal = [random.randint(0, size-1), random.randint(0, size-1)]
        else:
            self.goal = goal

        self.Q = {x: [(random.random()-.5)/1 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}
        self.e = {x: [0 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}

        self.rewards = {x: 0.0 for x in itertools.product(range(self.size), repeat=2)}
        for wall in obstacles:
            self.rewards[wall] = -1

    def get_reward(self, position):
        if tuple(position) not in self.rewards:
            return -1
        else:
            return self.rewards[tuple(position)]

    def reset_e(self):
        self.e = {x: [0 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}

    def reset_q(self):
        self.Q = {x: [(random.random()-0.5)/10 for y in range(4)] for x in itertools.product(range(self.size), repeat=2)}

    pass


class SARSA:
    def __init__(self, gridworld, alpha, gamma, lamb, epsilon):
        self.gridworld = gridworld
        self.alpha = alpha
        self.gamma = gamma
        self.lamb = lamb
        self.epsilon = epsilon

    def episode(self, count):
        # repeat for each step of episode until state is terminal
        # meaning in bounds, not on the goal, and not hitting an obstacle
        # also within running bounds, which are yet to be set

        for i in range(count):
            num = 0
            #initialize state and action
            state = (random.randint(0, self.gridworld.size - 1), random.randint(0, self.gridworld.size - 1))
            action = self.get_action(state)
            while (state in self.gridworld.Q) and (state is not self.gridworld.goal) and (state not in self.gridworld.obstacles):
                state, action = self.episode_step(state, action)

    def episode_step(self, state, action):
        self.gridworld.reset_e()
        state_prime = self.take_action(state, action)
        if state_prime not in self.gridworld.Q:
            return (-1, -1), -1

        reward = self.gridworld.get_reward(state_prime)
        action_prime = self.get_action(state_prime)

        derivate = reward + self.gamma * self.get_q_val(state_prime, action_prime) - self.get_q_val(state, action)

        self.gridworld.e[state][action] += 1

        for coord in self.gridworld.Q:
            for i in range(4):
                self.gridworld.Q[coord][i] += self.alpha * derivate * self.gridworld.e[coord][i]
                self.gridworld.e[coord][i] = self.gridworld.e[coord][i] * self.gamma * self.lamb

        state = state_prime
        action = action_prime

        return state, action

    def get_action(self, state):

        if random.random() < self.gamma:
            return random.randint(0, 3)
        else:
            return self.gridworld.Q[state].index(max(self.gridworld.Q[state]))
        pass

    def take_action(self, position, move):
        if move % 2 == 0:
            new_position = (position[0] - 1, position[1])
        else:
            new_position = (position[0], position[1] - 1)
        return new_position

    def get_q_val(self, state, action):
        if state in self.gridworld.Q:
            return self.gridworld.Q[state][action]
        else:
            return -10


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
    c = Gridworld(obstacles=[(7, 3), (1,1)])
    sarsa = SARSA(c, .5, .5, .5, .5)
    sarsa.episode(2)

    save_csv(c, 'test.csv')
    grid = open_csv('test.csv')
    sarsa = SARSA(grid, .9, .9, .9, .9)
    sarsa.episode(2)

    while True:
        print(
            grid.Q[(10,10)].index(
                max(grid.Q[(10,10)])
            )
        )
        print(grid.Q[(10,10)])

        sarsa.episode(100)

