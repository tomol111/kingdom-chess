from __future__ import annotations

import enum
import dataclasses
from typing import Final, Literal
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


PromotionTarget = Literal[PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]


class Color(enum.Enum):
    WHITE = "white"
    BLACK = "black"

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

    def to_unicode_with_coordinates(self, rotated: bool = False) -> str:
        """Create unicode image of the board state with showed coordinates on the edges."""
        rows = [[" ", *FILES, " "], *(
            [rank, *(piece_to_unicode[element] for element in row), rank]
            for rank, row in zip(RANKS, self._grid)
        ), [" ", *FILES, " "]]
        if rotated:
            for row in rows:
                row.reverse()
            rows.reverse()
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


# play
# ====


def play() -> None:
    """Provisional, untested game loop."""
    board = Board.initialy_filled()
    moving_color, enemy_color = Color.WHITE, Color.BLACK
    print(board.to_unicode_with_coordinates())
    while True:
        try:
            player_input = input(f"[{moving_color.value}] ")
        except EOFError:
            print()
            break
        try:
            departure = Position.from_coordinates(player_input[:2])
            destination = Position.from_coordinates(player_input[2:4])
            promotion_to: PromotionTarget | None
            match player_input[4:].lower():
                case "/q": promotion_to = PieceType.QUEEN
                case "/r": promotion_to = PieceType.ROOK
                case "/b": promotion_to = PieceType.BISHOP
                case "/n": promotion_to = PieceType.KNIGHT
                case _: promotion_to = None
        except ValueError:
            print("invalid coordinates")
            continue

        move = interpret_move(board, moving_color, departure, destination, promotion_to)

        if isinstance(move, str):
            print(move)
            continue

        do_move(move, board)

        if is_king_under_attack(board, move.moving_piece.color):
            undo_move(move, board)
            print("move leaves king under immediate attack")
            continue

        king_state = deduce_king_state(board, enemy_color)
        if king_state is KingState.CHECK:
            print("check")
        if king_state is KingState.CHECKMATE:
            print(f"CHECKMATE: {moving_color.value} won!")
            print(board.to_unicode_with_coordinates(rotated=moving_color is Color.BLACK))
            break

        moving_color, enemy_color = enemy_color, moving_color

        print()
        print(board.to_unicode_with_coordinates(rotated=moving_color is Color.BLACK))


# Move
# ====


class KingState(enum.Enum):
    SAFE = enum.auto()
    CHECK = enum.auto()
    CHECKMATE = enum.auto()


@dataclasses.dataclass(frozen=True)
class Move:
    """Should represents player's *valid* and potentialy *safe* move on the board.

    *Valid* means it follows the rules of pieces' moves.
    *Safe* means it is *valid* and follows the rules of king protection.
    """
    departure: Position
    destination: Position
    moving_piece: Piece
    captured_piece: Piece | None = None
    promotion_to: Piece | None = None


def do_move(move: Move, board: Board) -> None:
    """Apply move on the board."""
    board[move.departure] = None
    board[move.destination] = move.promotion_to or move.moving_piece


def undo_move(move: Move, board: Board) -> None:
    """Reverse move on the board."""
    board[move.destination] = move.captured_piece
    board[move.departure] = move.moving_piece


class MoveException(Exception):
    pass


def interpret_move(
    board: Board,
    moving_color: Color,
    departure: Position,
    destination: Position,
    promotion_to: PromotionTarget | None = None
) -> Move | str:
    """Create `Move` or `str` containing message which describes what is wrong with given move."""

    if departure == destination:
        return "destination is the same as departure"

    if not (moving_piece := board[departure]):
        return "departure have no piece"

    if moving_piece.color is not moving_color:
        return "can't move enemy piece"

    captured_piece = board[destination]
    dx, dy = destination.x - departure.x, destination.y - departure.y

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
            forward = (1 if moving_color is Color.BLACK else -1)
            if abs(dx) == 1 and dy == forward:  # diagonal move
                if not captured_piece:
                    return "pawn can move diagonally only when capturing"
            elif dx == 0:  # vertical move
                first_move = departure.y == (1 if moving_color is Color.BLACK else 6)
                double_move = first_move and dy == 2*forward
                if dy != forward and not double_move:
                    return "invalid pawn move"
                if double_move and not is_path_clear(board, departure, destination):
                    return "pawn can't leap over intervening piece"
                if captured_piece:
                    return "pawn can't capture on forward move"
            else:
                return "invalid pawn move"
            if destination.y == (7 if moving_color is Color.BLACK else 0):
                if not promotion_to:
                    return "pawn has to be promoted to something"
                return Move(
                    departure,
                    destination,
                    moving_piece,
                    captured_piece,
                    Piece(promotion_to, moving_color),
                )
            if promotion_to:
                return "pawn can't be promoted here"

    if captured_piece and captured_piece.color == moving_color:
        return "it's not alowed to capture allied piece"

    if promotion_to:
        return "only pawn can be promoted"

    return Move(departure, destination, moving_piece, captured_piece)


def deduce_king_state(board: Board, next_moving_color: Color) -> KingState:
    if not is_king_under_attack(board, next_moving_color):
        return KingState.SAFE

    pieces_positions = [
        pos for pos, piece in board.to_mapping().items()
        if piece.color is next_moving_color
    ]
    all_positions = [Position(x, y) for x in range(BOARD_SIDE_LEN) for y in range(BOARD_SIDE_LEN)]
    all_potential_moves = (
        potential_move
        for pos in pieces_positions
        for new_pos in all_positions
        if isinstance(
            potential_move := interpret_move(board, next_moving_color, pos, new_pos),
            Move,
        )
    )

    for potential_move in all_potential_moves:
        do_move(potential_move, board)
        if not is_king_under_attack(board, next_moving_color):
            undo_move(potential_move, board)
            return KingState.CHECK
        undo_move(potential_move, board)

    return KingState.CHECKMATE


def is_position_safe(board: Board, position: Position, enemy_color: Color) -> bool:
    """Check if given position is free of immediate attack.

    Given position can be occupied or not.
    """
    return not any(
        piece.color is enemy_color and isinstance(
            interpret_move(board, enemy_color, attacking_position, position),
            Move,
        )
        for attacking_position, piece in board.to_mapping().items()
    )


def is_king_under_attack(board: Board, color: Color) -> bool:
    """Search if king of given color is under immediate attack.

    If king has not been found return `False`.
    """
    for pos, piece in board.to_mapping().items():
        if piece.typ is PieceType.KING and piece.color is color:
            return not is_position_safe(board, pos, color.reversed)
    return False


def is_path_clear(board: Board, departure: Position, destination: Position) -> bool:
    """Checks if path between positions have intervening peace(s)."""
    dx, dy = departure.direction_to(destination)
    intermediate = departure.shift(dx, dy)
    while intermediate != destination:
        if board[intermediate] is not None:
            return False
        intermediate = intermediate.shift(dx, dy)
    return True
