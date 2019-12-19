from tkinter import *
import tkinter
import requests
from functools import partial
import time
import sys
sys.setrecursionlimit(1500)
from collections import deque   
###################################### Board Logic ###############################################
default_board = []
solve_board = []
speed = 1000
isSolve = False
lastRow = -1
lastCol = -1

def find_empty_location(board,l):
    for row in range(9):
        for col in range(9):
            if(board[row][col]==-1):
                l[0]=row
                l[1]=col
                return True
    return False

def used_in_row(board,row,num):
    for i in range(9):
        if(board[row][i]==num):
            return True
    return False

def used_in_col(board,col,num):
    for i in range(9):
        if(board[i][col]==num):
            return True
    return False

def used_in_box(board,row,col,num): #row,col = 0,0 0,3 0,6 3,0 3,3 ...
    for i in range(3):
        for j in range(3):
            if(board[i+row][j+col]==num):
                return True
    return False

def chack_location_is_safe(board,row,col,num):
    return not used_in_row(board,row,num) and not used_in_col(board,col,num) and not used_in_box(board,row-row%3,col-col%3,num)

def checkIsSolve():
    global solve_board
    chcek = True 
    for i in range(9):
        for j in range(9):
            if(solve_board[i][j]==-1):
                chcek = False
    return chcek
# Data backtrack
data = deque() 

def solve_sudoku():
    global master
    global numbers
    global solve_board
    l = [0,0]
    if(not find_empty_location(solve_board,l)):
        return True      
    row = l[0]
    col = l[1]
    for num in range(1,10):
        data.append((row,col,num))
        if(chack_location_is_safe(solve_board,row,col,num)):
            solve_board[row][col] = num
            res = solve_sudoku()
            if(res):
                return True
            else:
                solve_board[row][col] = -1
    return False

def solveBoard():
    global default_board
    global solve_board
    global isSolve
    for i in range(9):
        for j in range(9):
            solve_board[i][j] = default_board[i][j]
    data.clear()
    solve_sudoku()
    isSolve = True
    showBackTrack()

############################################## Tkinter #############################################
master = tkinter.Tk()
master.title('Sudoku Solver')
master.geometry("920x920") #"582x650"
master.resizable(0, 0)
master.config(bg="black")
#Varible
# number store all Label number store in board
level = IntVar() 
numbers = []
stateX = -1
stateY = -1

def showBackTrack():
    global data
    global master
    global numbers
    global solve_board
    global speed
    global lastRow
    global lastCol
    global default_board
    if(len(data)==0):
        return
    try:
        datax = data.popleft()
        row = datax[0]
        col = datax[1]
        value = datax[2]
        if(row<=lastRow and col<lastCol and lastRow!=-1 and lastCol!=-1):
            for i in range(row,lastRow+1):
                for j in range(col,lastCol+1):
                    if(default_board[i][j]==-1):
                        numbers[i][j]['text'] = ""
        numbers[row][col]['text'] = str(value)
        numbers[row][col]['bg'] = 'purple'
        for i in range(9):
            for j in range(9):
                if(i==row and j==col):
                    continue
                numbers[i][j]['bg'] = 'white'
        lastRow = row
        lastCol = col
        master.after(speed,showBackTrack)
    except:
        print('call back')


def setBoard():
    global numbers
    global default_board
    for i in range(9):
        for j in range(9):
            if(default_board[i][j]!=-1):
                numbers[i][j]['text'] = str(default_board[i][j])
            else:
                numbers[i][j]['text'] = ""


def clickNumber(i,j):
    global numbers
    global stateX
    global stateY
    global default_board
    if(default_board[i][j]!=-1):
        return
    numbers[i][j]['bg'] = 'pink'
    if(stateX!=-1 and stateY!=-1):
        numbers[stateX][stateY]['bg'] = 'white'
    stateX = i
    stateY = j

def updateBoard():
    global solve_board
    global numbers
    for i in range(9):
        for j in range(9):
            if(solve_board[i][j]!=-1):
                numbers[i][j]['text'] = str(solve_board[i][j])
            else:
                numbers[i][j]['text'] = ""

def resetColor():
    global number
    for i in range(9):
        for j in range(9):
            if(i==stateX and j==stateY):
                continue
            number = numbers[i][j]
            number['bg'] = 'white'

def getValue(event):
    global solve_board
    global numbers
    global master
    value = event.char
    if(value=='\x08'):
        solve_board[stateX][stateY] = -1
        updateBoard()
        return
    try:
        value = int(value)
    except:
        return
    if(stateX==-1 and stateY==-1):
        return
    if(value==0):
        return 
    # mark if can't use this number
    invalid = False
    for i in range(9):
        if(solve_board[stateX][i]==value):
            number = numbers[stateX][i]
            number['bg'] = 'red'
            invalid = True
    for i in range(9):
        if(solve_board[i][stateY]==value):
            number = numbers[i][stateY]
            number['bg'] = 'red'
            invalid = True
    row = stateX-stateX%3
    col = stateY-stateY%3
    for i in range(3):
        for j in range(3):
            if(solve_board[i+row][j+col]==value):
                number = numbers[i+row][j+col]
                number['bg'] = 'red'
                invalid = True

    if(not invalid):
        solve_board[stateX][stateY] = value
        updateBoard()
    else:
        updateBoard()
        master.after(500,resetColor)

def newGame():
    global isSolve
    global default_board
    global solve_board
    strx = level.get()
    if(isSolve):
        return
    if(strx<=0 or strx>3):
        strx = 3
    url = "http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level="+str(strx)
    response = requests.get(url)
    default_board.clear()
    solve_board.clear()
    for i in range(9):
        default_board.append([])
        solve_board.append([])
        for j in range(9):
            default_board[i].append(-1) #-1 is unknow
            solve_board[i].append(-1) #-1 is unknow
    # get board in api call
    for data in response.json()['squares']:
        default_board[int(data['x'])][int(data['y'])] = int(data['value'])
        solve_board[int(data['x'])][int(data['y'])] = int(data['value'])
    setBoard()

def set_speed(val):
    global speed
    speed = 1250 - int(val)

padSubBoard = 3
for i in range(9):
    numbers.append([])
    frame = Frame(master,bg="black")
    frame.pack()
    pady = 0
    if(i%3==2):
        pady=padSubBoard
    for j in range(9):
        padx = 0
        if(j%3==2):
            padx = padSubBoard
        number = Label(frame,text="",bg='white',width= 6,height=3,borderwidth=1, relief = "solid",font=("Times New Roman", 20, "bold"),
                        highlightbackground="blue")
        number.config(highlightbackground="RED")
        number.pack(side=LEFT,padx=(0,padx),pady=(0,pady))
        number.bind("<Button-1>",lambda event,i=i,j=j:clickNumber(i,j))
        numbers[i].append(number)

############################## Bottom Window (option) #######################################################
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb   

bottomFrame = Frame(master)
bottomFrame.pack()
textSpeed = Label(bottomFrame,text="Speed = ")
textSpeed.pack(side=LEFT)
speedBtn = Scale(bottomFrame,from_=0, to=1000,width = 13,orient = HORIZONTAL,showvalue=False,command=set_speed)
speedBtn.pack(side=LEFT)
solveBtn = tkinter.Button(bottomFrame,height=2,width=39,text='Solve Game',bg=_from_rgb((3, 252, 240)),command=partial(solveBoard))
solveBtn.pack(side=LEFT)
newBtn = tkinter.Button(bottomFrame,height=2,width=40,text='New Game',bg=_from_rgb((3, 252, 240)),command=partial(newGame))
newBtn.pack(side=LEFT)
Radiobutton(bottomFrame, text='Easy', variable=level, value=1).pack(side=LEFT) 
Radiobutton(bottomFrame, text='Medium', variable=level, value=2).pack(side=LEFT)
Radiobutton(bottomFrame, text='Hard', variable=level, value=3).pack(side=LEFT)

newGame()
master.bind('<Key>', lambda event : getValue(event))
master.mainloop()