from typing import NamedTuple


class BatteryBank(NamedTuple):
    batteries: tuple[int]

    @classmethod
    def parse_row(cls, row: str):
        return cls(tuple(int(element) for element in row.strip()))

    def largest_battery_pair(self):
        largest_value = 0
        largest_index = None
        for index, battery in enumerate(self.batteries[:-1]):
            if battery > largest_value:
                largest_index = index
                largest_value = battery
        second_battery = 0
        for battery in self.batteries[largest_index+1:]:
            if battery > second_battery:
                second_battery = battery
        return largest_value, second_battery

    def largest_value(self):
        return int(''.join(map(str, self.largest_battery_pair())))

EXAMPLE_IN = """987654321111111
811111111111119
234234234234278
818181911112111""".splitlines()

def solve_1(lines):
    total = 0
    for line in lines:
        bank = BatteryBank.parse_row(line)
        total += bank.largest_value()
    return total

assert solve_1(EXAMPLE_IN) == 357


with open('inputs/day3.txt') as infile:
    print("Part 1 Solution: ", solve_1(infile))