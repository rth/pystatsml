'''
Numpy: arrays and matrices
==========================

NumPy is an extension to the Python programming language, adding support for large, multi-dimensional (numerical) arrays and matrices, along with a large library of high-level mathematical functions to operate on these arrays.

**Sources**:

- Kevin Markham: https://github.com/justmarkham
'''

from __future__ import print_function
import numpy as np

'''
Create arrays
-------------
'''

# create ndarrays from lists
# note: every element must be the same type (will be converted if possible)
data1 = [1, 2, 3, 4, 5]             # list
arr1 = np.array(data1)              # 1d array
data2 = [range(1, 5), range(5, 9)]  # list of lists
arr2 = np.array(data2)              # 2d array
arr2.tolist()                       # convert array back to list

# examining arrays
arr1.dtype      # float64
arr2.dtype      # int32
arr2.ndim       # 2
arr2.shape      # (2, 4) - axis 0 is rows, axis 1 is columns
arr2.size       # 8 - total number of elements
len(arr2)       # 2 - size of first dimension (aka axis)

# create special arrays
np.zeros(10)
np.zeros((3, 6))
np.ones(10)
np.linspace(0, 1, 5)            # 0 to 1 (inclusive) with 5 points
np.logspace(0, 3, 4)            # 10^0 to 10^3 (inclusive) with 4 points

# arange is like range, except it returns an array (not a list)
int_array = np.arange(5)
float_array = int_array.astype(float)


'''
Reshaping
---------
'''

matrix = np.arange(10, dtype=float).reshape((2, 5))
print(matrix.shape)
print(matrix.reshape(5, 2))

# Add an axis
a = np.array([0, 1])
a_col = a[:, np.newaxis]
# array([[0],
#       [1]])

# Transpose
a_col.T
#array([[0, 1]])

'''
Stack arrays
------------

Stack flat arrays in columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
a = np.array([0, 1])
b = np.array([2, 3])

np.stack((a, b)).T
# [[0 2]
# [1 3]]

# or
np.hstack((a[:, None], b[:, None]))
# array([[0, 2],
#       [1, 3]])

'''
Selection
---------

Single item
~~~~~~~~~~~
'''

arr1[0]         # 0th element (slices like a list)
arr2[0, 3]      # row 0, column 3: returns 4
arr2[0][3]      # alternative syntax

'''
Slicing
~~~~~~~
'''

arr2[0, :]      # row 0: returns 1d array ([1, 2, 3, 4])
arr2[:, 0]      # column 0: returns 1d array ([1, 5])
arr2[:, :2]     # columns strictly before index 2 (2 first columns)
arr2[:, 2:]     # columns after index 2 included
arr2[:, 1:4]    # columns between index 1 (included) and 4 (exluded)

'''
Views and copies
~~~~~~~~~~~~~~~~
'''

arr = np.arange(10)
arr[5:8]                    # returns [5, 6, 7]
arr[5:8] = 12               # all three values are overwritten (would give error on a list)
arr_view = arr[5:8]         # creates a "view" on arr, not a copy
arr_view[:] = 13            # modifies arr_view AND arr
arr_copy = arr[5:8].copy()  # makes a copy instead
arr_copy[:] = 14            # only modifies arr_copy

'''
using boolean arrays
~~~~~~~~~~~~~~~~~~~~
'''

arr[arr > 5]

'''
Boolean selection return a view wich authorizes the modification of the
original array
'''

arr[arr > 5] = 0
print(arr)


names = np.array(['Bob', 'Joe', 'Will', 'Bob'])
names == 'Bob'                          # returns a boolean array
names[names != 'Bob']                   # logical selection
(names == 'Bob') | (names == 'Will')    # keywords "and/or" don't work with boolean arrays
names[names != 'Bob'] = 'Joe'           # assign based on a logical selection
np.unique(names)                        # set function

'''
Vectorized operations
---------------------
'''

nums = np.arange(5)
nums * 10                           # multiply each element by 10
nums = np.sqrt(nums)                # square root of each element
np.ceil(nums)                       # also floor, rint (round to nearest int)
np.isnan(nums)                      # checks for NaN
nums + np.arange(5)                 # add element-wise
np.maximum(nums, np.array([1, -2, 3, -4, 5]))  # compare element-wise

# Compute Euclidean distance between 2 vectors
vec1 = np.random.randn(10)
vec2 = np.random.randn(10)
dist = np.sqrt(np.sum((vec1 - vec2) ** 2))

# math and stats
rnd = np.random.randn(4, 2) # random normals in 4x2 array
rnd.mean()
rnd.std()
rnd.argmin()                # index of minimum element
rnd.sum()
rnd.sum(axis=0)             # sum of columns
rnd.sum(axis=1)             # sum of rows


# methods for boolean arrays
(rnd > 0).sum()             # counts number of positive values
(rnd > 0).any()             # checks if any value is True
(rnd > 0).all()             # checks if all values are True

# reshape, transpose, flatten
nums = np.arange(32).reshape(8, 4) # creates 8x4 array
nums.T                       # transpose
nums.flatten()               # flatten

# random numbers
np.random.seed(12234)       # Set the seed
np.random.rand(2, 3)        # 2 x 3 matrix in [0, 1]
np.random.randn(10)         # random normals (mean 0, sd 1)
np.random.randint(0, 2, 10) # 10 randomly picked 0 or 1

'''
Broadcasting
------------

Sources https://docs.scipy.org/doc/numpy-1.13.0/user/basics.broadcasting.html

Implicite conversion to allow operations on arrays of different sizes.

- The smaller array is stretched or “broadcasted” across the larger array so that they have
compatible shapes.

- Fast vectorized operation in C instead of Python.

- No needless copies.

Rules
~~~~~

Starting with the trailing axis and working backward, Numpy compares arrays dimensions.

- If two dimensions are equal then continues

- If one of the operand has dimension 1 stretches it to match the largest one

- When one of the shapes runs out of dimensions (because it has less dimensions than the other shape), Numpy will use 1 in the comparison process until the other shape's dimensions run out as well.


.. figure:: images/numpy_broadcasting.png


   Broadcasting (http://www.scipy-lectures.org)
'''

a = np.array([[ 0,  0,  0],
              [10, 10, 10],
              [20, 20, 20],
              [30, 30, 30]])

b = np.array([0, 1, 2])
a + b

'''
.. parsed-literal::

    array([[ 0,  1,  2],
           [10, 11, 12],
           [20, 21, 22],
           [30, 31, 32]])
'''

'''
Examples

Shapes of operands A, B and result:
'''

A      (2d array):  5 x 4
B      (1d array):      1
Result (2d array):  5 x 4

A      (2d array):  5 x 4
B      (1d array):      4
Result (2d array):  5 x 4

A      (3d array):  15 x 3 x 5
B      (3d array):  15 x 1 x 5
Result (3d array):  15 x 3 x 5

A      (3d array):  15 x 3 x 5
B      (2d array):       3 x 5
Result (3d array):  15 x 3 x 5

A      (3d array):  15 x 3 x 5
B      (2d array):       3 x 1
Result (3d array):  15 x 3 x 5



'''
Exercises
---------

Given the array:
'''

X = np.random.randn(4, 2) # random normals in 4x2 array

'''
- For each column find the row index of the minimiun value.

- Write a function ``standardize(X)`` that return an array whose columns are centered and scaled (by std-dev).
'''
