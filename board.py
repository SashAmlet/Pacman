import random
import numpy as np

# Eller's algorithm
def generate_maze(cols, rows):
    counter = 0

    maze = np.zeros((rows, cols), dtype=int)
    v_brdrs = np.zeros((rows, cols), dtype=int)
    h_brdrs = np.zeros((rows, cols), dtype=int)

    def choise():
        return random.choice([0, 1])
    
    def update_counter():
        nonlocal counter
        counter+=1
        return counter

    def init_row():
        array = np.zeros(cols, dtype=int)
        for i in range(cols):
            array[i] = update_counter()
            
        return array
    
    def set_concatenation(row, colnum):
        for i in range(colnum+1, cols):
            if row[i] == row[colnum+1]: 
                row[i] = row[colnum]

    def vertical_walls(row, rownum):
         for i in range(cols-1):
            if choise() == 1:
                v_brdrs[rownum, i] = 1
            # elif row[i] == row[i+1]:
            #     v_brdrs[rownum, i] = 1
            else:
                set_concatenation(row, i)

    def not_unique(row, colnum, rownum): # check - whether there is an element in the set without a lower bound except for the given one.
        indices = [index for index, value in enumerate(row) if value == row[colnum] and index != colnum]
        # indices = np.where((row == row[colnum]) & (np.arange(len(row)) != colnum))[0]

        result = 0
        result = np.sum(h_brdrs[rownum, indices]) # if the sum of h_brdrs < the number of elements of the set, then there are elements without a lower bound
        
        return 1 if result < len(indices) else 0

    def horizontal_walls(row, rownum):
        #test_choise = [1, 1, 1, 1, 1]
        for i in range(cols):
            if choise() == 0: #test_choise[i] == 0: # 
                continue
            elif not_unique(row, i, rownum):
                h_brdrs[rownum, i] = 1
    
    maze[0, :] = init_row()

    for rownum, row in enumerate(maze):
        if rownum == 0: # first line
            vertical_walls(row, rownum)
            horizontal_walls(row, rownum) 

        elif rownum == len(maze) - 1: # last line
            h_brdrs[rownum, :] = [0] * len(row)
            maze[rownum, :] = maze[rownum-1, :].copy() 
            v_brdrs[rownum, :] = v_brdrs[rownum-1, :].copy() 
            for i in range(rownum):
                if row[i] != row[i+1]:
                    v_brdrs[rownum, i] = 0
        else:
            prev_row = h_brdrs[rownum-1, :].copy()
            indices = [index for index, value in enumerate(prev_row) if value == 1]
            maze[rownum, :] = maze[rownum-1, :].copy() 
            for i in indices:
                row[i] = update_counter()
            vertical_walls(row, rownum)
            horizontal_walls(row, rownum)

    return (v_brdrs, h_brdrs)

def get_maze(cols, rows):

    COLS = cols
    ROWS = rows

    cols = (cols - 4) // 2
    rows = (rows - 4) // 2


    
    v_brdrs, h_brdrs = generate_maze(cols, rows)

    if v_brdrs.shape != h_brdrs.shape:
        raise ValueError("Matrices must have the same dimensions")
    
    rows, cols = v_brdrs.shape
    maze = np.ones((rows*2, cols*2), dtype=int)

    def super_dot(probability):
        if 1 <= random.randint(1, 100) <= probability:
            return 3
        else:
            return 2

    for i in range(0, rows * 2, 2):
        for j in range(0, cols * 2, 2):

            num = super_dot(10)

            maze[i,j] = num

            num = super_dot(10)

            if v_brdrs[i//2, j//2] == 0:
                maze[i,j+1] = num
            if h_brdrs[i//2, j//2] == 0:
                maze[i+1,j] = num

    def insert_box(matrix):
        rows, cols = matrix.shape
        if rows < 6 or cols < 6:
            raise ValueError("The matrix must be at least 6*6 in size.")

        center_row = rows // 2
        center_col = cols // 2

        start_row = center_row - 3
        start_col = center_col - 3

        matrix[start_row:start_row + 6, start_col:start_col + 6] = 0

        start_row = center_row - 2
        start_col = center_col - 2

        matrix[start_row:start_row+4, start_col] = 1
        matrix[start_row:start_row+4, start_col+3] = 1
        matrix[start_row, start_col:start_col+4] = 1
        matrix[start_row+3, start_col:start_col+4] = 1
        
        start_row = center_row - 2
        start_col = center_col - 1
        matrix[start_row, start_col:start_col+2] = 4

        return matrix

    def add_borders(matrix):
        ones_columns = np.ones((matrix.shape[0], 1))
        zeros_columns = np.zeros((matrix.shape[0], 1))

        ones_row = np.ones((1, matrix.shape[1]+4))
        zeros_row = np.zeros((1, matrix.shape[1]+4))

        new_matrix = np.hstack((ones_columns, zeros_columns, matrix, zeros_columns, ones_columns))
        final_matrix = np.vstack((ones_row, zeros_row, new_matrix, zeros_row, ones_row))

        final_matrix[1][0] = 5
        final_matrix[1][COLS-1] = 5
        final_matrix[ROWS-2][0] = 5
        final_matrix[ROWS-2][COLS-1] = 5

        return final_matrix
    
    maze_w_box = insert_box(maze)
    final_maze = add_borders(maze_w_box)



    print(v_brdrs)
    print()
    print(h_brdrs)
    # print()
    # print(final_maze)

    return final_maze





















## Eller's original algorithm ##
def generate_maze1(cols, rows):
    counter = 0

    maze = np.zeros((rows, cols), dtype=int)
    v_brdrs = np.zeros((rows, cols), dtype=int)
    h_brdrs = np.zeros((rows, cols), dtype=int)

    def choise():
        return random.choice([0, 1])
    
    def update_counter():
        nonlocal counter
        counter+=1
        return counter

    def init_row():
        array = np.zeros(cols, dtype=int)
        for i in range(cols):
            array[i] = update_counter()
            
        return array
    
    def set_concatenation(row, colnum):
        for i in range(colnum+1, cols):
            if row[i] == row[colnum+1]: 
                row[i] = row[colnum]

    def vertical_walls(row, rownum):
         for i in range(cols-1):
            if choise() == 1:
                v_brdrs[rownum, i] = 1
            elif row[i] == row[i+1]:
                v_brdrs[rownum, i] = 1
            else:
                set_concatenation(row, i)

    def not_unique(row, colnum, rownum): # проверка - есть ли в множестве элемент без нижней границы кроме данного.
        indices = [index for index, value in enumerate(row) if value == row[colnum] and index != colnum]
        # indices = np.where((row == row[colnum]) & (np.arange(len(row)) != colnum))[0]

        result = 0
        result = np.sum(h_brdrs[rownum, indices]) # если сумма h_brdrs < количества элементов для множества, значить есть элементы без нижней границы
        
        return 1 if result < len(indices) else 0


    def horizontal_walls(row, rownum):
        #test_choise = [1, 1, 1, 1, 1]
        for i in range(cols):
            if choise() == 0: #test_choise[i] == 0: # 
                continue
            elif not_unique(row, i, rownum):
                h_brdrs[rownum, i] = 1
    
    maze[0, :] = init_row()

    for rownum, row in enumerate(maze):
        if rownum == 0: # первая строка
            vertical_walls(row, rownum)
            horizontal_walls(row, rownum) 

        elif rownum == len(maze) - 1: #последняя строка
            h_brdrs[rownum, :] = [1] * len(row)
            maze[rownum, :] = maze[rownum-1, :].copy() 
            v_brdrs[rownum, :] = v_brdrs[rownum-1, :].copy() 
            for i in range(rownum):
                if row[i] != row[i+1]:
                    v_brdrs[rownum, i] = 0
        else:
            prev_row = h_brdrs[rownum-1, :].copy()
            indices = [index for index, value in enumerate(prev_row) if value == 1]
            maze[rownum, :] = maze[rownum-1, :].copy() 
            for i in indices:
                row[i] = update_counter()
            vertical_walls(row, rownum)
            horizontal_walls(row, rownum)

    return (v_brdrs, h_brdrs)