import enum


class Dir(enum.Enum):
    R = (1, 0)
    D = (0, 1)
    L = (-1, 0)
    U = (0, -1)

    def succ(self: 'Dir') -> 'Dir':
        return Dir(matmul(SUCC, self.value))

    def pred(self: 'Dir') -> 'Dir':
        return Dir(matmul(PRED, self.value))

    def opp(self: 'Dir') -> 'Dir':
        return Dir(matmul(OPP, self.value))

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


SUCC = ((0, -1),
        (1, 0))
PRED = ((0, 1),
        (-1, 0))
OPP = ((-1, 0),
       (0, -1))
VAL2CHAR = [
    ' ',  # 0b0000
    '╷',  # 0b0001
    '╴',  # 0b0010
    '┐',  # 0b0011
    '╵',  # 0b0100
    '│',  # 0b0101
    '┘',  # 0b0110
    '┤',  # 0b0111
    '╶',  # 0b1000
    '┌',  # 0b1001
    '─',  # 0b1010
    '┬',  # 0b1011
    '└',  # 0b1100
    '├',  # 0b1101
    '┴',  # 0b1110
    '┼',  # 0b1111
]
CHAR2VAL = {
    ' ': 0b0000,
    '╷': 0b0001,
    '╴': 0b0010,
    '┐': 0b0011,
    '╵': 0b0100,
    '│': 0b0101,
    '┘': 0b0110,
    '┤': 0b0111,
    '╶': 0b1000,
    '┌': 0b1001,
    '─': 0b1010,
    '┬': 0b1011,
    '└': 0b1100,
    '├': 0b1101,
    '┴': 0b1110,
    '┼': 0b1111,
}
DIR2VAL = {
    'R': 0b1000,
    'D': 0b0001,
    'L': 0b0010,
    'U': 0b0100,
}


def str2val(coords: str) -> int:
    val = 0
    for coord in coords:
        val |= DIR2VAL[coord]
    return val


def overlay(first: str, second: str) -> str:
    return VAL2CHAR[CHAR2VAL[first] | CHAR2VAL[second]]


def matmul(mat: tuple[tuple[int, int], tuple[int, int]], vec: tuple[int, int]) -> tuple[int, int]:
    x = mat[0][0] * vec[0] + mat[0][1] * vec[1]
    y = mat[1][0] * vec[0] + mat[1][1] * vec[1]

    return x, y


class Turn(enum.Enum):
    L = enum.auto()
    R = enum.auto()


def walk(initial_dir: Dir, turns: list[Turn]) -> tuple[tuple[int, int], tuple[int, int]]:
    (x, y) = (min_x, min_y) = (max_x, max_y) = (0, 0)
    this_dir = initial_dir

    def step():
        nonlocal x, y, min_x, min_y, max_x, max_y
        x += this_dir.x
        y += this_dir.y
        min_x, _, max_x = sorted([min_x, max_x, x])
        min_y, _, max_y = sorted([min_y, max_y, y])

    step()
    for turn in turns:
        match turn:
            case Turn.R:
                this_dir = this_dir.succ()
            case Turn.L:
                this_dir = this_dir.pred()
        step()

    return (min_x, min_y), (max_x, max_y)


def go(grid: list[list[str]], x: int, y: int, dir: Dir, x_step: int, y_step: int) -> tuple[int, int]:
    grid[y][x] = overlay(grid[y][x], VAL2CHAR[str2val(dir.name)])
    x += dir.x
    y += dir.y
    if dir in {Dir.R, Dir.L}:
        step = x_step
    else:
        step = y_step
    for _ in range(step - 1):
        grid[y][x] = overlay(grid[y][x], VAL2CHAR[str2val(dir.name + dir.opp().name)])
        x += dir.x
        y += dir.y
    grid[y][x] = overlay(grid[y][x], VAL2CHAR[str2val(dir.opp().name)])
    return x, y


def draw(initial_dir: Dir, turns: list[Turn], x_step, y_step):
    (min_x, min_y), (max_x, max_y) = walk(initial_dir, turns)

    grid = [
        [
            ' '
            for _x in range((max_x - min_x) * x_step + 1)
        ]
        for _y in range((max_y - min_y) * y_step + 1)
    ]

    this_dir = Dir.R
    x = (-min_x) * x_step
    y = (-min_y) * y_step
    for turn in turns:
        x, y = go(grid, x, y, this_dir, x_step, y_step)
        match turn:
            case Turn.R:
                this_dir = this_dir.succ()
            case Turn.L:
                this_dir = this_dir.pred()
    go(grid, x, y, this_dir, x_step, y_step)

    print('\n'.join([''.join(row) for row in grid]))
