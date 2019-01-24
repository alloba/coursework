import random
import re


class Markov:
    def __init__(self, filelocation, order=2):
        self.order = order
        self.text = open(filelocation, 'r').read().split()
        self.text += self.text
        self.graph = {}

    def generate(self):
        for i in range(len(self.text)):
            if i == len(self.text) - self.order:
                break

            key = ''
            for j in range(self.order):
                key += self.text[i + j] + ' '
            key = key[:-1]
            if key not in self.graph:
                self.graph[key] = []
            self.graph[key].append(self.text[i + self.order])

    def grabWord(self, inputkey):
        try:
            return random.choice(self.graph[inputkey])
        except KeyError:
            print('no key found: ' + inputkey)
            return 'err'

    def grabWords(self, startingkey, numwords):
        sentence = []
        operatingkey = startingkey
        while len(sentence) < self.order:
            sentence.append(self.grabWord(operatingkey))
            operatingkey = ' '.join(operatingkey.split(' ')[1:]) + ' ' + sentence[-1]

            # if the order is 1, there will be an extra whitespace at the beginning. this is to address the issue.
            if operatingkey[0] == ' ':
                operatingkey = operatingkey[1:]
            numwords -= 1

        while numwords > 0:
            newword = self.grabWord(operatingkey)
            sentence.append(newword)
            oplist = operatingkey.split(' ')[1:]
            oplist.append(newword)
            operatingkey = ' '.join(oplist)
            numwords -= 1
        return sentence

    def grabStartingPhrase(self):
        return random.choice(list(self.graph.keys()))


def splitsentences(wordlist):
    # split based on existence of punctuation
    # get rid of the first entry, since it is pretty much never going to be formatted correctly
    return re.findall(r"(.*?[.!?])", ' '.join(wordlist))[1:]


markov = Markov('C:/Projects/MarkovPython/big.txt', 2)
markov.generate()


for s in splitsentences(markov.grabWords(markov.grabStartingPhrase(), 200)):
    print(s)
