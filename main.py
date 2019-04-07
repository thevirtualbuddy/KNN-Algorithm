from csv import reader
from sys import exit
from math import sqrt
from operator import itemgetter


def load_data_set(filename):
    try:
        with open(filename, newline='') as diabetes:
            return list(reader(diabetes, delimiter=','))
    except FileNotFoundError as e:
        raise e


def convert_to_float(data_set, mode):
    new_set = []
    try:
        if mode == 'training':
            for data in data_set:
                new_set.append([float(x) for x in data[:len(data)-1]] + [data[len(data)-1]])

        elif mode == 'test':
            for data in data_set:
                new_set.append([float(x) for x in data])

        else:
            print('Invalid mode, program will exit.')
            exit()

        return new_set

    except ValueError as v:
        print(v)
        print('Invalid data set format, program will exit.')
        exit()


def get_classes(training_set):
    return list(set([c[-1] for c in training_set]))


def find_neighbors(distances, k):
    return distances[0:k]


def find_response(neighbors, classes):
    votes = [0] * len(classes)

    for instance in neighbors:
        for ctr, c in enumerate(classes):
            if instance[-2] == c:
                votes[ctr] += 1

    return max(enumerate(votes), key=itemgetter(1))


def knn(training_set, test_set, k):
    distances = []
    dist = 0
    limit = len(training_set[0]) - 1
    res = []
    inp = []
    fxx = []
    vote = []
    # generate response classes from training data
    classes = get_classes(training_set)

    try:
        for test_instance in test_set:
            for row in training_set:
                for x, y in zip(row[:limit], test_instance):
                    dist += (x-y) * (x-y)
                distances.append(row + [sqrt(dist)])
                dist = 0

            distances.sort(key=itemgetter(len(distances[0])-1))

            # find k nearest neighbors
            neighbors = find_neighbors(distances, k)

            # get the class with maximum votes
            index, value = find_response(neighbors, classes)

            # Display prediction

            res.append(classes[index])
            inp.append(test_instance)
            vote.append(value)

            # empty the distance list
            distances.clear()
        z = 0

        headline = ['Samp','Preg','Gluc','Blod','Skin','Insu','BMI','Diab','Age','Res','Vote']
        for n in headline:
            print(n, '\t',end='')

        print('\n')
        for x in inp:
            print(z,'\t',end='')
            for v in x:
                print(v, '\t',end='')
            print(res[z],'\t',end='')
            print(vote[z],'/',k)
            z = z+1
            print('\n')

    except Exception as e:
        print(e)



def main():
    try:
        # get value of k
        k = int(input('Enter the value of k : '))

        # load the training and test data set
        training_file = input('Enter name of training data file : ')
        test_file = input('Enter name of test data file : ')
        training_set = convert_to_float(load_data_set(training_file), 'training')
        test_set = convert_to_float(load_data_set(test_file), 'test')

        if not training_set:
            print('Empty training set')

        elif not test_set:
            print('Empty test set')

        elif k > len(training_set):
            print('Expected number of neighbors is higher than number of training data instances')

        else:
            knn(training_set, test_set, k)

    except ValueError as v:
        print(v)

    except FileNotFoundError:
        print('File not found')


if __name__ == '__main__':
    main()
