import random, sys, copy, os, pygame
from pygame.locals import *


pygame.init()

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH/2)
HALF_WINHEIGHT = int(WINHEIGHT/2)
FPSClock = pygame.time.Clock()


TILESIZE = 60

BRIGHTBLUE =  ( 0, 170, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (165, 42, 42)
CREAM = (255, 250, 204)
GREEN = (0, 255, 0)
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
    color = NONE
    alive = True
    selected = False
    
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color 
    
    def kill(self):
        self.alive = False
        
    

REPEATEDPIECES = [ROOK, KNIGHT, BISHOP]

def init_board():
    board = [[Piece(NONE, NONE) for i in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j].row = i
            board[i][j].column = j
            
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
    
    board[0][3] = Piece(KING, BLACK)
    board[0][3].row = 0
    board[0][3].column = 3
    board[7][3] = Piece(KING, WHITE)
    board[7][3].row = 7
    board[7][3].column = 3
    
    board[0][4] = Piece(QUEEN, BLACK)
    board[0][4].row = 0
    board[0][4].column = 4
    board[7][4] = Piece(QUEEN, WHITE)
    board[7][4].row = 7
    board[7][4].column = 4
    
    for i in range(8):
        board[1][i] = Piece(PAWN, BLACK)
        board[1][i].row = 1
        board[1][i].column = i
    
    for i in range(8):
        board[6][i] = Piece(PAWN, WHITE)
        board[6][i].row = 6
        board[6][i].column = i
    return board


board = init_board()

WHITE_PAWN = pygame.image.load("wp.png")
WHITE_ROOK = pygame.image.load("wr.png")
WHITE_BISHOP = pygame.image.load("wb.png")
WHITE_KNIGHT = pygame.image.load("wn.png")
WHITE_QUEEN = pygame.image.load("wq.png")
WHITE_KING = pygame.image.load("wk.png")

BLACK_PAWN = pygame.image.load("bp.png")
BLACK_ROOK = pygame.image.load("br.png")
BLACK_BISHOP = pygame.image.load("bb.png")
BLACK_KNIGHT = pygame.image.load("bn.png")
BLACK_QUEEN = pygame.image.load("bq.png")
BLACK_KING = pygame.image.load("bk.png")

def draw_board():
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(DISPLAYSURF, (CREAM if (i + j) % 2 == 0 else BROWN), (j * TILESIZE, i * TILESIZE, TILESIZE, TILESIZE))
            if i == selectedTile[0] and selectedTile[1] == j:
                pygame.draw.rect(DISPLAYSURF, GREEN, (j * TILESIZE, i * TILESIZE, TILESIZE, TILESIZE), 3)
            if i == selectedPiece.row and selectedPiece.column == j:
                pygame.draw.rect(DISPLAYSURF, GREEN, (j * TILESIZE, i * TILESIZE, TILESIZE, TILESIZE), 3)
            
            if(board[i][j].piece_type != NONE):
                if board[i][j].piece_type == PAWN:
                    if board[i][j].color == WHITE:
                        DISPLAYSURF.blit(WHITE_PAWN, (j * TILESIZE, i * TILESIZE))
                    elif board[i][j].color == BLACK:
                        DISPLAYSURF.blit(BLACK_PAWN, (j * TILESIZE, i * TILESIZE))
                elif board[i][j].piece_type == ROOK:
                    if board[i][j].color == WHITE:
                        DISPLAYSURF.blit(WHITE_ROOK, (j * TILESIZE, i * TILESIZE))
                    elif board[i][j].color == BLACK:
                        DISPLAYSURF.blit(BLACK_ROOK, (j * TILESIZE, i * TILESIZE))
                elif board[i][j].piece_type == BISHOP:
                    if board[i][j].color == WHITE:
                        DISPLAYSURF.blit(WHITE_BISHOP, (j * TILESIZE, i * TILESIZE))
                    elif board[i][j].color == BLACK:
                        DISPLAYSURF.blit(BLACK_BISHOP, (j * TILESIZE, i * TILESIZE))
                elif board[i][j].piece_type == KNIGHT:
                    if board[i][j].color == WHITE:
                        DISPLAYSURF.blit(WHITE_KNIGHT, (j * TILESIZE, i * TILESIZE))
                    elif board[i][j].color == BLACK:
                        DISPLAYSURF.blit(BLACK_KNIGHT, (j * TILESIZE, i * TILESIZE))
                elif board[i][j].piece_type == QUEEN:
                    if board[i][j].color == WHITE:
                        DISPLAYSURF.blit(WHITE_QUEEN, (j * TILESIZE, i * TILESIZE))
                    elif board[i][j].color == BLACK:
                        DISPLAYSURF.blit(BLACK_QUEEN, (j * TILESIZE, i * TILESIZE))
                elif board[i][j].piece_type == KING:
                    if board[i][j].color == WHITE:
                        DISPLAYSURF.blit(WHITE_KING, (j * TILESIZE, i * TILESIZE))
                    elif board[i][j].color == BLACK:
                        DISPLAYSURF.blit(BLACK_KING, (j * TILESIZE, i * TILESIZE))
                
                
    pygame.display.update()
    FPSClock.tick(FPS)

def get_selected(mousex, mousey):
    for i in range(8):
        for j in range(8):
            checkTile = pygame.Rect((j * TILESIZE, i * TILESIZE, TILESIZE, TILESIZE))
            if checkTile.collidepoint(mousex, mousey):
                return board[i][j]

def main():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    global selectedTile, selectedPiece
    selectedTile = (-1, -1)
    selectedPiece = Piece(NONE, NONE)
    selectedPiece.row = -1
    selectedPiece.column = -1
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                tile = get_selected(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if tile.piece_type != NONE:
                    selectedPiece = tile
                else: 
                    selectedTile = (tile.row, tile.column)
                
                
                
        draw_board()
        pygame.display.update()
        FPSClock.tick(FPS)
main()