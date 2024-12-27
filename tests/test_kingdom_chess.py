import textwrap

import pytest

from kingdom_chess import (
    Board,
    Game,
    KingState,
    Color,
    Move,
    deduce_king_state,
    do_move,
    interpret_move,
    is_king_under_attack,
    MoveError,
    Piece,
    PieceType,
    Position,
    undo_move,
)


@pytest.mark.parametrize(("file", "rank"), [(-1, 4), (8, 4), (2, -1), (2, 8)])
def test_position_should_not_be_outside_board(file, rank):
    with pytest.raises(ValueError):
        _ = Position(file, rank)


@pytest.mark.parametrize(("coordinate", "file", "rank"), [
    ("a8", 0, 0), ("c2", 2, 6), ("h1", 7, 7)
])
def test_position_should_be_creatable_from_coordinate(coordinate, file, rank):
    assert Position.from_coordinate(coordinate) == Position(file, rank)


@pytest.mark.parametrize("coord", ["a83", "b", "i3", "b0"])
def test_position_should_not_be_created_from_invalid_coordinates(coord):
    with pytest.raises(ValueError) as exc_info:
        _ = Position.from_coordinate(coord)
    assert coord in exc_info.value.args


def test_board_should_place_a_piece():
    board = Board()
    board[Position(3, 6)] = Piece(PieceType.KNIGHT, Color.WHITE)
    assert board[Position(3, 6)] == Piece(PieceType.KNIGHT, Color.WHITE)


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


def test_board_should_be_empty_by_default():
    assert Board().to_mapping() == {}


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

    assert board.to_mapping() == {
        Position(1, 0): Piece(PieceType.QUEEN, Color.BLACK),
        Position(6, 0): Piece(PieceType.ROOK, Color.WHITE),
        Position(3, 1): Piece(PieceType.QUEEN, Color.WHITE),
        Position(1, 2): Piece(PieceType.KNIGHT, Color.BLACK),
        Position(5, 2): Piece(PieceType.PAWN, Color.WHITE),
        Position(2, 3): Piece(PieceType.PAWN, Color.BLACK),
        Position(4, 3): Piece(PieceType.BISHOP, Color.WHITE),
        Position(6, 4): Piece(PieceType.KNIGHT, Color.WHITE),
        Position(1, 5): Piece(PieceType.ROOK, Color.BLACK),
        Position(5, 5): Piece(PieceType.KING, Color.WHITE),
        Position(2, 6): Piece(PieceType.BISHOP, Color.BLACK),
        Position(4, 7): Piece(PieceType.KING, Color.BLACK),
    }


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

    assert board.to_unicode() == textwrap.dedent("""\
        ⋅ ⋅ ⋅ ♙ ⋅ ⋅ ⋅ ⋅
        ♟ ♜ ♚ ⋅ ⋅ ♛ ⋅ ♔
        ⋅ ⋅ ♗ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ♝ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ♖ ⋅ ⋅ ⋅
        ♕ ⋅ ⋅ ⋅ ⋅ ♞ ⋅ ⋅
        ⋅ ⋅ ♘ ⋅ ⋅ ⋅ ⋅ ⋅
    """)


def test_board_should_be_represented_with_unicode_with_showed_coordinates():
    board = Board()
    board[Position(1, 3)] = Piece(PieceType.BISHOP, Color.BLACK)
    board[Position(4, 5)] = Piece(PieceType.ROOK, Color.WHITE)
    assert board.to_unicode_with_coordinates() == textwrap.dedent("""\
          a b c d e f g h  
        8 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 8
        7 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 7
        6 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 6
        5 ⋅ ♝ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 5
        4 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 4
        3 ⋅ ⋅ ⋅ ⋅ ♖ ⋅ ⋅ ⋅ 3
        2 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 2
        1 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 1
          a b c d e f g h  
    """)  # noqa: W291


def test_board_should_be_represented_with_unicode_rotated():
    board = Board()
    board[Position(1, 3)] = Piece(PieceType.BISHOP, Color.BLACK)
    board[Position(4, 5)] = Piece(PieceType.ROOK, Color.WHITE)
    assert board.to_unicode_with_coordinates(rotated=True) == textwrap.dedent("""\
          h g f e d c b a  
        1 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 1
        2 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 2
        3 ⋅ ⋅ ⋅ ♖ ⋅ ⋅ ⋅ ⋅ 3
        4 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 4
        5 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ♝ ⋅ 5
        6 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 6
        7 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 7
        8 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ 8
          h g f e d c b a  
    """)  # noqa: W291


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


def test_board_should_be_initialy_filled():
    assert Board.initialy_filled() == Board.from_unicode("""
        ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
        ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
        ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
    """)


def test_should_not_allow_to_move_piece_in_place():
    board = Board()
    board[Position(2, 2)] = Piece(PieceType.KING, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(2, 2), Position(2, 2))
    assert result == "destination is the same as departure"


def test_should_detect_move_from_empty_departure():
    board = Board()

    result = interpret_move(board, Color.WHITE, Position(3, 0), Position(4, 1))
    assert result == "departure have no piece"


def test_should_not_allow_to_move_piece_of_wrong_color():
    board = Board()
    board[Position(3, 5)] = Piece(PieceType.KING, Color.WHITE)

    result = interpret_move(board, Color.BLACK, Position(3, 5), Position(3, 4))
    assert result == "can't move enemy piece"


def test_should_allow_to_move_king():
    board = Board()
    board[Position(4, 4)] = Piece(PieceType.KING, Color.WHITE)

    result1 = interpret_move(board, Color.WHITE, Position(4, 4), Position(3, 4))
    assert isinstance(result1, Move)

    result2 = interpret_move(board, Color.WHITE, Position(4, 4), Position(3, 3))
    assert isinstance(result2, Move)


def test_should_not_allow_to_move_king_incorrectly():
    board = Board()
    board[Position(4, 4)] = Piece(PieceType.KING, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(4, 4), Position(2, 4))
    assert result == "invalid king move"


def test_should_allow_to_move_rook():
    board = Board()
    board[Position(5, 1)] = Piece(PieceType.ROOK, Color.BLACK)

    result1 = interpret_move(board, Color.BLACK, Position(5, 1), Position(5, 5))
    assert isinstance(result1, Move)

    result2 = interpret_move(board, Color.BLACK, Position(5, 1), Position(3, 1))
    assert isinstance(result2, Move)


def test_should_not_allow_to_move_rook_incorrectly():
    board = Board()
    board[Position(5, 1)] = Piece(PieceType.ROOK, Color.BLACK)

    result = interpret_move(board, Color.BLACK, Position(5, 1), Position(3, 2))
    assert result == "invalid rook move"


def test_should_allow_to_move_bishop():
    board = Board()
    board[Position(2, 6)] = Piece(PieceType.BISHOP, Color.WHITE)

    result1 = interpret_move(board, Color.WHITE, Position(2, 6), Position(5, 3))
    assert isinstance(result1, Move)

    result2 = interpret_move(board, Color.WHITE, Position(2, 6), Position(3, 7))
    assert isinstance(result2, Move)


def test_should_not_allow_to_move_bishop_incorrectly():
    board = Board()
    board[Position(2, 6)] = Piece(PieceType.BISHOP, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(2, 6), Position(3, 4))
    assert result == "invalid bishop move"


def test_should_allow_to_move_knight():
    board = Board()
    board[Position(4, 4)] = Piece(PieceType.KNIGHT, Color.WHITE)

    result1 = interpret_move(board, Color.WHITE, Position(4, 4), Position(2, 3))
    assert isinstance(result1, Move)

    result2 = interpret_move(board, Color.WHITE, Position(4, 4), Position(5, 6))
    assert isinstance(result2, Move)


def test_should_not_allow_to_move_knight_incorrectly():
    board = Board()
    board[Position(3, 1)] = Piece(PieceType.KNIGHT, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(3, 1), Position(4, 2))
    assert result == "invalid knight move"


def test_should_allow_to_move_queen():
    board = Board()
    board[Position(5, 7)] = Piece(PieceType.QUEEN, Color.BLACK)

    result1 = interpret_move(board, Color.BLACK, Position(5, 7), Position(5, 3))
    assert isinstance(result1, Move)

    result2 = interpret_move(board, Color.BLACK, Position(5, 7), Position(2, 4))
    assert isinstance(result2, Move)


def test_should_not_allow_to_move_queen_incorrectly():
    board = Board()
    board[Position(5, 7)] = Piece(PieceType.QUEEN, Color.BLACK)

    result = interpret_move(board, Color.BLACK, Position(5, 7), Position(4, 5))
    assert result == "invalid queen move"


def test_should_allow_to_move_pawn():
    board = Board()
    board[Position(3, 5)] = Piece(PieceType.PAWN, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(3, 5), Position(3, 4))
    assert isinstance(result, Move)

    board = Board()
    board[Position(5, 2)] = Piece(PieceType.PAWN, Color.BLACK)
    result = interpret_move(board, Color.BLACK, Position(5, 2), Position(5, 3))
    assert isinstance(result, Move)


def test_should_not_allow_to_move_pawn_incorrectly():
    board = Board()
    board[Position(5, 4)] = Piece(PieceType.PAWN, Color.WHITE)
    result = interpret_move(board, Color.WHITE, Position(5, 4), Position(5, 5))
    assert result == "invalid pawn move"

    result = interpret_move(board, Color.WHITE, Position(5, 4), Position(5, 2))
    assert result == "invalid pawn move"

    board = Board()
    board[Position(5, 2)] = Piece(PieceType.PAWN, Color.BLACK)
    result = interpret_move(board, Color.BLACK, Position(5, 2), Position(4, 3))
    assert result == "pawn can move diagonally only when capturing"


def test_should_allow_pawn_to_make_long_move_on_first_move():
    board = Board()
    board[Position(7, 1)] = Piece(PieceType.PAWN, Color.BLACK)
    result = interpret_move(board, Color.BLACK, Position(7, 1), Position(7, 3))
    assert isinstance(result, Move)


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

    result = interpret_move(board, Color.BLACK, departure, destination)
    assert result == "rook can't leap over intervening pieces"


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

    result = interpret_move(board, Color.BLACK, departure, destination)
    assert result == "bishop can't leap over intervening pieces"


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

    result = interpret_move(board, Color.WHITE, departure, destination)
    assert result == "queen can't leap over intervening pieces"


def test_should_move_pawn_without_leaping_over_pieces():
    board = Board()
    board[Position(2, 6)] = Piece(PieceType.PAWN, Color.WHITE)
    board[Position(2, 5)] = Piece(PieceType.PAWN, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(2, 6), Position(2, 4))
    assert result == "pawn can't leap over intervening piece"

    board = Board()
    board[Position(4, 1)] = Piece(PieceType.PAWN, Color.BLACK)
    board[Position(4, 2)] = Piece(PieceType.PAWN, Color.WHITE)

    result = interpret_move(board, Color.BLACK, Position(4, 1), Position(4, 3))
    assert result == "pawn can't leap over intervening piece"


def test_should_apply_move_on_board():
    board = Board()
    board[Position(2, 4)] = Piece(PieceType.QUEEN, Color.BLACK)
    move = Move(Position(2, 4), Position(3, 3), Piece(PieceType.QUEEN, Color.BLACK))
    expected = Board.from_mapping({Position(3, 3): Piece(PieceType.QUEEN, Color.BLACK)})

    do_move(move, board)
    assert board == expected


def test_should_unapply_move_on_board():
    board = Board()
    board[Position(3, 3)] = Piece(PieceType.QUEEN, Color.BLACK)
    move = Move(Position(2, 4), Position(3, 3), Piece(PieceType.QUEEN, Color.BLACK))
    expected = {Position(2, 4): Piece(PieceType.QUEEN, Color.BLACK)}

    undo_move(move, board)
    assert board.to_mapping() == expected


def test_should_move_piece_capturing_enemy_piece():
    board = Board()
    board[Position(3, 6)] = Piece(PieceType.QUEEN, Color.WHITE)
    board[Position(3, 4)] = Piece(PieceType.PAWN, Color.BLACK)

    result = interpret_move(board, Color.WHITE, Position(3, 6), Position(3, 4))
    assert isinstance(result, Move)


def test_should_apply_move_with_capturing():
    board = Board()
    board[Position(3, 6)] = Piece(PieceType.QUEEN, Color.WHITE)
    board[Position(3, 4)] = Piece(PieceType.PAWN, Color.BLACK)
    move = Move(Position(3, 6), Position(3, 4), Piece(PieceType.QUEEN, Color.WHITE))
    expected = {Position(3, 4): Piece(PieceType.QUEEN, Color.WHITE)}

    do_move(move, board)
    assert board.to_mapping() == expected


def test_should_unapply_move_with_capturing():
    board = Board()
    board[Position(3, 4)] = Piece(PieceType.QUEEN, Color.WHITE)
    move = Move(
        Position(3, 6), Position(3, 4),
        Piece(PieceType.QUEEN, Color.WHITE), Piece(PieceType.PAWN, Color.BLACK),
    )
    expected = {
        Position(3, 6): Piece(PieceType.QUEEN, Color.WHITE),
        Position(3, 4): Piece(PieceType.PAWN, Color.BLACK),
    }

    undo_move(move, board)
    assert board.to_mapping() == expected


def test_should_not_allow_to_capture_allied_piece():
    board = Board()
    board[Position(3, 6)] = Piece(PieceType.KING, Color.WHITE)
    board[Position(3, 5)] = Piece(PieceType.PAWN, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(3, 6), Position(3, 5))
    assert result == "it's not alowed to capture allied piece"


def test_pawn_should_not_capture_on_forward_move():
    board = Board()
    board[Position(3, 5)] = Piece(PieceType.PAWN, Color.WHITE)
    board[Position(3, 4)] = Piece(PieceType.PAWN, Color.BLACK)

    result = interpret_move(board, Color.WHITE, Position(3, 5), Position(3, 4))
    assert result == "pawn can't capture on forward move"


def test_pawn_should_not_capture_on_long_forward_move():
    board = Board()
    board[Position(4, 1)] = Piece(PieceType.PAWN, Color.BLACK)
    board[Position(4, 3)] = Piece(PieceType.PAWN, Color.WHITE)

    result = interpret_move(board, Color.BLACK, Position(4, 1), Position(4, 3))
    assert result == "pawn can't capture on forward move"


def test_pawn_should_capture_on_diagonal_move():
    board = Board()
    board[Position(4, 1)] = Piece(PieceType.PAWN, Color.BLACK)
    board[Position(5, 2)] = Piece(PieceType.BISHOP, Color.WHITE)

    result = interpret_move(board, Color.BLACK, Position(4, 1), Position(5, 2))
    assert isinstance(result, Move)


def test_pawn_should_not_move_diagonaly():
    board = Board()
    board[Position(4, 1)] = Piece(PieceType.PAWN, Color.BLACK)

    result = interpret_move(board, Color.BLACK, Position(4, 1), Position(5, 2))
    assert result == "pawn can move diagonally only when capturing"


def test_should_promote_pawn():
    board = Board()
    board[Position(4, 6)] = Piece(PieceType.PAWN, Color.BLACK)

    result = interpret_move(
        board, Color.BLACK, Position(4, 6), Position(4, 7), promotion_to=PieceType.QUEEN
    )
    assert isinstance(result, Move)

    do_move(result, board)

    assert board.to_mapping() == {Position(4, 7): Piece(PieceType.QUEEN, Color.BLACK)}


def test_should_force_promotion():
    board = Board()
    board[Position(2, 1)] = Piece(PieceType.PAWN, Color.WHITE)

    result = interpret_move(board, Color.WHITE, Position(2, 1), Position(2, 0), promotion_to=None)
    assert result == "pawn has to be promoted to something"


def test_should_reject_invalid_promotion():
    board = Board()
    board[Position(2, 2)] = Piece(PieceType.PAWN, Color.WHITE)
    board[Position(3, 5)] = Piece(PieceType.BISHOP, Color.WHITE)

    result = interpret_move(
        board, Color.WHITE, Position(2, 2), Position(2, 1), promotion_to=PieceType.ROOK
    )
    assert result == "pawn can't be promoted here"
    result = interpret_move(
        board, Color.WHITE, Position(3, 5), Position(4, 6), promotion_to=PieceType.QUEEN
    )
    assert result == "only pawn can be promoted"


def test_should_detect_if_king_is_in_check():
    initial_state = {
        Position(2, 2): Piece(PieceType.KING, Color.BLACK),
        Position(3, 3): Piece(PieceType.PAWN, Color.BLACK),
        Position(2, 4): Piece(PieceType.QUEEN, Color.WHITE),
        Position(4, 7): Piece(PieceType.KING, Color.WHITE),
    }
    board = Board.from_mapping(initial_state)

    check_status = deduce_king_state(board, Color.BLACK)
    assert check_status == KingState.CHECK


def test_should_detect_checkmate_if_king_cant_move_to_safe_place():
    initial_state = {
        Position(0, 0): Piece(PieceType.KING, Color.BLACK),
        Position(0, 2): Piece(PieceType.KING, Color.WHITE),
        Position(1, 2): Piece(PieceType.ROOK, Color.WHITE),
        Position(2, 2): Piece(PieceType.QUEEN, Color.WHITE),
    }
    board = Board.from_mapping(initial_state)

    check_status = deduce_king_state(board, Color.BLACK)
    assert check_status == KingState.CHECKMATE


def test_should_reject_mate_if_ally_can_save_king():
    initial_state = {
        Position(0, 0): Piece(PieceType.KING, Color.BLACK),
        Position(4, 0): Piece(PieceType.BISHOP, Color.BLACK),
        Position(0, 2): Piece(PieceType.KING, Color.WHITE),
        Position(1, 2): Piece(PieceType.ROOK, Color.WHITE),
        Position(2, 2): Piece(PieceType.QUEEN, Color.WHITE),
    }
    board = Board.from_mapping(initial_state)

    check_status = deduce_king_state(board, Color.BLACK)
    assert check_status == KingState.CHECK


def test_should_answer_if_king_is_under_immediate_attack():
    board = Board.from_unicode("""
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ♜ ⋅
        ⋅ ⋅ ♚ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ♙ ⋅
        ⋅ ♟ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ♗ ♔ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
        ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅
    """)
    assert is_king_under_attack(board, Color.BLACK)
    assert not is_king_under_attack(board, Color.WHITE)


class TestGame:
    def test_should_keep_state_of_the_game(self):
        initial_state = {
            Position(2, 5): Piece(PieceType.KING, Color.WHITE),
            Position(1, 2): Piece(PieceType.KING, Color.BLACK),
        }

        game = Game(Board.from_mapping(initial_state), Color.BLACK)

        assert game.board.to_mapping() == initial_state
        assert game.moving_color == Color.BLACK
        assert game.enemy_color == Color.WHITE
        assert game.enemy_king_state == KingState.SAFE

    def test_should_be_created_with_fresh_initial_state(self):
        game = Game.fresh()

        assert game.board == Board.initialy_filled()
        assert game.moving_color == Color.WHITE
        assert game.enemy_color == Color.BLACK
        assert game.enemy_king_state == KingState.SAFE

    def test_should_deduce_king_state_on_initialization(self):
        board = Board.from_mapping({
            Position(2, 2): Piece(PieceType.KING, Color.BLACK),
            Position(3, 3): Piece(PieceType.PAWN, Color.BLACK),
            Position(2, 4): Piece(PieceType.QUEEN, Color.WHITE),
            Position(4, 7): Piece(PieceType.KING, Color.WHITE),
        })

        game = Game(board, Color.WHITE)

        assert game.enemy_king_state == KingState.CHECK

    def test_should_make_move_with_given_coordinates(self):
        initial_board = Board.from_mapping({
            Position(2, 5): Piece(PieceType.KING, Color.WHITE),
            Position(1, 2): Piece(PieceType.KING, Color.BLACK),
        })
        game = Game(initial_board, Color.BLACK)

        result = game.make_move(Position(1, 2), Position(1, 1), None)

        assert isinstance(result, Move)
        assert game.board.to_mapping() == {
            Position(2, 5): Piece(PieceType.KING, Color.WHITE),
            Position(1, 1): Piece(PieceType.KING, Color.BLACK),
        }
        assert game.moving_color == Color.WHITE
        assert game.enemy_color == Color.BLACK
        assert game.enemy_king_state == KingState.SAFE

    def test_should_not_allow_to_place_king_under_immediate_attack(self):
        initial_state = {
            Position(5, 4): Piece(PieceType.KING, Color.WHITE),
            Position(3, 5): Piece(PieceType.KING, Color.BLACK),
        }
        game = Game(Board.from_mapping(initial_state), Color.WHITE)

        result = game.make_move(Position(5, 4), Position(4, 4), None)

        assert result == "move leaves king under immediate attack"
        assert game.board.to_mapping() == initial_state

    def test_should_not_allow_to_leave_king_under_immediate_attack(self):
        initial_state = {
            Position(2, 2): Piece(PieceType.KING, Color.BLACK),
            Position(3, 3): Piece(PieceType.PAWN, Color.BLACK),
            Position(2, 4): Piece(PieceType.PAWN, Color.WHITE),
            Position(4, 4): Piece(PieceType.BISHOP, Color.WHITE),
        }
        game = Game(Board.from_mapping(initial_state), Color.BLACK)

        result = game.make_move(Position(3, 3), Position(2, 4), None)
        assert result == "move leaves king under immediate attack"
        assert game.board.to_mapping() == initial_state
