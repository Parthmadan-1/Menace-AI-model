
#! /usr/bin/env python3

from collections import Counter
import random


class Board:
   
    # constructor to initialize the board
    def __init__(self):
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    # function to print the board
    def __str__(self):
        return("\n 0 | 1 | 2     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 3 | 4 | 5     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 6 | 7 | 8     %s | %s | %s" % (self.board[0], self.board[1], self.board[2],
                                                self.board[3], self.board[4], self.board[5],
                                                self.board[6], self.board[7], self.board[8]))

    # function to check if the move we trying is valid or not
    def valid_move(self, move):
        try:
            move = int(move)
        except ValueError:
            return False
        if 0 <= move <= 8 and self.board[move] == ' ':
            return True
        return False

    # checking the winning condition
    def winning(self):
        return ((self.board[0] != ' ' and
                 ((self.board[0] == self.board[1] == self.board[2]) or
                  (self.board[0] == self.board[3] == self.board[6]) or
                  (self.board[0] == self.board[4] == self.board[8])))
                or (self.board[4] != ' ' and
                    ((self.board[1] == self.board[4] == self.board[7]) or
                    (self.board[3] == self.board[4] == self.board[5]) or
                    (self.board[2] == self.board[4] == self.board[6])))
                or (self.board[8] != ' ' and
                    ((self.board[2] == self.board[5] == self.board[8]) or
                    (self.board[6] == self.board[7] == self.board[8]))))

    
    # If all the elements in the board are not equal to a single space character, then this method returns True. Otherwise, it returns False.
    def draw(self):
        return all((x != ' ' for x in self.board))


    # function to make the move.
    def play_move(self, position, marker):
        self.board[position] = marker

    # function to return the board in the string form.
    def board_string(self):
        return ''.join(self.board)


class MenacePlayer:
    def __init__(self):
        # dictionary to store the beads corresponding to each board state
        self.matchboxes = {}
        self.num_win = 0
        self.num_draw = 0
        self.num_lose = 0

    def start_game(self):
      # list to store the tuples (board,bead) for each state.
      # what is the optimal bead  for each board state such that the manace is most likely to win.
        self.moves_played = []

    def get_move(self, board):
        # Find board in matchboxes and choose a bead
        # If the matchbox is empty, return -1 (resign)
        board = board.board_string()
        if board not in self.matchboxes:
            # making new beads for the board state
            new_beads = [pos for pos, mark in enumerate(board) if mark == ' ']
            # Early boards start with more beads
            self.matchboxes[board] = new_beads * ((len(new_beads) + 2) // 2)

        beads = self.matchboxes[board]
        if len(beads):
           # selecting random bead from the list of beads
            bead = random.choice(beads)
            # adding the move to the moves_played list
            self.moves_played.append((board, bead))
        else:
            # if the length of beads list is 0 ,the return 0
            bead = -1
        return bead

    def win_game(self):
        # We won, add three beads to each of the board state in moves_played
        for (board, bead) in self.moves_played:
            self.matchboxes[board].extend([bead, bead, bead])
        self.num_win += 1

    def draw_game(self):
        # A draw, add one bead
        for (board, bead) in self.moves_played:
            self.matchboxes[board].append(bead)
        self.num_draw += 1

    def lose_game(self):
        # Lose, remove a bead
        for (board, bead) in self.moves_played:
            matchbox = self.matchboxes[board]
            del matchbox[matchbox.index(bead)]
        self.num_lose += 1

    # function to print the summary of the training of menac
    def print_stats(self):
        print('Have learnt %d boards' % len(self.matchboxes))
        # printing how many boards menac has learned in the process of training.
        print('W/D/L: %d/%d/%d' % (self.num_win, self.num_draw, self.num_lose))
        # printing how many games menac has won,drawn and lose while the process of training.

    def print_probability(self, board):
        board = board.board_string()
        try:
            print("Stats for this board: " +
                  str(Counter(self.matchboxes[board]).most_common()))
            # printing the number of beads of each type present in the board state
        except KeyError:
            print("Never seen this board before.")


class HumanPlayer:
    def __init__(self):
        pass

    def start_game(self):
        print("Get ready!")

    def get_move(self, board):
        while True:
            move = input('Make a move: ')
            if board.valid_move(move):
                break
            print("Not a valid move")
        return int(move)

    def win_game(self):
        print("You won!")

    def draw_game(self):
        print("It's a draw.")

    def lose_game(self):
        print("You lose.")

    def print_probability(self, board):
        pass


def play_game(first, second, silent=False):
    first.start_game()
    second.start_game()
    board = Board()

    if not silent:
        print("\n\nStarting a new game!")
        print(board)

    while True:
        if not silent:
            first.print_probability(board)
        move = first.get_move(board)
        if move == -1:
            if not silent:
                print("Player resigns")
            first.lose_game()
            second.win_game()
            break
        board.play_move(move, 'X')
        if not silent:
            print(board)
        if board.winning():
            first.win_game()
            second.lose_game()
            break
        if board.draw():
            first.draw_game()
            second.draw_game()
            break

        if not silent:
            second.print_probability(board)
        move = second.get_move(board)
        if move == -1:
            if not silent:
                print("Player resigns")
            second.lose_game()
            first.win_game()
            break
        board.play_move(move, 'O')
        if not silent:
            print(board)
        if board.winning():
            second.win_game()
            first.lose_game()
            break


if __name__ == '__main__':
    go_first_menace = MenacePlayer()
    go_second_menace = MenacePlayer()
    human = HumanPlayer()

    for i in range(1000):
        play_game(go_first_menace, go_second_menace, silent=True)

    go_first_menace.print_stats()
    go_second_menace.print_stats()

    play_game(go_first_menace, human)
    play_game(human, go_second_menace)
     
