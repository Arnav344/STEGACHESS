id="jlwmn3"
import chess
import chess.pgn
import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox

BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_ROOT)

from crypto.aes_utils import decrypt_message


def get_safe_moves(board):

    legal_moves = sorted(
        list(board.legal_moves),
        key=lambda m: m.uci()
    )

    safe_moves = []

    for move in legal_moves:

        temp_board = board.copy()
        temp_board.push(move)

        next_moves = list(
            temp_board.legal_moves
        )

        if len(next_moves) >= 4:
            safe_moves.append(move)

    if len(safe_moves) >= 4:
        return safe_moves

    return legal_moves


pgn_path = os.path.join(
    BASE_DIR,
    "encoded_game.pgn"
)

with open(
    pgn_path,
    "r",
    encoding="utf-8"
) as pgn_file:

    game = chess.pgn.read_game(
        pgn_file
    )

board = game.board()

binary = ""

for move in game.mainline_moves():

    safe_moves = get_safe_moves(board)

    move_index = safe_moves.index(move)

    chunk = format(
        move_index,
        "02b"
    )

    binary += chunk

    board.push(move)

print("Recovered Binary:\n")
print(binary)


def binary_to_text(binary):

    decoded_text = ""

    for i in range(
        0,
        len(binary),
        8
    ):

        byte = binary[i:i+8]

        if len(byte) == 8:

            decoded_text += chr(
                int(byte, 2)
            )

    return decoded_text


encrypted_message = binary_to_text(binary)

print("\nRecovered Encrypted Message:\n")
print(encrypted_message)

root = tk.Tk()
root.withdraw()

aes_key = simpledialog.askstring(
    "StegaChess",
    "Enter AES Key:"
)

if not aes_key:
    messagebox.showerror(
        "Error",
        "AES Key required."
    )
    exit()

try:

    original_message = decrypt_message(
        encrypted_message,
        aes_key
    )

    messagebox.showinfo(
        "Secret Message",
        original_message
    )

    root.destroy()

except Exception:

    messagebox.showerror(
        "Access Denied",
        "Invalid AES Key or corrupted ciphertext."
    )

    root.destroy()