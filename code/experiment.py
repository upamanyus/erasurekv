#!/usr/bin/env python3

# Try finding inverses for appropriate submatrices of the code-generation
# matrix.

import numpy as np
from numpy.linalg import inv

# Generate the "2" matrix for each chunk having size n, and k chunks being
# enough to reconstruct the original data of size (n*k).
def M2(n):
    data = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == 0 and j == 0: # put a 1 at the top-left.
                row.append(1)
            else:
                row.append(1 if j == (i + 1) % n else 0)
        data.append(row)
    return np.matrix(data)

# Generate the coding matrix for each chunk having size n, and k chunks being
# enough to reconstruct the original data of size (n*k).
def code_matrix_blocks(n, k):
    # first, generate an nk x nk identity matrix, row by row
    code_matrix_block_form = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append(np.identity(n,dtype=int) if i == j else np.zeros((n,n),dtype=int))
        code_matrix_block_form.append(row)

    # add [I I I ... I] submatrix
    row = []
    for i in range(k):
        row.append(np.identity(n,dtype=int) )
    code_matrix_block_form.append(row)


    # add [I M M^2 ... M^^k] submatrix
    row = []
    m2 = M2(n)
    for i in range(k):
        row.append(m2**i)
    code_matrix_block_form.append(row)

    # print(np.block(code_matrix_block_form))
    return code_matrix_block_form


def check_inverses(n, k):
    c = code_matrix_blocks(n, k)

    # Want to pick k rows in block form.
    # Then, construct nk x nk matrix, and try inverting.

    # For now, let's try the last k rows. This will mean the first two data
    # chunks are lost, and we need to use both parity chunks.
    print("Candidate partial matrix to invert:")
    m = np.block(c[2:])
    print(m)

    print("Inverse of partial matrix:")
    print(inv(m))
    print("This inverse has entries purely in Z, so we can project into F2, and get an inverse in F2.")

# print(M2(5))
# print(code_matrix_blocks(4, 2))
# check_inverses(2, 128)
check_inverses(4, 3)
