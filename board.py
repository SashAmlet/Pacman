import random
import numpy as np

# Eller's algorithm
def generate_maze(cols, rows):
    counter=0

    maze = np.zeros((rows, cols), dtype=int)
    v_brdrs = np.zeros((rows, cols), dtype=int)
    h_brdrs = np.zeros((rows, cols), dtype=int)

    def choise():
        return random.choice([0, 1])
    
    def update_counter():
        global counter
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
        for i in range(cols):
            if choise() == 1:
                v_brdrs[i][rownum] = 1
            elif row[i] == row[i+1]:
                v_brdrs[i][rownum] = 1
            else:
                set_concatenation(row, i)

    def not_unique(row, colnum, rownum): # проверка - есть ли в множестве элемент без нижней границы кроме данного.
        indices = [index for index, value in enumerate(row) if value == row[colnum] and index != colnum]
        # indices = np.where((row == row[colnum]) & (np.arange(len(row)) != colnum))[0]



        result = 0
        # for i in indices:
        #     result += h_brdrs[i][rownum]
        result = np.sum(h_brdrs[indices, rownum])
        
        return 1 if result < len(indices) else 0


    def horizontal_walls(row, rownum):
        for i in range(cols):
            if choise() == 0:
                continue
            elif not_unique(row, i, rownum):
                h_brdrs[i][rownum] = 1
    
    maze[0][:] = init_row()

    for rownum, row in enumerate(maze):
        if rownum == 1: # первая строка
            vertical_walls(row, rownum)
            horizontal_walls(row, rownum)

        elif rownum == len(maze) - 1: #последняя строка
            h_brdrs[:][rownum] = [1] * len(row)
            for i in range(row):
                if row[i] != row[i+1]:
                    v_brdrs[i][rownum] = 0
        else:
            prev_row = h_brdrs[:][rownum-1].copy()
            indices = [index for index, value in enumerate(prev_row) if value == 1]
            for i in indices:
                row[i] = update_counter()
            vertical_walls(row, rownum)
            horizontal_walls(row, rownum)





    


    return (v_brdrs, h_brdrs)


         
    


width, height = 5, 5
v_brdrs, h_brdrs = generate_maze(width, height)
