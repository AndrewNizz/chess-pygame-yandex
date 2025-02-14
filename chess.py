from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QPlainTextEdit
from PyQt6.QtCore import QTimer, Qt, QTime
from PyQt6.QtGui import QImage, QPixmap, QPainter, QFont
from copy import deepcopy
import sys
import csv
import datetime

import pygame

WHITE = 1
BLACK = 0
current = 'white'

nums_to_letters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}


def opposite(turn):
    return 'white' if turn == 'black' else 'black'


def write_log(log):
    with open('logs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quotechar='"')
        writer.writerow([log + f' at {datetime.datetime.now()}'])


class Rook:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moved = False
        if color == 'white':
            self.image = pygame.image.load('white-rook.png')
        else:
            self.image = pygame.image.load('black-rook.png')
        self.image = pygame.transform.scale(self.image, (90, 90))

    def can_move(self, pos):
        r, c = pos
        new_cell = board[r][c]
        if r > 7 or r < 0 or c > 7 or c < 0 or\
                (self.row != r and self.col != c):
            return False
        if self.check_obstacles(pos):
            return False
        if new_cell is not None and new_cell.color == self.color:
            return False
        if bo.is_connected(self):
            return False
        return True

    def ext_can_move(self, pos):
        king = white_king if self.color == 'white' else black_king
        king_under_attack = king.under_attack()
        if not self.can_move(pos):
            return False
        if king_under_attack and not self.can_defend(king_under_attack, king):
            return False
        if bo.is_connected(self):
            return False
        return True

    def check_obstacles(self, pos):
        r, c = pos
        if r != self.row and c != self.col:
            return True
        step = 1 if r >= self.row else -1
        for i in range(self.row + step, r, step):
            if board[i][self.col] is not None:
                return True

        step = 1 if c >= self.col else -1
        for i in range(self.col + step, c, step):
            if board[self.row][i] is not None:
                return True
        return False

    def can_defend(self, offender, kng):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.can_move((i, j)) and offender.can_move((i, j)) and board[i][j] != kng:
                    return True
        return False

    def eat(self, pos):  # дописать изменение состава съеденных фигур у игроков
        eaten = board[pos[0]][pos[1]]
        board[self.row][self.col] = None
        self.row = pos[0]
        self.col = pos[1]
        if self.color == 'white':
            black_eaten.append(eaten)
        else:
            white_eaten.append(eaten)
        board[pos[0]][pos[1]] = self
        return True

    def move(self, pos):
        new_cell = board[pos[0]][pos[1]]
        if not self.ext_can_move(pos):
            return False
        if new_cell is not None and new_cell.color != self.color:
            self.eat(pos)
            return True
        else:
            board[self.row][self.col] = None
            self.row = pos[0]
            self.col = pos[1]
            board[pos[0]][pos[1]] = self
            return True

    def letter(self):
        return 'R'


class Bishop:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moved = False
        if color == 'white':
            self.image = pygame.image.load('white-bishop.png')
        else:
            self.image = pygame.image.load('black-bishop.png')
        self.image = pygame.transform.scale(self.image, (90, 90))

    def can_move(self, pos):
        r, c = pos
        new_cell = board[r][c]
        if r > 7 or r < 0 or c > 7 or c < 0:
            return False
        if self.row == r or self.col == c:
            return False
        if new_cell is not None and new_cell.color == self.color:
            return False
        if not abs(self.row - r) == abs(self.col - c):
            return False
        if self.check_obstacles(pos):
            return False
        return True

    def ext_can_move(self, pos):
        king = white_king if self.color == 'white' else black_king
        king_under_attack = king.under_attack()
        if not self.can_move(pos):
            return False
        if king_under_attack and not self.can_defend(king_under_attack, king):
            return False
        if bo.is_connected(self):
            return False
        return True

    def check_obstacles(self, pos):
        r, c = pos
        stepr = 1 if self.row <= r else -1
        stepc = 1 if self.col <= c else -1
        for i in range(1, abs(self.row - r)):
            ind = self.row + i * stepr
            ind2 = self.col + i * stepc
            if board[self.row + i * stepr][self.col + i * stepc] is not None:
                return True
        return False

    def can_defend(self, offender, kng):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.can_move((i, j)) and offender.can_move((i, j)) and board[i][j] != kng:
                    return True
        return False

    def eat(self, pos):  # дописать изменение состава съеденных фигур у игроков
        eaten = board[pos[0]][pos[1]]
        board[self.row][self.col] = None
        self.row = pos[0]
        self.col = pos[1]
        if self.color == 'white':
            black_eaten.append(eaten)
        else:
            white_eaten.append(eaten)
        board[pos[0]][pos[1]] = self
        return True

    def move(self, pos):
        new_cell = board[pos[0]][pos[1]]
        if not self.ext_can_move(pos):
            return False
        if new_cell is not None and new_cell.color != self.color:
            self.eat(pos)
            return True
        else:
            board[self.row][self.col] = None
            self.row = pos[0]
            self.col = pos[1]
            board[pos[0]][pos[1]] = self
            return True

    def letter(self):
        return 'B'


class Knight:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moved = False
        if color == 'white':
            self.image = pygame.image.load('white-knight.png')
        else:
            self.image = pygame.image.load('black-knight.png')
        self.image = pygame.transform.scale(self.image, (90, 90))

    def can_move(self, pos):
        r, c = pos
        new_cell = board[r][c]
        if r > 7 or r < 0 or c > 7 or c < 0:
            return False
        if not((abs(self.row - r) == 2 and abs(self.col - c) == 1) or
               (abs(self.row - r) == 1 and abs(self.col - c) == 2)):
            return False
        if new_cell is not None and new_cell.color == self.color:
            return False
        return True

    def ext_can_move(self, pos):
        king = white_king if self.color == 'white' else black_king
        king_under_attack = king.under_attack()
        if not self.can_move(pos):
            return False
        if king_under_attack and not self.can_defend(king_under_attack, king):
            return False
        if bo.is_connected(self):
            return False
        return True

    def can_defend(self, offender, kng):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.can_move((i, j)) and offender.can_move((i, j)) and board[i][j] != kng:
                    return True
        return False

    def eat(self, pos):
        eaten = board[pos[0]][pos[1]]
        board[self.row][self.col] = None
        self.row = pos[0]
        self.col = pos[1]
        if self.color == 'white':
            black_eaten.append(eaten)
        else:
            white_eaten.append(eaten)
        board[pos[0]][pos[1]] = self
        return True

    def move(self, pos):
        new_cell = board[pos[0]][pos[1]]
        if not self.ext_can_move(pos):
            return False
        if new_cell is not None and new_cell.color != self.color:
            self.eat(pos)
            return True
        else:
            board[self.row][self.col] = None
            self.row = pos[0]
            self.col = pos[1]
            board[pos[0]][pos[1]] = self
            return True

    def letter(self):
        return 'N'


class Queen:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moved = False
        if color == 'white':
            self.image = pygame.image.load('white-queen.png')
        else:
            self.image = pygame.image.load('black-queen.png')
        self.image = pygame.transform.scale(self.image, (90, 90))

    def can_move(self, pos):
        r, c = pos
        new_cell = board[r][c]
        if r > 7 or r < 0 or c > 7 or c < 0:
            return False
        if not abs(self.row - r) == abs(self.col - c) and not(self.row == r or self.col == c):
            return False
        if self.check_obstacles(pos):
            return False
        if new_cell is not None and new_cell.color == self.color:
            return False
        return True

    def ext_can_move(self, pos):
        king = white_king if self.color == 'white' else black_king
        king_under_attack = king.under_attack()
        if not self.can_move(pos):
            return False
        if king_under_attack and not self.can_defend(king_under_attack, king):
            return False
        if bo.is_connected(self):
            return False
        return True

    def check_obstacles(self, pos):
        r, c = pos
        if abs(self.row - r) == abs(self.col - c):
            stepr = 1 if self.row <= r else -1
            stepc = 1 if self.col <= c else -1
            for i in range(1, abs(self.row - r)):
                if board[self.row + stepr * i][self.col + stepc * i] is not None:
                    return True

        elif self.row == r or self.col == c:
            step = 1 if self.row <= r else -1
            for ii in range(self.row + step, r, step):
                if board[ii][self.col] is not None:
                    return True

            step = 1 if self.col <= c else -1
            for i in range(self.col + step, c, step):
                if board[self.row][c] is not None:
                    return True
        return False

    def can_defend(self, offender, kng):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.can_move((i, j)) and offender.can_move((i, j)) and board[i][j] != kng:
                    return True
        return False

    def eat(self, pos):
        eaten = board[pos[0]][pos[1]]
        board[self.row][self.col] = None
        self.row = pos[0]
        self.col = pos[1]
        if self.color == 'white':
            black_eaten.append(eaten)
        else:
            white_eaten.append(eaten)
        board[pos[0]][pos[1]] = self
        return True

    def move(self, pos):
        new_cell = board[pos[0]][pos[1]]
        if not self.ext_can_move(pos):
            return False
        if new_cell is not None and new_cell.color != self.color:
            self.eat(pos)
            return True
        else:
            board[self.row][self.col] = None
            self.row = pos[0]
            self.col = pos[1]
            board[pos[0]][pos[1]] = self
            return True

    def letter(self):
        return 'Q'


class King:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moved = False
        if color == 'white':
            self.image = pygame.image.load('white-king.png')
        else:
            self.image = pygame.image.load('black-king.png')
        self.image = pygame.transform.scale(self.image, (90, 90))

    def can_move(self, pos):
        r, c = pos
        new_cell = board[r][c]
        if r > 7 or r < 0 or c > 7 or c < 0:
            return False
        if new_cell is not None and new_cell.color == self.color:
            return False
        if (r == self.row == 7 or r == self.row == 0) and (abs(self.col - c) == 2 or abs(self.col - c) == 3) \
                and not self.moved:
            return 'castle'
        if self.row != r and self.col != c and abs(self.row - r) != abs(self.col - c):
            return False
        elif abs(self.row - r) != 1 and abs(self.col - c) != 1:
            return False
        return True

    def under_attack(self):
        for row in board:
            for p in row:
                if p is not None and p.color != self.color and p.can_move((self.row, self.col)):
                    return p
        return False

    def cell_under_attack(self, pos):
        for row in board:
            for p in row:
                if p is not None and p.color != self.color and p.can_move(pos):
                    return True
        return False

    def ext_can_move(self, pos):
        if not self.can_move(pos):
            return False
        if self.cell_under_attack(pos):
            return False
        return True

    def eat(self, pos):
        eaten = board[pos[0]][pos[1]]
        board[self.row][self.col] = None
        self.row = pos[0]
        self.col = pos[1]
        if self.color == 'white':
            black_eaten.append(eaten)
        else:
            white_eaten.append(eaten)
        board[pos[0]][pos[1]] = self
        return True

    def move(self, pos):
        new_cell = board[pos[0]][pos[1]]
        res = self.ext_can_move(pos)
        if not res:
            return False
        if res == 'castle':
            return bo.castling(self, pos[1])
        if new_cell is not None and new_cell.color != self.color:
            self.eat(pos)
            return True
        else:
            board[self.row][self.col] = None
            self.row = pos[0]
            self.col = pos[1]
            board[pos[0]][pos[1]] = self
            return True

    def letter(self):
        return 'K'


class Pawn:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moved = False
        if color == 'white':
            self.image = pygame.image.load('white-pawn.png')
        else:
            self.image = pygame.image.load('black-pawn.png')
        self.image = pygame.transform.scale(self.image, (90, 90))

    def can_move(self, pos):
        r, c = pos
        new_cell = board[r][c]
        qwe = new_cell is not None and new_cell.color == self.color
        if r > 7 or r < 0 or c > 7 or c < 0:
            return False
        if qwe:
            return False
        if self.color == 'white' and r > self.row:
            return False
        elif self.color == 'black' and r < self.row:
            return False
        if abs(self.row - r) == 1 and abs(self.col - c) == 1 and new_cell is not None and new_cell.color != self.color:
            return True
        if self.moved is False and abs(r - self.row) == 2 and abs(self.col - c) == 0 and not qwe:
            return True
        if not (abs(self.row - r) == 1 and abs(self.col - c) == 0):
            return False
        return True

    def ext_can_move(self, pos):
        king = white_king if self.color == 'white' else black_king
        king_under_attack = king.under_attack()
        if not self.can_move(pos):
            print('passed1')
            return False
        if king_under_attack and not self.can_defend(king_under_attack, king):
            print('passed2')
            return False
        if bo.is_connected(self):
            print('passed3')
            return False
        return True

    def move(self, pos):
        new_cell = board[pos[0]][pos[1]]
        if not self.ext_can_move(pos):
            return False
        if new_cell is not None and new_cell.color != self.color:
            self.eat(pos)
            return True
        else:
            board[self.row][self.col] = None
            self.row = pos[0]
            self.col = pos[1]
            board[pos[0]][pos[1]] = self
            return True

    def eat(self, pos):
        eaten = board[pos[0]][pos[1]]
        board[self.row][self.col] = None
        self.row = pos[0]
        self.col = pos[1]
        if self.color == 'white':
            black_eaten.append(eaten)
        else:
            white_eaten.append(eaten)
        board[pos[0]][pos[1]] = self
        return True

    def can_defend(self, offender, kng):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.can_move((i, j)) and offender.can_move((i, j)) and board[i][j] != kng:
                    return True
        return False

    def letter(self):
        return 'P'


class Board:
    def __init__(self):
        pass

    def create_board(self):
        white_king, black_king = None, None
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        b = [[None] * 8 for _ in range(8)]
        for i in range(8):
            p_bl = pieces[i](0, i, 'black')
            p_wh = pieces[i](7, i, 'white')
            if isinstance(p_wh, King):
                white_king = p_wh
                black_king = p_bl
            b[0][i] = p_bl
            b[1][i] = Pawn(1, i, 'black')
            b[6][i] = Pawn(6, i, 'white')
            b[7][i] = p_wh
        return b, white_king, black_king

    def is_connected(self, piece):
        try:
            board_copy = deepcopy(board)
            king = white_king if piece.color == 'white' else black_king
            print(isinstance(piece, Pawn))
            print(piece.row, piece.col)
            board_copy[piece.row][piece.col] = None
            for row in board_copy:
                for p in row:
                    if p is not None and p.color != piece.color and p.can_move((king.row, king.col)):
                        return True
            return False
        except Exception as e:
            print(e)

    def castling(self, kingg, coll): # добавить как особенный ход короля -> изменить кен мув
        row = 0 if kingg.color == 'white' else 7
        rook = board[row][0] if coll == 1 else board[row][7]
        if rook is None or rook.moved or not isinstance(rook, Rook):
            return False
        rook_col = 2 if coll == 1 else 4
        board[kingg.row][kingg.col] = None
        board[row][coll] = kingg
        kingg.row, kingg.col = row, coll
        board[rook.row][rook.col] = None
        board[row][rook_col] = rook
        rook.row, rook.col = row, rook_col
        return True

    def draw_check_square(self, surf):
        if white_king.under_attack():
            pygame.draw.rect(surf, (255, 0, 0), (white_king.col * 93, white_king.row * 93, 93, 93), 4)
        elif black_king.under_attack():
            pygame.draw.rect(surf, (255, 0, 0), (black_king.col * 93 + 5, black_king.row * 93, 93, 93), 4)

    def color_cells(self, surf, piece): # если что это раньше было методом класса
        for r in range(8):
            for c in range(8):
                if piece.ext_can_move((r, c)) and piece.color == current:
                    pygame.draw.circle(surf, (100, 100, 100, 10), (c * 94 + 47, r * 94 + 47), 10)
        surf.blit(piece.image, (piece.col * 94, piece.row * 94))


bo = Board()
board, white_king, black_king = bo.create_board()
white_check, black_check = False, False
white_eaten, black_eaten = [], []
blacks, whites = board[0] + board[1], board[6] + board[7]
benefits = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}


def draw_text(text, w, h, surf):
    font = pygame.font.Font(None, 70)
    text = font.render(text, True, (100, 255, 100))
    text_x = w // 2 - text.get_width() // 2
    text_y = h // 2 - text.get_height() // 2
    surf.blit(text, (text_x, text_y))
    pygame.display.flip()


def check_winner(kingg): # добавить в основной цикл
    underatt = kingg.under_attack()
    if not underatt:
        return False
    c = 0
    cd = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dy != 0 or dx != 0:
                if not kingg.ext_can_move((kingg.row + dy, kingg.col + dx)):
                    c += 1
    if c >= 8:
        for i in board:
            for j in i:
                if j is not None and j.color == kingg.color and j.can_defend(underatt, kingg):
                    return False
        return True
    return False


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Первое окно")
        self.setGeometry(100, 100, 700, 400)

        pixmap = QPixmap('background.jpg')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        image = QLabel(self)
        image.resize(self.width(), self.height())
        # Отображаем содержимое QPixmap в объекте QLabel
        image.setPixmap(pixmap)
        layout = QVBoxLayout()
        layout.addWidget(image)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.text_lbl = QLabel(self)
        self.text_lbl.resize(600, 400)
        self.text_lbl.setText('Добро пожаловать в шахматы!\nНажмите любую клавишу чтобы продолжить')
        self.text_lbl.setFont(QFont('Arial', 20))
        self.text_lbl.setStyleSheet('''color: rgb(250, 250, 250);
                                       text-align: center;''')
        self.text_lbl.move(700 // 2 - self.text_lbl.width() // 2, 400 // 2 - self.text_lbl.height() // 2)

    def keyPressEvent(self, event):
        # Проверяем, была ли нажата клавиша пробела
        self.closeEvent(event)
        self.destroy()

    def closeEvent(self, event):
        # Создаем второе окно и показываем его
        self.second_window = MainWindow()
        self.second_window.show()
        event.accept()  # Закрываем первое окно


class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(1, 1, 1000, 700)

        self.timer_white = QTimer(self)
        self.time_left_white = 10 * 60
        self.timer_white.timeout.connect(self.update_timer_white)

        self.timer_black = QTimer(self)
        self.time_left_black = 10 * 60
        self.timer_black.timeout.connect(self.update_timer_black)

        # Таймер для обновления Pygame
        self.main_timer = QTimer(self)
        self.main_timer.timeout.connect(self.update_pygame)
        self.start_btn = QPushButton(self)
        self.start_btn.setText('START')
        self.start_btn.setFont(QFont('Arial', 16))
        self.start_btn.resize(210, 32)
        self.start_btn.setStyleSheet('''QPushButton {
                                            border-radius:10px;
                                            background-color:rgb(200,200,200);
                                        }
                                        QPushButton:hover {
                                            background-color:rgb(245,245,245);
                                            border: 2px solid rgb(1,1,1);
                                        }''')
        self.start_btn.move(730, 25)
        self.start_btn.clicked.connect(self.start_timer)

        self.lbl1 = QLabel(self)
        self.lbl1.setText('White:')
        self.lbl1.resize(200, self.lbl1.height())
        self.lbl1.setFont(QFont('Arial', 13))
        self.lbl1.move(730, 90)
        self.white_timer_lbl = QLabel(self)
        self.white_timer_lbl.resize(200, 30)
        self.white_timer_lbl.setFont(QFont('Arial', 13))
        self.white_timer_lbl.setStyleSheet('''background-color:rgb(240,240,240);
                                                border-radius:15px;
                                                justify-content:center;''')
        self.white_timer_lbl.setText(self.format_time(self.time_left_white))
        self.white_timer_lbl.move(730, 120)

        self.lbl2 = QLabel(self)
        self.lbl2.setText('Black:')
        self.lbl2.setFont(QFont('Arial', 13))
        self.lbl2.resize(200, self.lbl2.height())
        self.lbl2.move(730, 200)
        self.black_timer_lbl = QLabel(self)
        self.black_timer_lbl.resize(200, 30)
        self.black_timer_lbl.setFont(QFont('Arial', 13))
        self.black_timer_lbl.setStyleSheet('''background-color:rgb(240,240,240);
                                                        border-radius:15px;
                                                        justify-content:center;''')
        self.black_timer_lbl.setText(self.format_time(self.time_left_black))
        self.black_timer_lbl.move(730, 230)

        self.lbl3 = QLabel(self)
        self.lbl3.setText('Moves:')
        self.lbl3.setFont(QFont('Arial', 13))
        self.lbl3.move(730, 300)
        self.moves_lbl = QPlainTextEdit(self)
        self.moves_lbl.setStyleSheet('''border: 2px solid rgb(2,2,2);
                                        border-radius:10px;''')
        self.moves_lbl.setFont(QFont('Arial', 10))
        self.moves_lbl.resize(230, 320)
        self.moves_lbl.sizeHint()
        self.moves_lbl.move(730, 330)

        self.mouse_pos = (400, 300)
        self.left_button_pressed = False
        self.setMouseTracking(True)
        self.init_pygame()

    def display_benefits(self):
        total_wh = 0
        total_bl = 0
        for i in board:
            for j in i:
                if j is not None:
                    if j.color == 'white':
                        total_wh += benefits[j.letter()]
                    else:
                        total_bl += benefits[j.letter()]
        if total_wh > total_bl:
            self.lbl1.setText(f'White: +{total_wh - total_bl}')
        elif total_bl > total_wh:
            self.lbl2.setText(f'Black: +{total_bl - total_wh}')

    def init_pygame(self):
        pygame.init()
        size = (1100, 754)
        self.screen = pygame.Surface(size)
        self.screen.fill((250, 250, 250))
        self.new_screen = pygame.Surface(size, pygame.SRCALPHA)
        self.width_ = self.height_ = 93
        self.margin = 1
        self.picked = None
        self.time_over_wh = False
        self.time_over_bl = False
        self.prev_pos = 0, 0

        # Запуск таймера для игрового цикла
        self.main_timer.start(16)  # ~60 FPS

    def mouseMoveEvent(self, event):
        # Обновляем позицию мыши
        self.mouse_pos = (event.position().x(), event.position().y())

    def mousePressEvent(self, event):
        # Обработка нажатия левой кнопки мыши
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_button_pressed = True
        elif event.button() == Qt.MouseButton.RightButton:
            self.left_button_pressed = True
    def mouseReleaseEvent(self, event):
        # Обработка отпускания левой кнопки мыши
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_button_pressed = False

    def update_pygame(self):
        try:
            pos = self.mouse_pos
            r, c = int((pos[0] + 40) // 93), int((pos[1] + 40) // 93)
            if self.left_button_pressed and self.prev_pos != (c, r):
                global current
                write_log(f'button down at {c, r}')
                print(pos)
                if self.picked is None:
                    print('lalala')
                    print(c, r)
                    try:
                        self.picked = board[c][r]
                        write_log(f'picked {board[c][r]} {self.picked.row, self.picked.col} {current=}')
                        print(f'picked {board[c][r]} {self.picked.row, self.picked.col} {current=}')
                    except Exception as e:
                        print(e)
                    self.prev_pos = (c, r)
                else:
                    print('smak', self.left_button_pressed)
                    if self.picked.color == current:
                        res = self.picked.move((c, r))
                        self.picked.moved = True
                        print(c, r)
                        write_log(f'moved {self.picked}, {self.picked.row, self.picked.col} {res}')
                        print(f'moved {self.picked}, {self.picked.row, self.picked.col} {res}')
                        try:
                            self.moves_lbl.setPlainText(self.moves_lbl.toPlainText() + '\n' +
                                                        f'{self.picked.letter()}{nums_to_letters[c]}{r}')
                        except Exception as e:
                            print(e)
                        self.picked = None
                        if res:
                            if current == 'white':
                                self.timer_white.stop()
                                self.timer_black.start(1000)
                                write_log('timer stopped WHITE')
                            elif current == 'black':
                                self.timer_black.stop()
                                self.timer_white.start(1000)
                                write_log('timer stopped BLACK')
                            current = opposite(current)
                        write_log(f'{current=}')
                        self.prev_pos = (c, r)
                        self.display_benefits()
                    else:
                        print('not your turn')
        except Exception as e:
            print(e)

        color_1 = (160, 82, 45)
        color_2 = (245, 222, 179)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    color = color_1
                else:
                    color = color_2

                y = row * self.height_ + (row + 1) * self.margin
                x = col * self.width_ + (col + 1) * self.margin
                pygame.draw.rect(self.new_screen, color, (x, y, self.width_, self.height_))
        for row in board:
            for piece in row:
                if piece is not None:
                    self.new_screen.blit(piece.image, (piece.col * 94, piece.row * 94))

        if self.picked is not None:
            bo.color_cells(self.new_screen, self.picked)

        bo.draw_check_square(self.new_screen)
        if check_winner(black_king) or self.time_over_bl:
            draw_text('WHITE WINS', 500, 500, self.new_screen)
        elif check_winner(white_king) or self.time_over_wh:
            draw_text('BLACK WINS', 500, 500, self.new_screen)

        self.screen.blit(self.new_screen, (0, 0))
        # Обновляем виджет
        self.update()

    def paintEvent(self, event):
        # Отображаем поверхность Pygame на виджете Qt
        if hasattr(self, 'screen'):
            # Преобразуем поверхность Pygame в QImage
            buf = pygame.image.tostring(self.screen, 'RGBA')
            image = QImage(buf, self.screen.get_width(), self.screen.get_height(), QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(image)

            # Рисуем QPixmap на виджете
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), pixmap)
            painter.end()

    def start_timer(self):
        if not self.timer_white.isActive():
            self.timer_white.start(1000)
        else:
            self.timer_white.stop()

    def update_timer_white(self):
        if self.time_left_white > 0:
            self.time_left_white -= 1
            self.white_timer_lbl.setText(self.format_time(self.time_left_white))
        else:
            self.timer_white.stop()
            self.white_timer_lbl.setText("Время вышло!")
            self.time_over_wh = True

    def update_timer_black(self):
        if self.time_left_black > 0:
            self.time_left_black -= 1
            self.black_timer_lbl.setText(self.format_time(self.time_left_black))
        else:
            self.timer_black.stop()
            self.black_timer_lbl.setText("Время вышло!")
            self.time_over_bl = True

    def format_time(self, seconds):
        time = QTime(0, 0)
        time = time.addSecs(seconds)
        return time.toString("mm:ss")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(10, 10, 1000, 700)
        self.setWindowTitle("Pygame in PyQt6")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Создаем виджет с Pygame
        self.pygame_widget = PygameWidget()
        layout.addWidget(self.pygame_widget)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем первое окно
    first_window = StartWindow()
    first_window.show()

    sys.exit(app.exec())
