import math
import numpy as np
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def liner(x):
    return x
def tanh(x):
    return math.tanh(x)
def ReLU(x):
    if x<0:
        return 0
    else:
        return x
def sig10(x):
    return 1 / (1 + np.exp(-x*0.1))
def tanh10(x):
    return math.tanh(x*0.1)