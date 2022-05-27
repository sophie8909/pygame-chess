class breakthrough_board():
    def __init__(self, p1_is_white):
        # save who is white(first)
        self.p1_is_white = p1_is_white
        # save white chessmen's position with bitmap
        self.white_board = self.generate_half_chessmen()
        self.black_board = self.white_board << (8*6)
        self.row_bitmap = 0 
        for col in range(8):
            self.row_bitmap += 1 << col
        self.white_home_row = self.row_bitmap
        self.black_home_row = self.row_bitmap << (7*8)
        self.col_bitmap = 0
        for row in range(8):
            self.col_bitmap += 1 << row*8
        self.a_bound = self.col_bitmap
        self.h_bound = self.col_bitmap << 7
        self.alive_credit = 100
        self.win_credit = 1000
        
        
        
        
    def position_credit(self, row_from_home):
        return row_from_home ** 2
    def black_rewards(self):
        rewards = 0
        position = 1
        for row in range(8):
            for col in range(8):
                if self.black_board & position:
                    # win
                    if row == 0:
                        rewards += self.win_credit
                    # position
                    rewards += self.position_credit(8-row)
                    # alive 
                    rewards += self.alive_credit
                position <<= 1
        return rewards
    def white_rewards(self):
        rewards = 0
        position = 1
        for row in range(8):
            for col in range(8):
                if self.white_board & position:
                    # win
                    if row == 7:
                        rewards += self.win_credit
                    # position  
                    rewards += self.position_credit(row+1)
                    # alive 
                    rewards += self.alive_credit

                position <<= 1
        return rewards       
    # generate two row of chessmen
    def generate_half_chessmen(self):
        chessmen = 0
        for i in range(16):
            chessmen += 1 << i
        return chessmen
    def show_whole_board(self):
        board = ''
        for r in range(8):
            row = ''
            if self.white_home_row & 1 << (r * 8):
                board += ' abcdefgh '[::-1] + '\n'
            for c in range(8):
                position = r*8+c
                if self.a_bound & (1 << position):
                    row += str(r+1)
                if self.black_board & (1 << position):
                    row += 'B'
                elif self.white_board & (1 << position):
                    row += 'W'
                else:
                    row += ' '
                if self.h_bound & (1 << position):
                    row += str(r+1)
            board += row[::-1] + '\n'
            if self.black_home_row & 1 << (r * 8):
                board += ' abcdefgh '[::-1] + '\n'
        print(board[::-1], file=sys.stderr, flush=True)
    def set_player_chess(self, white):
        if white == 'p1':
            self.p1_is_white = True
    def print_bitmap(self, bitmap):
        board = ''
        for r in range(8):
            row = ''
            if self.white_home_row & 1 << (r * 8):
                board += ' abcdefgh '[::-1] + '\n'
            for c in range(8):
                position = r*8+c
                if self.a_bound & (1 << position):
                    row += str(r+1)
                if bitmap & (1 << position):
                    row += '1'
                else:
                    row += ' '
                if self.h_bound & (1 << position):
                    row += str(r+1)
            board += row[::-1] + '\n'
            if self.black_home_row & 1 << (r * 8):
                board += ' abcdefgh '[::-1] + '\n'
        print(board[::-1], file=sys.stderr, flush=True)
    # convert from board coordinate to bitmap
    def board_to_bitmap(self, p):
        # print(p, file=sys.stderr, flush=True)
        col = ord(p[0]) - ord('a')
        row = ord(p[1]) - ord('1')
        # print(row, col, file=sys.stderr, flush=True)
        return 1 << (row*8 + col)
    # convert from bitmap to board coordinate 
    def bitmap_to_board(self, row, col):
        command = str(chr(col+ord('a')))
        command += str(row+1)
        
        return command
    def move_chessmen(self, command):
        # print("command in move_chessmen()", command, file=sys.stderr, flush=True)
        ori, new = command[:2], command[2:]
        ori, new = self.board_to_bitmap(ori), self.board_to_bitmap(new)
        # move chess is black
        if ori & self.black_board:
            self.black_board ^= ori
            self.black_board |= new
            if new & self.white_board:
                self.white_board ^= new
        # move chess is white
        else:
            self.white_board ^= ori
            self.white_board |= new
            if new & self.black_board:
                self.black_board ^= new
        # self.show_whole_board()
    def is_game_end(self):
        # white chess is reaching black's home row or black chess is reaching white's home row
        return (self.black_home_row & self.white_board) or (self.white_home_row & self.black_board)
    def generate_legal_moves(self, is_p1_turn):
        is_white_turn = False
        # is p1 turn and p1 is white or is p2 turn and p2 is white
        if (is_p1_turn and self.p1_is_white) or (not is_p1_turn and not self.p1_is_white):
            is_white_turn = True
        # print("is_white_turn", is_white_turn, file=sys.stderr, flush=True)
        legal_moves = []
        if is_white_turn:
            position = 1
            for row in range(7):
                for col in range(8):
                    now_position_coordinate = self.bitmap_to_board(row, col)
                    
                    # print("now_position_coordinate", now_position_coordinate, file=sys.stderr, flush=True)
                    if self.white_board & position:
                        target_position = position << 7
                        # left diagonally (can be empty or black(eat it))
                        if (not (position & self.a_bound)) and (not (self.white_board & target_position)):
                            legal_moves.append(now_position_coordinate+self.bitmap_to_board(row+1, col-1))
                        
                        target_position <<= 1
                        # forward (must be empty)
                        if not (self.white_board & target_position or self.black_board & target_position):
                            legal_moves.append(now_position_coordinate+self.bitmap_to_board(row+1, col))
                        target_position <<= 1
                        # right diagonally (can be empty or black(eat it))
                        if (not (position & self.h_bound)) and  (not (self.white_board & target_position)):
                            legal_moves.append(now_position_coordinate+self.bitmap_to_board(row+1, col+1))
                    position <<= 1
        # is black turn  
        else:
            position = 1<<8
            for row in range(1, 8):
                for col in range(8):
                    now_position_coordinate = self.bitmap_to_board(row, col)
                    # print(f"{row} {col} {now_position_coordinate}", file=sys.stderr, flush=True)
                    if self.black_board & position:
                        target_position = position >> 7
                        # right diagonally (can be empty or white(eat it))
                        if (not (position & self.h_bound)) and  (not (self.black_board & target_position)):
                            legal_moves.append(now_position_coordinate+self.bitmap_to_board(row-1, col+1))
                        
                        target_position >>= 1
                        # forward (must be empty)
                        if not (self.white_board & target_position or self.black_board & target_position):
                            legal_moves.append(now_position_coordinate+self.bitmap_to_board(row-1, col))
                        target_position >>= 1
                        
                         # left diagonally (can be empty or white(eat it))
                        if (not (position & self.a_bound)) and (not (self.black_board & target_position)):
                            legal_moves.append(now_position_coordinate+self.bitmap_to_board(row-1, col-1))
                    position <<= 1            
        # print(f"legal_moves:{legal_moves}", file=sys.stderr, flush=True)
        return legal_moves
    
    '''
    reward is sum of all chessmen's square of distance from home row
    if chessmen is eaten, its reward is 0
    '''
    def evaluate(self):
        reward = 0
        if self.p1_is_white:
            reward = self.white_rewards() - self.black_rewards()
        else:
            reward = self.black_rewards() - self.white_rewards()
        return reward