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
WINDOW.fill(BLACK)
FPS=60
clock=pygame.time.Clock()

#we represent the shapes of the tetrominoes using lists
TETROMINOES = {
    "L": [[1,0], [1,0], [1,1]],
    "J": [[0,1], [0,1], [1,1]],
    "I": [[1], [1], [1], [1]],
    "O": [[1,1], [1,1]],
    "S": [[0,1,1], [1,1,0]],
    "Z": [[1,1,0], [0,1,1]],
    "T": [[1,1,1], [0,1,0]]
}

#we create an empty board by assigning each position an initial value of 0
board=[]
for row in range(GRID_HEI):
    board_row=[]
    for col in range(GRID_WID):
        board_row.append(0)
    board.append(board_row)

current_piece=None
piece_pos=[0,0]

def draw_board():
    WINDOW.fill(BLACK)
    for row in range(GRID_HEI):
        for col in range(GRID_WID):
            if board[row][col]==1:
                pygame.draw.rect(WINDOW, RED, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(WINDOW, WHITE, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        if current_piece:
            for row in range(len(current_piece)):
                for col in range(len(current_piece[0])):
                    if current_piece[row][col]==1:
                        pygame.draw.rect(WINDOW, RED, ((piece_pos[1]+col)*CELL_SIZE, (piece_pos[0]+row)*CELL_SIZE, CELL_SIZE, CELL_SIZE))

score=0
FONT=pygame.font.SysFont("arial", 30)
def draw_score():
    score_text=FONT.render(f"Score: {score}", True, WHITE)
    WINDOW.blit(score_text, (10,10))
import random
def spawn_piece():
    global current_piece, piece_pos
    current_piece=random.choice(list(TETROMINOES.values()))
    piece_pos=[0, GRID_WID//2-len(current_piece[0])//2]

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
            if board[row][col]==0:
                full=False
                break
        if full:
            rows_cleared+=1
            score+=rows_cleared*100

    new_board = []
    for row in range(GRID_HEI):
        new_row=[]
        for col in range(GRID_WID):
            new_row.append(0)
        new_board.append(new_row)

    new_row=GRID_HEI-1
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
    board=new_board
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
    
running = True
fall_time=0
fall_speed=500
while running:

    clock.tick(FPS)
    fall_time+=clock.get_time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:#if a button is pressed
            if event.key==pygame.K_UP and current_piece:#if button is up and there is a piece, rotate the piece
                rotate_piece()
            if event.key==pygame.K_DOWN and not check_collision(current_piece, [piece_pos[0]+1, piece_pos[1]]):
                piece_pos[0]+=1
                fall_time=0
            if event.key==pygame.K_LEFT and not check_collision(current_piece, [piece_pos[0], piece_pos[1]-1]):
                piece_pos[1]-=1
            if event.key==pygame.K_RIGHT and not check_collision(current_piece, [piece_pos[0], piece_pos[1]+1]):
                piece_pos[1]+=1
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
                running= False
        fall_time=0
    draw_board()
    draw_score()
    pygame.display.update()


