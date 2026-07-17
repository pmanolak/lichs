"""Terminal rendering of a chess board.

The colours and piece glyphs are inspired by the `chs` project
(https://github.com/nickzuber/chs): real wood-tone squares with colored
Unicode pieces, rank/file coordinates and last-move / check highlighting.
"""

import chess


class Colors:
    RESET = "\x1b[0m"
    GRAY = "\x1b[38;5;242m"
    # Piece foreground colors
    WHITE_PIECE = "\x1b[38;5;231;1m"
    BLACK_PIECE = "\x1b[38;5;232;1m"

    class Bg:
        LIGHT = "\x1b[48;5;215m"       # light (tan) square
        DARK = "\x1b[48;5;172m"        # dark (wood) square
        MOVE_LIGHT = "\x1b[48;5;143m"  # last move, light square
        MOVE_DARK = "\x1b[48;5;136m"   # last move, dark square
        CHECK = "\x1b[48;5;9m"         # king in check


# Filled glyphs for every piece; the color (not the glyph) distinguishes sides.
PIECE_GLYPHS = {
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]


def render_board(chess_board, is_white, last_move=None):
    """Return a string drawing of ``chess_board`` from the player's point of view.

    :param chess_board: a ``chess.Board``
    :param is_white: ``True`` to view from White's side, ``False`` from Black's
    :param last_move: optional ``chess.Move`` to highlight
    """
    ranks = range(7, -1, -1) if is_white else range(8)
    files = range(8) if is_white else range(7, -1, -1)

    check_square = None
    if chess_board.is_check():
        check_square = chess_board.king(chess_board.turn)

    highlighted = set()
    if last_move is not None:
        highlighted = {last_move.from_square, last_move.to_square}

    lines = []
    for rank in ranks:
        row = " {}{} ".format(Colors.GRAY, rank + 1)  # rank label
        for file in files:
            square = chess.square(file, rank)
            is_light = (rank + file) % 2 == 1

            if square == check_square:
                bg = Colors.Bg.CHECK
            elif square in highlighted:
                bg = Colors.Bg.MOVE_LIGHT if is_light else Colors.Bg.MOVE_DARK
            else:
                bg = Colors.Bg.LIGHT if is_light else Colors.Bg.DARK

            piece = chess_board.piece_at(square)
            if piece is None:
                cell = "  "
            else:
                fg = Colors.WHITE_PIECE if piece.color == chess.WHITE else Colors.BLACK_PIECE
                cell = "{}{} ".format(fg, PIECE_GLYPHS[piece.symbol().lower()])
            row += "{}{}{}".format(bg, cell, Colors.RESET)
        lines.append(row)

    # File labels along the bottom.
    file_labels = FILES if is_white else FILES[::-1]
    footer = "   {}{}".format(Colors.GRAY, "".join(" " + f for f in file_labels))
    lines.append(footer + Colors.RESET)

    return "\n".join(lines)
