#Filler main.py
from tetrominoes import *
from game import Game, GRID_WIDTH, GRID_HEIGHT, LEFT, RIGHT, GRID_HOLD_NEXT_WIDTH, GRID_HOLD_NEXT_HEIGHT

GRID_SIZE = 20
RADIUS = GRID_SIZE // 2
BOARD_START_X = 40
BOARD_START_Y = 50
EDGE_SIZE = GRID_SIZE//2
TEXT_POS = (10, 8)
MAIN_BOARD_WIDTH = 280

WHITE_COLOR = [255]*3
BLACK_COLOR = [0]*3
RED_COLOR = [255, 0, 0]
ORANGE_COLOR = [255, 128, 0]
YELLOW_COLOR = [255, 255, 0]
GREEN_COLOR = [0, 255, 0]
BLUE_COLOR = [0, 0, 255]
PURPLE_COLOR = [128, 0, 255]

COLOR_DICT = {
    -2 : GREEN_COLOR,
    -1 : WHITE_COLOR,
     1 : BLACK_COLOR,
     2 : YELLOW_COLOR,
     3 : ORANGE_COLOR,
     4 : RED_COLOR }
                #this would be representative of the amount of "level" of hardness
                #of a mino/grid section
                #0/empty is white, 1 is black, 2 is red, 3 orange etc

BORDER_COLOR = [0] * 3
BOARD_COLOR = [68, 101, 194]

TEXT_COLOR = [0] * 3
ACTIVE_COLOR = [0]*3

board = [ [0]*10 for i in range(25)]
board[24] = [1, 1, 0, 0, 1, 1, 1, 1, 1, 1]

class Tetris():
    def __init__(self, board):
        #self.board = [ [0]*10 for i in range(20)]
        #self.board[19] = [1, 1, 0, 0, 1, 1, 1, 1, 1, 1]
        pygame.init()
        self.screen = pygame.display.set_mode((280+160, 600))
        pygame.display.set_caption("Experimental Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("ariel",18)
        self.going = True
        #self.clock = pygame.time.Clock()

        self.game = Game(None, board)

    def printTheBoard(self):
        self.game.printBoard()

    def printTheNexts(self):
        self.game.printNexts()

    def loop(self):
        self.draw()
        while self.going:
            self.update()
            self.draw()
        pygame.quit()


    #current piece on board onscreen
    #show holoplacement
    #user inpute moves piece or rotates it, repeat onscreen and HOLO until placement
    #place piece, current piece is now "none"
    #check lines and clear any lines, award scoring
    #check lines and any EMPTY rows are "forced downward"
    #check if gameover/fail
    #next piece becomes current piece
    #generate piece for next peice
    def update(self):
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONDOWN:
                self.going = False
                print("exiting game")
            #keydown, s is hard drop, a is left move, d is right move
            if e.type == KEYDOWN:
                if e.key ==K_s:
                    #drop
                    print("s pressed")
                    self.game.placePiece()
                    #self.game.currentPiece = setofRandompieces[3][0]
                    #self.game.currentPiece = self.game.generatePiece()
                    self.game.gettingNext()
                    self.game.resetAfterPlace()
                    self.game.holoPlace()
                if e.key ==K_a:
                    #move left
                    print("a pressed")
                    self.game.removeHOLO()
                    self.game.movePiece(LEFT)
                    self.game.holoPlace()
                if e.key ==K_d:
                    #move right
                    print("d pressed")
                    self.game.removeHOLO()
                    self.game.movePiece(RIGHT)
                    self.game.holoPlace()
                if e.key ==K_q:
                    #rotate left (counter clock)
                    print("q pressed")
                    self.game.removeHOLO()
                    self.game.spinPiece(LEFT)
                    self.game.holoPlace()
                if e.key ==K_e:
                    #rotate right (clock)
                    print("e pressed")
                    self.game.removeHOLO()
                    self.game.spinPiece(RIGHT)
                    self.game.holoPlace()
                if e.key ==K_t:
                    print("t pressed")
                    self.game.removeHOLO()
                    self.game.holdAndSwap()
                    self.game.regenerateNHBoard()
                    self.game.holoPlace()
        self.game.lineClearSet()
        self.game.checkFail()


        #SPACER
        #self.game.current = setofRandompieces[3][0]
        #self.game.holoPlace()

    def draw(self):
        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, BOARD_COLOR,
                            [BOARD_START_X - EDGE_SIZE, BOARD_START_Y - EDGE_SIZE,
                            (GRID_WIDTH - 1) * GRID_SIZE + EDGE_SIZE * 2,
                            (GRID_HEIGHT - 1) * GRID_SIZE + EDGE_SIZE * 2], 0)

        # draw horizontal line for main board
        for r in range(GRID_HEIGHT):
            y = BOARD_START_Y + r * GRID_SIZE
            if r == 5:
                pygame.draw.line(self.screen, RED_COLOR, [BOARD_START_X, y],
                             [BOARD_START_X + GRID_SIZE * (GRID_WIDTH - 1), y], 2)
            else:
                pygame.draw.line(self.screen, ACTIVE_COLOR, [BOARD_START_X, y],
                             [BOARD_START_X + GRID_SIZE * (GRID_WIDTH - 1), y], 2)
        # draw vertical line for main board
        for c in range(GRID_WIDTH):
            x = BOARD_START_X + c * GRID_SIZE
            pygame.draw.line(self.screen, ACTIVE_COLOR, [x, BOARD_START_Y],
                             [x, BOARD_START_Y + GRID_SIZE * (GRID_HEIGHT - 1)], 2)

        # draw pieces/filled elements/minos for main board
        for r in range(GRID_HEIGHT - 1):
            for c in range(GRID_WIDTH - 1):
                minoType = self.game.grid[r][c]
                if minoType != 0:
                    #print("minotype number: ", minoType)
                    #there is an error where the holo peices trigger a line clear
                    mino_color = COLOR_DICT[minoType]
                    x = BOARD_START_X + (c * GRID_SIZE) + EDGE_SIZE
                    y = BOARD_START_Y + (r * GRID_SIZE) + EDGE_SIZE
                    specs = [(0, RADIUS, mino_color)]
                    for width, radius, color in specs:
                        pygame.draw.circle(self.screen, color, [x, y], radius, width)

        pygame.draw.rect(self.screen, PURPLE_COLOR,
                            [BOARD_START_X - EDGE_SIZE + MAIN_BOARD_WIDTH, BOARD_START_Y - EDGE_SIZE,
                            (GRID_HOLD_NEXT_WIDTH - 1) * GRID_SIZE + EDGE_SIZE * 2,
                            (GRID_HOLD_NEXT_HEIGHT - 1) * GRID_SIZE + EDGE_SIZE * 2], 0)

        # draw horizontal line for hold and next
        for r in range(GRID_HOLD_NEXT_HEIGHT):
            y = BOARD_START_Y + r * GRID_SIZE
            if (r % 4) == 0:
                pygame.draw.line(self.screen, GREEN_COLOR, [BOARD_START_X + MAIN_BOARD_WIDTH, y],
                                 [BOARD_START_X + MAIN_BOARD_WIDTH + GRID_SIZE * (GRID_HOLD_NEXT_WIDTH - 1), y], 2)
            else:
                pygame.draw.line(self.screen, ACTIVE_COLOR, [BOARD_START_X + MAIN_BOARD_WIDTH, y],
                             [BOARD_START_X + MAIN_BOARD_WIDTH + GRID_SIZE * (GRID_HOLD_NEXT_WIDTH - 1), y], 2)
        # draw vertical line for hold and next
        for c in range(GRID_HOLD_NEXT_WIDTH):
            x = BOARD_START_X + c * GRID_SIZE
            pygame.draw.line(self.screen, ACTIVE_COLOR, [x + MAIN_BOARD_WIDTH, BOARD_START_Y],
                             [x + MAIN_BOARD_WIDTH, BOARD_START_Y + GRID_SIZE * (GRID_HOLD_NEXT_HEIGHT - 1)], 2)

        # draw peices/minoes for the hold and next
        for r in range(GRID_HOLD_NEXT_HEIGHT - 1):
            for c in range(GRID_HOLD_NEXT_WIDTH - 1):
                minoType = self.game.NHasBoard[r][c]
                if minoType != 0:
                #if True:
                    #print("minotype number: ", minoType)
                    #there is an error where the holo peices trigger a line clear
                    mino_color = BLACK_COLOR #COLOR_DICT[minoType]
                    x = BOARD_START_X + MAIN_BOARD_WIDTH + (c * GRID_SIZE) + EDGE_SIZE
                    y = BOARD_START_Y + (r * GRID_SIZE) + EDGE_SIZE
                    specs = [(0, RADIUS, mino_color)]
                    for width, radius, color in specs:
                        pygame.draw.circle(self.screen, color, [x, y], radius, width)

        self.screen.blit(self.font.render("Testing text thing on tetris ", True, (0, 0, 0)), TEXT_POS)

        if self.game.gameOver:
            self.screen.blit(self.font.render("Game Over  ", True, (0, 0, 0)), TEXT_POS)

        pygame.display.update()




def quickReset(boardState):
    for row in range(len(boardState)):
        for col in range(len(boardState[row])):
            if boardState[row][col] == -1:
                boardState[row][col] = 0
    #return boardState

def calculateGoDown(summon, boardState, moveRight):
        goDown = 0
        breakOut = False
        while True:
            for r in range(len(summon)):
                for c in range(len(summon[r])):
                    if not summon[r][c] == 0:
                        #board[r][c] = tpiece[r][c]
                        if r+goDown+1 < len(boardState):
                            #print("r godown 1: ", r+goDown+1)
                            if not boardState[r+goDown+1][c+moveRight] == 0: #meaning future move will collide
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

if __name__ == '__main__':
    print("doing something right now to see ")
    #for row in tpiece:
    #    print(row)
    print("testing board ")
    for row in board:
        print(row)

    #for pieceType in setofRandompieces:
    #    print(" ")
    #    print("Begin piece ")
    #    print(" ")
    #    oreintNum = 1
    #    for orientation in pieceType:
    #        print(" ")
    #        print("Orientation ", oreintNum)
    #        print(" ")
    #        oreintNum += 1
    #        for row in orientation:
    #            print(row)
    #holoplace
    #visually, it puts a holo piece that symbolize where it would be
    #idea --> check from bottom up of the piece "grid" and see if it collides
    #on board state. if no collide (be it bottom line or filled pieces) move
    #the holo piece downwards
    #collide when a 1 on the piece would meet a 1 on the board or on row 19 (last row)

    summoned = setofRandompieces[2][1]
    goDowned = calculateGoDown(summoned, board, 0)
    #        #r+17 will cause out of bounds array issue so do a check thing
    #    #rowNum += 1
    ##board = board + tpiece
    for r in range(len(summoned)):
        for c in range(len(summoned[r])):
            if not summoned[r][c] == 0:
                board[r+goDowned][c] = -1
    print("updated board ")
    for row in board:
        print(row)

    #board =
    quickReset(board)
    print("updated after quick reset board ")
    for row in board:
        print(row)

    print("move right test: ")
    goDowned = calculateGoDown(summoned, board, 2)
    for r in range(len(summoned)):
        for c in range(len(summoned[r])):
            if not summoned[r][c] == 0:
                board[r+goDowned][c+2] = -1
    print("updated board ")
    for row in board:
        print(row)

    print("testing Game instance: ")
    import pygame
    from pygame.locals import *
    newGame = Tetris(board)
    newGame.printTheBoard()
    newGame.printTheNexts()
    newGame.loop()
    #newGame.printBoard()
    #newGame.calculateGoDown
