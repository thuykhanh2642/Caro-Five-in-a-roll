import pygame
import sys

pygame.init()

WindowSize = 1024
GridSize = 15
CellSize = WindowSize//GridSize
LineW = 3
HeaderSize = 100
Player1 = 1
Player2 = 2
AGENT = 3
GridColor = (50,50,50)
Player1Color=(255,0,0)
Player2Color=(0,0,255)
BG_Color  = (0,0,0)
Color2 = (20,50,20)
White = (255,255,255)
font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 60)
current_player = Player1
Screen = pygame.display.set_mode((WindowSize, WindowSize + HeaderSize))
pygame.display.set_caption('CaroChess')

winning_line = [ ]
Grid = [[0 for _ in range(GridSize)] for _ in range (GridSize)]
Score = {Player1: 0, Player2: 0}

def draw_grid():
     for x in range(GridSize):
         pygame.draw.line(Screen, GridColor, (x * CellSize, HeaderSize),(x*CellSize,WindowSize+HeaderSize), LineW)
         pygame.draw.line(Screen,GridColor,(0,x*CellSize + HeaderSize),(WindowSize,x*CellSize+HeaderSize),LineW)
         
def draw_board():
    for row in range(GridSize):
        for col in range(GridSize):
            if Grid[row][col] == Player1:
                pygame.draw.line(Screen, Player1Color, (col * CellSize + 10, row * CellSize + 10 + HeaderSize), 
                                 ((col + 1) * CellSize - 10, (row + 1) * CellSize - 10 + HeaderSize), LineW)
                pygame.draw.line(Screen, Player1Color, ((col + 1) * CellSize - 10, row * CellSize + 10 + HeaderSize), 
                                 (col * CellSize + 10, (row + 1) * CellSize - 10 + HeaderSize), LineW)
            elif Grid[row][col] == Player2:
                pygame.draw.circle(Screen, Player2Color, 
                                   (col * CellSize + CellSize // 2, row * CellSize + CellSize // 2 + HeaderSize), 
                                   CellSize // 2 - 10, LineW)

def draw_header():
    Screen.fill(White)
    title_text = title_font.render('Caro Game', True, BG_Color)
    Screen.blit(title_text, (WindowSize // 4, 10))

    # Player turn indicator
    if current_player == Player1:
        turn_text = font.render("Player 1's Turn", True, Player1Color)
    else:
        turn_text = font.render("Player 2's Turn", True, Player2Color)
    Screen.blit(turn_text, (WindowSize // 3, 60))

    # Display score
    score_text = font.render(f"X: {Score[Player1]}  O: {Score[Player2]}", True, BG_Color)
    Screen.blit(score_text, (10, 60))

def highlight_winning_line():
    if winning_line:
        for row, col in winning_line:
            pygame.draw.rect(Screen, Color2, 
                             (col * CellSize, row * CellSize + HeaderSize, CellSize, CellSize), 4)

def check_winner(player):
    global winning_line
    # Check rows, columns and diagonals for a winning line of 5
    for row in range(GridSize):
        for col in range(GridSize):
            if (check_line(player, row, col, 1, 0) or  # Horizontal
                check_line(player, row, col, 0, 1) or  # Vertical
                check_line(player, row, col, 1, 1) or  # Diagonal (top-left to bottom-right)
                check_line(player, row, col, 1, -1)):  # Diagonal (bottom-left to top-right)
                return True
    return False

def check_line(player, row, col, delta_row, delta_col):
    global winning_line
    count = 0
    line = []
    for i in range(5):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < GridSize and 0 <= c < GridSize and Grid[r][c] == player:
            count += 1
            line.append((r, c))
        else:
            break
    if count == 5:
        winning_line = line
        return True
    return False

def reset_game():
    global Grid, current_player, winning_line
    Grid = [[0 for _ in range(GridSize)] for _ in range(GridSize)]
    current_player = Player1
    winning_line = []

# Game loop
running = True
game_over = False
while running:
    Screen.fill(White)
    draw_header()
    draw_grid()
    draw_board()
    highlight_winning_line()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()


            if mouse_y > HeaderSize:
                col = mouse_x // CellSize
                row = (mouse_y - HeaderSize) // CellSize


                if Grid[row][col] == 0:
                    Grid[row][col] = current_player

                    # Check for a winner
                    if check_winner(current_player):
                        Score[current_player] += 1
                        game_over = True
                        winner_text = "Player 1 Wins!" if current_player == Player1 else "Player 2 Wins!"
                        text = font.render(winner_text, True, BG_Color)
                        Screen.blit(text, (WindowSize // 2 - 100, WindowSize + HeaderSize // 2))
                    else:

                        current_player = Player2 if current_player == Player1 else Player1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:  # Reset game if '0' is pressed
                game_over = True

                reset_game()

    pygame.display.flip()

# Quit pygame
pygame.quit()
