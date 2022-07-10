from tetrominoes import *
from game import Game, GRID_WIDTH, GRID_HEIGHT, LEFT, RIGHT, GRID_HOLD_NEXT_WIDTH, GRID_HOLD_NEXT_HEIGHT

GRID_SIZE = 20
RADIUS = GRID_SIZE // 2
BOARD_START_X = 40
BOARD_START_Y = 50
EDGE_SIZE = GRID_SIZE//2
GAME_OVER = (10, 8)
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


class Tetris():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((280+160, 600))
        pygame.display.set_caption("Experimental Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("ariel",18)
        self.going = True
        self.game = Game()

    def printTheBoard(self):
        self.game.printBoard()

    def printTheNexts(self):
        self.game.printNexts()

    def loop(self):
        self.draw()
        self.game.holoPlace()
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
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    #Reset the game
                    self.game.reset()
                    self.game.removeHOLO()
                    self.game.holoPlace()
            if self.game.gameOver == False:
                if e.type == KEYDOWN:
                    if e.key == K_s:
                        #drop
                        self.game.placePiece()
                        self.game.gettingNext()
                        self.game.resetAfterPlace()
                        self.game.holoPlace()
                    if e.key == K_a:
                        #move left
                        self.game.removeHOLO()
                        self.game.movePiece(LEFT)
                        self.game.holoPlace()
                    if e.key ==K_d:
                        #move right
                        self.game.removeHOLO()
                        self.game.movePiece(RIGHT)
                        self.game.holoPlace()
                    if e.key == K_q:
                        #rotate left (counter clock)
                        self.game.removeHOLO()
                        self.game.spinPiece(LEFT)
                        self.game.holoPlace()
                    if e.key == K_e:
                        #rotate right (clock)
                        self.game.removeHOLO()
                        self.game.spinPiece(RIGHT)
                        self.game.holoPlace()
                    if e.key == K_t:
                        #hold/swap piece in hold
                        self.game.removeHOLO()
                        self.game.holdAndSwap()
                        self.game.regenerateNHBoard()
                        self.game.holoPlace()
                    if e.key == K_z:
                        #modification - force left
                        self.game.removeHOLO()
                        self.game.modForceLeft()
                        self.game.holoPlace()
                    if e.key == K_x:
                        #modification - force down
                        self.game.removeHOLO()
                        self.game.modForceDown()
                        self.game.holoPlace()
                self.game.lineClearSet()
                self.game.checkFail()


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
                    mino_color = BLACK_COLOR
                    x = BOARD_START_X + MAIN_BOARD_WIDTH + (c * GRID_SIZE) + EDGE_SIZE
                    y = BOARD_START_Y + (r * GRID_SIZE) + EDGE_SIZE
                    specs = [(0, RADIUS, mino_color)]
                    for width, radius, color in specs:
                        pygame.draw.circle(self.screen, color, [x, y], radius, width)


        self.screen.blit(self.font.render("A/D to move Left/Right ", True, (0, 0, 0)), (260 , 470))
        self.screen.blit(self.font.render("Q/E to rotate Counter/Clock ", True, (0, 0, 0)), (260 , 485))
        self.screen.blit(self.font.render("S to drop, T to Hold/Swap ", True, (0, 0, 0)), (260 , 500))
        self.screen.blit(self.font.render("Space to Reset game ", True, (0, 0, 0)), (260 , 515))
        self.screen.blit(self.font.render("Z/X to force board Left/Down ", True, (0, 0, 0)), (260 , 530))


        if self.game.gameOver:
            self.screen.blit(self.font.render("Game Over  ", True, (0, 0, 0)), GAME_OVER)

        pygame.display.update()


if __name__ == '__main__':
    import pygame
    from pygame.locals import *
    newGame = Tetris()
    newGame.loop()
