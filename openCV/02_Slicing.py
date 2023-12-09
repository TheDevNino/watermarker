import numpy as np

# Creating a 1-dimensional array
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# Slicing: [start:stop]
subset = arr[2:7]
print(subset)
# Output: [2 3 4 5 6]

# Slicing with a step: [start:stop:step]
subset_step = arr[1:9:2]
print(subset_step)
# Output: [1 3 5 7]

# Omitting start or stop indices
subset_omit_start = arr[:5]
subset_omit_stop = arr[5:]
print(subset_omit_start)
# Output: [0 1 2 3 4]
print(subset_omit_stop)
# Output: [5 6 7 8 9]

# Negative indices
subset_negative = arr[-4:-1]
print(subset_negative)
# Output: [6 7 8]

# 2-dimensional array
arr_2d = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Slicing rows and columns
row_slice = arr_2d[0:2, :]
col_slice = arr_2d[:, 1:3]

print(row_slice)
# Output:
# [[1 2 3]
#  [4 5 6]]

print(col_slice)
# Output:
# [[2 3]
#  [5 6]
#  [8 9]]
