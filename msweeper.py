import string

class Board:
    def __init__(self, height, width, bomb):
        self.height = height
        self.width = width
        self.bomb = bomb

        self.square = [[Square() for i in range(width+2)]for i in range(height+2)]

    def open(self, x, y):
        if self.square[y][x].visible_state != 0:
            return
        else:
            self.square[y][x].visible_state = 1

        check_table = [[-1,-1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

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
                if self.square[i][j].visible_state == 0: #invisible
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

class Square:
    def __init__(self):
        self.visible_state = -1
        self.state = 0
        self.around_bomb = 0
        


def setting_board(board):
    print('in setting_board')
    #put bomb
    bomb_count = board.bomb
    for i in range(1, board.height+1):
        for j in range(1, board.width+1):
            if bomb_count > 0:
                board.square[i][j].state = 1
                board.square[i][j].visible_state = 0
                bomb_count -= 1
            else:
                board.square[i][j].state = 0
                board.square[i][j].visible_state = 0
            
    board.show()
    print('out setting_board')


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


def main_game(height, width, bomb):
    print('in main_game')
    board = Board(height, width, bomb)
    board.show()
    setting_board(board)

    while True:
        while True:
            temp_x = input('Please enter the open square x-axis(a-' + string.ascii_lowercase[width-1] + ')').lower() #大文字対策
            temp_y = input('Please entre the open square y-axis(1-' + str(height) + ')')
            
            if ord(temp_x[0]) - ord('a') + 1 in range(1, width+1) and int(temp_y) in range(1, height+1):
                command_x = ord(temp_x[0]) - ord('a') + 1
                command_y = int(temp_y)
                break

        board.open(command_x, command_y)
        board.show()
        if board.square[command_y][command_x].state == 1:
            break
            

    print('out main_game')


def postprocess_game(board_info):
    print('in postprocess_game')

    while True:
        print('continue? y/n')
        command = input()
        if command in {'y', 'n'}:
            break

    print('out postprocess_game')
    return command


if __name__ == '__main__':
    init_game()
    
    board_info = {}

    while True:
        preprocess_game(board_info)
        main_game(board_info['height'], board_info['width'], board_info['bomb'])
        cont = postprocess_game(board_info)

        if cont == 'n':
            break



