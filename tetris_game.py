import pygame

pygame.init()

WID, HEI=300,600
GRID_WID, GRID_HEI=10, 20
CELL_SIZE=30
WINDOW=pygame.display.set_mode((WID,HEI))
pygame.display.set_caption("Maybe a functioning Tetris game")
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
WINDOW.fill(BLACK)
FPS=60
clock=pygame.time.Clock()#our clock object. This allows us to use methods to control time in the game 

#we represent the shapes of the tetrominoes using rectangular matrices
TETROMINOES = {
    "L": [[1,0], 
          [1,0], 
          [1,1]],

    "J": [[0,1], 
          [0,1], 
          [1,1]],

    "I": [[1], 
          [1], 
          [1], 
          [1]],

    "O": [[1,1], 
          [1,1]],

    "S": [[0,1,1], 
          [1,1,0]],

    "Z": [[1,1,0], 
          [0,1,1]],

    "T": [[1,1,1], 
          [0,1,0]]
}

#we create an empty board by assigning each position an initial value of 0(meaning it is not occupied by a block)
board=[]
for row in range(GRID_HEI):
    board_row=[]
    for col in range(GRID_WID):
        board_row.append(0)
    board.append(board_row)

current_piece=None
piece_pos=[90,90]#this is a placeholder for now

def draw_board():
    WINDOW.fill(BLACK)
    for row in range(GRID_HEI):
        for col in range(GRID_WID):
            #pygame.draw.rect(WINDOW, WHITE, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            #fill a cell white if it is occupied
            if board[row][col]==1:
                pygame.draw.rect(WINDOW, RED, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(WINDOW, WHITE, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        if current_piece is not None:
            for row in range(len(current_piece)):
                for col in range(len(current_piece[0])):#we use the length of the first row because all rows of our matrix have the same number of columns 
                    if current_piece[row][col]==1:
                        pygame.draw.rect(WINDOW, RED, ((piece_pos[1]+col)*CELL_SIZE, (piece_pos[0]+row)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
#initialise score to 0, then write a functio that dynamically draws the score on the game window
score=0
FONT=pygame.font.SysFont("arial", 30)
def draw_score():
    score_text=FONT.render(f"Score: {score}", False, GREEN)
    WINDOW.blit(score_text, (10,10))

#import the random module and wtite a functuon that picks a random matrix out of our 7 tetromino matrices to use as our current piece
import random
def spawn_piece():
    global current_piece, piece_pos
    current_piece=random.choice(list(TETROMINOES.values()))
    piece_pos=[0, GRID_WID//2-len(current_piece[0])//2]#center the piece horizontally so that it spawns at the top middle of the grid

#the function below returns true if any part of the current piece goes lower than the bottom of the grid, or beyond the sides of the grid, or into any cell already occupied by a block
def check_collision(piece, pos):
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            if piece[row][col]==1:
                board_row=pos[0]+row
                board_col=pos[1]+col
                if (board_row>=GRID_HEI or board_col<0 or board_col>=GRID_WID or board[board_row][board_col]==1):
                    return True

def lock_piece():
    for row in range(len(current_piece)):
        for col in range(len(current_piece[0])):
            if current_piece[row][col]==1:
                board[piece_pos[0]+row][piece_pos[1]+col]=1

#This function removes filled rows from the board by creating a new board without the removed row
def clear_rows():
    global board
    global score
    rows_cleared=0
    for row in range(GRID_HEI-1, -1, -1):
        full=True
        for col in range(GRID_WID):
            if board[row][col]==0:#checks each row for an unfilled cell, if none are present, the row is full.
                full=False
                break
        if full:
            rows_cleared+=1
    score+=rows_cleared*100#moved this line outside the loop because it caused incorrect compounding of the scores

    new_board = [] #create a new empty board the same size as the OG board
    for row in range(GRID_HEI):
        new_row=[]
        for col in range(GRID_WID):
            new_row.append(0)
        new_board.append(new_row)

    new_row=GRID_HEI-1#only copy the rows that are NOT full
    for row in range(GRID_HEI-1, -1, -1):
        full=True
        for col in range(GRID_WID):
            if board[row][col]==0:
                full=False
                break
        if not full:
            for col in range(GRID_WID):
                new_board[new_row][col]=board[row][col]
            new_row-=1

    board=new_board#replace old board with new board

#This function lets us rotate the piece 90 degrees clockwise when the button is pressed
def rotate_piece():
    global current_piece
    new_piece = []
    for col in range(len(current_piece[0])):
        new_row = []
        for row in reversed(range(len(current_piece))):
            new_row.append(current_piece[row][col])
        new_piece.append(new_row)
    
    if not check_collision(new_piece, piece_pos):
        current_piece = new_piece

def draw_game_over():
    game_over_text=FONT.render("You fumbled it lmao", True, GREEN)
    restart_text=FONT.render("R to restart", True, GREEN)
    WINDOW.blit(game_over_text, (WID//2-game_over_text.get_width()//2, HEI//2-50))
    WINDOW.blit(restart_text, (WID//2-restart_text.get_width()//2, HEI//2+50))


game_over=False#we introduce a game over flag because our previous version exits the game immediately when running becomes false
running = True
fall_time=0
fall_speed=500


while running:

    clock.tick(FPS)#limit our game to run at "FPS" frames per second
    fall_time+=clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if not game_over and event.type==pygame.KEYDOWN:#if a button is pressed and game_over is not flagged
            if event.key==pygame.K_UP and current_piece:#if button is up and there is a piece, rotate the piece
                rotate_piece()
            if event.key==pygame.K_DOWN and not check_collision(current_piece, [piece_pos[0]+1, piece_pos[1]]):
                piece_pos[0]+=1
                fall_time=0
            if event.key==pygame.K_LEFT and not check_collision(current_piece, [piece_pos[0], piece_pos[1]-1]):
                piece_pos[1]-=1
            if event.key==pygame.K_RIGHT and not check_collision(current_piece, [piece_pos[0], piece_pos[1]+1]):
                piece_pos[1]+=1
        
        if game_over and event.type==pygame.KEYDOWN and event.key==pygame.K_r:
            board=[[0 for _ in range(GRID_WID)] for _ in range(GRID_HEI)]
            current_piece=None
            piece_pos=[0,0]
            score=0
            game_over=False
    
    if not game_over:
        #spawn a new piece if none exists
        if current_piece is None:
            spawn_piece()
        if fall_time>=fall_speed:
            if not check_collision(current_piece, [piece_pos[0]+1, piece_pos[1]]):
                piece_pos[0]+=1
            else:
                lock_piece()
                clear_rows()
                spawn_piece()
                if check_collision(current_piece, piece_pos):
                    game_over=True
            fall_time=0

    draw_board()
    draw_score()

    if game_over:
        draw_game_over()

    pygame.display.update()


