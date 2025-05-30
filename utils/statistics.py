import numpy as np

from utils.ADRS import ADRS
from utils.paretoComparer import ParetoComparer

def geometric_mean(iterable: list):
    a = np.array(iterable)
    # remove None values
    filtered_array = a[a != None]
    for i in range(len(filtered_array)):
        #add a little e value to all elements of array
        e = 0.1
        if filtered_array[i]:
            filtered_array[i] += e

    return filtered_array.prod() ** (1.0 / len(filtered_array))

def arithmetic_mean_adrs(reference_set, timestamps, comparer=None):
    if not comparer:
        comparer = ADRS('resources', 'latency')

    all_best_adrs = [comparer.compare(reference_set, timestamp) for timestamp in timestamps]
    filtered = [adrs for adrs in all_best_adrs if adrs is not None]
    return np.mean(filtered) if filtered else None

def arithmetic_mean_percentage(solutions1, solutions2, comparer=None):
    if not comparer:
        comparer = ParetoComparer('resources', 'latency')

    all_best_percentage = [comparer.compare(s1, s2) for s1, s2 in zip(solutions1, solutions2)]
    filtered = [p for p in all_best_percentage if p is not None]
    return np.mean(filtered)