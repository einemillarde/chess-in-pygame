import pygame
import chess_calculator as calc
import copy

# Constants
L_SQ_COL = "#edd6b0"
D_SQ_COL = "#b88762"

D = (W, H) = (520, 520)
SQ_D = (SQ_W, SQ_W) = (60, 60)
SP_D = (SP_X, SP_Y) = (20, 20)
REV_TUP = (8, 0)

DEFAULT_GRID = [
    [ "br", "bn", "bb", "bq", "bk", "bb", "bn", "br" ],
    [ "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp" ],
    [ "", "", "", "", "", "", "", "" ],
    [ "", "", "", "", "", "", "", "" ],
    [ "", "", "", "", "", "", "", "" ],
    [ "", "", "", "", "", "", "", "" ],
    [ "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp" ],
    [ "wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr" ],
]

# Functions
def draw_grid():
    for y in range(8):
        for x in range(8):
            i = x + y * 8
            surf = pygame.Surface(SQ_D)
            surf.fill(L_SQ_COL if (i + y) % 2 == 0 else D_SQ_COL)
            pos = (SP_X + x * SQ_W, SP_Y + y * SQ_W) if calc.data["white to move"] else (SP_X + SQ_W * (7 - x), SP_Y + SQ_W * (7 - y))
            screen.blit(surf, pos)

            key = grid[y][x]

            if selected_square == (x, y):
                surf = pygame.Surface(SQ_D, pygame.SRCALPHA)
                surf.fill("#ffff0040")
                screen.blit(surf, pos)

            if (x, y) in movable_squares:
                surf = pygame.Surface(SQ_D, pygame.SRCALPHA)
                if grid[y][x] == "":
                    pygame.draw.circle(surf, "#00000040", (SQ_W / 2, SQ_W / 2), SQ_W / 6)
                else:
                    pygame.draw.circle(surf, "#00000040", (SQ_W / 2, SQ_W / 2), SQ_W / 2, width = 5)
                screen.blit(surf, pos)

            if key == "": continue

            surf = pygame.image.load(f"pieces/{key}.png")
            surf = pygame.transform.scale(surf, SQ_D)
            screen.blit(surf, pos)

def display_choose():
    if choose:
        pos = (SP_X + choose[0] * SQ_W, SP_Y) if calc.data["white to move"] else (SP_X + SQ_W * (7 - choose[0]), SP_Y)
        dims = (SQ_W, SQ_W * 4)
        surf = pygame.Surface(dims)
        surf.fill("#ffffff")

        col = "w" if choose[1] == 0 else "b"

        im_q = pygame.image.load(f"pieces/{col}q.png")
        im_n = pygame.image.load(f"pieces/{col}n.png")
        im_r = pygame.image.load(f"pieces/{col}r.png")
        im_b = pygame.image.load(f"pieces/{col}b.png")

        im_q = pygame.transform.scale(im_q, SQ_D)
        im_n = pygame.transform.scale(im_n, SQ_D)
        im_r = pygame.transform.scale(im_r, SQ_D)
        im_b = pygame.transform.scale(im_b, SQ_D)

        surf.blit(im_q, (0, 0))
        surf.blit(im_n, (0, SQ_W))
        surf.blit(im_r, (0, SQ_W * 2))
        surf.blit(im_b, (0, SQ_W * 3))

        screen.blit(surf, pos)

def fen(grid, white_to_move, castling, en_passant, halfmove, fullmove):
    rows = []

    for row in grid:
        fen_row = ""
        empty_count = 0

        for piece in row:
            if piece == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0

                color = piece[0]
                piece_type = piece[1]

                fen_piece = {
                    "p": "p",
                    "r": "r",
                    "n": "n",
                    "b": "b",
                    "q": "q",
                    "k": "k",
                }[piece_type]

                if color == "w":
                    fen_piece = fen_piece.upper()

                fen_row += fen_piece

        if empty_count > 0:
            fen_row += str(empty_count)

        rows.append(fen_row)

    board_part = "/".join(rows)

    side_to_move = "w" if white_to_move else "b"

    return f"{board_part} {side_to_move} {castling} {en_passant} {halfmove} {fullmove}"

def dead_position(grid):
    pieces = []

    for row in grid:
        for piece in row:
            if piece != "":
                pieces.append(piece)

    non_kings = [p for p in pieces if p[1] != "k"]

    if len(non_kings) == 0:
        return True

    if len(non_kings) == 1:
        return non_kings[0][1] in ("b", "n")

    if len(non_kings) == 2:
        return (
            non_kings[0][1] == "b"
            and non_kings[1][1] == "b"
        )

    return False

# Global variables
grid = copy.deepcopy(DEFAULT_GRID)
# grid = [
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "br", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "wr", "", "", "", "wk", "", "", "wr" ],
# ]
selected_square = None
movable_squares = []
choose = None
prev_selected_square = None
count = 0
fullmove = 1
halfmove = 0
castling = "KQkq"
en_passant = "-"
history = dict()
history[fen(grid, True, castling, en_passant, halfmove, fullmove)] = 1

# Main Logic
calc.clear_pawn_data()

calc.data["bk was moved"] = False if grid[0][4] == "bk" else True
calc.data["queenside br was moved"] = False if grid[0][0] == "br" else True
calc.data["kingside br was moved"] = False if grid[0][7] == "br" else True
calc.data["wk was moved"] = False if grid[7][4] == "wk" else True
calc.data["queenside wr was moved"] = False if grid[7][0] == "wr" else True
calc.data["kingside wr was moved"] = False if grid[7][7] == "wr" else True

calc.data["white to move"] = True

calc.data["wk pos"] = (4, 7)
calc.data["bk pos"] = (4, 0)

pygame.init()

screen = pygame.display.set_mode(D)
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x < SP_X or x > SP_X + 8 * SQ_W or y < SP_Y or y > SP_Y + 8 * SQ_W:
                selected_square = None
                continue
            x, y = (x - SP_X) // SQ_W, (y - SP_Y) // SQ_W
            selected_square = (x, y) if calc.data["white to move"] else (7 - x, 7 - y)

    # Loop
    clock.tick(60)

    try:
        choose = (grid[0].index("wp"), 0)
    except ValueError:
        try:
            choose = (grid[7].index("bp"), 7)
        except ValueError:
            choose = None

    if choose:
        if selected_square and selected_square[0] == choose[0]:
            if choose[1] == 0:
                match selected_square[1]:
                    case 0:
                        grid[0][choose[0]] = "wq"
                    case 1:
                        grid[0][choose[0]] = "wn"
                    case 2:
                        grid[0][choose[0]] = "wr"
                    case 3:
                        grid[0][choose[0]] = "wb"
            else:
                 match selected_square[1]:
                    case 7:
                        grid[7][choose[0]] = "bq"
                    case 6:
                        grid[7][choose[0]] = "bn"
                    case 5:
                        grid[7][choose[0]] = "br"
                    case 4:
                        grid[7][choose[0]] = "bb"
            calc.next_turn()
        selected_square = None
    else:
        if selected_square in movable_squares and selected_square and prev_selected_square:
            calc.clear_pawn_data()
            x, y = selected_square
            x0, y0 = prev_selected_square

            if grid[y0][x0] == "bp" and y0 + 2 == y:
                calc.data[f"bp {x} pushed 2 squares"] = True

            if grid[y0][x0] == "wp" and y0 - 2 == y:
                calc.data[f"wp {x} pushed 2 squares"] = True

            if grid[y0][x0] == "wp" and grid[y][x] == "" and x != x0:
                grid[y + 1][x] = ""

            if grid[y0][x0] == "bp" and grid[y][x] == "" and x != x0:
                grid[y - 1][x] = ""

            if grid[y0][x0] == "bk":
                calc.data["bk was moved"] = True
                calc.data["bk pos"] = (x, y)
                castling = castling.replace("q", "")
                castling = castling.replace("k", "")

            if grid[y0][x0] == "wk":
                calc.data["wk was moved"] = True
                calc.data["wk pos"] = (x, y)
                castling = castling.replace("Q", "")
                castling = castling.replace("K", "")

            if grid[y0][x0] == "wr" and x0 == 0:
                calc.data["queenside wr was moved"] = True
                castling = castling.replace("Q", "")

            if grid[y0][x0] == "wr" and x0 == 7:
                calc.data["kingside wr was moved"] = True
                castling = castling.replace("K", "")

            if grid[y0][x0] == "br" and x0 == 0:
                calc.data["queenside br was moved"] = True
                castling = castling.replace("q", "")

            if grid[y0][x0] == "br" and x0 == 7:
                calc.data["kingside br was moved"] = True
                castling = castling.replace("k", "")

            if castling == "":
                castling = "-"

            if grid[y0][x0] == "wk" and x == x0 + 2:
                grid[7][5] = "wr"
                grid[7][7] = ""

            if grid[y0][x0] == "wk" and x == x0 - 2:
                grid[7][3] = "wr"
                grid[7][0] = ""

            if grid[y0][x0] == "bk" and x == x0 + 2:
                grid[0][5] = "br"
                grid[0][7] = ""

            if grid[y0][x0] == "bk" and x == x0 - 2:
                grid[0][3] = "br"
                grid[0][0] = ""

            is_capture = grid[y][x] != ""
            is_pawn_advance = grid[y0][x0][1] == "p"
            is_en_passant = grid[y0][x0][1] == "p" and x != x0 and grid[y][x] == ""

            if is_capture or is_en_passant or is_pawn_advance:
                halfmove = 0
            else:
                halfmove += 1

            grid[y][x] = grid[y0][x0]
            grid[y0][x0] = ""
            selected_square = None

            if not "wp" in grid[0] and not "bp" in grid[7]:
                calc.next_turn()

            if calc.data["white to move"]:
                fullmove += 1
                white_legal_moves = []

                for x in range(8):
                    for y in range(8):
                        square = (x, y)
                        piece = grid[y][x]
                        if piece != "" and piece[0] == "w":
                            white_legal_moves += calc.calc_moves(grid, square)

                if not white_legal_moves:
                    if calc.data["wk pos"] in calc.seen_by_black(grid):
                        print("black won by checkmate")
                        running = False
                    else:
                        print("draw by stalemate")
                        running = False
            else:
                black_legal_moves = []

                for x in range(8):
                    for y in range(8):
                        square = (x, y)
                        piece = grid[y][x]
                        if piece != "" and piece[0] == "b":
                            black_legal_moves += calc.calc_moves(grid, square)

                if not black_legal_moves:
                    if calc.data["bk pos"] in calc.seen_by_white(grid):
                        print("white won by checkmate")
                        running = False
                    else:
                        print("draw by stalemate")
                        running = False

            fen_str = fen(grid, calc.data["white to move"], castling, en_passant, halfmove, fullmove)
            repetition_key = " ".join(fen_str.split(" ")[:4])
            history[repetition_key] = history.get(repetition_key, 0) + 1
            if history[repetition_key] >= 3:
                print("draw by repetition")
                running = False

            if halfmove >= 100:
                print("draw by 50-move rule")
                running = False

            if dead_position(grid):
                print("draw by dead position")
                running = False

        if selected_square:
            x, y = selected_square
            if grid[y][x] == "":
                selected_square = None

        movable_squares = calc.calc_moves(grid, selected_square)

    prev_selected_square = selected_square

    # Draw
    draw_grid()

    display_choose()

    pygame.display.update()

pygame.quit()
