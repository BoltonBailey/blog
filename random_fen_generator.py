#!/usr/bin/env python3
"""
Generate a random FEN string by starting from the initial position
and making 15 random moves.
"""

import chess
import random


def generate_random_fen(num_moves: int = 15) -> str:
    """
    Generate a random FEN by making random legal moves from the starting position.

    Args:
        num_moves: Number of random moves to make (default 15)

    Returns:
        FEN string of the resulting position
    """
    board = chess.Board()

    for _ in range(num_moves):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            # Game is over (checkmate or stalemate)
            break
        move = random.choice(legal_moves)
        board.push(move)

    return board.fen()


def main():
    # Generate and print a random FEN
    fen = generate_random_fen(15)
    print(f"Random FEN after 15 moves:")
    print(fen)

    # Also print the chessboardimage.com URL format
    # This format uses only the board position (first part of FEN) with slashes removed
    board_position = fen.split(" ")[0].replace("/", "")
    print(f"\nChessboard image URL:")
    print(f"https://chessboardimage.com/{board_position}.png")

    # Print the board for visualization
    print(f"\nBoard visualization:")
    board = chess.Board(fen)
    print(board)


if __name__ == "__main__":
    main()
