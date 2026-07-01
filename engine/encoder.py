
import chess
import chess.pgn
import os
import hashlib
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import datetime

BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_ROOT)

from crypto.aes_utils import encrypt_message


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

root = tk.Tk()
root.withdraw()

AUTH_KEY = simpledialog.askstring(
    "StegaChess",
    "Enter Authentication Key:"
)

if not AUTH_KEY:
    messagebox.showerror(
        "Error",
        "Authentication Key required."
    )
    exit()

AES_KEY = simpledialog.askstring(
    "StegaChess",
    "Enter AES Key:"
)

if not AES_KEY:
    messagebox.showerror(
        "Error",
        "AES Key required."
    )
    exit()

SECRET_MESSAGE = simpledialog.askstring(
    "StegaChess",
    "Enter Secret Message:"
)

if not SECRET_MESSAGE:
    messagebox.showerror(
        "Error",
        "Message required."
    )
    exit()

encrypted_message = encrypt_message(
    SECRET_MESSAGE,
    AES_KEY
)

print("\nEncrypted Message:")
print(encrypted_message)

binary = ''.join(
    format(ord(c), '08b')
    for c in encrypted_message
)

chunks = [
    binary[i:i+2]
    for i in range(0, len(binary), 2)
]

TOTAL_CHECKPOINTS = 6
total_moves = len(chunks)

checkpoint_interval = max(
    1,
    total_moves // TOTAL_CHECKPOINTS
)

board = chess.Board()
game = chess.pgn.Game()
node = game
checkpoints = []

for move_number, chunk in enumerate(chunks):

    safe_moves = get_safe_moves(board)

    move_index = int(chunk, 2)

    if move_index >= len(safe_moves):
        raise Exception(
            f"Not enough safe moves at chunk {chunk}"
        )

    selected_move = safe_moves[move_index]

    board.push(selected_move)
    node = node.add_variation(selected_move)

    if (
        (move_number + 1) % checkpoint_interval == 0
        and len(checkpoints) < TOTAL_CHECKPOINTS
    ):
        checkpoints.append({
            "checkpoint_id": len(checkpoints) + 1,
            "fen": board.fen()
        })

while len(checkpoints) < TOTAL_CHECKPOINTS:
    checkpoints.append({
        "checkpoint_id": len(checkpoints) + 1,
        "fen": board.fen()
    })

pgn_path = os.path.join(
    BASE_DIR,
    "encoded_game.pgn"
)

with open(
    pgn_path,
    "w",
    encoding="utf-8"
) as f:
    print(game, file=f)

checkpoint_path = os.path.join(
    PROJECT_ROOT,
    "auth",
    "checkpoints.txt"
)

with open(
    checkpoint_path,
    "w",
    encoding="utf-8"
) as f:

    for checkpoint in checkpoints:
        f.write(
            f"CHECKPOINT:{checkpoint['checkpoint_id']}\n"
        )
        f.write(
            f"FEN:{checkpoint['fen']}\n\n"
        )

auth_key_hash = hashlib.sha256(
    AUTH_KEY.encode()
).hexdigest()

auth_hash_path = os.path.join(
    PROJECT_ROOT,
    "auth",
    "key_hash.txt"
)

with open(
    auth_hash_path,
    "w",
    encoding="utf-8"
) as f:
    f.write(auth_key_hash)

with open(pgn_path, "rb") as f:
    pgn_hash = hashlib.sha256(
        f.read()
    ).hexdigest()

pgn_hash_path = os.path.join(
    PROJECT_ROOT,
    "auth",
    "pgn_hash.txt"
)

with open(
    pgn_hash_path,
    "w",
    encoding="utf-8"
) as f:
    f.write(pgn_hash)

print("\n===================")
print("ENCODING COMPLETE")
print("===================")
print("\nTotal Moves:", total_moves)
print("Total Checkpoints:", len(checkpoints))
print("PGN Saved:", pgn_path)
print("Checkpoints Saved:", checkpoint_path)
print("Auth Key Hash Saved:", auth_hash_path)
print("PGN Hash Saved:", pgn_hash_path)

storage_dir = os.path.join(
    PROJECT_ROOT,
    "storage",
    "sent"
)

os.makedirs(storage_dir, exist_ok=True)

with open(pgn_path, "r", encoding="utf-8") as f:
    pgn_text = f.read()

checkpoint_list = []

for checkpoint in checkpoints:
    checkpoint_list.append({
        "checkpoint_id": checkpoint["checkpoint_id"],
        "fen": checkpoint["fen"]
    })

stg_data = {
    "sender": "default_user",
    "pgn": pgn_text,
    "checkpoints": checkpoint_list,
    "key_hash": auth_key_hash,
    "pgn_hash": pgn_hash
}

stg_path = os.path.join(
    storage_dir,
    "message.stg"
)

with open(stg_path, "w", encoding="utf-8") as f:
    json.dump(stg_data, f, indent=4)

print("STG File Saved:", stg_path)

messagebox.showinfo(
    "StegaChess",
    f"Encoding Complete!\n\n"
    f"Total Moves: {total_moves}\n"
    f"Total Checkpoints: {len(checkpoints)}"
)

root.destroy()