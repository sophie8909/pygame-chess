import time
import sys
inf = 10000
class algorithm():
    def __init__(self, board):
        self.board = board
        self.start_time = 0.0
    def is_time_limit(self):
        return time.time() - self.start_time >= 60
        # return False
    # start from p1 turn
    def negative_max(self, depth, is_p1_turn, move):
        best_value = -inf
        best_move = move
        if depth <= 0 or self.board.is_game_end() or self.is_time_limit():
            return self.board.evaluate(), move
        
        for legal_move in self.board.generate_legal_moves(is_p1_turn):
            ori_black_board = self.board.black_board
            ori_white_board = self.board.white_board
            # make the move
            self.board.move_chessmen(legal_move)
            value, move = self.negative_max(depth-1, not is_p1_turn, legal_move)
            value = -value
            # undo the move
            self.board.black_board = ori_black_board
            self.board.white_board = ori_white_board

            if value > best_value:
                best_value = value
                if is_p1_turn:
                    best_move = legal_move
        # self.my_chessboard.show_whole_board()
        print(f"{depth}", file=sys.stderr, flush=True)
        # print()
        return best_value, best_move
    def min_value(self, depth, alpha, beta, move):
        min_value = inf
        best_move = move
        # self.board.show_whole_board()
        # print(f"{depth}", file=sys.stderr, flush=True)
        if depth <= 0 or self.board.is_game_end() or self.is_time_limit():
            return self.board.evaluate(), move
        for legal_move in self.board.generate_legal_moves(False):
            ori_black_board = self.board.black_board
            ori_white_board = self.board.white_board
            # make the move
            self.board.move_chessmen(legal_move)
            value, move = self.max_value(depth-1, alpha, beta, legal_move)
            # undo the move
            self.board.black_board = ori_black_board
            self.board.white_board = ori_white_board

            if value < min_value:
                min_value = value
            if min_value <= alpha: 
                return min_value, best_move
            beta = min(beta, min_value)
        # self.my_chessboard.show_whole_board()
        
        # print()
        return min_value, best_move
    def max_value(self, depth, alpha, beta, move):
        max_value = -inf
        best_move = move
        # print(f"{depth}", file=sys.stderr, flush=True)
        # self.board.show_whole_board()
        
        # print(self.board.evaluate(), file=sys.stderr, flush=True)
        if depth <= 0 or self.board.is_game_end() or self.is_time_limit():
            return self.board.evaluate(), move
        for legal_move in self.board.generate_legal_moves(True):
            ori_black_board = self.board.black_board
            ori_white_board = self.board.white_board
            # make the move
            self.board.move_chessmen(legal_move)
            value, move = self.min_value(depth-1, alpha, beta, legal_move)
            # undo the move
            self.board.black_board = ori_black_board
            self.board.white_board = ori_white_board

            if value > max_value:
                max_value = value
                best_move = legal_move
            if max_value >= beta: 
                return max_value, best_move
            alpha = max(alpha, max_value)
        # self.my_chessboard.show_whole_board()
        
        # print()
        return max_value, best_move
            
    def alpha_beta_pruning(self, depth, alpha, beta, move):
        return self.max_value(depth, alpha, beta, move)
    def mcts(self, depth, move):
        pass