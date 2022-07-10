from __future__ import print_function
from tetrominoes import *
import copy
import random

HOLO = -1
FILLED = 1
EMPTY = 0
LEFT = -1
RIGHT = 1

GRID_WIDTH = 11
GRID_HEIGHT = 26
GRID_HOLD_NEXT_WIDTH = 5
GRID_HOLD_NEXT_HEIGHT = 21
#when the threshold at row 21 (from bottom up) is acheive, it is game over
#i think the intend qould be to have a 24 tall grid with top 4 being threshold/buffer limit

class Game():
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [ [0]*10 for i in range(25) ]
        self.currentPiece = self.generatePiece()
        self.orient = 0
        self.holdPiece = None
        self.nextPieces = [self.generatePiece(), self.generatePiece(), self.generatePiece(), self.generatePiece()]  #array of 4
        self.gameOver = False
        self.horizontal = 3
        self.NHasBoard = self.makeNHBoard()

    def printBoard(self):
        for row in self.grid:
            print(row)

    def printNexts(self):
        for next in self.nextPieces:
            print("Begin Piece of Next")
            for row in next[0]:
                print(row)

    def makeNHBoard(self):
        nahBoard = []
        if self.holdPiece == None:
            nahBoard.append( [0]*4 )
            nahBoard.append( [0]*4 )
            nahBoard.append( [0]*4 )
            nahBoard.append( [0]*4 )
        else:
            for holdrow in self.holdPiece[0]:
                nahBoard.append(holdrow)

        for npiece in self.nextPieces:
            for nextrow in npiece[0]:
                nahBoard.append(nextrow)
        return nahBoard

    def regenerateNHBoard(self):
        self.NHasBoard = self.makeNHBoard()

    def gettingNext(self):
        #making the "first element" of next array be the current
        #and make a queue
        #so pop[0] into current, and append for the end
        self.currentPiece = self.nextPieces.pop(0)
        self.nextPieces.append(self.generatePiece())
        self.NHasBoard = self.makeNHBoard()

    def movePiece(self, direction):
        #move the piece? HOLO? left or right one unit
        checkLR = self.canLorR(direction, self.currentPiece[self.orient], self.grid)
        if checkLR == True:
            self.horizontal = self.horizontal + direction

    def canLorR(self, direction, summon, boardState):
        for r in range(len(summon)):
            for c in range(len(summon[r])):
                if not summon[r][c] == EMPTY:
                    rightCheck = (c+self.horizontal+direction < len(boardState[r]))
                    leftCheck = (c+self.horizontal+direction > -1)
                    if not (rightCheck and leftCheck):
                        return False
        return True

    def resetAfterPlace(self):
        self.horizontal = 3
        self.orient = 0

    def holoPlace(self):
        #visually, it puts a HOLO piece that symbolize where it would be
        #idea --> check from bottom up of the piece "grid" and see if it collides
        #on board state. if no collide (be it bottom line or FILLED pieces) move
        #the HOLO piece downwards

        goDowned = self.calculateGoDown(self.currentPiece[self.orient], self.grid, self.horizontal)
        for r in range(len(self.currentPiece[self.orient])):
            for c in range(len(self.currentPiece[self.orient])):
                if not self.currentPiece[self.orient][r][c] == 0:
                    self.grid[r+goDowned][c+self.horizontal] = HOLO

    #removes the holo piece for an updated version on left or right moves
    def removeHOLO(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == HOLO:
                    self.grid[r][c] = EMPTY

    def calculateGoDown(self, summon, boardState, moveRight):
            goDown = 0
            breakOut = False
            while True:
                for r in range(len(summon)):
                    for c in range(len(summon[r])):
                        if not summon[r][c] == 0:
                            if r+goDown+1 < len(boardState):
                                if not boardState[r+goDown+1][c+moveRight] == EMPTY: #meaning future move will collide
                                    breakOut = True
                                    break
                            else:
                                breakOut = True
                                break
                        if breakOut == True:
                            break
                    if breakOut == True:
                        break
                if breakOut == True:
                    break
                goDown += 1
            return goDown

    def placePiece(self):
        #full confirm the location of the HOLO piece
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == HOLO:
                    self.grid[r][c] = FILLED

    def lineClearSet(self):
        rowsFilled = self.checkLineFILLED()
        for row in rowsFilled:
            self.clearLine(row)
        rowsEmptied = self.checkLineEMPTY(rowsFilled)
        for row in rowsEmptied:
            self.collapseLines(row)

    def checkLineFILLED(self):
        #Go through all rows
        #if row is full, call clearline on row
        #after checking all rows, check again and see EMPTY

        #change of plans 6/25/22, to make things easier and prevent overextended loops
        #in clear line, check line empty, and collapseLines
        #return a mini array of lines that were filled
        arrayLinesFilled = []
        for r in range(len(self.grid)):
            filledCounter = 0
            for c in range(len(self.grid[r])):
                if self.grid[r][c] > 0:
                    filledCounter += 1
            if filledCounter == len(self.grid[r]):
                arrayLinesFilled.append(r)
        return arrayLinesFilled

    def clearLine(self, rowNumber):
        #emtpy out all element in that row
        #then force all rows above to go downwars 1? layer
        #(above is now delagated to checkLineEMPTY and collapseLines)
        #row 19 is top, 0 is bottom

        #6/25/22 given checkLineFILLED, the "main" will iterate through that and then
        #put in a row number into this method
        for c in range(len(self.grid[rowNumber])):
            self.grid[rowNumber][c] -= 1

    def checkLineEMPTY(self, arrayFilled):
        #check all rows and see if empty
        #if row is empty, collapse lines
        #if row n is cleared, rows n+1 goes downward where n+1 is now new n

        #6/25/22 checks the arrayFilled and then see if there is a total wipeout
        #then it returns another array of the total wipeout from filled
        arrayLinesEMPTY = []
        for row in arrayFilled:
            if self.grid[row].count(EMPTY) == len(self.grid[row]):
                #all spots are not empty/filled in some way
                arrayLinesEMPTY.append(row)
        return arrayLinesEMPTY

    def collapseLines(self, rowNumber):
        #given that row is empty, we collapse lines
        #such that rows above move downward
        #so it be like this:
        #rows above move downward one, the top row then becomes a 0 row
        #becasue of current formatting, 0 is the top row, and 19 is the bottom row
        #so rows n-1 goes downward
        currRowNum = rowNumber
        #the collapsing part up to top row
        while currRowNum > 0:
            self.grid[currRowNum] = self.grid[currRowNum - 1]
            currRowNum -= 1
        self.grid[0] = [0]*10
        #this part is when reach top row, and becasue nothing as index -1, we set 0 as an empty


    def spinPiece(self, direction):
        self.orient = (self.orient + direction) % 4
        self.horizontal = 3
        #i put resert horizontal here as a measure as it would prevent out of index bounds
        #each peice whill have their own arrangement pattern in an array thing
        #spin piece will cycle through the array of the piece

    def holdAndSwap(self):
        #if hold is EMPTY, store piece into hold
        #maybe outside of this, if piece is none, next becomes current piece
        #else (hold is not EMPTY), swap pieces
        if self.holdPiece == None:
            self.holdPiece = self.currentPiece
            self.currentPiece = self.generatePiece()
        else:
            tempholder = self.holdPiece
            self.holdPiece = self.currentPiece
            self.currentPiece = tempholder
        self.horizontal = 3

    def generatePiece(self):
        #given the list of pieces, randomly picks one out
        returnPiece = random.choice(setofRandompieces)
        return returnPiece

    def checkFail(self):
        #checks if any piece or elements is in a threshold row and return true if yes, false if no
        for row in range(5):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] > 0:
                    self.gameOver = True

    def modForceDown(self):
        for col in range(len(self.grid[0])):
            for row in range(len(self.grid) - 1):
                #from bottom up, it is 25 - index - 1
                #going from bottom row to top-1 row
                #if lower row has a 0, go up until find a non zero row
                #if go through all rows with out finding a nonzero row, indicate a
                #break out of row loop
                restZeros = False
                if self.grid[25 - row - 1][col] == 0:
                    #do swap thing
                    initialCounter = 25 - row - 2
                    while self.grid[initialCounter][col] == 0:
                        initialCounter -= 1
                        if initialCounter < 0:
                            restZeros = True
                            break
                    if restZeros == True:
                        break
                    else:
                        swapHold = self.grid[initialCounter][col]
                        self.grid[initialCounter][col] = self.grid[25 - row - 1][col]
                        self.grid[25 - row - 1][col] = swapHold

    def modForceLeft(self):
        for row in range(len(self.grid)):
            numZeros = self.grid[row].count(0)
            for counter in range(numZeros):
                self.grid[row].remove(0)
            for counter in range(numZeros):
                self.grid[row].append(0)

    #def modThirdDspin(self):
        #After contemplation: I will not be Incorporating this mechanic
        #7/3/22
