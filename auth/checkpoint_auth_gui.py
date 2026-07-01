import tkinter as tk
from tkinter import messagebox, simpledialog
import chess
import hashlib
import os
import subprocess
import datetime
import json
from tkinter import filedialog

from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
pgn_file = os.path.join(
    BASE_DIR,
    "engine",
    "encoded_game.pgn"
)

pgn_hash_file = os.path.join(
    BASE_DIR,
    "auth",
    "pgn_hash.txt"
)

try:

    with open(pgn_file, "rb") as f:
        current_hash = hashlib.sha256(
            f.read()
        ).hexdigest()

    with open(
        pgn_hash_file,
        "r",
        encoding="utf-8"
    ) as f:
        stored_hash = f.read().strip()

except FileNotFoundError:

    temp_root = tk.Tk()
    temp_root.withdraw()

    messagebox.showerror(
        "Integrity Error",
        "PGN or hash file missing.\nRun encoder first."
    )

    temp_root.destroy()
    exit()

if current_hash != stored_hash:

    temp_root = tk.Tk()
    temp_root.withdraw()

    messagebox.showerror(
        "Tampering Detected",
        "PGN file integrity check failed!"
    )

    temp_root.destroy()
    exit()


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

root = tk.Tk()

root.withdraw()

auth_key = simpledialog.askstring(
    "Authentication",
    "Enter Shared Secret Key:"
)

if auth_key is None:

    messagebox.showerror(
        "Access Denied",
        "No key entered."
    )

    root.destroy()

    exit()

key_hash_file = os.path.join(
    BASE_DIR,
    "auth",
    "key_hash.txt"
)

try:

    with open(
        key_hash_file,
        "r",
        encoding="utf-8"
    ) as f:

        stored_hash = f.read().strip()

except FileNotFoundError:

    root.deiconify()

    messagebox.showerror(
        "Error",
        "key_hash.txt not found.\nRun encoder.py first."
    )

    root.destroy()

    exit()

entered_hash = hashlib.sha256(
    auth_key.encode()
).hexdigest()

if entered_hash != stored_hash:

    root.deiconify()

    messagebox.showerror(
        "Access Denied",
        "Wrong Authentication Key!"
    )

    root.destroy()

    exit()

root.deiconify()

messagebox.showinfo(
    "Authentication",
    "Key Verified Successfully"
)

root.deiconify()

current_checkpoint = 0

attempts = 0

MAX_ATTEMPTS = 3

selected_square = None

board = None

root.title("StegaChess Authentication")

canvas = tk.Canvas(
    root,
    width=520,
    height=520
)

canvas.pack()

square_size = 60

colors = ["#F0D9B5", "#B58863"]

pieces = {}

piece_names = {
    'P': 'pawn-w',
    'R': 'rook-w',
    'N': 'knight-w',
    'B': 'bishop-w',
    'Q': 'queen-w',
    'K': 'king-w',

    'p': 'pawn-b',
    'r': 'rook-b',
    'n': 'knight-b',
    'b': 'bishop-b',
    'q': 'queen-b',
    'k': 'king-b'
}

for symbol, filename in piece_names.items():

    image_path = os.path.join(
        BASE_DIR,
        "assets",
        f"{filename}.png"
    )

    image = Image.open(image_path)

    image = image.resize((50, 50))

    pieces[symbol] = ImageTk.PhotoImage(image)


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
            f"Authentication Failure\n"
        )


def get_expected_move(fen):

    temp_board = chess.Board(fen)

    legal_moves = sorted(
        list(temp_board.legal_moves),
        key=lambda m: m.uci()
    )

    hash_input = auth_key + fen + str(current_checkpoint)

    hash_value = hashlib.sha256(
        hash_input.encode()
    ).hexdigest()

    move_index = int(
        hash_value,
        16
    ) % len(legal_moves)

    return legal_moves[move_index]


def draw_board():

    canvas.delete("all")

    board_offset = 20

    for row in range(8):

        for col in range(8):

            x1 = board_offset + col * square_size
            y1 = row * square_size

            x2 = x1 + square_size
            y2 = y1 + square_size

            square = chess.square(
                col,
                7 - row
            )

            color = colors[
                (row + col) % 2
            ]

            if square == selected_square:
                color = "yellow"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color
            )

            piece = board.piece_at(square)

            if piece:

                canvas.create_image(
                    x1 + 30,
                    y1 + 30,
                    image=pieces[
                        piece.symbol()
                    ]
                )

    for row in range(8):

        canvas.create_text(
            10,
            row * square_size + 30,
            text=str(8 - row),
            font=("Arial", 12, "bold")
        )

    for col in range(8):

        canvas.create_text(
            board_offset + col * square_size + 30,
            495,
            text=chr(ord('a') + col),
            font=("Arial", 12, "bold")
        )


def load_checkpoint():

    global board

    checkpoint = checkpoints[
        current_checkpoint
    ]

    board = chess.Board(
        checkpoint["fen"]
    )

    expected_move = get_expected_move(
        checkpoint["fen"]
    )

    draw_board()

    from_square = chess.square_name(
        expected_move.from_square
    )

    to_square = chess.square_name(
        expected_move.to_square
    )

    messagebox.showinfo(
        "Checkpoint Authentication",
        f"Checkpoint {checkpoint['id']}\n\n"
        f"From: {from_square}\n"
        f"To: {to_square}"
    )


def authentication_success():

    global current_checkpoint
    global selected_square

    current_checkpoint += 1

    selected_square = None

    if current_checkpoint >= len(
        checkpoints
    ):

        messagebox.showinfo(
            "Success",
            "All checkpoints passed."
        )

        decoder_path = os.path.join(
            BASE_DIR,
            "engine",
            "decoder.py"
        )

        subprocess.run(
            ["python", decoder_path]
        )

        root.destroy()

        return

    load_checkpoint()


def breach_alert():

    write_breach_log()

    messagebox.showerror(
        "Breach Alert",
        "Maximum attempts exceeded."
    )

    root.destroy()


def on_click(event):

    global selected_square
    global attempts

    board_offset = 20

    if event.x < board_offset:
        return

    col = (
        event.x - board_offset
    ) // square_size

    row = 7 - (
        event.y // square_size
    )

    if not (
        0 <= col <= 7
        and
        0 <= row <= 7
    ):
        return

    clicked_square = chess.square(
        col,
        row
    )

    checkpoint = checkpoints[
        current_checkpoint
    ]

    expected_move = get_expected_move(
        checkpoint["fen"]
    )

    if selected_square is None:

        piece = board.piece_at(
            clicked_square
        )

        if piece:

            selected_square = clicked_square

            draw_board()

        else:

         move = chess.Move(
            selected_square,
            clicked_square
        )

    else:

        move = chess.Move(
            selected_square,
            clicked_square
        )

        if move == expected_move:

            selected_square = None

            messagebox.showinfo(
                "Success",
                "Checkpoint Passed"
            )

            authentication_success()

            return

        else:

            attempts += 1

            messagebox.showwarning(
                "Wrong Move",
                f"Attempt {attempts}/3"
            )

            if attempts >= MAX_ATTEMPTS:
                breach_alert()

        selected_square = None
        draw_board()


canvas.bind(
    "<Button-1>",
    on_click
)

load_checkpoint()

root.mainloop()
