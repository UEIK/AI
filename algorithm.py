from program import *
import json

class Algorithm:
    def __init__(self, board_size=3):
        self.result = None
        self.board_size = board_size
        self.initialize_game()

    def initialize_game(self):
        self.current_state = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.player_turn = 'X'

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px >= self.board_size or py < 0 or py >= self.board_size:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        win_count_needed = 3 if self.board_size == 3 else 5

        for i in range(self.board_size):
            for j in range(self.board_size - win_count_needed + 1):
                if self.current_state[i][j] != '.':
                    win = True
                    for k in range(1, win_count_needed):
                        if self.current_state[i][j] != self.current_state[i][j + k]:
                            win = False
                            break
                    if win:
                        return self.current_state[i][j]

        for i in range(self.board_size - win_count_needed + 1):
            for j in range(self.board_size):
                if self.current_state[i][j] != '.':
                    win = True
                    for k in range(1, win_count_needed):
                        if self.current_state[i][j] != self.current_state[i + k][j]:
                            win = False
                            break
                    if win:
                        return self.current_state[i][j]

        for i in range(self.board_size - win_count_needed + 1):
            for j in range(self.board_size - win_count_needed + 1):
                if self.current_state[i][j] != '.':
                    win = True
                    for k in range(1, win_count_needed):
                        if self.current_state[i][j] != self.current_state[i + k][j + k]:
                            win = False
                            break
                    if win:
                        return self.current_state[i][j]

        for i in range(self.board_size - win_count_needed + 1):
            for j in range(win_count_needed - 1, self.board_size):
                if self.current_state[i][j] != '.':
                    win = True
                    for k in range(1, win_count_needed):
                        if self.current_state[i][j] != self.current_state[i + k][j - k]:
                            win = False
                            break
                    if win:
                        return self.current_state[i][j]

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == '.':
                    return None

        self.result = '.'
        return '.'

    def check_winer(self, gaming=None):
        self.result = self.is_end()
        print(f"check_winer called, result = {self.result}")  # Debug
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
                pygame.draw.rect(DISPLAYSURF, WHITE, (440, 290, 250, 60))
                DISPLAYSURF.blit(FONT.render("  NGƯỜI THẮNG", True, RED, WHITE), (460, 300))
                if gaming:
                    gaming.update_score('X')
            elif self.result == 'O':
                print('The winner is O!')
                pygame.draw.rect(DISPLAYSURF, WHITE, (440, 290, 250, 60))
                DISPLAYSURF.blit(FONT.render("  MÁY THẮNG", True, RED, WHITE), (460, 300))
                if gaming:
                    gaming.update_score('O')
            elif self.result == '.':
                print("It's a tie!")
                pygame.draw.rect(DISPLAYSURF, WHITE, (440, 290, 250, 60))
                DISPLAYSURF.blit(FONT.render("     HÒA   ", True, RED, WHITE), (460, 300))
                if gaming:
                    gaming.update_score('.')
            pygame.display.update()  # Cập nhật UI ngay lập tức
            return True
        return False

    def evaluate(self):
        score = 0
        for i in range(self.board_size):
            for j in range(self.board_size - 1):
                if self.current_state[i][j] == 'O' and self.current_state[i][j + 1] == 'O':
                    score += 0.1
                if self.current_state[i][j] == 'X' and self.current_state[i][j + 1] == 'X':
                    score -= 0.1
        for i in range(self.board_size - 1):
            for j in range(self.board_size):
                if self.current_state[i][j] == 'O' and self.current_state[i + 1][j] == 'O':
                    score += 0.1
                if self.current_state[i][j] == 'X' and self.current_state[i + 1][j] == 'X':
                    score -= 0.1
        for i in range(self.board_size - 1):
            for j in range(self.board_size - 1):
                if self.current_state[i][j] == 'O' and self.current_state[i + 1][j + 1] == 'O':
                    score += 0.1
                if self.current_state[i][j] == 'X' and self.current_state[i + 1][j + 1] == 'X':
                    score -= 0.1
        for i in range(self.board_size - 1):
            for j in range(1, self.board_size):
                if self.current_state[i][j] == 'O' and self.current_state[i + 1][j - 1] == 'O':
                    score += 0.1
                if self.current_state[i][j] == 'X' and self.current_state[i + 1][j - 1] == 'X':
                    score -= 0.1
        return score

class MinMax(Algorithm):
    def __init__(self, board_size=3):
        super().__init__(board_size)
        self.max_depth = 9 if board_size == 3 else 3

    def max(self, depth=0):
        maxv = -2
        px = None
        py = None
        result = self.is_end()
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        if self.board_size == 5 and depth >= self.max_depth:
            return (self.evaluate(), 0, 0)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min(depth + 1)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'
        return (maxv, px, py)

    def min(self, depth=0):
        minv = 2
        qx = None
        qy = None
        result = self.is_end()
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        if self.board_size == 5 and depth >= self.max_depth:
            return (self.evaluate(), 0, 0)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max(depth + 1)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'
        return (minv, qx, qy)

    def play_min_max(self, px=0, py=0, ai_First=False, gaming=None):
        if self.check_winer(gaming):
            return

        if ai_First:
            (m, px, py) = self.max()
            self.current_state[px][py] = 'O'
            self.player_turn = 'X'
            if self.check_winer(gaming):
                return
            return

        if self.is_valid(px, py):
            self.current_state[px][py] = 'X'
            self.player_turn = 'O'
        else:
            return

        if self.check_winer(gaming):
            return

        (m, px, py) = self.max()

        if px is None or py is None:
            return

        self.current_state[px][py] = 'O'
        self.player_turn = 'X'

        if self.check_winer(gaming):
            return

class AlphaBeta(Algorithm):
    def __init__(self, board_size=3):
        super().__init__(board_size)
        self.max_depth = 9 if board_size == 3 else 3

    def max_alpha_beta(self, alpha, beta, depth=0):
        maxv = -2
        px = None
        py = None
        result = self.is_end()
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        if self.board_size == 5 and depth >= self.max_depth:
            return (self.evaluate(), 0, 0)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min_alpha_beta(alpha, beta, depth + 1)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'
                    if maxv >= beta:
                        return (maxv, px, py)
                    if maxv > alpha:
                        alpha = maxv
        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta, depth=0):
        minv = 2
        qx = None
        qy = None
        result = self.is_end()
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        if self.board_size == 5 and depth >= self.max_depth:
            return (self.evaluate(), 0, 0)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta, depth + 1)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'
                    if minv <= alpha:
                        return (minv, qx, qy)
                    if minv < beta:
                        beta = minv
        return (minv, qx, qy)

    def play_alpha_beta(self, px=0, py=0, ai_First=False, gaming=None):
        if self.check_winer(gaming):
            return
        if ai_First:
            (m, px, py) = self.max_alpha_beta(-2, 2)
            self.current_state[px][py] = 'O'
            self.player_turn = 'X'
            if self.check_winer(gaming):
                return
            return
        if self.is_valid(px, py):
            self.current_state[px][py] = 'X'
            self.player_turn = 'O'
            print(px, py)
        else:
            print('The move is not valid! Try again.')
            return
        if self.check_winer(gaming):
            return
        (m, px, py) = self.max_alpha_beta(-2, 2)
        self.current_state[px][py] = 'O'
        self.player_turn = 'X'
        if self.check_winer(gaming):
            return