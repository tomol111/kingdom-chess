from __future__ import annotations

import enum
import dataclasses
from typing import Final
from collections.abc import Mapping


# Layout
# ======


BOARD_SIDE_LEN: Final = 8

FILES = "abcdefgh"
RANKS = "87654321"


@dataclasses.dataclass(frozen=True)
class Position:
    """Valid position on the board."""

    x: int
    y: int

    def __post_init__(self) -> None:
        if (not 0 <= self.x < BOARD_SIDE_LEN or not 0 <= self.y < BOARD_SIDE_LEN):
            raise ValueError(self.x, self.y)

    @classmethod
    def from_coordinates(cls, coords: str) -> Position:
        """Create `Position` from "{file}{rank}" labels."""
        if len(coords) != 2:
            raise ValueError(coords)
        file = FILES.find(coords[0])
        rank = RANKS.find(coords[1])
        if file == -1 or rank == -1:
            raise ValueError(coords)
        return Position(file, rank)

    def offset_from(self, other: Position) -> tuple[int, int]:
        return (self.x - other.x, self.y - other.y)

    def direction_to(self, destination: Position) -> tuple[int, int]:
        """Returns direction of move, if move is horizontal, vertical or diagonal."""
        assert (
            (dx := destination.x - self.x) != 0
            or (dy := destination.y - self.y) != 0
            or abs(dx) == abs(dy)
        )

        return _compare(self.x, destination.x), _compare(self.y, destination.y)

    def shift(self, dx: int, dy: int) -> Position:
        return Position(self.x + dx, self.y + dy)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def _compare(x: int, y: int) -> int:
    if x == y:
        return 0
    if x < y:
        return 1
    return -1


# Pieces
# ======


@dataclasses.dataclass(frozen=True)
class Piece:
    typ: PieceType
    color: Color


class PieceType(enum.Enum):
    KING = enum.auto()
    QUEEN = enum.auto()
    ROOK = enum.auto()
    BISHOP = enum.auto()
    KNIGHT = enum.auto()
    PAWN = enum.auto()


class Color(enum.Enum):
    WHITE = enum.auto()
    BLACK = enum.auto()

    @property
    def reversed(self) -> Color:
        return Color.BLACK if self is Color.WHITE else Color.WHITE


# Board
# =====

STARTING_BOARD_STATE: Final[Mapping[Position, Piece]] = {
    Position(0, 0): Piece(PieceType.ROOK, Color.BLACK),
    Position(1, 0): Piece(PieceType.KNIGHT, Color.BLACK),
    Position(2, 0): Piece(PieceType.BISHOP, Color.BLACK),
    Position(3, 0): Piece(PieceType.QUEEN, Color.BLACK),
    Position(4, 0): Piece(PieceType.KING, Color.BLACK),
    Position(5, 0): Piece(PieceType.BISHOP, Color.BLACK),
    Position(6, 0): Piece(PieceType.KNIGHT, Color.BLACK),
    Position(7, 0): Piece(PieceType.ROOK, Color.BLACK),

    Position(0, 1): Piece(PieceType.PAWN, Color.BLACK),
    Position(1, 1): Piece(PieceType.PAWN, Color.BLACK),
    Position(2, 1): Piece(PieceType.PAWN, Color.BLACK),
    Position(3, 1): Piece(PieceType.PAWN, Color.BLACK),
    Position(4, 1): Piece(PieceType.PAWN, Color.BLACK),
    Position(5, 1): Piece(PieceType.PAWN, Color.BLACK),
    Position(6, 1): Piece(PieceType.PAWN, Color.BLACK),
    Position(7, 1): Piece(PieceType.PAWN, Color.BLACK),

    Position(0, 6): Piece(PieceType.PAWN, Color.WHITE),
    Position(1, 6): Piece(PieceType.PAWN, Color.WHITE),
    Position(2, 6): Piece(PieceType.PAWN, Color.WHITE),
    Position(3, 6): Piece(PieceType.PAWN, Color.WHITE),
    Position(4, 6): Piece(PieceType.PAWN, Color.WHITE),
    Position(5, 6): Piece(PieceType.PAWN, Color.WHITE),
    Position(6, 6): Piece(PieceType.PAWN, Color.WHITE),
    Position(7, 6): Piece(PieceType.PAWN, Color.WHITE),

    Position(0, 7): Piece(PieceType.ROOK, Color.WHITE),
    Position(1, 7): Piece(PieceType.KNIGHT, Color.WHITE),
    Position(2, 7): Piece(PieceType.BISHOP, Color.WHITE),
    Position(3, 7): Piece(PieceType.QUEEN, Color.WHITE),
    Position(4, 7): Piece(PieceType.KING, Color.WHITE),
    Position(5, 7): Piece(PieceType.BISHOP, Color.WHITE),
    Position(6, 7): Piece(PieceType.KNIGHT, Color.WHITE),
    Position(7, 7): Piece(PieceType.ROOK, Color.WHITE),
}


class Board:
    """
    Chessboard

    Layout:

        x = 0..7         file = a..h
        y = 0..7         rank = 1..8

                  x
          .------->      rank ^
          |   B               |   B
          |                   |
          |Q     K            |Q     K
          |                   |
          |   W               |   W
        y v                   .------->
                                   file
    """

    def __init__(self) -> None:
        # grid[y/rank][x/file]
        self._grid: list[list[Piece | None]] = [
            [None] * BOARD_SIDE_LEN for _ in range(BOARD_SIDE_LEN)
        ]

    def __getitem__(self, pos: Position) -> Piece | None:
        return self._grid[pos.y][pos.x]

    def __setitem__(self, pos: Position, piece: Piece | None) -> None:
        self._grid[pos.y][pos.x] = piece

    @classmethod
    def initialy_filled(cls) -> Board:
        return Board.from_mapping(STARTING_BOARD_STATE)

    def to_mapping(self) -> dict[Position, Piece]:
        return {
            Position(x, y): piece
            for y, file in enumerate(self._grid)
            for x, piece in enumerate(file)
            if piece
        }

    @classmethod
    def from_mapping(cls, mapping: Mapping[Position, Piece]) -> Board:
        board = Board()
        for pos, piece in mapping.items():
            board[pos] = piece
        return board

    @classmethod
    def from_unicode(cls, unicode: str) -> Board:
        board = Board()
        unicode = "".join(unicode.split())

        positions = [
            Position(x, y)
            for y in range(BOARD_SIDE_LEN)
            for x in range(BOARD_SIDE_LEN)
        ]
        for pos, char in zip(positions, unicode, strict=True):
            board[pos] = unicode_to_piece[char]

        return board

    def to_unicode(self) -> str:
        """Create unicode image of the board state ."""
        return "\n".join(
            " ".join(piece_to_unicode[element] for element in row)
            for row in self._grid
        ) + "\n"

    def to_unicode_with_coordinates(self) -> str:
        """Create unicode image of the board state with showed coordinates on the edges."""
        rows = [[" ", *FILES], *(
            [rank, *(piece_to_unicode[element] for element in row), rank]
            for rank, row in zip(RANKS, self._grid)
        ), [" ", *FILES]]
        return "\n".join(" ".join(row) for row in rows) + "\n"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return all(
            self._grid[y][x] == other._grid[y][x]
            for x in range(BOARD_SIDE_LEN)
            for y in range(BOARD_SIDE_LEN)
        )


unicode_to_piece: Final[Mapping[str, Piece | None]] = {
    "⋅": None,
    "♔": Piece(PieceType.KING, Color.WHITE),
    "♕": Piece(PieceType.QUEEN, Color.WHITE),
    "♖": Piece(PieceType.ROOK, Color.WHITE),
    "♗": Piece(PieceType.BISHOP, Color.WHITE),
    "♘": Piece(PieceType.KNIGHT, Color.WHITE),
    "♙": Piece(PieceType.PAWN, Color.WHITE),
    "♚": Piece(PieceType.KING, Color.BLACK),
    "♛": Piece(PieceType.QUEEN, Color.BLACK),
    "♜": Piece(PieceType.ROOK, Color.BLACK),
    "♝": Piece(PieceType.BISHOP, Color.BLACK),
    "♞": Piece(PieceType.KNIGHT, Color.BLACK),
    "♟": Piece(PieceType.PAWN, Color.BLACK),
}

piece_to_unicode: Final[Mapping[Piece | None, str]] = {
    piece: unicode for unicode, piece in unicode_to_piece.items()
}


# Move
# ====


class MoveException(Exception):
    pass


def make_move(board: Board, departure: Position, destination: Position) -> None:
    """Move piece from departure to destination after checking if it is valid."""

    if err_msg := validate_move(board, departure, destination):
        raise MoveException(err_msg)

    moving_piece = board[departure]
    assert moving_piece
    if moving_piece.typ == PieceType.KING and not is_position_safe(
        board, destination, enemy_color=moving_piece.color.reversed
    ):
        raise MoveException("move leaves king under immediate attack")

    board[departure] = None
    board[destination] = moving_piece


def validate_move(board: Board, departure: Position, destination: Position) -> str | None:
    """Returns `None` if move is valid or `str` message describing what is wrong with given move.

    It does not validate if king will be placed under immediate attack.
    """
    if departure == destination:
        return "destination is the same as departure"

    if not (moving_piece := board[departure]):
        return "departure have no piece"

    captured_piece = board[destination]
    dx, dy = destination.offset_from(departure)

    match moving_piece.typ:
        case PieceType.KING:
            if abs(dx) > 1 or abs(dy) > 1:
                return "invalid king move"
        case PieceType.ROOK:
            if dx != 0 and dy != 0:
                return "invalid rook move"
            if not is_path_clear(board, departure, destination):
                return "rook can't leap over intervening pieces"
        case PieceType.BISHOP:
            if abs(dx) != abs(dy):
                return "invalid bishop move"
            if not is_path_clear(board, departure, destination):
                return "bishop can't leap over intervening pieces"
        case PieceType.KNIGHT:
            if (abs(dx), abs(dy)) not in [(1, 2), (2, 1)]:
                return "invalid knight move"
        case PieceType.QUEEN:
            if abs(dx) != abs(dy) and dx != 0 and dy != 0:
                return "invalid queen move"
            if not is_path_clear(board, departure, destination):
                return "queen can't leap over intervening pieces"
        case PieceType.PAWN:
            forward = (1 if moving_piece.color is Color.BLACK else -1)
            if abs(dx) == 1 and dy == forward:  # diagonal move
                if not captured_piece:
                    return "pawn can move diagonally only when capturing"
            elif dx == 0:  # vertical move
                first_move = departure.y == (1 if moving_piece.color is Color.BLACK else 6)
                double_move = first_move and dy == 2*forward
                if dy != forward and not double_move:
                    return "invalid pawn move"
                if double_move and not is_path_clear(board, departure, destination):
                    return "pawn can't leap over intervening piece"
                if captured_piece:
                    return "pawn can't capture on forward move"
            else:
                return "invalid pawn move"

    if captured_piece and captured_piece.color == moving_piece.color:
        return "it's not alowed to capture allied piece"

    return None


def is_move_valid(board: Board, departure: Position, destination: Position) -> bool:
    """Similar to `validate_move()` but returns `bool` instead."""
    return validate_move(board, departure, destination) is None


def is_position_safe(board: Board, position: Position, enemy_color: Color) -> bool:
    """Check if given position is free of immediate attack."""
    return not any(
        piece.color is enemy_color and is_move_valid(board, attacking_position, position)
        for attacking_position, piece in board.to_mapping().items()
    )


def is_path_clear(board: Board, departure: Position, destination: Position) -> bool:
    """Checks if path between positions have intervening peace(s)."""
    dx, dy = departure.direction_to(destination)
    intermediate = departure.shift(dx, dy)
    while intermediate != destination:
        if board[intermediate] is not None:
            return False
        intermediate = intermediate.shift(dx, dy)
    return True
