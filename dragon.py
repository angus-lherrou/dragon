import argparse

from cli_draw import Direction, Turn, draw


class Dragon:
    def __init__(self, depth: int):
        self.turns = []
        self.trace(depth)

    def trace(self, depth: int):
        self.trace_depth(depth, Turn.R)

    def trace_depth(self, n: int, turn: Turn):
        if n > 0:
            self.trace_depth(n - 1, Turn.R)
            self.write(turn)
            self.trace_depth(n - 1, Turn.L)

    def write(self, turn: Turn):
        self.turns.append(turn)


def main(depth: int = 5,
         initial_direction: Direction = Direction.R,
         x_step: int = 2,
         y_step: int = 1,
         turns_only: bool = False,
         ):
    dragon = Dragon(depth)
    if turns_only:
        print(''.join(turn.name for turn in dragon.turns))
    else:
        draw(initial_direction, dragon.turns, x_step, y_step)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Draw a dragon curve.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("DEPTH", type=int, help="Depth of the dragon curve to generate")
    parser.add_argument("--turns-only", action="store_true", help="Instead of drawing the curve, output the turns necessary for cli-draw to draw the curve")
    parser.add_argument(
        "--x-step",
        "-x",
        type=int,
        default=2,
        help="The number of columns a single x-axis step takes.",
    )
    parser.add_argument(
        "--y-step",
        "-y",
        type=int,
        default=1,
        help="The number of lines a single y-axis step takes.",
    )
    parser.add_argument(
        "--initial-direction",
        "-d",
        type=str,
        default="R",
        choices=Direction._member_names_,
        help="The starting direction of travel.",
    )

    args = parser.parse_args()

    main(args.DEPTH, Direction[args.initial_direction], args.x_step, args.y_step, args.turns_only)
