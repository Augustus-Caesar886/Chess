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
    moves = 0
    
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color 
    
    def kill(self):
        self.alive = False
    
    def assimilate(self, piece):
        board[piece.row][piece.column] = Piece(NONE, NONE)
        board[piece.row][piece.column].row = piece.row
        board[piece.row][piece.column].column = piece.column
        piece.row = self.row
        piece.column = self.column
        board[self.row][self.column] = piece
        
        self.alive = False
    

REPEATEDPIECES = [ROOK, KNIGHT, BISHOP]

def init_board():
    board = [[Piece(NONE, NONE) for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            board[i][j].row = i
            board[i][j].column = j
            
    for i in range(3):
        board[0][i] = Piece(REPEATEDPIECES[i % 3], BLACK)
        board[0][7-i] = Piece(REPEATEDPIECES[i % 3], BLACK)
        board[0][i].row = board[0][7-i].row = 0
        board[0][i].column = i
        board[0][7-i].column = 7-i
        
    for i in range(3):
        board[7][i] = Piece(REPEATEDPIECES[i % 3], WHITE)
        board[7][7-i] = Piece(REPEATEDPIECES[i % 3], WHITE)
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
    return Piece(NONE, NONE)

def get_vertical_dist(piece, tile):
    return -(tile[0] - piece.row )

def get_horizontal_dist(piece, tile):
    return (tile[1] - piece.column)

def check_valid_move(piece, tile):
    if piece.color == board[tile[0]][tile[1]].color:
        return False
    
    if piece.piece_type == PAWN:
        
        if (((get_vertical_dist(piece, tile) == ( 1 if piece.color == WHITE else -1 ) or (get_vertical_dist(piece, tile) == (2 if piece.color == WHITE else -2) and piece.moves == 0)) and get_horizontal_dist(piece, tile)==0)) and board[tile[0]][tile[1]].color == NONE:
            return True
        else:
            if(board[tile[0]][tile[1]].color != turn and board[tile[0]][tile[1]].color != NONE ):
                if(int(get_vertical_dist(piece, tile) == 1) and abs(get_horizontal_dist(piece, tile)) == 1 and piece.color == WHITE): #TODO: implement for black pawn
                    return True
                elif(int(get_vertical_dist(piece, tile) == -1) and abs(get_horizontal_dist(piece, tile)) == 1 and piece.color == BLACK):
                    return True
            return False
    elif piece.piece_type == ROOK:
        if((get_vertical_dist(piece, tile) != 0 and get_horizontal_dist(piece, tile)==0) or (get_vertical_dist(piece, tile) == 0 and get_horizontal_dist(piece, tile)!=0)):
            xdir = 0
            ydir = 0
            length = 0
            length = max(abs(get_horizontal_dist(piece, tile)), abs(get_vertical_dist(piece, tile)))
            if(get_horizontal_dist(piece, tile) > 0):
                xdir = 1
            elif get_horizontal_dist(piece, tile) < 0:
                xdir = -1
            if get_vertical_dist(piece, tile) > 0:
                ydir = -1
            elif get_vertical_dist(piece, tile) < 0:
                ydir = 1
            if check_line_validity(piece.row, piece.column, xdir, ydir, length):
                return True
            else:
                return False
        else:
            return False
    elif piece.piece_type == BISHOP:
        if( abs(get_vertical_dist(piece, tile)) == abs(get_horizontal_dist(piece, tile)) and (get_vertical_dist(piece, tile) != 0 )):
            xdir = 0
            ydir = 0
            length = max(abs(get_horizontal_dist(piece, tile)), abs(get_vertical_dist(piece, tile)))
            if(get_horizontal_dist(piece, tile) > 0):
                xdir = 1
            elif get_horizontal_dist(piece, tile) < 0:
                xdir = -1
            if get_vertical_dist(piece, tile) > 0:
                ydir = -1
            elif get_vertical_dist(piece, tile) < 0:
                ydir = 1
            if check_line_validity(piece.row, piece.column, xdir, ydir, length):
                return True
            else:
                return False
        else:
            return False 
    elif piece.piece_type == KNIGHT:
        if( (abs(get_vertical_dist(piece, tile)) == 2 and abs(get_horizontal_dist(piece, tile)) == 1) or (abs(get_vertical_dist(piece, tile)) == 1 and abs(get_horizontal_dist(piece, tile)) == 2) ):
            return True
        else:
            return False
    elif piece.piece_type == QUEEN:
        if( (abs(get_vertical_dist(piece, tile)) == abs(get_horizontal_dist(piece, tile))) or  ((get_vertical_dist(piece, tile) != 0 and get_horizontal_dist(piece, tile)==0) or (get_vertical_dist(piece, tile) == 0 and get_horizontal_dist(piece, tile)!=0))):
            xdir = 0
            ydir = 0
            length = 0
            length = max(abs(get_horizontal_dist(piece, tile)), abs(get_vertical_dist(piece, tile)))
            if(get_horizontal_dist(piece, tile) > 0):
                xdir = 1
            elif get_horizontal_dist(piece, tile) < 0:
                xdir = -1
            if get_vertical_dist(piece, tile) > 0:
                ydir = -1
            elif get_vertical_dist(piece, tile) < 0:
                ydir = 1
            if check_line_validity(piece.row, piece.column, xdir, ydir, length):
                return True
            else:
                return False
        else:
            return False
    elif piece.piece_type == KING:
        if( (abs(get_vertical_dist(piece, tile)) + abs(get_horizontal_dist(piece, tile)) == 1) or (abs(get_vertical_dist(piece, tile)) == abs(get_horizontal_dist(piece, tile)) and abs(get_vertical_dist(piece, tile)) == 1)):
            return True
    
    return False

def check_line_validity(piecerow, piececol, xdir, ydir, length):
    if piecerow + (ydir*length) >= 8 or piecerow + (ydir*length) < 0:
        return False
    if piececol + (xdir*length) >= 8 or piececol + (xdir*length) < 0:
        return False
        
    
    for i in range(length):
        if (board[piecerow + (i+1) * ydir][piececol + (i+1) * xdir].piece_type != NONE):
            
            if(i == length-1 and (board[piecerow + (i+1) * ydir][piececol + (i+1) * xdir].color != turn)):
                return True
            else:
                return False    
    return True

CHECKMATE = "CHECKMATE"
CHECK = "CHECK"
SAFE = "SAFE"

def find_king(color):
    king_row = -1
    king_col = -1
    for i in range(8):
        for j in range(8):
            if board[i][j].piece_type == KING and board[i][j].color == color:
                king_row = board[i][j].row
                king_col = board[i][j].column
    return (king_col, king_row)

def invert_color(color):
    return WHITE if color == BLACK else (BLACK if color == WHITE else NONE)

def display_turn():
    msg = "Turn: " + ("WHITE" if turn == WHITE else "BLACK")
    font = pygame.font.Font("freesansbold.ttf", 16)
    text = font.render(msg, True, WHITE)
    textRect = text.get_rect()
    textRect.topleft = (8 * TILESIZE, 0)
    DISPLAYSURF.blit(text, textRect)

def check_pawn_status():
    for i in range(2):
        for j in range(8):
            if board[i*7][j].piece_type == PAWN:
                return board[i*7][j]
    return Piece(NONE, NONE)

PAWN_UPGRADES = [WHITE_ROOK, WHITE_BISHOP, WHITE_KNIGHT, WHITE_QUEEN]

def display_pawn_upgrades():
    coords = (int(8.5 * TILESIZE), TILESIZE)
    length = len(PAWN_UPGRADES)
    height = TILESIZE
    pygame.draw.rect(DISPLAYSURF, CREAM, (coords[0], coords[1], length*TILESIZE, height))
    for i in range(length):
        DISPLAYSURF.blit(PAWN_UPGRADES[i], (coords[0] + i * TILESIZE,coords[1]))

def await_pawn_choice(pawn):
    upgrade_coords = (int(8.5 * TILESIZE), TILESIZE)
    choice = NONE
    while(choice == NONE):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mousecoords = pygame.mouse.get_pos()
                rook_upgrade = pygame.Rect(upgrade_coords[0], upgrade_coords[1], TILESIZE, TILESIZE);
                bishop_upgrade = pygame.Rect(upgrade_coords[0] + TILESIZE, upgrade_coords[1], TILESIZE, TILESIZE);
                knight_upgrade = pygame.Rect(upgrade_coords[0] + (2 * TILESIZE), upgrade_coords[1], TILESIZE, TILESIZE);
                queen_upgrade = pygame.Rect(upgrade_coords[0] + (3 * TILESIZE), upgrade_coords[1], TILESIZE, TILESIZE);
                
                if(rook_upgrade.collidepoint(mousecoords)):
                    choice = ROOK
                elif (bishop_upgrade.collidepoint(mousecoords)):
                    choice = BISHOP
                elif (knight_upgrade.collidepoint(mousecoords)):
                    choice = KNIGHT
                elif (queen_upgrade.collidepoint(mousecoords)):
                    choice = QUEEN
        draw_board()
        pygame.display.update()
        FPSClock.tick(FPS)
    pawn.piece_type = choice

def count_non_kings():
    count = 0
    for i in range(8):
        for j in range(8):
            if(board[i][j].piece_type != NONE and board[i][j].piece_type != KING):
                count += 1
    return count

def missing_king():
    king_coords = find_king(WHITE)
    if(king_coords == (-1, -1)):
        return "BLACK" #Which side wins
    king_coords = find_king(BLACK)
    if(king_coords == (-1, -1)):
        return "WHITE"
    return NONE

def game_over_screen(gamestate):
    msg = ""
    if(gamestate != NONE):
        msg = "Winner: " + gamestate
    else:
        msg = "Stalemate"
    font = pygame.font.Font("freesansbold.ttf", 16)
    text = font.render(msg, True, WHITE)
    textRect = text.get_rect()
    textRect.topleft = (9 * TILESIZE, 0)
    
    button_msg = "Reset"
    button_txt = font.render(button_msg, True, WHITE)
    button_txt_rect = text.get_rect()
    button_txt_rect.topleft = (9 * TILESIZE, TILESIZE)
    
    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect((0, 0), (WINWIDTH, WINHEIGHT)))
    
    cont = False
    while(not(cont)):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mousecoords = pygame.mouse.get_pos()
                if button_txt_rect.collidepoint(mousecoords):
                    cont = True
        if(not(cont)):
            draw_board()
            DISPLAYSURF.blit(text, textRect)
            pygame.draw.rect(DISPLAYSURF, GREEN, button_txt_rect);
            DISPLAYSURF.blit(button_txt, button_txt_rect)
            FPSClock.tick(FPS)
            pygame.display.update()
        else:
            pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect((0, 0), (WINWIDTH, WINHEIGHT)))
            draw_board()
            FPSClock.tick(FPS)
            pygame.display.update()
    

def main():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    global selectedTile, selectedPiece
    selectedTile = (-1, -1)
    selectedPiece = Piece(NONE, NONE)
    selectedPiece.row = -1
    selectedPiece.column = -1
    global turn
    turn = WHITE
    gameover = False
    winner = NONE
    
    global board 
    board = init_board()
    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect((0, 0), (WINWIDTH, WINHEIGHT)))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                tile = get_selected(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if tile.piece_type != NONE and turn == tile.color and tile.alive:
                    selectedPiece = tile
                    selectedPiece.selected = True
                else: 
                    selectedTile = (tile.row, tile.column)
                    board[selectedTile[0]][selectedTile[1]].selected = True
        if(gameover):
            pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect((0, 0), (WINWIDTH, WINHEIGHT)))
            draw_board();
            game_over_screen(winner)
            board = init_board()
            turn = WHITE
            winner = NONE
            gameover = False
        elif selectedPiece.row != -1 and selectedPiece.column != -1 and selectedTile != (-1, -1):
            if check_valid_move(selectedPiece, selectedTile):
                if(board[selectedTile[0]][selectedTile[1]].piece_type != NONE):
                    board[selectedTile[0]][selectedTile[1]].kill()
                board[selectedTile[0]][selectedTile[1]].assimilate(selectedPiece)
                board[selectedTile[0]][selectedTile[1]].moves += 1
                if turn == WHITE:
                    turn = BLACK
                else:
                    turn = WHITE
                pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect((0, 0), (WINWIDTH, WINHEIGHT)))
                upgrade_pawn = check_pawn_status()
                if upgrade_pawn.piece_type != NONE:
                    display_pawn_upgrades()
                    await_pawn_choice(upgrade_pawn)
                    draw_board()
                    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect((0, 0), (WINWIDTH, WINHEIGHT)))
            else:
                selectedPiece = Piece(NONE, NONE)
                selectedPiece.row = -1
                selectedPiece.column = -1
                selectedTile = (-1, -1)
        elif(count_non_kings() == 0):
            gameover = True
        elif(missing_king() != NONE):
            winner = missing_king()
            gameover = True
        draw_board()
        display_turn()
        pygame.display.update()
        FPSClock.tick(FPS)
main()