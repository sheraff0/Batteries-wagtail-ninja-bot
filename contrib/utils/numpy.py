import numpy as np


def array_from_dict(dict_):
    return np.array([x or 0 for x in dict_.values()])
