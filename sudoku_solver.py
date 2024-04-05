from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import copy

options = Options()

service = Service('./chromedriver.exe')

#We need to open a web driver for the board to load
driver = webdriver.Chrome(service=service, options=options)

website = "https://www.sudoku.net/es"
driver.get(website)

driver.implicitly_wait(20)

content = driver.page_source

driver.save_screenshot('screenshot.png')

file = open('sudoku_web.txt', 'w', encoding="utf-8")
file.write(content)

#file = open('sudoku_web.txt', 'r', encoding="utf-8")
#content = file

soup = BeautifulSoup(content, 'html.parser')
sudoku_table = soup.find('table', {'class': 'sudoku-board'})

if sudoku_table:
    rows = sudoku_table.find_all('tr')
    unsolved_board = []
    for row in rows:
        cols = row.find_all('td', {'class': 'sudoku-col'})
        row_values = []
        for col in cols:
            value = col.find('span', {'class': 'cell-value'})
            if value:
                if value.text.strip() == "":
                    row_values.append(0)
                else:row_values.append(int(value.text.strip()))
        if row_values:
            unsolved_board.append(row_values)

##Checking if a move is valid
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

still_unsolved_board = copy.deepcopy(unsolved_board)
print("grid1", still_unsolved_board)

solve(unsolved_board,0,0)

print("grid2", still_unsolved_board)
cells = driver.find_elements(By.CLASS_NAME, "sudoku-cell")
for i in range(9):
    for j in range(9):
        if still_unsolved_board[i][j] == 0 :
            cells[i][j].click() 
            cells[i][j].send_keys(str(unsolved_board[i][j])) 
        else:
            pass

driver.save_screenshot('sudoku_resuelto.png')
driver.quit()