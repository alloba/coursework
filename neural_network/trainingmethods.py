import pickle, copy, random
from Network import Network


def import_data(training_data, testing_data):
    f = open(testing_data, 'r')
    test_list = []
    for line in f:
        if len(line.strip()) == 0:
            pass
        else:
            a = [int(i) for i in line.split(',')]
            test_list.append(a)

    f = open(training_data, 'r')
    train_list = []
    for line in f:
        if len(line.strip()) == 0:
            pass
        else:
            a = [int(i) for i in line.split(',')]
            train_list.append(a)

    return train_list, test_list


def get_value(data):
    return data[-1]


def convert_to_output_list(output):
    ret = []
    for i in range(10):
        if i == output:
            ret.append(1)
        else:
            ret.append(0)
    return ret


def convert_to_answer(output_list):
    most_confident = -1
    amount = 0.0
    for i in range(len(output_list)):
        if output_list[i] > amount:
            most_confident = i
            amount = output_list[i]
    return most_confident


def accuracy(net, test_data):
    total = len(test_data)
    result_list = []
    for i in test_data:
        out = net.getoutput(i[:-1])
        expected = i[-1]
        if expected == convert_to_answer(out):
            result_list.append(1)
        else:
            result_list.append(0)
    return sum(result_list) / total


def start_new(dimensions, learning_rate):
    n = Network(dimensions, learning_rate)

    current_accuracy = accuracy(n, test)
    best_accuracy = 0.0
    best_net = copy.deepcopy(n)

    for j in range(800):
        if j % 2 == 0:
            new_accuracy = accuracy(n, test)
            print(str(j) + ": " + str(new_accuracy))

            diff = abs(current_accuracy - new_accuracy) / (current_accuracy + new_accuracy) * 100
            if diff < 0.01:
                n.learning_rate = l_rate * 2
            else:
                n.learning_rate = l_rate

            if new_accuracy > best_accuracy:
                best_accuracy = new_accuracy
                best_net = copy.deepcopy(n)

            current_accuracy = new_accuracy

        for i in range(len(train)):
            n.cycle(train[i][:-1], convert_to_output_list(train[i][-1]))

    pickle.dump(best_net, open('best_net.p', 'wb'))


def work_on_existing_net(net, learning_rate):
    n = net
    n.learning_rate = learning_rate

    best_net = copy.deepcopy(net)
    best_accuracy = accuracy(net, test)

    current_accuracy = accuracy(n, test)

    for j in range(50):
        fails_in_a_row = 0

        if j % 2 == 0:
            new_accuracy = accuracy(n, test)
            print(str(j) + ": " + str(new_accuracy))

            if new_accuracy > best_accuracy:
                best_accuracy = new_accuracy
                best_net = copy.deepcopy(n)
                fails_in_a_row = 0
            else:
                fails_in_a_row += 1

            if fails_in_a_row > 10:
                break
            print(fails_in_a_row)

            current_accuracy = new_accuracy

        #random.shuffle(test)
        for i in range(len(train)):
            n.cycle(train[i][:-1], convert_to_output_list(train[i][-1]))

    pickle.dump(best_net, open('best_net.p', 'wb'))

random.seed(0)
train, test = import_data('optdigits_train.txt', 'optdigits_test.txt')
l_rate = 3.0

net = pickle.load(open('best_net.p', 'rb'))
#net = Network([64,40,10], 4)
#start_new([64, 40, 10], 4)
#work_on_existing_net(net, 0.4)

print(accuracy(net, test))
print(accuracy(net, train))
print()
