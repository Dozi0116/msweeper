import string
import random

class Board:
    def __init__(self, height, width, bomb):
        self.height = height
        self.width = width
        self.bomb = bomb
        self.invisible_square_num = height * width

        self.square = [[Square() for i in range(width+2)]for i in range(height+2)]

    def open(self, x, y):
        if self.square[y][x].visible_state != 0:
            return
        else:
            self.square[y][x].visible_state = 1
            self.invisible_square_num -= 1

        check_table = [[-1,-1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
        for i in check_table:
            if self.square[y + i[0]][x + i[1]].state == 1: #bomb
                self.square[y][x].around_bomb += 1

        if self.square[y][x].around_bomb == 0:
            for i in check_table:
                self.open(x+i[1], y+i[0])
        

    def show(self):

        print('   ' + string.ascii_lowercase[:self.width])
        for i in range(1, self.width+1):
            print(str(i).rjust(2) + ' ', end = '')
            for j in range(1, self.height+1):
                if self.square[i][j].visible_state in {0, -1}: #invisible
                    print('.', end = '')
                elif self.square[i][j].visible_state == 1: #visible
                    if self.square[i][j].state == 1:
                        print('M', end = '')
                    elif self.square[i][j].around_bomb == 0: 
                        print(' ', end = '')
                    else:
                        print(self.square[i][j].around_bomb, end = '')
                elif self.square[i][j].visible_state == 2: #flag
                    print('P', end = '')
                elif self.square[i][j].visible_state == 3: #?
                    print('?', end='')

            print('')

    def setting(self, x, y):
        #put bomb
        bomb_count = self.bomb
        for i in range(1, self.height+1):
            for j in range(1, self.width+1):
                if bomb_count > 0:
                    self.square[i][j].state = 1
                    self.square[i][j].visible_state = 0
                    bomb_count -= 1
                else:
                    self.square[i][j].state = 0
                    self.square[i][j].visible_state = 0
            
        #swap
        for i in range(self.height * self.width):
            a = [random.randint(1, self.height), random.randint(1, self.width)]
            b = [random.randint(1, self.height), random.randint(1, self.width)]
            self.square[a[0]][a[1]], self.square[b[0]][b[1]] = self.square[b[0]][b[1]], self.square[a[0]][a[1]]
        
        while self.square[y][x].state == 1:
            b = [random.randint(1, self.height), random.randint(1, self.width)]
            self.square[y][x], self.square[b[0]][b[1]] = self.square[b[0]][b[1]], self.square[y][x]

class Square:
    def __init__(self):
        self.visible_state = -1
        self.state = 0
        self.around_bomb = 0
        



def init_game():
    print('in init_game')
    print('out init_game')


def preprocess_game(board_info):
    
    while True:
        print('Please serect board size(number of bomb)')
        print('1: 9* 9(10)\n2:16*16(40)\n3:25*25(90)\n4: other')
        command = int(input())
        if command in range(1, 5): # 1 <= command && command < 5
            break

    #set board info
    if command == 1:
        height = width = 9
        bomb = 10
    elif command == 2:
        height = width = 16
        bomb = 40
    elif command == 3:
        height = width = 25
        bomb = 90
    elif command == 4:
        while True:
            height = int(input('Please enter the height size(5-26)'))
            if height in range(5, 27):
                break
        while True:
            width = int(input('Please enter the width size(5-26)'))
            if width in range(5, 27):
                break
        while True:
            bomb = int(input('Please enter the number of bombs(5-' + str(height * width - 2)  + ')'))
            if bomb in range(5,height * width - 1):
                break

    board_info['height'] = height
    board_info['width'] = width
    board_info['bomb'] = bomb


def read_command(command, board):
    
    while True:
        temp_x = input('Please enter the open square x-axis(a-' + string.ascii_lowercase[board.width-1] + ')').lower() #大文字対策
        temp_y = input('Please enter the open square y-axis(1-' + str(board.height) + ')')
        
        if ord(temp_x[0]) - ord('a') + 1 in range(1, board.width+1) and int(temp_y) in range(1, board.height+1):
            command['x'] = ord(temp_x[0]) - ord('a') + 1
            command['y'] = int(temp_y)
            break


def main_game(height, width, bomb):
    board = Board(height, width, bomb)

    command = {}
    board.show()
    read_command(command, board)
    board.setting(command['x'], command['y'])

    while True:
        board.open(command['x'], command['y'])

        if board.square[command['y']][command['x']].state == 1:
            return False
        elif board.invisible_square_num <= board.bomb:
            for i in range(1, height+1):
                for j in range(1, width+1):
                    if board.square[i][j].state == 1:
                        board.square[i][j].visible_state = 2
            board.show()
            return True
        
        board.show()

        read_command(command, board)


def postprocess_game(is_clear):
    if is_clear:
        print('GAME CLEAR!!')
    else:
        print('GAME OVER')

    while True:
        print('continue? y/n')
        command = input()
        if command in {'y', 'n'}:
            break

    return command


if __name__ == '__main__':
    init_game()
    
    board_info = {}

    while True:
        preprocess_game(board_info)
        is_clear = main_game(board_info['height'], board_info['width'], board_info['bomb'])
        cont = postprocess_game(is_clear)

        if cont == 'n':
            break



