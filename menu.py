from button import Button
from algorithm import *
import json


class MenuIntro:
    def __init__(self):
        self.btnvoiAI = Button (220, 230, 'Với máy')
        self.btnvoiNguoi = Button (545, 230, 'Với người')

    def draw (self):
        DISPLAYSURF.blit(MENU_BG, (0,0))
        self.btnvoiAI.update()
        self.btnvoiNguoi.update()
        font = pygame.font.SysFont('cambria', 30, bold=True)
        DISPLAYSURF.blit(font.render('CHỌN CHẾ ĐỘ CHƠI', True, BABY_PINK), (240, 130))

    def action (self, event):
        if self.btnvoiAI.checkForInput(pygame.mouse.get_pos(), event):
            self.btnvoiAI.set_selected(True)
            self.btnvoiNguoi.set_selected(False)
            self.btnvoiNguoi.update()
            self.btnvoiAI.update()
        if self.btnvoiNguoi.checkForInput(pygame.mouse.get_pos(), event):
            self.btnvoiNguoi.set_selected(True)
            self.btnvoiAI.set_selected(False)
            self.btnvoiNguoi.update()
            self.btnvoiAI.update()

        if self.btnvoiNguoi.checkForInput(pygame.mouse.get_pos(), event) or self.btnvoiAI.checkForInput(pygame.mouse.get_pos(), event):
            if self.btnvoiNguoi.selected:
                return Screen.MENUSIZEHUMAN 
            else:
                return Screen.MENUAI
        return Screen.MENUINTRO
    
class MenuSizeHuman:
    def __init__(self):
        self.btn3x3 = Button(220, 230, '3 x 3')
        self.btn5x5 = Button(545, 230, '5 x 5')
        self.btnBatDau = Button(360, 650, 'BẮT ĐẦU')
        self.btnQuayLai = Button(360, 720, 'QUAY LẠI')
        self.play_game = None

    def drawMenuSize(self):
        DISPLAYSURF.blit(MENU_BG, (0, 0))
        self.btn3x3.update()
        self.btn5x5.update()
        self.btnBatDau.update()
        self.btnQuayLai.update()
        font = pygame.font.SysFont('cambria', 30, bold=True)
        DISPLAYSURF.blit(font.render('CHỌN KÍCH THƯỚC BẢNG', True, BABY_PINK), (240, 130))

    def action(self, event, play_game=None):
        global BOARD_SIZE

        if self.btn3x3.checkForInput(pygame.mouse.get_pos(), event):
            self.btn3x3.set_selected(True)
            self.btn5x5.set_selected(False)
            self.btn3x3.update()
            self.btn5x5.update()
            BOARD_SIZE = 3

        if self.btn5x5.checkForInput(pygame.mouse.get_pos(), event):
            self.btn3x3.set_selected(False)
            self.btn5x5.set_selected(True)
            self.btn3x3.update()
            self.btn5x5.update()
            BOARD_SIZE = 5

        if self.btnBatDau.checkForInput(pygame.mouse.get_pos(), event):
            self.play_game = GamingHuman()
            self.play_game.board_size = BOARD_SIZE
            self.play_game.initialize_game()  
            self.play_game.game_over = False
            return Screen.GAMINGHUMAN

        elif self.btnQuayLai.checkForInput(pygame.mouse.get_pos(), event):
            MenuIntro().draw()
            return Screen.MENUINTRO

        return Screen.MENUSIZEHUMAN
    
    def get_play_game(self):
        return self.play_game

class GamingHuman:
    def __init__(self):
        self.imgX = pygame.image.load('img/X.png')
        self.imgY = pygame.image.load('img/O.png')
        self.gameBg = pygame.image.load('img/tic-tac-toe.jpg')
        self.btnReplay = Button(590, 570, 'CHƠI LẠI')
        self.board_size = 3
        self.game_over = False
        self.current_player = 'X' 
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def draw(self):
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(self.gameBg, (0, 50))
        DISPLAYSURF.blit(FONT.render("Player 1: ", True, BLACK, WHITE), (500, 370))
        DISPLAYSURF.blit(FONT.render("Player 2: ", True, BLACK, WHITE), (500, 450))
        DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('img/X.png'), (70, 70)), (630, 340))
        DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('img/O.png'),(70, 70)), (630, 420))
        DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('img/back.png'), (90, 90)), (10, 10))
        
        if self.board_size == 3:
            cell_size = 110
            spacing = 110
        else:
            cell_size = 70
            spacing = 80

        icon_size = int(cell_size * 0.8)
        scaled_imgX = pygame.transform.scale(self.imgX, (icon_size, icon_size))
        scaled_imgY = pygame.transform.scale(self.imgY, (icon_size, icon_size))

        for i in range(self.board_size + 1):
            pygame.draw.line(DISPLAYSURF, PINK,
                             (70, 220 + i * spacing),
                             (70 + self.board_size * spacing, 220 + i * spacing), 5)
            pygame.draw.line(DISPLAYSURF, PINK,
                             (70 + i * spacing, 220),
                             (70 + i * spacing, 220 + self.board_size * spacing), 5)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 'X':
                    icon_x = 70 + j * spacing + (cell_size - icon_size) // 2
                    icon_y = 220 + i * spacing + (cell_size - icon_size) // 2
                    DISPLAYSURF.blit(scaled_imgX, (icon_x, icon_y))
                elif self.board[i][j] == 'O':
                    icon_x = 70 + j * spacing + (cell_size - icon_size) // 2
                    icon_y = 220 + i * spacing + (cell_size - icon_size) // 2
                    DISPLAYSURF.blit(scaled_imgY, (icon_x, icon_y))
        
        if self.game_over:
            result = self.check_winner()
            if result == 'X':
                DISPLAYSURF.blit(FONT.render("PLAYER 1 THẮNG", True, RED, WHITE), (320, 120))
            elif result == 'O':
                DISPLAYSURF.blit(FONT.render("PLAYER 2 THẮNG", True, RED, WHITE), (320, 120))
            elif result == '.':
                DISPLAYSURF.blit(FONT.render("      HÒA     ", True, RED, WHITE), (320, 1220))

            self.btnReplay.update()

    def action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if self.game_over:
                if 460 < x < 660 and 480 < y < 560:
                    self.initialize_game()
                    return Screen.GAMINGHUMAN
                return Screen.GAMINGHUMAN
            
            cell_size = 110 if self.board_size == 3 else 70
            spacing = 110 if self.board_size == 3 else 80

            for i in range(self.board_size):
                for j in range(self.board_size):
                    cell_x_start = 70 + j * spacing
                    cell_y_start = 220 + i * spacing
                    cell_x_end = cell_x_start + cell_size
                    cell_y_end = cell_y_start + cell_size

                    if cell_x_start < x < cell_x_end and cell_y_start < y < cell_y_end:
                        if self.board[i][j] == '.':
                            self.board[i][j] = self.current_player
                            result = self.check_winner()
                            if result in ['X', 'O', '.']:
                                self.game_over = True
                            self.current_player = 'O' if self.current_player == 'X' else 'X'
                        return Screen.GAMINGHUMAN

            if 10 < x < 100 and 10 < y < 100:
                self.initialize_game()
                self.game_over = False
                return Screen.MENUSIZEHUMAN

        return Screen.GAMINGHUMAN

    def initialize_game(self):
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.game_over = False
        self.current_player = 'X'

    def check_winner(self):
        for row in self.board:
            if row[0] != '.' and all(s == row[0] for s in row):
                return row[0]

        for col in range(self.board_size):
            if self.board[0][col] != '.' and all(self.board[row][col] == self.board[0][col] for row in range(self.board_size)):
                return self.board[0][col]

        if self.board[0][0] != '.' and all(self.board[i][i] == self.board[0][0] for i in range(self.board_size)):
            return self.board[0][0]

        if self.board[0][self.board_size - 1] != '.' and all(self.board[i][self.board_size - 1 - i] == self.board[0][self.board_size - 1] for i in range(self.board_size)):
            return self.board[0][self.board_size - 1]

        if all(self.board[i][j] != '.' for i in range(self.board_size) for j in range(self.board_size)):
            return '.' 

        return None
    
    def update_score(self, result):
        with open('game_data.json', 'r') as f:
            data = json.load(f)

        if result == 'X':
            data['player_1'] += 1
        elif result == 'O':
            data['player_2'] += 1
        elif result == '.':
            data['draws'] += 1

        with open('game_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return Screen.GAMINGHUMAN
 
class MenuAI:
    def __init__(self):
        self.btnAi = Button(220, 230, 'AI')
        self.btnNguoi = Button(545, 230, 'NGƯỜI')
        self.btnTiep = Button(360, 650, 'TIẾP')
        self.btnQuayLai = Button(360, 720, 'QUAY LẠI')

    def drawMenu(self):
        DISPLAYSURF.blit(MENU_BG, (0, 0))
        self.btnAi.update()
        self.btnNguoi.update()
        self.btnTiep.update()
        self.btnQuayLai.update()
        font = pygame.font.SysFont('cambria', 30, bold=True)
        DISPLAYSURF.blit(font.render('CHỌN BÊN ĐI TRƯỚC', True, BABY_PINK), (240, 130))

    def action(self, event):
        if self.btnAi.checkForInput(pygame.mouse.get_pos(), event):
            self.btnAi.set_selected(True)
            self.btnNguoi.set_selected(False)
            self.btnAi.update()
            self.btnNguoi.update()

        if self.btnNguoi.checkForInput(pygame.mouse.get_pos(), event):
            self.btnAi.set_selected(False)
            self.btnNguoi.set_selected(True)
            self.btnAi.update()
            self.btnNguoi.update()

        if self.btnTiep.checkForInput(pygame.mouse.get_pos(), event):
            MenuAIgo().drawMenuAlgo()
            return Screen.SELECT_AIGO
        elif self.btnQuayLai.checkForInput(pygame.mouse.get_pos(), event):
            MenuAIgo().drawMenuAlgo()
            return Screen.MENUINTRO
        else:
            return Screen.MENUAI

    def get_btnAi(self):
        return self.btnAi

    def get_btnNguoi(self):
        return self.btnNguoi

    def get_btnTiep(self):
        return self.btnTiep


class MenuAIgo:
    def __init__(self):
        self.btnMinMax = Button(220, 230, 'Min_Max')
        self.btnAlphaBeta = Button(545, 230, 'Alpha_Beta')
        self.btnBatDau = Button(360, 650, 'TIẾP')
        self.btnQuayLai = Button(360, 720, 'QUAY LẠI')
        self.btnMinMax.set_selected(True)

    def drawMenuAlgo(self):
        DISPLAYSURF.blit(MENU_BG, (0, 0))
        self.btnMinMax.update()
        self.btnAlphaBeta.update()
        self.btnBatDau.update()
        self.btnQuayLai.update()
        font = pygame.font.SysFont('cambria', 30, bold=True)
        DISPLAYSURF.blit(font.render('CHỌN THUẬT TOÁN', True, BABY_PINK), (240, 130))

    def get_btnAnphaBeta(self):
        return self.btnAlphaBeta

    def action(self, event, play_game, al_goes_first):
        if self.btnMinMax.checkForInput(pygame.mouse.get_pos(), event):
            self.btnMinMax.set_selected(True)
            self.btnAlphaBeta.set_selected(False)
            self.btnMinMax.update()
            self.btnAlphaBeta.update()

        if self.btnAlphaBeta.checkForInput(pygame.mouse.get_pos(), event):
            self.btnMinMax.set_selected(False)
            self.btnAlphaBeta.set_selected(True)
            self.btnMinMax.update()
            self.btnAlphaBeta.update()

        if self.btnBatDau.checkForInput(pygame.mouse.get_pos(), event):
            MenuSize().drawMenuSize()
            return Screen.SELECT_SIZE

        elif self.btnQuayLai.checkForInput(pygame.mouse.get_pos(), event):
            MenuAI().drawMenu()
            return Screen.MENUAI
        return Screen.SELECT_AIGO


class MenuSize:
    def __init__(self):
        self.btn3x3 = Button(220, 230, '3 x 3')
        self.btn5x5 = Button(545, 230, '5 x 5')
        self.btnBatDau = Button(360, 650, 'BẮT ĐẦU')
        self.btnQuayLai = Button(360, 720, 'QUAY LẠI')

    def drawMenuSize(self):
        DISPLAYSURF.blit(MENU_BG, (0, 0))
        self.btn3x3.update()
        self.btn5x5.update()
        self.btnBatDau.update()
        self.btnQuayLai.update()
        font = pygame.font.SysFont('cambria', 30, bold=True)
        DISPLAYSURF.blit(font.render('CHỌN KÍCH THƯỚC BẢNG', True, BABY_PINK), (240, 130))

    def action(self, event, play_game, al_goes_first, use_alpha_beta):
        global BOARD_SIZE

        if self.btn3x3.checkForInput(pygame.mouse.get_pos(), event):
            self.btn3x3.set_selected(True)
            self.btn5x5.set_selected(False)
            self.btn3x3.update()
            self.btn5x5.update()
            BOARD_SIZE = 3

        if self.btn5x5.checkForInput(pygame.mouse.get_pos(), event):
            self.btn3x3.set_selected(False)
            self.btn5x5.set_selected(True)
            self.btn3x3.update()
            self.btn5x5.update()
            BOARD_SIZE = 5

        if self.btnBatDau.checkForInput(pygame.mouse.get_pos(), event):
            if use_alpha_beta:
                txt = "Thuật toán cắt tỉa Alpha Beta"
            else:
                txt = "Thuật toán Min_Max"

            play_game.board_size = BOARD_SIZE
            play_game.alphaBeta = AlphaBeta(BOARD_SIZE)
            play_game.minMax = MinMax(BOARD_SIZE)
            play_game.game_over = False
            play_game.draw(txt)

            if al_goes_first:
                if use_alpha_beta:
                    play_game.Al_alpha_beta_play_first()
                else:
                    play_game.Al_min_max_first()

            return Screen.GAMING

        elif self.btnQuayLai.checkForInput(pygame.mouse.get_pos(), event):
            MenuAIgo().drawMenuAlgo()
            return Screen.SELECT_AIGO

        return Screen.SELECT_SIZE


class Gaming:
    def __init__(self):
        self.imgX = pygame.image.load('img/X.png')
        self.imgY = pygame.image.load('img/O.png')
        self.gameBg = pygame.image.load('img/tic-tac-toe.jpg')
        self.board_size = 3
        self.alphaBeta = AlphaBeta(self.board_size)
        self.minMax = MinMax(self.board_size)
        self.game_over = False
        self.current_algorithm = "Alpha Beta"  # Default algorithm

    def draw(self, txt):
        PINK = (255, 204, 204)
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(self.gameBg, (0, 50))
        font = pygame.font.SysFont('cambria', 30, bold=True)
        DISPLAYSURF.blit(font.render(txt, True, PINK, WHITE), (150, 120))
        self.current_algorithm = txt  # Store the current algorithm name
        DISPLAYSURF.blit(FONT.render("MÁY: ", True, BLACK, WHITE), (480, 400))
        DISPLAYSURF.blit(FONT.render("NGƯỜI: ", True, BLACK, WHITE), (480, 480))
        DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('img/O.png'), (70, 70)), (590, 380))
        DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('img/X.png'), (70, 70)), (590, 450))
        DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('img/back.png'), (90, 90)), (10, 10))

        if self.board_size == 3:
            cell_size = 110
            spacing = 110
        else:
            cell_size = 70
            spacing = 80

        icon_size = int(cell_size * 0.8)
        scaled_imgX = pygame.transform.scale(self.imgX, (icon_size, icon_size))
        scaled_imgY = pygame.transform.scale(self.imgY, (icon_size, icon_size))

        for i in range(self.board_size + 1):
            pygame.draw.line(DISPLAYSURF, PINK,
                             (70, 220 + i * spacing),
                             (70 + self.board_size * spacing, 220 + i * spacing), 5)
            pygame.draw.line(DISPLAYSURF, PINK,
                             (70 + i * spacing, 220),
                             (70 + i * spacing, 220 + self.board_size * spacing), 5)

        # Determine which algorithm's state to use based on the current algorithm
        is_alpha_beta = "Alpha Beta" in self.current_algorithm
        current_board = self.alphaBeta.current_state if is_alpha_beta else self.minMax.current_state

        for i in range(self.board_size):
            for j in range(self.board_size):
                if current_board[i][j] == 'X':
                    icon_x = 70 + j * spacing + (cell_size - icon_size) // 2
                    icon_y = 220 + i * spacing + (cell_size - icon_size) // 2
                    DISPLAYSURF.blit(scaled_imgX, (icon_x, icon_y))
                elif current_board[i][j] == 'O':
                    icon_x = 70 + j * spacing + (cell_size - icon_size) // 2
                    icon_y = 220 + i * spacing + (cell_size - icon_size) // 2
                    DISPLAYSURF.blit(scaled_imgY, (icon_x, icon_y))

        if self.game_over:
            # Use the appropriate algorithm's result based on the current algorithm
            result = self.alphaBeta.result if is_alpha_beta else self.minMax.result
            if result == 'X':
                pygame.draw.rect(DISPLAYSURF, WHITE, (480, 290, 250, 60))
                DISPLAYSURF.blit(FONT.render("  NGƯỜI THẮNG", True, RED, WHITE), (500, 300))
            elif result == 'O':
                pygame.draw.rect(DISPLAYSURF, WHITE, (480, 290, 250, 60))
                DISPLAYSURF.blit(FONT.render("  MÁY THẮNG", True, RED, WHITE), (500, 300))
            elif result == '.':
                pygame.draw.rect(DISPLAYSURF, WHITE, (480, 290, 250, 60))
                DISPLAYSURF.blit(FONT.render("     HÒA   ", True, RED, WHITE), (500, 300))

    def Al_alpha_beta_play_first(self):
        self.alphaBeta.play_alpha_beta(ai_First=True, gaming=self)

    def Al_min_max_first(self):
        self.minMax.play_min_max(ai_First=True, gaming=self)

    def action(self, event, menuAlgo):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if self.board_size == 3:
                cell_size = 110
                spacing = 110
            else:
                cell_size = 70
                spacing = 80

            if self.game_over:
                if 10 < x < 100 and 10 < y < 100:
                    menuAlgo.drawMenuAlgo()
                    self.alphaBeta.initialize_game()
                    self.minMax.initialize_game()
                    self.game_over = False
                    return Screen.SELECT_AIGO
                return Screen.GAMING

            for i in range(self.board_size):
                for j in range(self.board_size):
                    if 70 + j * spacing < x < 70 + (j + 1) * spacing and 220 + i * spacing < y < 220 + (
                            i + 1) * spacing:
                        # Determine which algorithm to use based on the current algorithm
                        is_alpha_beta = "Alpha Beta" in self.current_algorithm

                        if is_alpha_beta:
                            self.alphaBeta.play_alpha_beta(i, j, gaming=self)
                        else:
                            self.minMax.play_min_max(i, j, gaming=self)

                        # Force redraw after move
                        self.draw(self.current_algorithm)
                        pygame.display.update()

                        # Check for game over
                        if (is_alpha_beta and self.alphaBeta.result is not None) or \
                                (not is_alpha_beta and self.minMax.result is not None):
                            self.game_over = True
                        return Screen.GAMING

            if 10 < x < 100 and 10 < y < 100:
                menuAlgo.drawMenuAlgo()
                self.alphaBeta.initialize_game()
                self.minMax.initialize_game()
                self.game_over = False
                return Screen.SELECT_AIGO

        return Screen.GAMING

    def update_score(self, result):
        with open('game_data.json', 'r') as f:
            data = json.load(f)

        if result == 'X':
            data['player_score'] += 1
        elif result == 'O':
            data['ai_score'] += 1
        elif result == '.':
            data['draws'] += 1

        with open('game_data.json', 'w') as f:
            json.dump(data, f, indent=4)
