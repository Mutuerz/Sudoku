import copy
import math
import numpy as np
import time

# Number = Color, for reading proposes

# Creates an adjacency matrix for any given size of a sudoku board
def create_adjacency_matrix(size):
    list1 = np.arange(size**2).reshape(size, size)  # We declare an ordered matrix with the positions in board
    vector = []
    count = 0
    count2 = -1
    adjacency_matrix = np.zeros((size**2, size**2))  # Declare a matrix

    # Adjacency for rows
    for i2 in range(0, size**2):
        count2 = count2+1
        if count2 == size:
            count2 = 0
        for j2 in range(i2, size**2):
            count = count + 1
            if count == (size+1)-count2:
                count = 0
                break
            if j2 != i2:  # Same Rows and columns
                    if adjacency_matrix[i2][j2] != 1:  # If is already fill
                        adjacency_matrix[i2][j2] = 1   # Assign value

    # Adjacency for columns
    for i2 in range(0, size**2):
        for j2 in range(i2, size**2, size):
            if j2 != i2:  # Same Rows and columns
                    if adjacency_matrix[i2][j2] != 1:  # If is already fill
                        adjacency_matrix[i2][j2] = 1   # Assign value

    # Adjacency for sub-matrix
    # Here we save the values of the positions that are in the same region
    for j2 in range(0, size, int(math.sqrt(size))):
        for i2 in range(0, size):
            for n in range(0, int(math.sqrt(size))):
                vector.append(list1[i2][j2+n])

    # Here we fill the cells and verify is not in diagonal
    for i in range(0, size**2, size):
        for i2 in range(0, size):
            for j in range(0, size):
                if i2+i != i+j:
                    if adjacency_matrix[vector[i2+i]][vector[i+j]] != 1:  # If is already fill
                        adjacency_matrix[vector[i2+i]][vector[i+j]] = 1  # Assign value

    # Here we copy upper triangle into the lower triangle
    for i, rows in enumerate(adjacency_matrix):
        for j, cols in enumerate(adjacency_matrix):
            adjacency_matrix[j][i] = adjacency_matrix[i][j]
    return adjacency_matrix


# This function creates a matrix and fill it with the restriction values
def restrictor(board2, positions2, restricted2, adjacency):
    visited = []  # Vector of visited colors
    for i in range(0, size):
        for j in range(0, size):
            if board2[i][j] == 0:
                pos = positions2[i][j]  # Save non-colored node id
                for i2 in range(0, size ** 2):
                    # Verify that there is an adjacency, that the colors is not already in
                    if adjacency[i2][pos] == 1 and board2[int(i2/size)][i2 % size] not in visited and board2[int(i2/size)][i2 % size] != 0:
                        visited.append(board2[int(i2/size)][i2 % size])
                restriction = len(visited)  # Amount of colors in array indicates the restriction value
                restricted2[i][j] = restriction
                visited.clear()

    return restricted2


# This ugly function provides, using the index, to which region a position belongs
def regions(size2):
    # size = 16;
    n2 = int(math.sqrt(size2));
    # regiones = n*n;
    # Celdas = (n*2)(n**2);
    Nofila = n2 ** 2;
    NoColumna = n2 ** 2;
    # print(' {} regiones: {} '.format('#', regiones) )
    # matrizOriginal  = np.arange(Celdas).reshape(Nofila, NoColumna)
    # print(matrizOriginal)
    MatrizGenerada = np.zeros((Nofila, NoColumna))
    # print(MatrizGenerada)
    cont = 0;
    for si in range(1, n2 + 1):
        for sj in range(1, n2 + 1):
            for mi in range(1, n2 + 1):
                for mj in range(1, n2 + 1):
                    Fila = n2 * (si - 1) + mi;
                    Columna = n2 * (sj - 1) + mj;
                    MatrizGenerada[Fila - 1][Columna - 1] = cont
                    cont = cont + 1;
                    # print(' cont: {} Fila: {} Columna: {} '.format(cont, Fila, Columna) )
    return np.array(MatrizGenerada)
    # print(MatrizGenerada);


# This function receives the board, and using the restricted matrix decide where to play and which number to use
def play(board2, restricted2):
    array = list(range(1, size+1))  # Array of colors
    higher = 0
    r = 0
    please_break = False
    number_restriction = size**2  # Number of cells affected
    # Search in the restricted for the highest number
    for i in range(0, size):
        for j in range(0, size):
            if restricted2[i][j] >= np.amax(restricted2):
                affected_cells = cells_affected(restricted2, size, j, i, r)
                if affected_cells < number_restriction:
                    # Highest number coordinates are stored
                    number_restriction = affected_cells
                    j2 = copy.deepcopy(j)
                    i2 = copy.deepcopy(i)

    minor = 100
    # We start checking available colors
    for n in array:
        isin = False  # Verify if there is another node with the same number
        #print("This is ene: {}".format(n))

        # Following verifications verify that the n color
        # When rows are zero, Row verification
        for k in range(0, size):
            if board2[k][j2] == n:
                #print("Rows")
                #print(isin)
                #print(n)
                isin = True
        if not isin:  # If isin is not true means that rows are checked

            # When Columns are zero, column verifications¿
            for l in range(0, size):
                if board2[i2][l] == n:
                    #print("Columns")
                    #print(isin)
                    #print(n)
                    isin = True
            if not isin:  # If isin is not true means that columns are checked

                # Check in regions
                regions_cool = regions(size)
                for ri, reg in enumerate(regions_cool):
                    if positions[i2][j2] in reg:
                        r = copy.deepcopy(ri)  # Region in which the position in question is

                # we search for the lowest value, that gives  the i and j position to start
                # Minor stores the lowest position number, that gives us the starting coordinates
                for o in range(0, size):
                    if regions_cool[r][o] < minor:
                        minor = regions_cool[r][o]

                for o in range(0, size):
                    for p in range(0, size):
                        if positions[o][p] == minor:  # if a position matches the minor value we stored them
                            cor1 = copy.deepcopy(o)
                            cor2 = copy.deepcopy(p)
                            break
                #print("Origen region= o: {}, P: {} ".format(cor1, cor2))

                # We search in the region of the board in which the n color may be
                for o in range(cor1, cor1 + int(math.sqrt(size))):
                    if please_break:
                        break
                    for p in range(cor2, cor2 + int(math.sqrt(size))):

                        if board2[o][p] == n:  # This conditions validate if a number is already in the region
                            isin = True
                            #please_break = True
                            break

                if not isin:  # If n color is not in region we proceed to play
                    print("En la pos {},{} se jugo {}".format(i2, j2, n))
                    board2[i2][j2] = n
                    please_break = True
                    break
    return np.array(board2)


def cells_affected (restriction_matrix, size, j2, i2, r):
    affected = 0
    minor = 100
    please_break = False
    # Number of restrictions affected in a row
    for k in range(0, size):
        if restriction_matrix[k][j2] == 0:
            affected = affected + 1
    # Number of restrictions affected in a column
    for l in range(0, size):
        if restriction_matrix[i2][l] == 0:
            affected = affected + 1
    # Number of restrictions affected in a region
    regions_cool = regions(size)
    for ri, reg in enumerate(regions_cool):
        if positions[i2][j2] in reg:
            r = copy.deepcopy(ri)  # Region in which the position in question is

    # we search for the lowest value, that gives  the i and j position to start
    # Minor stores the lowest position number, that gives us the starting coordinates
    for o in range(0, size):
        if regions_cool[r][o] < minor:
            minor = regions_cool[r][o]

    for o in range(0, size):
        for p in range(0, size):
            if positions[o][p] == minor:  # if a position matches the minor value we stored them
                cor1 = copy.deepcopy(o)
                cor2 = copy.deepcopy(p)
                break

    # We search in the region of the board in which the n color may be
    for o in range(cor1, cor1 + int(math.sqrt(size))):
        for p in range(cor2, cor2 + int(math.sqrt(size))):
            if restriction_matrix[o][p] == 0:  # This conditions validate if a number is already in the region
                affected = affected + 1

    return affected


if __name__ == "__main__":

    board5 = np.array(
                        [[0, 8, 0, 0, 0, 4, 0, 0, 5],
                        [0, 7, 0, 9, 0, 3, 0, 2, 0],
                        [9, 4, 2, 0, 0, 0, 0, 0, 1],
                        [0, 2, 0, 0, 4, 0, 0, 0, 8],
                        [0, 0, 0, 3, 0, 9, 0, 0, 0],
                        [4, 0, 0, 0, 6, 0, 0, 9, 0],
                        [0, 0, 0, 0, 0, 5, 0, 3, 6],
                        [0, 5, 0, 7, 0, 2, 0, 4, 0],
                        [2, 0, 0, 0, 0, 6, 0, 0, 0]
                        ])
    board6 = np.array(
                        [[0, 5, 0, 9, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 5, 0, 1, 2],
                         [9, 0, 0, 0, 7, 0, 0, 5, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [2, 1, 9, 0, 0, 0, 7, 0, 0],
                         [0, 0, 0, 0, 0, 8, 0, 9, 1],
                         [0, 4, 5, 0, 9, 0, 0, 0, 0],
                         [7, 0, 0, 0, 0, 3, 0, 6, 0],
                         [6, 0, 1, 2, 0, 0, 0, 0, 4]
                         ])

    board1 = np.array(
                [[0, 0, 4, 0],
                [2, 0, 0, 1],
                [3, 0, 0, 4],
                [0, 2, 0, 0]])


    board2 = np.array(
                [[0, 0, 0, 4],
                [0, 4, 2, 0],
                [0, 3, 0, 0],
                [1, 0, 0, 0]])


    board3 = np.array(
                [[4, 0, 0, 2],
                [0, 2, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 3]])

    board4 = np.array(
                [[4, 0, 0, 0],
                [0, 0, 0, 2],
                [3, 0, 0, 0],
                [0, 0, 0, 1]
                ])
board = copy.deepcopy(board6)  # HERE YOU SELECT WHICH SUDOKU TO USE
size = len(board)
start_time = time.time()
positions = np.arange(size**2).reshape(size, size)
adjacency_matrix = create_adjacency_matrix(size)

nfurcation = False  # This variable indicates if we arrive to a furcation, this is used to save the start point if it finds no solution
contador = 0
boardcopia=[]
while 0 in board:
    if boardcopia is board:
        break
    boardcopia = copy.deepcopy(board)
    contador = contador +1
    restricted = np.zeros((size, size))
    restricted = copy.deepcopy(restrictor(board, positions, restricted, adjacency_matrix))
    print("Restriction")
    print(restricted)
    board = copy.deepcopy(play(board, restricted))

    print(board)
print("Numero de iteraciones: ", contador)
print("--- {} seconds ---".format(time.time() - start_time))
