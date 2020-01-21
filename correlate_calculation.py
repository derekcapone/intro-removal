import numpy as np

def correlate(arr1, arr2):
    return np.correlate(arr1, arr2, "same")

if __name__ == "__main__":
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([0, 1, 0.5])

    corr = correlate(arr1, arr2)

    
