import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from tslearn.barycenters import euclidean_barycenter, dtw_barycenter_averaging, softdtw_barycenter
from tslearn.datasets import CachedDatasets


def amplitude_avg(class_x):
    class_avg = [list() for i in range(len(class_x))]
    for c in range(len(class_x)):
        class_avg[c] = np.array(class_x[c]).mean(axis=0)
    class_avg = np.array(class_avg)
    return class_avg


def dtw_avg(class_x):
    class_avg = [list() for i in range(len(class_x))]
    for c in range(len(class_x)):
        class_avg[c] = dtw_barycenter_averaging(class_x[c], max_iter=100)
    class_avg = np.array(class_avg)
    return class_avg


def soft_dtw_avg(class_x):
    class_avg = [list() for i in range(len(class_x))]
    for c in range(len(class_x)):
        class_avg[c] = softdtw_barycenter(class_x[c], gamma=1., max_iter=100)
    class_avg = np.array(class_avg)
    return class_avg
