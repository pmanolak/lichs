import threading
import datetime
import chess

import os

from .render import render_board


def format_clock(td):
    """Format a timedelta as MM:SS."""
    total_seconds = max(0, int(td.total_seconds()))
    return "%02d:%02d" % (total_seconds // 60, total_seconds % 60)


class Game(threading.Thread):

    def __init__(self, board, game_id, player_id, isWhite, color, time, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.board = board
        self.stream = board.stream_game_state(game_id)
        self.player_id = player_id
        self.isWhite = isWhite
        self.color = color
        self.chess_board = chess.Board()
        # Seed the clock with the time control; the server sends authoritative
        # times (as timedeltas) in every gameState after that.
        start_time = datetime.timedelta(minutes=time)
        self.clock = {'white': start_time, 'black': start_time}
        if self.isWhite:
            self.white_first_move()

    def run(self):
        for event in self.stream:
            if event['type'] == "gameFull":
                self.handle_game_full(event)
            elif event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    def handle_state_change(self, game_state):

        if game_state.get(self.color[0].lower() + "draw") is True:
            self.handle_draw_state(game_state)
        elif game_state["status"] == "resign":
            print("The opponent resigned. Congrats!")
            os._exit(0)

        else:
            # update time (berserk gives wtime/btime as timedeltas)
            self.clock['white'] = game_state['wtime']
            self.clock['black'] = game_state['btime']

            # there's no "amount of turns" variable in the JSON, so we have to construct one manually
            turn = len(game_state["moves"].split())-1
            if turn%2 == self.isWhite:

                print(self.color + " moved.")
                print()

                self.chess_board.push_uci(game_state["moves"].split()[-1])
                self.display_board()
                print()

                self.check_mate()

                self.prompt_move()

                self.display_board()
                self.check_mate()
                print()
                print(self.color + "'s turn...")

    def handle_game_full(self, gamefull):
        # TODO Write this method
        pass

    def handle_draw_state(self, game_state):
        # TODO Write this method
        pass

    def handle_chat_line(self, event):
        # TODO Write this method
        pass

    def white_first_move(self):
        self.display_board()
        self.prompt_move()
        self.display_board()
        print(self.color + "'s turn...")

    def prompt_move(self):
        """Read a legal move (or a resignation) from the user and play it."""
        while True:
            try:
                move = input("Make your move: ")
                if move.lower() == "resign":
                    self.board.resign_game(self.game_id)
                    print("You resigned the game!")
                    print("Thanks for playing!")
                    os._exit(0)
                else:
                    chess_move = self.chess_board.parse_san(move)
                    self.board.make_move(self.game_id, chess_move.uci())
                    self.chess_board.push(chess_move)
            except Exception as e:
                print("You can't make that move. Try again!")
                print(f"Reason: {e}")
                continue
            break

    def check_mate(self):
        result = self.chess_board.result()
        if result == "*":
            return
        if result == "1-0":
            won = self.isWhite
        elif result == "0-1":
            won = not self.isWhite
        else:  # "1/2-1/2"
            won = None

        if won is None:
            print("The game ended in a stalemate (draw)!")
        elif won:
            print("Congrats! You won by checkmating your opponent!")
        else:
            print("You lose! Your opponent has checkmated you!")

        print("Thanks for playing!")
        os._exit(0)

    def display_board(self):
        # highlight the most recent move, if there is one
        last_move = self.chess_board.peek() if self.chess_board.move_stack else None
        print(render_board(self.chess_board, self.isWhite, last_move))

        print("[%s : %s]" % (format_clock(self.clock['white']),
                             format_clock(self.clock['black'])))
        print()
