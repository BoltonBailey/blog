"""
Chess Position Counting Script

Counts the number of "legal" chess positions based on three restrictions:
1. Exactly one white king and one black king on the board
2. Castling rights only valid if corresponding king and rook occupy starting squares
3. En passant only valid if there's a pawn in front of the capture square

Board piece options (excluding kings which are placed separately):
- Empty
- White: Pawn, Knight, Bishop, Rook, Queen (5 pieces)
- Black: Pawn, Knight, Bishop, Rook, Queen (5 pieces)
Total: 11 options per non-king square
"""

# Key insight for counting:
# - 64 squares total, 2 occupied by kings, leaving 62 squares
# - Each non-king square can hold 11 things (empty, or one of 10 non-king pieces)
# - Castling rights constrain rook squares only when the right is available
# - En passant constrains a pawn square when EP is active


# Square indices (0-63, a1=0, b1=1, ..., h1=7, a2=8, ..., h8=63)
def sq(file, rank):
    """Convert file (0-7 = a-h) and rank (0-7 = 1-8) to square index."""
    return rank * 8 + file


E1 = sq(4, 0)  # e1 = 4  (White king start)
E8 = sq(4, 7)  # e8 = 60 (Black king start)
A1 = sq(0, 0)  # a1 = 0  (White queenside rook)
H1 = sq(7, 0)  # h1 = 7  (White kingside rook)
A8 = sq(0, 7)  # a8 = 56 (Black queenside rook)
H8 = sq(7, 7)  # h8 = 63 (Black kingside rook)

# En passant pawn squares (where the capturing pawn would land, the captured pawn is one rank behind)
# EP on rank 3 (0-indexed) means white pawn on rank 4 (index 3) e.g. EP square e3, pawn on e4
# EP on rank 6 (0-indexed) means black pawn on rank 5 (index 4) e.g. EP square e6, pawn on e5
EP_PAWN_SQUARES = [sq(f, 3) for f in range(8)] + [
    sq(f, 4) for f in range(8)
]  # 16 total


def count_positions_for_params(
    castling_rights: tuple[bool, bool, bool, bool], ep_square: int | None
) -> int:
    """
    Count positions for a specific castling rights configuration and en passant square.

    Args:
        castling_rights: (white_queenside, white_kingside, black_queenside, black_kingside)
        ep_square: The pawn square index for en passant (0-63), or None if no en passant

    Returns:
        Number of valid board positions (before multiplying by turn and half-move clock)
    """
    # Squares on ranks 1 and 8 can't have pawns: 9 options (empty + 4 white + 4 black non-pawn non-king)
    # Squares on ranks 2-7 have 11 options (empty + 5 white + 5 black non-king pieces)
    PIECES_NO_PAWN = 9  # For ranks 1 and 8
    PIECES_WITH_PAWN = 11  # For ranks 2-7

    w_qside, w_kside, b_qside, b_kside = castling_rights

    # Squares on rank 1 (indices 0-7) and rank 8 (indices 56-63)
    RANK_1 = set(range(0, 8))
    RANK_8 = set(range(56, 64))
    RANKS_1_AND_8 = RANK_1 | RANK_8  # 16 squares total

    # Rook squares (all on ranks 1 and 8)
    rook_constrained_squares = set()
    if w_qside:
        rook_constrained_squares.add(A1)
    if w_kside:
        rook_constrained_squares.add(H1)
    if b_qside:
        rook_constrained_squares.add(A8)
    if b_kside:
        rook_constrained_squares.add(H8)

    total = 0

    # Enumerate all 64 * 63 king placements
    for wk in range(64):
        for bk in range(64):
            if wk == bk:
                continue  # Kings can't be on same square

            # Check castling validity: king must be on start square for castling rights
            if (w_qside or w_kside) and wk != E1:
                continue  # White has castling rights but king not on e1
            if (b_qside or b_kside) and bk != E8:
                continue  # Black has castling rights but king not on e8

            # Check en passant validity: pawn square can't be occupied by a king
            if ep_square is not None and (ep_square == wk or ep_square == bk):
                continue

            # Count free squares by rank type
            # Ranks 1 and 8: 16 squares, minus kings on those ranks, minus rook constraints
            # Ranks 2-7: 48 squares, minus kings on those ranks, minus EP constraint

            kings_on_ranks_1_8 = (wk in RANKS_1_AND_8) + (bk in RANKS_1_AND_8)
            kings_on_ranks_2_7 = 2 - kings_on_ranks_1_8

            # Free squares on ranks 1 and 8 (9 options each)
            free_no_pawn = 16 - kings_on_ranks_1_8 - len(rook_constrained_squares)

            # Free squares on ranks 2-7 (11 options each)
            free_with_pawn = 48 - kings_on_ranks_2_7
            if ep_square is not None:
                free_with_pawn -= 1  # EP square is on rank 4 or 5, always in ranks 2-7

            total += (PIECES_NO_PAWN**free_no_pawn) * (PIECES_WITH_PAWN**free_with_pawn)

    return total


def count_positions() -> int:
    """
    Count total valid positions by summing over all 16 * 17 combinations
    of castling rights and en passant squares.
    """
    total = 0

    # Iterate over all 16 castling configurations
    for w_qside in [False, True]:
        for w_kside in [False, True]:
            for b_qside in [False, True]:
                for b_kside in [False, True]:
                    castling = (w_qside, w_kside, b_qside, b_kside)

                    # No en passant
                    total += count_positions_for_params(castling, None)

                    # En passant on each of 16 pawn squares
                    for ep_sq in EP_PAWN_SQUARES:
                        total += count_positions_for_params(castling, ep_sq)

    # Multiply by turn (2) and half-move clock (100)
    total *= 2 * 100

    return total


if __name__ == "__main__":
    print("Calculating chess positions with constraints:")
    print("1. Exactly one white king and one black king")
    print("2. Castling rights require king and rook on starting squares")
    print("3. En passant requires pawn in front of capture square")
    print("4. No pawns on ranks 1 or 8")
    print()

    result = count_positions()
    print(f"Total number of positions: {result}")
    print(f"Scientific notation: {result:.6e}")

    # Compare with reference values
    print()
    print("Comparison with bounds:")

    naive_bound = (13**64) * 2 * (2**4) * 17 * 100
    print(f"  Naive upper bound (13^64 * 2 * 2^4 * 17 * 100): {naive_bound:.6e}")

    kings_only = 64 * 63 * (11**62) * 2 * (2**4) * 17 * 100
    print(
        f"  Kings-only constraint (64 * 63 * 11^62 * 2 * 16 * 17 * 100): {kings_only:.6e}"
    )

    print()
    print(f"Ratio (our count / naive): {result / naive_bound:.6e}")
    print(f"Ratio (our count / kings-only): {result / kings_only:.6e}")
