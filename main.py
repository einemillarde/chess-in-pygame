import pygame
import chess_calculator as calc

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

# Global variables
grid = DEFAULT_GRID
# grid = [
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
#     [ "", "", "", "", "", "", "", "" ],
# ]
selected_square = None
movable_squares = []
choose = False
prev_selected_square = None

# Functions
def draw_grid():
    for y in range(8):
        for x in range(8):
            i = x + y * 8
            surf = pygame.Surface(SQ_D)
            surf.fill(L_SQ_COL if (i + y) % 2 == 0 else D_SQ_COL)
            pos = (SP_X + x * SQ_W, SP_Y + y * SQ_W) if calc.data["white to move"] else (SP_X + SQ_W * (7 - x), SP_Y + SQ_W * (7 - y))
            # pos = (7 - pos[0] + SQ_W * 8, 7 - pos[1] + SQ_W * 8)
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
    pos = (SP_X + choose[0] * SQ_W, SP_Y + choose[1] * SQ_W)
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

    if col == "w":
        surf.blit(im_q, (0, 0))
        surf.blit(im_n, (0, SQ_W))
        surf.blit(im_r, (0, SQ_W * 2))
        surf.blit(im_b, (0, SQ_W * 3))
    else:
        surf.blit(im_b, (0, 0))
        surf.blit(im_r, (0, SQ_W))
        surf.blit(im_n, (0, SQ_W * 2))
        surf.blit(im_q, (0, SQ_W * 3))

    screen.blit(surf, pos)

# Main Logic
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
            choose = (grid[7].index("bp"), 4)
        except ValueError:
            choose = False

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
        selected_square = None
    else:
        if selected_square in movable_squares:
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

            if grid[y0][x0] == "wk":
                calc.data["wk was moved"] = True

            if grid[y0][x0] == "wr" and x0 == 0:
                calc.data["queenside wr was moved"] = True

            if grid[y0][x0] == "wr" and x0 == 7:
                calc.data["kingside wr was moved"] = True

            if grid[y0][x0] == "br" and x0 == 0:
                calc.data["queenside br was moved"] = True

            if grid[y0][x0] == "br" and x0 == 7:
                calc.data["kingside br was moved"] = True

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

            grid[y][x] = grid[y0][x0]
            grid[y0][x0] = ""
            selected_square = None

            calc.next_turn()

        if selected_square:
            x, y = selected_square
            if grid[y][x] == "":
                selected_square = None

        movable_squares = calc.calc_moves(grid, selected_square)

    prev_selected_square = selected_square

    # Draw
    draw_grid()

    if choose: display_choose()

    pygame.display.update()

pygame.quit()