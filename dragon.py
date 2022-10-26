from cli_draw import Direction, Turn, draw


class Dragon:
    def __init__(self, depth: int):
        self.turns = []
        self.dir: Direction = Direction.R
        self.trace(depth)

    def trace(self, depth: int):
        self.trace_depth(depth, Turn.R)
        print("")

    def trace_depth(self, n: int, turn: Turn):
        if n > 0:
            self.trace_depth(n - 1, Turn.R)
            self.write(turn)
            self.trace_depth(n - 1, Turn.L)

    def write(self, turn: Turn):
        self.turns.append(turn)
        self.dir = self.dir.turn(turn)


def main(depth=5, x_step=2, y_step=1):
    dragon = Dragon(depth)
    draw(Direction.R, dragon.turns, x_step, y_step)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Draw a dragon curve.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("DEPTH", type=int, help="Depth of the dragon curve to generate")
    parser.add_argument("--x-step", "-x", type=int, default=2, help="x-axis scaling")
    parser.add_argument("--y-step", "-y", type=int, default=1, help="y-axis scaling")

    args = parser.parse_args()

    main(args.DEPTH, args.x_step, args.y_step)
