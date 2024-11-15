import textwrap

import pytest

from kingdom_chess import (
    Board,
    Color,
    make_move,
    MoveException,
    Piece,
    PieceType,
    Position,
)


def test_coordinates_should_not_point_outside_board():
    with pytest.raises(ValueError):
        Position(-1, 4)
    with pytest.raises(ValueError):
        Position(8, 4)
    with pytest.raises(ValueError):
        Position(2, -1)
    with pytest.raises(ValueError):
        Position(2, 8)


def test_board_should_place_a_piece():
    board = Board()
    board[Position(3, 6)] = Piece(PieceType.KNIGHT, Color.WHITE)
    assert board[Position(3, 6)] == Piece(PieceType.KNIGHT, Color.WHITE)


def test_board_should_be_empty_be_default():
    board = Board()

    assert board[Position(0, 0)] is None
    assert board[Position(1, 0)] is None
    assert board[Position(2, 0)] is None
    assert board[Position(3, 0)] is None
    assert board[Position(4, 0)] is None
    assert board[Position(5, 0)] is None
    assert board[Position(6, 0)] is None
    assert board[Position(7, 0)] is None

    assert board[Position(0, 1)] is None
    assert board[Position(1, 1)] is None
    assert board[Position(2, 1)] is None
    assert board[Position(3, 1)] is None
    assert board[Position(4, 1)] is None
    assert board[Position(5, 1)] is None
    assert board[Position(6, 1)] is None
    assert board[Position(7, 1)] is None

    assert board[Position(0, 2)] is None
    assert board[Position(1, 2)] is None
    assert board[Position(2, 2)] is None
    assert board[Position(3, 2)] is None
    assert board[Position(4, 2)] is None
    assert board[Position(5, 2)] is None
    assert board[Position(6, 2)] is None
    assert board[Position(7, 2)] is None

    assert board[Position(0, 3)] is None
    assert board[Position(1, 3)] is None
    assert board[Position(2, 3)] is None
    assert board[Position(3, 3)] is None
    assert board[Position(4, 3)] is None
    assert board[Position(5, 3)] is None
    assert board[Position(6, 3)] is None
    assert board[Position(7, 3)] is None

    assert board[Position(0, 4)] is None
    assert board[Position(1, 4)] is None
    assert board[Position(2, 4)] is None
    assert board[Position(3, 4)] is None
    assert board[Position(4, 4)] is None
    assert board[Position(5, 4)] is None
    assert board[Position(6, 4)] is None
    assert board[Position(7, 4)] is None

    assert board[Position(0, 5)] is None
    assert board[Position(1, 5)] is None
    assert board[Position(2, 5)] is None
    assert board[Position(3, 5)] is None
    assert board[Position(4, 5)] is None
    assert board[Position(5, 5)] is None
    assert board[Position(6, 5)] is None
    assert board[Position(7, 5)] is None

    assert board[Position(0, 6)] is None
    assert board[Position(1, 6)] is None
    assert board[Position(2, 6)] is None
    assert board[Position(3, 6)] is None
    assert board[Position(4, 6)] is None
    assert board[Position(5, 6)] is None
    assert board[Position(6, 6)] is None
    assert board[Position(7, 6)] is None

    assert board[Position(0, 7)] is None
    assert board[Position(1, 7)] is None
    assert board[Position(2, 7)] is None
    assert board[Position(3, 7)] is None
    assert board[Position(4, 7)] is None
    assert board[Position(5, 7)] is None
    assert board[Position(6, 7)] is None
    assert board[Position(7, 7)] is None


def test_board_should_be_initialy_filled():
    board = Board.initialy_filled()

    assert board[Position(0, 0)] == Piece(PieceType.ROOK, Color.BLACK)
    assert board[Position(1, 0)] == Piece(PieceType.KNIGHT, Color.BLACK)
    assert board[Position(2, 0)] == Piece(PieceType.BISHOP, Color.BLACK)
    assert board[Position(3, 0)] == Piece(PieceType.QUEEN, Color.BLACK)
    assert board[Position(4, 0)] == Piece(PieceType.KING, Color.BLACK)
    assert board[Position(5, 0)] == Piece(PieceType.BISHOP, Color.BLACK)
    assert board[Position(6, 0)] == Piece(PieceType.KNIGHT, Color.BLACK)
    assert board[Position(7, 0)] == Piece(PieceType.ROOK, Color.BLACK)

    assert board[Position(0, 1)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(1, 1)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(2, 1)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(3, 1)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(4, 1)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(5, 1)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(6, 1)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(7, 1)] == Piece(PieceType.PAWN, Color.BLACK)

    assert board[Position(0, 2)] is None
    assert board[Position(1, 2)] is None
    assert board[Position(2, 2)] is None
    assert board[Position(3, 2)] is None
    assert board[Position(4, 2)] is None
    assert board[Position(5, 2)] is None
    assert board[Position(6, 2)] is None
    assert board[Position(7, 2)] is None

    assert board[Position(0, 3)] is None
    assert board[Position(1, 3)] is None
    assert board[Position(2, 3)] is None
    assert board[Position(3, 3)] is None
    assert board[Position(4, 3)] is None
    assert board[Position(5, 3)] is None
    assert board[Position(6, 3)] is None
    assert board[Position(7, 3)] is None

    assert board[Position(0, 4)] is None
    assert board[Position(1, 4)] is None
    assert board[Position(2, 4)] is None
    assert board[Position(3, 4)] is None
    assert board[Position(4, 4)] is None
    assert board[Position(5, 4)] is None
    assert board[Position(6, 4)] is None
    assert board[Position(7, 4)] is None

    assert board[Position(0, 5)] is None
    assert board[Position(1, 5)] is None
    assert board[Position(2, 5)] is None
    assert board[Position(3, 5)] is None
    assert board[Position(4, 5)] is None
    assert board[Position(5, 5)] is None
    assert board[Position(6, 5)] is None
    assert board[Position(7, 5)] is None

    assert board[Position(0, 6)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(1, 6)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(2, 6)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(3, 6)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(4, 6)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(5, 6)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(6, 6)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(7, 6)] == Piece(PieceType.PAWN, Color.WHITE)

    assert board[Position(0, 7)] == Piece(PieceType.ROOK, Color.WHITE)
    assert board[Position(1, 7)] == Piece(PieceType.KNIGHT, Color.WHITE)
    assert board[Position(2, 7)] == Piece(PieceType.BISHOP, Color.WHITE)
    assert board[Position(3, 7)] == Piece(PieceType.QUEEN, Color.WHITE)
    assert board[Position(4, 7)] == Piece(PieceType.KING, Color.WHITE)
    assert board[Position(5, 7)] == Piece(PieceType.BISHOP, Color.WHITE)
    assert board[Position(6, 7)] == Piece(PieceType.KNIGHT, Color.WHITE)
    assert board[Position(7, 7)] == Piece(PieceType.ROOK, Color.WHITE)


def test_board_should_be_convertable_to_mapping():
    board = Board()

    board[Position(2, 1)] = Piece(PieceType.KNIGHT, Color.WHITE)
    board[Position(3, 4)] = Piece(PieceType.QUEEN, Color.BLACK)

    assert board.to_mapping() == {
        Position(2, 1): Piece(PieceType.KNIGHT, Color.WHITE),
        Position(3, 4): Piece(PieceType.QUEEN, Color.BLACK),
    }


def test_board_should_be_created_from_mapping():
    state = {
        Position(0, 3): Piece(PieceType.KNIGHT, Color.WHITE),
        Position(2, 4): Piece(PieceType.QUEEN, Color.BLACK),
    }

    board = Board.from_mapping(state)

    assert board[Position(0, 3)] == Piece(PieceType.KNIGHT, Color.WHITE)
    assert board[Position(2, 4)] == Piece(PieceType.QUEEN, Color.BLACK)
    assert board[Position(3, 6)] is None


def test_board_should_be_created_from_unicode():
    board = Board.from_unicode("""
        ⋅ ♛ ⋅ ⋅ ⋅ ⋅ ♖ ⋅
        ⋅ ⋅ ⋅ ♕ ⋅ ⋅ ⋅ ⋅
        ⋅ ♞ ⋅ ⋅ ⋅ ♙ ⋅ ⋅
        ⋅ ⋅ ♟ ⋅ ♗ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ♘ ⋅
        ⋅ ♜ ⋅ ⋅ ⋅ ♔ ⋅ ⋅
        ⋅ ⋅ ♝ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ♚ ⋅ ⋅ ⋅
    """)

    assert board[Position(0, 0)] is None
    assert board[Position(1, 0)] == Piece(PieceType.QUEEN, Color.BLACK)
    assert board[Position(2, 0)] is None
    assert board[Position(3, 0)] is None
    assert board[Position(4, 0)] is None
    assert board[Position(5, 0)] is None
    assert board[Position(6, 0)] == Piece(PieceType.ROOK, Color.WHITE)
    assert board[Position(7, 0)] is None

    assert board[Position(0, 1)] is None
    assert board[Position(1, 1)] is None
    assert board[Position(2, 1)] is None
    assert board[Position(3, 1)] == Piece(PieceType.QUEEN, Color.WHITE)
    assert board[Position(4, 1)] is None
    assert board[Position(5, 1)] is None
    assert board[Position(6, 1)] is None
    assert board[Position(7, 1)] is None

    assert board[Position(0, 2)] is None
    assert board[Position(1, 2)] == Piece(PieceType.KNIGHT, Color.BLACK)
    assert board[Position(2, 2)] is None
    assert board[Position(3, 2)] is None
    assert board[Position(4, 2)] is None
    assert board[Position(5, 2)] == Piece(PieceType.PAWN, Color.WHITE)
    assert board[Position(6, 2)] is None
    assert board[Position(7, 2)] is None

    assert board[Position(0, 3)] is None
    assert board[Position(1, 3)] is None
    assert board[Position(2, 3)] == Piece(PieceType.PAWN, Color.BLACK)
    assert board[Position(3, 3)] is None
    assert board[Position(4, 3)] == Piece(PieceType.BISHOP, Color.WHITE)
    assert board[Position(5, 3)] is None
    assert board[Position(6, 3)] is None
    assert board[Position(7, 3)] is None

    assert board[Position(0, 4)] is None
    assert board[Position(1, 4)] is None
    assert board[Position(2, 4)] is None
    assert board[Position(3, 4)] is None
    assert board[Position(4, 4)] is None
    assert board[Position(5, 4)] is None
    assert board[Position(6, 4)] == Piece(PieceType.KNIGHT, Color.WHITE)
    assert board[Position(7, 4)] is None

    assert board[Position(0, 5)] is None
    assert board[Position(1, 5)] == Piece(PieceType.ROOK, Color.BLACK)
    assert board[Position(2, 5)] is None
    assert board[Position(3, 5)] is None
    assert board[Position(4, 5)] is None
    assert board[Position(5, 5)] == Piece(PieceType.KING, Color.WHITE)
    assert board[Position(6, 5)] is None
    assert board[Position(7, 5)] is None

    assert board[Position(0, 6)] is None
    assert board[Position(1, 6)] is None
    assert board[Position(2, 6)] == Piece(PieceType.BISHOP, Color.BLACK)
    assert board[Position(3, 6)] is None
    assert board[Position(4, 6)] is None
    assert board[Position(5, 6)] is None
    assert board[Position(6, 6)] is None
    assert board[Position(7, 6)] is None

    assert board[Position(0, 7)] is None
    assert board[Position(1, 7)] is None
    assert board[Position(2, 7)] is None
    assert board[Position(3, 7)] is None
    assert board[Position(4, 7)] == Piece(PieceType.KING, Color.BLACK)
    assert board[Position(5, 7)] is None
    assert board[Position(6, 7)] is None
    assert board[Position(7, 7)] is None


def test_board_should_be_represented_with_unicode():
    board = Board()

    board[Position(0, 1)] = Piece(PieceType.PAWN, Color.BLACK)
    board[Position(0, 6)] = Piece(PieceType.QUEEN, Color.WHITE)
    board[Position(1, 1)] = Piece(PieceType.ROOK, Color.BLACK)
    board[Position(1, 3)] = Piece(PieceType.BISHOP, Color.BLACK)
    board[Position(2, 1)] = Piece(PieceType.KING, Color.BLACK)
    board[Position(2, 2)] = Piece(PieceType.BISHOP, Color.WHITE)
    board[Position(2, 7)] = Piece(PieceType.KNIGHT, Color.WHITE)
    board[Position(3, 0)] = Piece(PieceType.PAWN, Color.WHITE)
    board[Position(4, 5)] = Piece(PieceType.ROOK, Color.WHITE)
    board[Position(5, 1)] = Piece(PieceType.QUEEN, Color.BLACK)
    board[Position(5, 6)] = Piece(PieceType.KNIGHT, Color.BLACK)
    board[Position(7, 1)] = Piece(PieceType.KING, Color.WHITE)

    assert str(board) == textwrap.dedent("""\
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
        ♟ ♜ ♚ ⋅ ⋅ ♛ ⋅ ♔
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ♝ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ♖ ⋅ ⋅ ⋅
        ♕ ⋅ ⋅ ⋅ ⋅ ♞ ⋅ ⋅
        ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅ ⋅
    """)


def test_board_should_check_for_equality():
    board1 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♚ ⋅ ⋅ ♛ ⋅ ♔
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♝ ⋅ ⋅
        ⋅ ⋅ ⋅ ♟ ⋅ ⋅ ⋅ ⋅
        ⋅ ♜ ⋅ ⋅ ♖ ⋅ ⋅ ⋅
        ♕ ⋅ ⋅ ⋅ ⋅ ♞ ⋅ ⋅
        ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅ ⋅
    """)

    board2 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♚ ⋅ ⋅ ♛ ⋅ ♔
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♝ ⋅ ⋅
        ⋅ ⋅ ⋅ ♟ ⋅ ⋅ ⋅ ⋅
        ⋅ ♜ ⋅ ⋅ ♖ ⋅ ⋅ ⋅
        ♕ ⋅ ⋅ ⋅ ⋅ ♞ ⋅ ⋅
        ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅ ⋅
    """)

    assert board1 == board2


def test_board_should_check_no_equality():
    board1 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♚ ⋅ ⋅ ♛ ⋅ ♔
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♝ ⋅ ⋅
        ⋅ ⋅ ⋅ ♟ ⋅ ⋅ ⋅ ⋅
        ⋅ ♜ ⋅ ⋅ ♖ ⋅ ⋅ ⋅
        ♕ ⋅ ⋅ ⋅ ⋅ ♞ ⋅ ⋅
        ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅ ⋅
    """)

    board2 = Board.from_unicode("""
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ♕ ⋅ ⋅ ⋅ ⋅ ♞ ⋅ ⋅
        ⋅ ⋅ ♚ ⋅ ⋅ ♛ ⋅ ♔
        ⋅ ⋅ ⋅ ♟ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♝ ⋅ ⋅
        ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ♜ ⋅ ⋅ ♖ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
    """)

    assert board1 != board2


def test_should_fail_to_move_in_place():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♔ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(2, 2), Position(2, 2))


def test_should_move_king():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ♔ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)

    result1 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♔ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(4, 4), Position(3, 4))
    assert board == result1

    result2 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♔ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(3, 4), Position(2, 3))
    assert board == result2


def test_should_not_move_king_incorrectly():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ♔ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(4, 4), Position(2, 4))


def test_should_move_rook():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♜ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)

    result1 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♜ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(5, 1), Position(5, 5))
    assert board == result1

    result2 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♜ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(5, 5), Position(3, 5))
    assert board == result2


def test_should_not_move_rook_incorrectly():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♜ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(5, 1), Position(3, 2))


def test_should_move_bishop():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)

    result1 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♗ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(2, 6), Position(5, 3))
    assert board == result1


def test_should_not_move_bishop_incorrectly():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(2, 6), Position(3, 4))


def test_should_move_knight():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ♘ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)

    result1 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(4, 4), Position(2, 3))
    assert board == result1

    result2 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(2, 3), Position(3, 1))
    assert board == result2


def test_should_not_move_knight_incorrectly():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(3, 1), Position(4, 2))


def test_should_move_queen():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♛ ⋅ ⋅
    """)

    result1 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♛ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(5, 7), Position(5, 3))
    assert board == result1

    result2 = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♛ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(5, 3), Position(3, 5))
    assert board == result2


def test_should_not_move_queen_incorrectly():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♛ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(5, 7), Position(4, 5))


def test_should_move_pawn():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    result = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(3, 5), Position(3, 4))
    assert board == result

    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♟ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    result = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♟ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    make_move(board, Position(5, 2), Position(5, 3))
    assert board == result


def test_should_not_move_pawn_incorrectly():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♟ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(5, 2), Position(4, 3))

    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♙ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(5, 4), Position(5, 5))


def test_should_fail_to_move_from_empty_departure():
    board = Board.from_unicode("""
        ⋅ ♛ ⋅ ⋅ ⋅ ⋅ ♖ ⋅
        ⋅ ⋅ ⋅ ♕ ⋅ ⋅ ⋅ ⋅
        ⋅ ♞ ⋅ ⋅ ⋅ ♙ ⋅ ⋅
        ⋅ ⋅ ♟ ⋅ ♗ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ♘ ⋅
        ⋅ ♜ ⋅ ⋅ ⋅ ♔ ⋅ ⋅
        ⋅ ⋅ ♝ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ♚ ⋅ ⋅ ⋅
    """)
    with pytest.raises(MoveException):
        make_move(board, Position(3, 0), Position(4, 1))


@pytest.mark.parametrize(("departure, obstacle, destination"), [
    (Position(2, 5), Position(2, 6), Position(2, 7)),
    (Position(3, 5), Position(3, 3), Position(3, 2)),
    (Position(1, 4), Position(3, 4), Position(5, 4)),
    (Position(7, 0), Position(3, 0), Position(0, 0)),
])
def test_should_move_rook_without_leaping_over_pieces(departure, obstacle, destination):
    board = Board()
    board[departure] = Piece(PieceType.ROOK, Color.BLACK)
    board[obstacle] = Piece(PieceType.PAWN, Color.BLACK)

    with pytest.raises(MoveException):
        make_move(board, departure, destination)


@pytest.mark.parametrize(("departure, obstacle, destination"), [
    (Position(3, 3), Position(4, 4), Position(5, 5)),
    (Position(2, 7), Position(4, 5), Position(5, 4)),
    (Position(6, 1), Position(4, 3), Position(2, 5)),
    (Position(7, 7), Position(3, 3), Position(0, 0)),
])
def test_should_move_bishop_without_leaping_over_pieces(departure, obstacle, destination):
    board = Board()
    board[departure] = Piece(PieceType.BISHOP, Color.BLACK)
    board[obstacle] = Piece(PieceType.PAWN, Color.BLACK)

    with pytest.raises(MoveException):
        make_move(board, departure, destination)


@pytest.mark.parametrize(("departure, obstacle, destination"), [
    (Position(2, 5), Position(2, 6), Position(2, 7)),
    (Position(3, 5), Position(3, 3), Position(3, 2)),
    (Position(1, 4), Position(3, 4), Position(5, 4)),
    (Position(7, 0), Position(3, 0), Position(0, 0)),
    (Position(3, 3), Position(4, 4), Position(5, 5)),
    (Position(2, 7), Position(4, 5), Position(5, 4)),
    (Position(6, 1), Position(4, 3), Position(2, 5)),
    (Position(7, 7), Position(3, 3), Position(0, 0)),
])
def test_should_move_queen_without_leaping_over_pieces(departure, obstacle, destination):
    board = Board()
    board[departure] = Piece(PieceType.QUEEN, Color.WHITE)
    board[obstacle] = Piece(PieceType.PAWN, Color.WHITE)

    with pytest.raises(MoveException):
        make_move(board, departure, destination)


def test_should_move_pawn_without_leaping_over_pieces():
    board = Board()
    board[Position(2, 6)] = Piece(PieceType.PAWN, Color.WHITE)
    board[Position(2, 5)] = Piece(PieceType.PAWN, Color.WHITE)

    with pytest.raises(MoveException):
        make_move(board, Position(2, 6), Position(2, 4))

    board = Board()
    board[Position(4, 1)] = Piece(PieceType.PAWN, Color.BLACK)
    board[Position(4, 2)] = Piece(PieceType.PAWN, Color.WHITE)

    with pytest.raises(MoveException):
        make_move(board, Position(4, 1), Position(4, 3))
