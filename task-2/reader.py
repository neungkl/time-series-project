import numpy as np


def get_x_label(file_name):
    data = open('../data/' + file_name, 'r')
    x = list()
    label = list()
    
    # Read data
    for i, line in enumerate(data): 
        array = line.split()
        label.append(int(float(array[0])))
        x.append(np.array(array[1:]).astype(float))

    label = np.array(label).reshape((len(label)))
    x = np.array(x).reshape((len(x), x[0].shape[0]))
    return x, label


def get_class_x(train_file_name):
    train_data = open('../data/' + train_file_name, 'r')
    train_x = list()
    train_label = list()
    
    # Read data
    for i, line in enumerate(train_data): 
        array = line.split()
        train_label.append(int(float(array[0])))
        train_x.append(np.array(array[1:]).astype(float))

    train_label = np.array(train_label).reshape((len(train_label)))
    train_x = np.array(train_x).reshape((len(train_x), train_x[0].shape[0]))

    # Collect data in class
    classes = np.unique(train_label)
    class_x = [list() for i in classes]
    for i in range(train_label.shape[0]):
        class_x[train_label[i]-1].append(np.array(train_x[i]))
    class_x = np.array(class_x)
    return class_x