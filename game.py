import numpy as np
from tkinter import *
nb_case = 50
WINDOW_SIDE = 400
cote_case = WINDOW_SIDE // nb_case
UPDATE_TIME = 200
ALIVE_CHAR = "O"
alive_cells = []


def find_neighbours(grid, cell_pos):
    x, y = cell_pos
    shape = grid.shape
    neighbours = []
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            pos_x = x+i
            pos_y = y+j
            if 0 <= pos_x < shape[0] and 0 <= pos_y < shape[1] and [pos_x, pos_y] != [x, y]:
                neighbours.append([pos_x, pos_y])
    return neighbours

def count(grid, neighbours):
    c = 0
    for n in neighbours:
        if grid[n[0], n[1]]:
            c +=1
    return c


def update(grid, cells):
    temp = []
    for cell in cells:
        neighbours = find_neighbours(grid, cell)
        c = count(grid, neighbours)
        if (grid[cell[0], cell[1]] == 1 and c in [2,3]) or (grid[cell[0], cell[1]] == 0 and c == 3):
            temp.append([cell, 1])
            if cell not in alive_cells:
                alive_cells.append(cell)
            draw_x, draw_y = cell[0] * cote_case, cell[1] * cote_case
            canvas.create_rectangle(draw_x, draw_y, draw_x + cote_case, draw_y + cote_case, fill="green")
        else:
            temp.append([cell, 0])
            if cell in alive_cells:
                alive_cells.remove(cell)
            draw_x, draw_y = cell[0] * cote_case, cell[1] * cote_case
            canvas.create_rectangle(draw_x, draw_y, draw_x + cote_case, draw_y + cote_case, fill="white")
    canvas.pack()
    for L in temp:
        grid[L[0][0], L[0][1]] = L[1]

def next_turn(grid):
    cells_to_update = []
    for cell in alive_cells:
        neighbours = find_neighbours(grid, cell)
        for n in neighbours:
            if n not in cells_to_update:
                cells_to_update.append(n)
    #print("alive cells:", len(alive_cells))
    #print("cells_to_update: ", len(cells_to_update))
    update(grid, cells_to_update)
    fenetre.after(UPDATE_TIME, next_turn, grid)


def key_handler(event):
    if event.keysym == "Return":
        next_turn(grid)


def left_click(event, grid):
    x = (event.x // cote_case)
    y = (event.y // cote_case)
    if grid[x, y] == 1:
        grid[x, y] = 0
        canvas.create_rectangle(x*cote_case, y*cote_case, (x+1)*cote_case, (y+1)*cote_case, fill="white")
        alive_cells.remove([x, y])
    else:
        grid[x, y] = 1
        canvas.create_rectangle(x*cote_case, y*cote_case, (x+1)*cote_case, (y+1)*cote_case, fill="green")
        alive_cells.append([x, y])
    canvas.pack()


def create_grid(canvas):
    canvas.delete("all")
    for i in range(1, nb_case):
        canvas.create_line(cote_case * i, 0, cote_case * i, WINDOW_SIDE)
        canvas.create_line(0, cote_case * i, WINDOW_SIDE, cote_case * i)
    canvas.pack()

def first_grid(grid):
    s = grid.shape
    for x in range (s[0]):
        for y in range(s[1]):
            if grid[x, y] == 0:
                canvas.create_rectangle(x * cote_case, y * cote_case, (x + 1) * cote_case, (y + 1) * cote_case,fill="white")
            else:
                canvas.create_rectangle(x * cote_case, y * cote_case, (x + 1) * cote_case, (y + 1) * cote_case,fill="green")
                alive_cells.append([x, y])


def grid_from_file():
    L = []
    f = open("sample.txt", "r")
    for line in f.readlines():
        temp = []
        for char in line:
            if char == ALIVE_CHAR:
                temp.append(1)
            else:
                temp.append(0)
        L.append(temp)
    grid = np.array(L, dtype=int, copy=False, order=None)
    first_grid(grid)
    return grid


if __name__ == '__main__':
    fenetre = Tk()
    fenetre.title("game of life")
    canvas = Canvas(fenetre, width=WINDOW_SIDE, height=WINDOW_SIDE, background='white')
    create_grid(canvas)
    grid = np.zeros((nb_case, nb_case), dtype=int)
    #grid = grid_from_file()
    canvas.bind("<Button-1>", lambda event, grid=grid: left_click(event, grid))
    fenetre.bind("<Key>", key_handler)
    fenetre.mainloop()
