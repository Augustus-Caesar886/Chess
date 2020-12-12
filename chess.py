import random, sys, copy, os, pygame
from pygame.locals import *


pygame.init()

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH/2)
HALF_WINHEIGHT = int(WINHEIGHT/2)
FPSClock = pygame.time.Clock()


TILESIZE = 50

BRIGHTBLUE =  ( 0, 170, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (165, 42, 42)
CREAM = (255, 250, 204)
BGCOLOR = BRIGHTBLUE

KING = "KING"
QUEEN = "QUEEN"
BISHOP = "BISHOP"
KNIGHT = "KNIGHT"
ROOK = "ROOK"
PAWN = "PAWN"
NONE = "NONE"

class Piece:
    row = 0
    column = 0
    piece_type = NONE
    color = BLACK
    alive = True
    selected = False
    
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color 
    
    def kill(self):
        alive = False

REPEATEDPIECES = [ROOK, KNIGHT, BISHOP]

def init_board():
    board = [[Piece(NONE, BLACK) for i in range(8)] for i in range(8)]
    for i in range(3):
        board[0][i] = board[0][7-i] = Piece(REPEATEDPIECES[i % 3], BLACK)
        board[0][i].row = board[0][7-i].row = 0
        board[0][i].column = i
        board[0][7-i].column = 7-i
        
    for i in range(3):
        board[7][i] = board[7][7-i] = Piece(REPEATEDPIECES[i % 3], WHITE)
        board[7][i].row = board[7][7-i].row = 7
        board[7][i].column = i
        board[7][7-i].column = 7-i
    
    board[0][4] = Piece(KING, BLACK)
    board[0][4].row = 0
    board[0][4].column = 4
    board[7][4] = Piece(KING, WHITE)
    board[7][4].row = 0
    board[7][4].column = 4
    
    board[0][5] = Piece(QUEEN, BLACK)
    board[0][5].row = 0
    board[0][5].column = 4
    board[7][5] = Piece(QUEEN, WHITE)
    board[7][5].row = 0
    board[7][5].column = 4
    
    for i in range(8):
        board[1][i] = Piece(PAWN, BLACK)
        board[1][i].row = 1
        board[1][i].column = i
    
    for i in range(8):
        board[6][i] = Piece(PAWN, BLACK)
        board[6][i].row = 6
        board[6][i].column = i


board = init_board()

def draw_board(DISPLAYSURF):
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(DISPLAYSURF, CREAM if (8 * i + j) % 2 == 0 else BROWN, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))
    pygame.display.update()
    FPSClock.tick(FPS)
    
def main():
    while True:
        DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        draw_board(DISPLAYSURF)
        pygame.display.update()
        FPSClock.tick(FPS)
main()