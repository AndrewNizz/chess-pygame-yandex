import pygame
import pprint
import copy

WHITE = 1
BLACK = 0
current = 'white'


def opposite(turn):
    return 'white' if turn == 'black' else 'black'


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
            pass
        if new_cell is not None and new_cell.color != self.color:
            self.eat(pos)
            return True
        else:
            board[self.row][self.col] = None
            self.row = pos[0]
            self.col = pos[1]
            board[pos[0]][pos[1]] = self
            return True


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
            return False
        if king_under_attack and not self.can_defend(king_under_attack, king):
            return False
        if bo.is_connected(self):
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
        board_copy = board[:][:]
        king = white_king if piece.color == 'white' else black_king
        board_copy[piece.row][piece.col] = None
        for row in board_copy:
            for p in row:
                if p is not None and p.color != piece.color and p.can_move((king.row, king.col)):
                    return True
        return False

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
                if piece.ext_can_move((r, c)):
                    pygame.draw.circle(surf, (100, 100, 100, 10), (c * 94 + 47, r * 94 + 47), 10)
        surf.blit(piece.image, (piece.col * 94, piece.row * 94))


bo = Board()
board, white_king, black_king = bo.create_board()
white_check, black_check = False, False
white_eaten, black_eaten = [], []
blacks, whites = board[0] + board[1], board[6] + board[7]
benefits = {Pawn: 1, Knight: 3, Bishop: 3, Rook: 5, Queen: 9}


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
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dy != 0 or dx != 0:
                if not kingg.ext_can_move((kingg.row + dy, kingg.col + dx)):
                    c += 1
    if c >= 8:
        return True
    return False


def main():
    global current
    pygame.init()
    size = (1100, 754)
    screen = pygame.display.set_mode(size)
    screen.fill((250, 250, 250))
    new_screen = pygame.Surface(size, pygame.SRCALPHA)
    pygame.display.set_caption('Шахматы')
    width = height = 93
    margin = 1
    color_1 = (160, 82, 45)
    color_2 = (245, 222, 179)

    runnung = True
    picked = None

    while runnung:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnung = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('down')
                pos = event.pos
                if picked is None:
                    r, c = pos[0] // 94, pos[1] // 94
                    picked = board[c][r]
                    print(f'picked {board[c][r]} {picked.row, picked.col} {current=}')
                else:
                    r, c = pos[0] // 94, pos[1] // 94
                    if picked.color == current:
                        print(isinstance(picked, King), picked.row == 0, picked.col == 4, picked.color == 'black')
                        res = picked.move((c, r))
                        picked.moved = True
                        print(c, r)
                        print(f'moved {picked}, {picked.row, picked.col} {res}')
                        picked = None
                        if res:
                            current = opposite(current)
                        print(f'{current=}')
                    else:
                        print('not your turn')

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    color = color_1
                else:
                    color = color_2

                y = row * height + (row + 1) * margin
                x = col * width + (col + 1) * margin
                pygame.draw.rect(new_screen, color, (x, y, width, height))
        for row in board:
            for piece in row:
                if piece is not None:
                    new_screen.blit(piece.image, (piece.col * 94, piece.row * 94))

        if picked is not None:
            bo.color_cells(new_screen, picked)

        bo.draw_check_square(new_screen)

        if check_winner(black_king):
            draw_text('WHITE WINS', 1100, 754, new_screen)
        elif check_winner(white_king):
            draw_text('BLACK WINS', 1100, 754, new_screen)

        screen.blit(new_screen, (0, 0))
        pygame.display.update()


main()