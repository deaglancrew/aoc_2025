from typing import NamedTuple, Literal


class Instruction(NamedTuple):
    direction: Literal['L', 'R']
    amount: int

    @classmethod
    def parse_token(cls, token: str):
        direction, *numbers = token.strip()
        return cls(direction, int(''.join(numbers)))


assert Instruction.parse_token('R14') == Instruction('R', 14)

class Dial:
    def __init__(self, degree=50):
        self._degree = degree

    def turn_left(self, amount: int):
        amount = amount % 100
        self._degree -= amount
        if self._degree < 0:
            self._degree += 100

    def turn_right(self, amount: int):
        amount = amount % 100
        self._degree += amount
        if self._degree >= 100:
            self._degree -= 100

    @property
    def degree(self):
        return self._degree

    def apply_instruction(self, instruction: Instruction):
        match instruction:
            case Instruction('L', amount):
                self.turn_left(amount)
            case Instruction('R', amount):
                self.turn_right(amount)
        return self

    def __repr__(self):
        return f'Dial(degree={self._degree})'

assert Dial(degree=5).apply_instruction(Instruction.parse_token('L10')).degree == 95

def solve_1(tokens):
    dial = Dial()
    count = 0
    for instruction in map(Instruction.parse_token, tokens):
        dial.apply_instruction(instruction)
        if dial.degree == 0:
            count += 1
    return count

EXAMPLE_IN = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''.splitlines()

assert solve_1(EXAMPLE_IN) == 3

with open('inputs/day1.txt') as infile:
    print('Part 1 solution:', solve_1(infile))

class SmartDial(Dial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._zero_count = 0

    def turn_left(self, amount: int):
        self._zero_count += amount // 100
        amount = amount % 100
        self._degree -= amount
        if self._degree <= 0 and abs(self._degree) != amount:
            self._zero_count += 1
        if self._degree < 0:
            self._degree += 100

    def turn_right(self, amount: int):
        self._zero_count += amount // 100
        amount = amount % 100
        self._degree += amount
        if self._degree >= 100:
            self._zero_count += 1
            self._degree -= 100

    @property
    def zero_count(self):
        return self._zero_count


def solve_2(tokens):
    dial = SmartDial()
    for instruction in map(Instruction.parse_token, tokens):
        dial.apply_instruction(instruction)
    return dial.zero_count

assert solve_2(EXAMPLE_IN) == 6
assert solve_2(['R1000']) == 10

with open('inputs/day1.txt') as infile:
    print('Part 2 solution:', solve_2(infile))