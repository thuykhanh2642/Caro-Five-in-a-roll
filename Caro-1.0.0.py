import pygame
import sys
import random
from agent import find_best_move

pygame.init()

WindowSize = 1024
GridSize = 10
CellSize = WindowSize // GridSize
LineW = 3
HeaderSize = 100
Player1 = 1
Player2 = 2
AGENT = 3
GridColor = (50, 50, 50)
Player1Color = (255, 0, 0)
Player2Color = (0, 0, 255)
BG_Color = (0, 0, 0)
White = (200, 200, 200)

font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 60)

current_player = Player1
Screen = pygame.display.set_mode((WindowSize, WindowSize + HeaderSize))
pygame.display.set_caption('CaroChess')
clock = pygame.time.Clock()

ani_progress = {}
winning_line = []
Grid = [[0 for _ in range(GridSize)] for _ in range(GridSize)]
Score = {Player1: 0, Player2: 0}
undo_stack = []
redo_stack = []


# Draw the grid
def draw_grid():
    for x in range(GridSize):
        pygame.draw.line(Screen, (30, 30, 30), (x * CellSize + 3, HeaderSize + 3),
                         (x * CellSize + 3, WindowSize + HeaderSize + 3), LineW + 2)
        pygame.draw.line(Screen, GridColor, (x * CellSize, HeaderSize), (x * CellSize, WindowSize + HeaderSize), LineW)

        pygame.draw.line(Screen, (30, 30, 30), (3, x * CellSize + HeaderSize + 3),
                         (WindowSize + 3, x * CellSize + HeaderSize + 3), LineW + 2)
        pygame.draw.line(Screen, GridColor, (0, x * CellSize + HeaderSize), (WindowSize, x * CellSize + HeaderSize),
                         LineW)


def draw_board():
    for row in range(GridSize):
        for col in range(GridSize):
            if Grid[row][col] == Player1:
                progress = ani_progress.get((row, col), 1)
                draw_animated_x(row, col, progress)
            elif Grid[row][col] == Player2:
                progress = ani_progress.get((row, col), 1)
                draw_animated_o(row, col, progress)
            elif Grid[row][col] == AGENT: 
                progress = ani_progress.get((row, col), 1)
                draw_animated_o(row, col, progress)  


def draw_header():
    Screen.fill(White)

    title_text = title_font.render('Mogoku', True, BG_Color)
    title_width = title_text.get_width()
    title_x = (WindowSize - title_width) // 2
    Screen.blit(title_text, (title_x, 10))

    if current_player == Player1:
        turn_text = font.render("Player 1's Turn", True, Player1Color)
    else:
        turn_text = font.render("Player 2's Turn", True, Player2Color)

    Screen.blit(turn_text, (WindowSize // 6, 60))

    score_text = font.render(f"X: {Score[Player1]}  O: {Score[Player2]}", True, BG_Color)
    Screen.blit(score_text, (10, 60))


def draw_animated_x(row, col, progress):
    start_x = col * CellSize + 10
    start_y = row * CellSize + 10 + HeaderSize
    end_x = (col + 1) * CellSize - 10
    end_y = (row + 1) * CellSize - 10 + HeaderSize

    pygame.draw.line(Screen, Player1Color,
                     (start_x, start_y),
                     (start_x + (end_x - start_x) * progress, start_y + (end_y - start_y) * progress), LineW)

    pygame.draw.line(Screen, Player1Color,
                     (end_x, start_y),
                     (end_x - (end_x - start_x) * progress, start_y + (end_y - start_y) * progress), LineW)


def draw_animated_o(row, col, progress):
    center = (col * CellSize + CellSize // 2, row * CellSize + CellSize // 2 + HeaderSize)
    max_radius = CellSize // 2 - 10
    current_radius = int(max_radius * progress) 
    pygame.draw.circle(Screen, Player2Color, center, current_radius, LineW)


def highlight_winning_line():
    if winning_line:
        for row, col in winning_line:
            for thickness in range(4, 9): 
                pygame.draw.rect(Screen, (0, 250, 0),
                                 (col * CellSize, row * CellSize + HeaderSize, CellSize, CellSize), thickness)





def check_winner(player):
    global winning_line
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
    global Grid, current_player, winning_line, undo_stack, redo_stack
    Grid = [[0 for _ in range(GridSize)] for _ in range(GridSize)]
    current_player = Player1
    winning_line = []
    undo_stack.clear()
    redo_stack.clear()
    game_over = False


def show_menu():
    Screen.fill(White)
    title_font = pygame.font.SysFont(None, 80)
    menu_font = pygame.font.SysFont(None, 40)
    
    # Render menu options
    title_text = title_font.render('Caro Chess', True, BG_Color)
    pvp_text = menu_font.render('1. Player vs Player', True, Player1Color)
    pve_text = menu_font.render('2. Player vs AI', True, Player2Color)

    # Display the menu text
    Screen.blit(title_text, (WindowSize // 4, WindowSize // 6))
    Screen.blit(pvp_text, (WindowSize // 4, WindowSize // 3))
    Screen.blit(pve_text, (WindowSize // 4, WindowSize // 3 + 50))

    pygame.display.flip()

    pvp_rect = pygame.Rect(WindowSize // 4, WindowSize // 3, 300, 50)  # PvP button area
    pve_rect = pygame.Rect(WindowSize // 4, WindowSize // 3 + 50, 300, 50)  # PvE button area

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if pvp_rect.collidepoint(mouse_x, mouse_y):
                    return 'pvp' 

                if pve_rect.collidepoint(mouse_x, mouse_y):
                    return 'pve' 


# Main Program
game_mode = show_menu()  
print(f"Selected game mode: {game_mode}")  

# Game loop
running = True
game_over = False
while running:
    Screen.fill(White)
    draw_header() 
    draw_grid()  
    draw_board()  
    highlight_winning_line()  

    for (row, col), progress in ani_progress.items():
        if progress < 1:
            ani_progress[(row, col)] += 0.05 
        else:
            ani_progress[(row, col)] = 1 

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y > HeaderSize:  
                col = mouse_x // CellSize
                row = (mouse_y - HeaderSize) // CellSize

                if Grid[row][col] == 0: 
                    Grid[row][col] = current_player
                    ani_progress[(row, col)] = 0  

                    if check_winner(current_player): 
                        Score[current_player] += 1
                        game_over = True
                    else:
                        if game_mode == 'pvp':  # Player vs Player mode
                            current_player = Player2 if current_player == Player1 else Player1
                        elif game_mode == 'pve':  # Player vs AI mode
                            current_player = AGENT

    if game_mode == 'pve' and current_player == AGENT and not game_over:
        print("AI is thinking...")  
        if find_best_move(Grid, GridSize, check_winner, ani_progress): 
            print("AI made a move!") 
            Score[AGENT] += 1
            game_over = True
        else:
            current_player = Player1  

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game()
        game_over = False

    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
