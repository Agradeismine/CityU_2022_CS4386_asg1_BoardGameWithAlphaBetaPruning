import numpy as np
import random
import ctypes, platform, time
from ctypes import *
import gui
import os
#import os,jpype
#from jpype import *
import ctypes as ct
import sys
import time
TIME_LIMIT=10
class Grid():
    def __init__(self):
        self.grid = np.full((6,6), None)

    def update(self, x, y, symbol):
        if(self.grid[x][y] is None):
            self.grid[x][y] = symbol
            return True
        print("Cell already used!")
        return False

    def isMoveAllowed(self, x, y):
        return self.grid[x][y] is None

    def __str__(self):
        grid = ""
        for i, row in enumerate(self.grid):
            grid += "|"
            for j, cell in enumerate(row):
                if(cell is None):
                    grid += " -"
                else:
                    grid += " " + self.grid[i][j]
            grid += " |\n"
        return grid

class Player():
    def __init__(self, name, symbole, isAI=False):
        # variable name is not used in this program
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score=0


    def get_isAI(self):
        return self.isAI
    def get_symbole(self):
        return self.symbole
    def get_score(self):
        return self.score
    def add_score(self,score):
        self.score+=score

def alignement(grid,x,y):
    #print("xy:",x,y)
    score=0

    #1.check horizontal
    if((grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5]  != None)):  
        score+=6
        #print("horizontal 6")
    else:
        if (grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] == None):
            if y==0 or y==1 or y==2:
                score+=3
                #print("1horizontal 3")
        elif (grid[x][0] == None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] == None):
            if y==1 or y==2 or y==3:
                score+=3
                #print("2horizontal 3")
        elif  (grid[x][1] == None) and (grid[x][2] != None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] == None):
            if y==2 or y==3 or y==4:
                score+=3
                #print("3horizontal 3")
        elif  (grid[x][2] == None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] != None):
            if y==3 or y==4 or y==5:
                score+=3
                #print("4horizontal 3")
            
    #2.check vertical
    if((grid[0][y] != None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y]!= None) and (grid[5][y]!= None)):
        score+=6
        #print("vertical 6")
    else:
        if (grid[0][y] != None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] == None):
            if x==0 or x==1 or x==2:
                score+=3
                #print("1vertical 3")
        elif (grid[0][y] == None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] != None) and (grid[4][y] == None):
            if x==1 or x==2 or x==3:
                score+=3
                #print("2vertical 3")
        elif (grid[1][y] == None) and (grid[2][y] != None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] == None):
            if x==2 or x==3 or x==4:
                score+=3
                #print("3vertical 3")
        elif  (grid[2][y] == None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] != None):
            if x==3 or x==4 or x==5:
                score+=3
                #print("4vertical 3")


    return score

def gridFull(grid):
    for rows in grid:
        for cell in rows:
            if cell is None:
                return False
    return True


def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell is None:
                cells.append([x, y])
    #print(cells)
    return cells

def gameLoop(screen, p1, p2):

    def switchPlayer(turn):
        if(turn == p1):
            return p2
        return p1

    # Initiliaze the Grid
    grid = Grid()

    # Choose the first player
    if(whoplayfirst=="1"):
        playerTurn = p1
        print("player1 (black) plays first")
    else:
        playerTurn = p2
        print("player2 (red) plays first")

    # Check if the player is player1 (black) or player2 (red)
    if(playerTurn.get_isAI()):
        #if the player is player2
        #1.if player2 written in C++
        if p2_language =="CPP":
            python_board=grid.grid
            char_arr2 = ctypes.c_char*6
            char_arr22 = char_arr2*6
            cpp_board = char_arr22()
            for row in range(6):
                for column in range(6):
                    if python_board[row][column]=="X":
                        cpp_board[row][column]=c_char(b"X")
                    elif python_board[row][column]=="O":
                        cpp_board[row][column]=c_char(b"O")	

            cpp_symbole= playerTurn.get_symbole()
            tic = time.time()
            
            move = playerTurn.get_move(cpp_board, cpp_symbole)
            toc = time.time()
            x, y = move.contents[0],move.contents[1]
            grid.update(x, y, chr(playerTurn.get_symbole()))
            gui.drawSymbole(screen, (x, y), chr(playerTurn.get_symbole()))
            print("Player2 (Red,C++), move is:",x,y)
            
        #2.if player2 written in JAVA
        elif p2_language=="JAVA":
            python_board=grid.grid
            java_board = java.util.ArrayList()
            for row in range(6):
                row_board= java.util.ArrayList()
                for column in range(6):
                    row_board.add(python_board[row][column])
                java_board.add(row_board)
            tic = time.time()
            
            move = playerTurn.get_move(java_board, playerTurn.get_symbole())
            toc = time.time()
            x, y = move[0], move[1]
            grid.update(x, y, playerTurn.get_symbole())
            gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
            print("Player2 (Red,JAVA), move is:",x,y)
        #3.if player2 written in Python
        else:
            tic = time.time()
            
            move = playerTurn.get_move(grid.grid, playerTurn.get_symbole())
            toc = time.time()
            x, y = move[0], move[1]
            grid.update(x, y, playerTurn.get_symbole())
            gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
            print("Player2 (Red,PYTHON), move is:",x,y)
            
        print("Player2 (Red) Time:", (toc - tic))
        if (toc - tic) > TIME_LIMIT:
            print("Timed out, game over.Player1 wins.")
            return "-2"

    else:
        # check the type of player1
        # if player1 written in c++
        if p1_language =="CPP":
            python_board=grid.grid
            char_arr2 = ctypes.c_char*6
            char_arr22 = char_arr2*6
            cpp_board = char_arr22()
            for row in range(6):
                for column in range(6):
                    if python_board[row][column]=="X":
                        cpp_board[row][column]=c_char(b"X")
                    elif python_board[row][column]=="O":
                        cpp_board[row][column]=c_char(b"O")	

            cpp_symbole= playerTurn.get_symbole()
            tic = time.time()
            
            move = playerTurn.get_move(cpp_board, cpp_symbole)
            toc = time.time()
            x, y = move.contents[0],move.contents[1]
            grid.update(x, y, chr(playerTurn.get_symbole()))
            gui.drawSymbole(screen, (x, y), chr(playerTurn.get_symbole()))
            print("Player1 (Black,C++), move is:",x,y)
        #2.if player1 written in JAVA
        elif p1_language=="JAVA":
            python_board=grid.grid
            java_board = java.util.ArrayList()
            for row in range(6):
                row_board= java.util.ArrayList()
                for column in range(6):
                    row_board.add(python_board[row][column])
                java_board.add(row_board)
            tic = time.time()
            
            move = playerTurn.get_move(java_board, playerTurn.get_symbole())
            toc = time.time()
            x, y = move[0], move[1]
            grid.update(x, y, playerTurn.get_symbole())
            gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
            print("Player1 (Black,JAVA), move is:",x,y)
        #3.if player1 written in Python
        elif p1_language=="PYTHON":
            tic = time.time()
            
            move = playerTurn.get_move(grid.grid, playerTurn.get_symbole())
            toc = time.time()
            x, y = move[0], move[1]
            grid.update(x, y, playerTurn.get_symbole())
            gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
            print("Player1 (Black,PYTHON), move is:",x,y)
        # if player1 is human
        else:
            # Get the human player input
            tic = time.time()
            x, y = gui.playerInput(screen)
            # Check if the cell is not already used
            while not grid.isMoveAllowed(x, y):
                x, y = gui.playerInput(screen)
            toc = time.time()
            grid.update(x, y, playerTurn.symbole)
            gui.drawSymbole(screen, (x, y), playerTurn.symbole)
            print("Player1 (Black,Human), move is:",x,y)
        print("Player1 (Black) Time:", (toc - tic))
        if (toc - tic) > TIME_LIMIT:
            print("Timed out, game over. Player2 wins.")
            return "-1"

    while(not gridFull(grid.grid)):
        # Switch player
        playerTurn = switchPlayer(playerTurn)

        # Check player is player1 or player2
        if(playerTurn.get_isAI()):
     
            #if player2 written in c++
            if p2_language =="CPP":
                python_board=grid.grid
                char_arr2 = ctypes.c_char*6
                char_arr22 = char_arr2*6
                cpp_board = char_arr22()
                for row in range(6):
                    for column in range(6):
                        if python_board[row][column]=="X":
                            cpp_board[row][column]=c_char(b"X")
                        elif python_board[row][column]=="O":
                            cpp_board[row][column]=c_char(b"O")
                cpp_symbole= playerTurn.get_symbole()
                tic = time.time()
                move = playerTurn.get_move(cpp_board, cpp_symbole)
                toc = time.time()
                x, y = move.contents[0],move.contents[1]
                grid.update(x, y, chr(playerTurn.get_symbole()))
                gui.drawSymbole(screen, (x,y), chr(playerTurn.get_symbole()))

                print("Player2 (Red,C++), move is:",x,y)
            #if player2 written in JAVA
            elif p2_language=="JAVA":
                python_board=grid.grid
                java_board = java.util.ArrayList()
                for row in range(6):
                    row_board= java.util.ArrayList()
                    for column in range(6):
                        row_board.add(python_board[row][column])
                    java_board.add(row_board)
                tic = time.time()
                move = playerTurn.get_move(java_board, playerTurn.get_symbole())
                toc = time.time()
                x, y = move[0], move[1]
                grid.update(x, y, playerTurn.get_symbole())
                gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
                print("Player2 (Red,JAVA), move is:",x,y)
            else:
                tic = time.time()
                move = playerTurn.get_move(grid.grid, playerTurn.get_symbole())
                toc = time.time()
                x, y = move[0], move[1]
                grid.update(x, y, playerTurn.get_symbole())
                gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
                print("Player2 (Red,Python), move is:",x,y)
            

            #check the score
            p_score = alignement(grid.grid,x,y)
            playerTurn.add_score(p_score)
            gui.writeScreen_4_show(screen, "[P1(Black)]:"+str(p1.get_score())+"    [P2(Red)]:"+str(p2.get_score()), line=4)
            print("Current score for player1 (black), player2 (red):",p1.get_score(),p2.get_score())

            print("Player2 (Red) Time:", (toc - tic))
            if (toc - tic) > TIME_LIMIT:
                print("Timed out, game over.Player1 wins.")
                return "-2"
        # if the player is player1
        else:
            # check the type of player1
            if p1_language =="CPP":
                python_board=grid.grid
                char_arr2 = ctypes.c_char*6
                char_arr22 = char_arr2*6
                cpp_board = char_arr22()
                for row in range(6):
                    for column in range(6):
                        if python_board[row][column]=="X":
                            cpp_board[row][column]=c_char(b"X")
                        elif python_board[row][column]=="O":
                            cpp_board[row][column]=c_char(b"O")	

                cpp_symbole= playerTurn.get_symbole()
                tic = time.time()
                move = playerTurn.get_move(cpp_board, cpp_symbole)
                toc = time.time()
                x, y = move.contents[0],move.contents[1]
                grid.update(x, y, chr(playerTurn.get_symbole()))
                gui.drawSymbole(screen, (x, y), chr(playerTurn.get_symbole()))
                print("Player1 (Black,C++), move is:",x,y)

            #2.if AI written in JAVA
            elif p1_language=="JAVA":
                python_board=grid.grid
                java_board = java.util.ArrayList()
                for row in range(6):
                    row_board= java.util.ArrayList()
                    for column in range(6):
                        row_board.add(python_board[row][column])
                    java_board.add(row_board)
                tic = time.time()
                
                move = playerTurn.get_move(java_board, playerTurn.get_symbole())
                toc = time.time()
                x, y = move[0], move[1]
                grid.update(x, y, playerTurn.get_symbole())
                gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
                print("Player1 (Black,JAVA), move is:",x,y)
            #3.if AI written in Python
            elif p1_language=="PYTHON":
                tic = time.time()
                
                move = playerTurn.get_move(grid.grid, playerTurn.get_symbole())
                toc = time.time()
                x, y = move[0], move[1]
                grid.update(x, y, playerTurn.get_symbole())
                gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
                print("Player1 (Black,PYTHON), move is:",x,y)
            else:
                # Get the human player input
                tic = time.time()
                x, y = gui.playerInput(screen)
                # Check if the cell is not already used
                while not grid.isMoveAllowed(x, y):
                    x, y = gui.playerInput(screen)
                toc = time.time()
                grid.update(x, y, playerTurn.symbole)
                gui.drawSymbole(screen, (x, y), playerTurn.symbole)
                print("Player1 (Black,Human), move is:",x,y)

           
            #check the score
            p_score = alignement(grid.grid,x,y)
            playerTurn.add_score(p_score)
            print("Current score for player1 (black), player2 (red):",p1.get_score(),p2.get_score())
            gui.writeScreen_4_show(screen, "[P1(Black)]:"+str(p1.get_score())+"    [P2(Red)]:"+str(p2.get_score()), line=4)
            
            print("Player1 (Black) Time:", (toc - tic))
            if (toc - tic) > TIME_LIMIT:
                print("Timed out, game over. Player2 wins.")
                return "-1"

        print("------------------------------------------")

    
    if(p1.get_score()>p2.get_score()):
        return "Black"

    elif(p1.get_score()<p2.get_score()):
        return "Red"
    else:
        return "0"

if __name__ == "__main__":

    # p1_language= {Human,CPP, JAVA,PYTHON}
    # The 'Human' mode is used for testing your ai algorithm
    p1_language=sys.argv[1]
    
    # p2_language ={CPP, JAVA,PYTHON}
    p2_language=sys.argv[2]
    
    #player1 canbe a human player or a AI player
    if p1_language=="Human":
        p1 = Player("human", "X")
        print("the first player is huamn")
    elif p1_language =="CPP":
        print("the first player is AI (C++)")
        p1 = CDLL('./cpp/aiplayer1.so')
        p1.add_symbole(c_char(b"X"))
        p1.add_isAI(False)
        p1.get_move.restype = ctypes.POINTER(ctypes.c_int*2)
    elif p1_language=="JAVA":
        import jpype
        from jpype import *
        print("the first player is AI (JAVA)")
        jarpath = os.path.join(os.path.abspath('.'), 'java/AIPlayer.jar')
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)
        AIPlayer = jpype.JClass('com.AIPlayer')
        p1 = AIPlayer()
        p1.add_symbole("X")
        p1.add_isAI(False)
    else:
        print("the first player is AI (PYTHON)")
        from python.AIPlayer import AIPlayer
        p1 = AIPlayer("AI1", "X", isAI=False)


    #player2 is an AI player, which can be implemented by C++, Java or Python
    if p2_language =="CPP":
        print("the second player is AI (C++)")
        p2 = CDLL('./cpp/aiplayer.so')
        p2.add_symbole(c_char(b"O"))
        p2.add_isAI(True)
        p2.get_move.restype = ctypes.POINTER(ctypes.c_int*2)
    elif p2_language=="JAVA":
        print("the second player is AI (JAVA)")
        jarpath = os.path.join(os.path.abspath('.'), 'java/AIPlayer.jar')
        if p1_language!="JAVA":
            import jpype
            from jpype import *
            jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)
        AIPlayer = jpype.JClass('com.AIPlayer')
        p2 = AIPlayer()
        p2.add_symbole("O")
    else:
        print("the second player is AI (PYTHON)")
        from python.AIPlayer import AIPlayer
        p2 = AIPlayer("AI2", "O", isAI=True)
        
    screen = gui.init()
    #determine the first player
    whoplayfirst=sys.argv[3]
    if True:

        # Start the game loop
        winner = gameLoop(screen, p1, p2)

        if(winner == "Black" or winner=="Red"):
            gui.writeScreen(screen, winner+" Won", line=1)
        elif(winner=="-1"):
            gui.writeScreen(screen, "TIME OUT", line=1)
            gui.writeScreen(screen, "P2(R) wins", line=2)
        elif(winner=="-2"):
            gui.writeScreen(screen, "TIME OUT", line=1)
            gui.writeScreen(screen, "P1(B) wins", line=2)
        else:
            gui.writeScreen(screen, "Draw!", line=1)

##        gui.writeScreen(screen, "Click to", line=2)
        gui.ask(screen, " Exit!", line=3)
        gui.clearScreen(screen)
    if p1_language =="JAVA" or p2_language=="JAVA":
        jpype.shutdownJVM()


