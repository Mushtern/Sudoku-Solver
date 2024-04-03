import re 
import requests
import colorama

website = "https://www.sudoku.net/es"
result = requests.get(website)
content = result.text
file = open("sudoku_web.txt", "w", encoding="utf-8") 
file.write(content)

print(content)


def is_valid_move(grid, row, col, number):
    for x in range(9):
        if grid[row][x] == number:
            return False
    for x in range(9):
        if grid[x][col] == number:
            return False
    
    corner_row = row - row % 3
    corner_col = col - col % 3

    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == number:
                return False

    return True

#Backtracking

def solve(grid, row, col):
    #If we reached the end we have solved it, if not, we change rows
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0
    
    #If there's already a value set, we change columns
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)
    
    for num in range(1, 10):

        if is_valid_move(grid, row, col, num):
            grid[row][col] = num

            if solve(grid, row, col + 1): 
                return True
        
        grid[row][col] = 0
    
    return False

grid = [[0,0,0,0,0,0,0,7,9],
        [8,0,5,0,7,4,1,0,0],
        [4,6,0,1,0,0,0,3,8],
        [0,0,0,6,5,0,9,1,0],
        [0,0,6,9,1,7,0,0,4],
        [0,1,9,4,3,2,0,8,7],
        [0,0,8,2,0,6,0,4,0],
        [6,0,2,0,0,0,0,9,1],
        [0,0,0,5,0,0,0,0,6]]

if solve(grid, 0, 0):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end = " ")
        print()
else:
    print("No solution")



