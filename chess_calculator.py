data = {}

def find_king(grid, color):
    target = 'wk' if color == 'w' else 'bk'
    for yy in range(8):
        for xx in range(8):
            if grid[yy][xx] == target:
                return (xx, yy)
    return None

def attacks_from(grid, x, y):
    piece = grid[y][x]
    if piece == "":
        return set()
    color = piece[0]
    pt = piece[1]
    res = set()
    if pt == 'p':
        if color == 'w':
            if x > 0 and y > 0: res.add((x-1, y-1))
            if x < 7 and y > 0: res.add((x+1, y-1))
        else:
            if x > 0 and y < 7: res.add((x-1, y+1))
            if x < 7 and y < 7: res.add((x+1, y+1))
        return res
    if pt == 'n':
        deltas = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
        for dx,dy in deltas:
            tx,ty = x+dx, y+dy
            if 0 <= tx <=7 and 0 <= ty <=7:
                res.add((tx,ty))
        return res
    if pt in ('b','r','q'):
        directions = []
        if pt in ('b','q'):
            directions += [(-1,-1),(-1,1),(1,-1),(1,1)]
        if pt in ('r','q'):
            directions += [(-1,0),(1,0),(0,-1),(0,1)]
        for dx,dy in directions:
            tx,ty = x,y
            while True:
                tx += dx; ty += dy
                if tx < 0 or tx > 7 or ty < 0 or ty > 7: break
                res.add((tx,ty))
                if grid[ty][tx] != "": break
        return res
    if pt == 'k':
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx == 0 and dy == 0: continue
                tx,ty = x+dx, y+dy
                if 0 <= tx <=7 and 0 <= ty <=7:
                    res.add((tx,ty))
        return res
    return res

def seen_by_black(grid):
    squares = set()
    for x in range(8):
        for y in range(8):
            piece = grid[y][x]
            if piece == "" or piece[0] == 'w':
                continue
            for mv in attacks_from(grid, x, y):
                squares.add(mv)
    return squares

def seen_by_white(grid):
    squares = set()
    for x in range(8):
        for y in range(8):
            piece = grid[y][x]
            if piece == "" or piece[0] == 'b':
                continue
            for mv in attacks_from(grid, x, y):
                squares.add(mv)
    return squares


def clear_pawn_data():
    for i in range(8):
        data[f"bp {i} pushed 2 squares"] = False
        data[f"wp {i} pushed 2 squares"] = False

def next_turn():
    data["white to move"] = not data["white to move"]


def calc_moves(grid, square):
    if not square: return []
    x, y = square
    squares = []
    if data["white to move"]:
        match grid[y][x]:
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
    else:
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
    return squares


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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "bp"
        bk_pos = find_king(grid, 'b')
        if bk_pos and bk_pos not in seen_by_white(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

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

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "bk"
        if move not in seen_by_white(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "bq"
        bk_pos = find_king(grid, 'b')
        if bk_pos and bk_pos not in seen_by_white(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "bb"
        bk_pos = find_king(grid, 'b')
        if bk_pos and bk_pos not in seen_by_white(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

def move_bn(grid, square):
    x, y = square
    squares = []
    deltas = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
    for dx, dy in deltas:
        x0 = x + dx
        y0 = y + dy
        if 0 <= x0 <= 7 and 0 <= y0 <= 7:
            if grid[y0][x0] == "" or grid[y0][x0][0] != 'b':
                squares.append((x0, y0))

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "bn"
        bk_pos = find_king(grid, 'b')
        if bk_pos and bk_pos not in seen_by_white(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "br"
        bk_pos = find_king(grid, 'b')
        if bk_pos and bk_pos not in seen_by_white(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "wp"
        wk_pos = find_king(grid, 'w')
        if wk_pos and wk_pos not in seen_by_black(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed


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

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "wk"
        if (find_king(grid, 'w') not in seen_by_black(grid)) and ((x0,y0) not in seen_by_black(grid)):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "wq"
        wk_pos = find_king(grid, 'w')
        if wk_pos and wk_pos not in seen_by_black(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "wb"
        wk_pos = find_king(grid, 'w')
        if wk_pos and wk_pos not in seen_by_black(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

def move_wn(grid, square):
    x, y = square
    squares = []
    deltas = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
    for dx, dy in deltas:
        x0 = x + dx
        y0 = y + dy
        if 0 <= x0 <= 7 and 0 <= y0 <= 7:
            if grid[y0][x0] == "" or grid[y0][x0][0] != 'w':
                squares.append((x0, y0))

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "wn"
        wk_pos = find_king(grid, 'w')
        if wk_pos and wk_pos not in seen_by_black(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

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

    allowed = []

    for move in squares:
        x0, y0 = move
        buff = grid[y0][x0]
        orig = grid[y][x]
        grid[y][x] = ""
        grid[y0][x0] = "wr"
        wk_pos = find_king(grid, 'w')
        if wk_pos and wk_pos not in seen_by_black(grid):
            allowed.append(move)
        grid[y0][x0] = buff
        grid[y][x] = orig

    return allowed

clear_pawn_data()

data["bk was moved"] = False
data["queenside br was moved"] = False
data["kingside br was moved"] = False
data["wk was moved"] = False
data["queenside wr was moved"] = False
data["kingside wr was moved"] = False

data["white to move"] = True

data["wk pos"] = (4, 7)
data["bk pos"] = (4, 0)