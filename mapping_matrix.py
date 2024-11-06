import numpy as np
import csv

memo = {}
def generate_block_matrix(M, A, k):
    # Get the dimensions of the matrices M and A
    m, n = M.shape
    p, n_A = A.shape
    
    # Ensure the matrices M and A have compatible column sizes
    if n != n_A:
        raise ValueError("Matrix M and matrix A must have the same number of columns.")
    
    # Create a list to store blocks for the main diagonal
    blocks = [[None]*k for _ in range(k)]
    
    # Fill the diagonal with M and rest with zeros
    for i in range(k):
        for j in range(k):
            if i == j:
                blocks[i][j] = M  # Place M on the diagonal
            else:
                blocks[i][j] = np.zeros((m, n))  # Place zero matrices elsewhere

    # Use np.block to combine the M blocks into a single block matrix
    block_matrix = np.block(blocks)
    
    # Now create the final row that contains the A matrices
    row_of_A = [A for _ in range(k)]
    
    # Combine everything into a full block matrix with A blocks in the last row
    # First combine the block_matrix with the row_of_A
    block_matrix_with_A = np.vstack([block_matrix, np.block([row_of_A])])
    
    return block_matrix_with_A

def M(n, d):
    global memo
    if (n, d) in memo:
        return memo[(n, d)]
    # If d = 1 we need only one row to get a 1-decodable matrix
    if d == 1:
        ans =  np.ones((1,n))
    # Base case: when n <= d, return identity matrix
    elif n <= d:
        ans = np.identity(n)
    
    # Case for M^n(d) when n > d and n < 1.5*(d+1)
    elif n < 1.5 * (d + 1):
        ans = np.block([[np.identity(n-1), np.ones((n-1, 1))]])
    
    # Recursive case for n >= 1.5*(d+1)
    else:
        ans = None
        # Recursive construction of matrix M
        for i in range(2,int(np.ceil(n/2)) + 1):
            block_top = M(int(np.ceil(n / i)), int(np.floor(d / 2)))
            block_bottom = M(int(np.ceil(n / i)), d)
            block_matrix = generate_block_matrix(block_top,block_bottom,i)
            if ans is None:
                ans = block_matrix
            else:
                if block_matrix.shape[0] < ans.shape[0]:
                    ans = block_matrix
            
        
        # Ensure the matrix has exactly n columns
        ans =  ans[:, :n]
    
    memo[(n,d)] = ans
    return ans


n = 500
d = 10
matrix = M(n, d)
print(matrix.shape)

# # Specify the CSV file name
# filename = 'matrix_' + str(n) + '_' + str(d) +'.csv'

# # Write to CSV file
# with open(filename, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(matrix)

# print(f"Matrix has been written to {filename}")