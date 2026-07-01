import tkinter as tk
from tkinter import simpledialog, messagebox
import chess
import hashlib
import os
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

checkpoint_file = os.path.join(
    BASE_DIR,
    "auth",
    "checkpoints.txt"
)

with open(
    checkpoint_file,
    "r",
    encoding="utf-8"
) as f:

    content = f.read()

blocks = content.strip().split("\n\n")

checkpoints = []

for block in blocks:

    lines = block.split("\n")

    checkpoint_id = int(
        lines[0].split(":")[1]
    )

    fen = lines[1][4:]

    checkpoints.append({
        "id": checkpoint_id,
        "fen": fen
    })

auth_key = simpledialog.askstring(
    "Authentication",
    "Enter Shared Secret Key:"
)

attempts = 0

MAX_ATTEMPTS = 3


def write_breach_log():

    log_file = os.path.join(
        BASE_DIR,
        "auth",
        "breach_log.txt"
    )

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{datetime.datetime.now()} "
            f"- Authentication Failure\n"
        )


def get_expected_move(fen):

    board = chess.Board(fen)

    legal_moves = sorted(
        list(board.legal_moves),
        key=lambda m: m.uci()
    )

    hash_input = auth_key + fen

    hash_value = hashlib.sha256(
        hash_input.encode()
    ).hexdigest()

    move_index = int(
        hash_value,
        16
    ) % len(legal_moves)

    return legal_moves[move_index]


for checkpoint in checkpoints:

    fen = checkpoint["fen"]

    board = chess.Board(fen)

    expected_move = get_expected_move(fen)

    print(
        f"\nCheckpoint {checkpoint['id']}"
    )

    print(
        "Expected move generated."
    )

    user_move = input(
        "Enter move (UCI): "
    ).strip()

    try:

        user_move_obj = chess.Move.from_uci(
            user_move
        )

    except:

        attempts += 1

        print(
            f"Invalid format. "
            f"Attempt {attempts}/3"
        )

        if attempts >= MAX_ATTEMPTS:

            write_breach_log()

            print(
                "\nBREACH ALERT"
            )

            exit()

        continue

    if user_move_obj == expected_move:

        print(
            "Checkpoint Passed"
        )

    else:

        attempts += 1

        print(
            f"Wrong Move. "
            f"Attempt {attempts}/3"
        )

        if attempts >= MAX_ATTEMPTS:

            write_breach_log()

            print(
                "\nBREACH ALERT"
            )

            exit()

print(
    "\nAuthentication Successful"
)

decoder_path = os.path.join(
    BASE_DIR,
    "engine",
    "decoder.py"
)

subprocess.run(
    ["python", decoder_path]
)