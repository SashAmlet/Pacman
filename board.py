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


         
    


width, height = 5, 5
v_brdrs, h_brdrs = generate_maze(width, height)
