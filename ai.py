import random

class TicTacToeAI:
    def __init__(self, ai_player="O", difficulty="easy"):
        self.ai_player = ai_player
        self.human_player = "X" if ai_player == "O" else "O"
        self.difficulty = difficulty  # 'easy', 'medium', 'hard'

    def get_move(self, board):
        if self.difficulty == "easy":
            return self.random_move(board)
        elif self.difficulty == "medium":
            return self.medium_move(board)
        elif self.difficulty == "hard":
            return self.minimax_move(board)
        else:
            return self.random_move(board)

    def random_move(self, board):
        available_moves = [i for i, cell in enumerate(board) if cell == ""]
        return random.choice(available_moves) if available_moves else None

    def medium_move(self, board):
        # Block human winning move if possible
        for move in self.available_moves(board):
            board_copy = board[:]
            board_copy[move] = self.human_player
            if self.check_winner(board_copy, self.human_player):
                return move
        return self.random_move(board)

    def minimax_move(self, board):
        best_score = -float('inf')
        best_move = None
        for move in self.available_moves(board):
            board[move] = self.ai_player
            score = self.minimax(board, False)
            board[move] = ""
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, is_maximizing):
        if self.check_winner(board, self.ai_player):
            return 1
        elif self.check_winner(board, self.human_player):
            return -1
        elif "" not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.available_moves(board):
                board[move] = self.ai_player
                score = self.minimax(board, False)
                board[move] = ""
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves(board):
                board[move] = self.human_player
                score = self.minimax(board, True)
                board[move] = ""
                best_score = min(score, best_score)
            return best_score

    def available_moves(self, board):
        return [i for i, cell in enumerate(board) if cell == ""]

    def check_winner(self, board, player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for line in wins:
            if all(board[i] == player for i in line):
                return True
        return False
