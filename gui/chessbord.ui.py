import tkinter as tk
import chess
import os

from PIL import Image, ImageTk

board = chess.Board()

selected_square = None

root = tk.Tk()
root.title("StegaChess")

canvas = tk.Canvas(root, width=520, height=520)
canvas.pack()

square_size = 60

colors = ["#F0D9B5", "#B58863"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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


def draw_board():

    canvas.delete("all")

    board_offset = 20

    for row in range(8):
        for col in range(8):

            x1 = board_offset + col * square_size
            y1 = row * square_size

            x2 = x1 + square_size
            y2 = y1 + square_size

            square = chess.square(col, 7 - row)

            color = colors[(row + col) % 2]

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
                    image=pieces[piece.symbol()]
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


def on_click(event):

    global selected_square

    board_offset = 20

    if event.x < board_offset:
        return

    col = (event.x - board_offset) // square_size

    row = 7 - (event.y // square_size)

    if not (0 <= col <= 7 and 0 <= row <= 7):
        return

    clicked_square = chess.square(col, row)

    if selected_square is None:

        piece = board.piece_at(clicked_square)

        if piece:

            selected_square = clicked_square

            print(
                "Selected:",
                chess.square_name(selected_square)
            )

    else:

        move = chess.Move(
            selected_square,
            clicked_square
        )

        if move in board.legal_moves:

            print("Move played:", move)

            board.push(move)

        else:

            print("Illegal move!")

        selected_square = None

        draw_board()


draw_board()

canvas.bind("<Button-1>", on_click)

root.mainloop()