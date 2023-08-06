import numpy as np


def operator_1(A: np.array, row_i: int, row_j: int):
    A[[row_i, row_j]] = A[[row_j, row_i]]
    
def operator_2(A: np.array, row_i: int, w: float):
    A[[row_i]] = A[[row_i]] * w

def operator_3(A: np.array, row_i: int, row_j: int, w: float):
    A[[row_i]] = A[[row_i]] + A[[row_j]] * w