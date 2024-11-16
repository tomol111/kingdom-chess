from __future__ import annotations

import enum
import dataclasses
from typing import Final
from collections.abc import Mapping


# Layout
# ======


BOARD_SIDE_LEN: Final = 8


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __post_init__(self) -> None:
        x_invalid = not 0 <= self.x < BOARD_SIDE_LEN
        y_invalid = not 0 <= self.y < BOARD_SIDE_LEN
        if x_invalid and y_invalid:
            raise ValueError(f"invalid values of {self!r}")
        if x_invalid:
            raise ValueError(f"invalid x value of {self!r}")
        if y_invalid:
            raise ValueError(f"invalid y value of {self!r}")

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


# Board
# =====


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
        board = Board()

        border_pieces_types = [
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK,
        ]

        for i, typ in enumerate(border_pieces_types):
            board._grid[0][i] = Piece(typ, Color.BLACK)

        for i in range(BOARD_SIDE_LEN):
            board._grid[1][i] = Piece(PieceType.PAWN, Color.BLACK)

        for i in range(BOARD_SIDE_LEN):
            board._grid[6][i] = Piece(PieceType.PAWN, Color.WHITE)

        for i, typ in enumerate(border_pieces_types):
            board._grid[7][i] = Piece(typ, Color.WHITE)

        return board

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

    def __str__(self) -> str:
        return "\n".join(
            " ".join(piece_to_unicode[self._grid[y][x]] for x in range(BOARD_SIDE_LEN))
            for y in range(BOARD_SIDE_LEN)
        ) + "\n"

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
    if departure == destination:
        raise MoveException("destination is the same as departure")

    if not (moving_piece := board[departure]):
        raise MoveException("departure have no piece")

    captured_piece = board[destination]
    dx, dy = destination.offset_from(departure)

    match moving_piece.typ:
        case PieceType.KING:
            if abs(dx) > 1 or abs(dy) > 1:
                raise MoveException("invalid king move")
        case PieceType.ROOK:
            if dx != 0 and dy != 0:
                raise MoveException("invalid rook move")
            if not is_path_clear(board, departure, destination):
                raise MoveException("rook can't leap over intervening pieces")
        case PieceType.BISHOP:
            if abs(dx) != abs(dy):
                raise MoveException("invalid bishop move")
            if not is_path_clear(board, departure, destination):
                raise MoveException("bichop can't leap over intervening pieces")
        case PieceType.KNIGHT:
            if (abs(dx), abs(dy)) not in [(1, 2), (2, 1)]:
                raise MoveException("invalid knight move")
        case PieceType.QUEEN:
            if abs(dx) != abs(dy) and dx != 0 and dy != 0:
                raise MoveException("invalid queen move")
            if not is_path_clear(board, departure, destination):
                raise MoveException("queen can't leap over intervening pieces")
        case PieceType.PAWN:
            forward = (1 if moving_piece.color is Color.BLACK else -1)
            if abs(dx) == 1 and dy == forward:  # diagonal move
                if not captured_piece:
                    raise MoveException("pawn can move diagonally only when capturing")
            elif dx == 0:  # vertical move
                first_move = departure.y == (1 if moving_piece.color is Color.BLACK else 6)
                double_move = first_move and dy == 2*forward
                if dy != forward and not double_move:
                    raise MoveException("invalid pawn move")
                if double_move and not is_path_clear(board, departure, destination):
                    raise MoveException("pawn can't leap over intervening piece")
                if captured_piece:
                    raise MoveException("pawn can't capture on forward move")
            else:
                raise MoveException("invalid pawn move")

    if captured_piece and captured_piece.color == moving_piece.color:
        raise MoveException("it's not alowed to capture allied piece")

    board[departure] = None
    board[destination] = moving_piece


def is_path_clear(board: Board, departure: Position, destination: Position) -> bool:
    """Checks if path between positions have intervening peace(s)."""
    dx, dy = departure.direction_to(destination)
    intermediate = departure.shift(dx, dy)
    while intermediate != destination:
        if board[intermediate] is not None:
            return False
        intermediate = intermediate.shift(dx, dy)
    return True
