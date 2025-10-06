import copy

data = {}

def seen_by_black(grid):
    squares = set()

    for x in range(8):
        for y in range(8):
            piece = grid[y][x]
            if piece == "" or piece[0] == "w":
                continue

            if piece[1] == "p":
                if x > 0 and y < 7:
                    squares.add((x - 1, y + 1))
                if x < 7 and y < 7:
                    squares.add((x + 1, y + 1))
            elif piece[1] == "k":
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0: continue
                        x1, y1 = x + dx, y + dy
                        if 0 <= x1 <= 7 and 0 <= y1 <= 7:
                            squares.add((x1, y1))
            else:
                moves = calc_moves(grid, (x, y))
                for move in moves:
                    squares.add(move)

    return squares

def seen_by_white(grid):
    squares = set()

    for x in range(8):
        for y in range(8):
            piece = grid[y][x]
            if piece == "" or piece[0] == "b":
                continue

            if piece[1] == "p":
                if x > 0 and y > 0:
                    squares.add((x - 1, y - 1))
                if x < 7 and y > 0:
                    squares.add((x + 1, y - 1))
            elif piece[1] == "k":
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0: continue
                        x1, y1 = x + dx, y + dy
                        if 0 <= x1 <= 7 and 0 <= y1 <= 7:
                            squares.add((x1, y1))
            else:
                moves = calc_moves(grid, (x, y))
                for move in moves:
                    squares.add(move)

    return squares


def clear_pawn_data():
    for i in range(8):
        data[f"bp {i} pushed 2 squares"] = False
        data[f"wp {i} pushed 2 squares"] = False

def calc_moves(grid, square):
    if not square: return []
    x, y = square
    match grid[y][x]:
        case "bp":
            squares = move_bp(grid, square)
        case "bk":
            squares = move_bk(grid, square)
        case "bq":
            squares = move_bq(grid, square)
        case "bb":
            squares = move_bb(grid, square)
        case "bn":
            squares = move_bn(grid, square)
        case "br":
            squares = move_br(grid, square)
        case "wp":
            squares = move_wp(grid, square)
        case "wk":
            squares = move_wk(grid, square)
        case "wq":
            squares = move_wq(grid, square)
        case "wb":
            squares = move_wb(grid, square)
        case "wn":
            squares = move_wn(grid, square)
        case "wr":
            squares = move_wr(grid, square)
    return [] if not squares else squares


def move_bp(grid, square):
    x, y = square
    squares = []

    if y < 7 and grid[y + 1][x] == "":
        squares.append((x, y + 1))
        if y == 1 and grid[3][x] == "":
            squares.append((x, 3))

    if y < 7 and x > 0 and grid[y + 1][x - 1] != "" and grid[y + 1][x - 1][0] == "w":
        squares.append((x - 1, y + 1))

    if y < 7 and x < 7 and grid[y + 1][x + 1] != "" and grid[y + 1][x + 1][0] == "w":
        squares.append((x + 1, y + 1))

    if y == 4:
        if x != 0 and data[f"wp {x - 1} pushed 2 squares"]:
            squares.append((x - 1, 5))
        elif x != 7 and data[f"wp {x + 1} pushed 2 squares"]:
            squares.append((x + 1, 5))

    return squares

def move_bk(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            x0 = x + i
            y0 = y + j
            if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: continue
            if grid[y0][x0] != "":
                if grid[y0][x0][0] == "b":
                    continue
                else:
                    squares.append((x0, y0))
                    continue
            squares.append((x0, y0))

    attacked = seen_by_white(grid)

    if not data["bk was moved"] and not square in attacked:
        if not data["kingside br was moved"] and grid[0][5] == "" and grid[0][6] == "" and (5, 0) not in attacked:
            squares.append((6, 0))
        if not data["queenside br was moved"] and grid[0][1] == "" and grid[0][2] == "" and grid[0][3] == "" and (3, 0) not in attacked and (2, 0) not in attacked:
            squares.append((2, 0))

    allowed = []

    for i, move in enumerate(squares):
        x0, y0 = move
        grid0 = copy.deepcopy(grid)
        grid0[y0][x0] = "bk"
        grid0[y][x] = ""
        if move in seen_by_black(grid0):
            continue
        allowed.append(move)

    return allowed

def move_bq(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            x0, y0 = (x, y)
            while True:
                x0 += i
                y0 += j
                if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: break
                if grid[y0][x0] != "":
                    if grid[y0][x0][0] == "b":
                        break
                    else:
                        squares.append((x0, y0))
                        break
                squares.append((x0, y0))

    return squares

def move_bb(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            x0, y0 = (x, y)
            while True:
                x0 += i
                y0 += j
                if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: break
                if grid[y0][x0] != "":
                    if grid[y0][x0][0] == "b":
                        break
                    else:
                        squares.append((x0, y0))
                        break
                squares.append((x0, y0))

    return squares

def move_bn(grid, square):
    x, y = square
    squares = []

    for i in range(4):
        i0 = -2 if i == 0 else -1 if i == 1 else 1 if i == 2 else 2
        for j in range(2):
            j0 = (-1 if j == 0 else 1) if abs(i0) == 2 else (-2 if j == 0 else 2)
            x0 = i0 + x
            y0 = j0 + y
            if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: continue
            if grid[y0][x0] != "" and grid[y0][x0][0] == "b": continue
            squares.append((x0, y0))

    return squares

def move_br(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) == abs(j): continue
            x0, y0 = (x, y)
            while True:
                x0 += i
                y0 += j
                if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: break
                if grid[y0][x0] != "":
                    if grid[y0][x0][0] == "b":
                        break
                    else:
                        squares.append((x0, y0))
                        break
                squares.append((x0, y0))

    return squares

def move_wp(grid, square):
    x, y = square
    squares = []

    if y > 0 and grid[y - 1][x] == "":
        squares.append((x, y - 1))
        if y == 6 and grid[4][x] == "":
            squares.append((x, 4))

    if y > 0 and x > 0 and grid[y - 1][x - 1] != "" and grid[y - 1][x - 1][0] == "b":
        squares.append((x - 1, y - 1))

    if y > 0 and x < 7 and grid[y - 1][x + 1] != "" and grid[y - 1][x + 1][0] == "b":
        squares.append((x + 1, y - 1))

    if y == 3:
        if x != 0 and data[f"bp {x - 1} pushed 2 squares"]:
            squares.append((x - 1, 2))
        elif x != 7 and data[f"bp {x + 1} pushed 2 squares"]:
            squares.append((x + 1, 2))


    return squares


def move_wk(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            x0 = x + i
            y0 = y + j
            if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: continue
            if grid[y0][x0] != "":
                if grid[y0][x0][0] == "w":
                    continue
                else:
                    squares.append((x0, y0))
                    continue
            squares.append((x0, y0))

    attacked = seen_by_black(grid)

    if not data["wk was moved"] and not square in attacked:
        if not data["kingside wr was moved"] and grid[7][5] == "" and grid[7][6] == "" and (5, 7) not in attacked:
            squares.append((6, 7))
        if not data["queenside wr was moved"] and grid[7][1] == "" and grid[7][2] == "" and grid[7][3] == "" and (3, 7) not in attacked and (2, 7) not in attacked:
            squares.append((2, 7))

    allowed = []

    for i, move in enumerate(squares):
        x0, y0 = move
        grid0 = copy.deepcopy(grid)
        grid0[y0][x0] = "wk"
        grid0[y][x] = ""
        if move in seen_by_black(grid0):
            continue
        allowed.append(move)

    return allowed


def move_wq(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            x0, y0 = (x, y)
            while True:
                x0 += i
                y0 += j
                if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: break
                if grid[y0][x0] != "":
                    if grid[y0][x0][0] == "w":
                        break
                    else:
                        squares.append((x0, y0))
                        break
                squares.append((x0, y0))

    return squares

def move_wb(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            x0, y0 = (x, y)
            while True:
                x0 += i
                y0 += j
                if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: break
                if grid[y0][x0] != "":
                    if grid[y0][x0][0] == "w":
                        break
                    else:
                        squares.append((x0, y0))
                        break
                squares.append((x0, y0))

    return squares

def move_wn(grid, square):
    x, y = square
    squares = []

    for i in range(4):
        i0 = -2 if i == 0 else -1 if i == 1 else 1 if i == 2 else 2
        for j in range(2):
            j0 = (-1 if j == 0 else 1) if abs(i0) == 2 else (-2 if j == 0 else 2)
            x0 = i0 + x
            y0 = j0 + y
            if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: continue
            if grid[y0][x0] != "" and grid[y0][x0][0] == "w": continue
            squares.append((x0, y0))

    return squares

def move_wr(grid, square):
    x, y = square
    squares = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) == abs(j): continue
            x0, y0 = (x, y)
            while True:
                x0 += i
                y0 += j
                if x0 < 0 or x0 > 7 or y0 < 0 or y0 > 7: break
                if grid[y0][x0] != "":
                    if grid[y0][x0][0] == "w":
                        break
                    else:
                        squares.append((x0, y0))
                        break
                squares.append((x0, y0))

    return squares

clear_pawn_data()
data["bk was moved"] = False
data["queenside br was moved"] = False
data["kingside br was moved"] = False
data["wk was moved"] = False
data["queenside wr was moved"] = False
data["kingside wr was moved"] = False