from typing import NamedTuple

class IdRange(NamedTuple):
    start: int
    end: int

    @classmethod
    def from_string(cls, string):
        start, end = string.split('-')
        return cls(int(start), int(end))

    def starting_palindrome(self):
        return MultiNumber.first_multi_after(self.start)

    def all_matching_palindromes(self):
        palindrome = self.starting_palindrome()
        while palindrome.value <= self.end:
            yield palindrome
            palindrome = palindrome.next_number()

    def all_matching_multi_numbers(self):
        for i in range(2, len(str(self.end)) + 1):
            number = MultiNumber.first_multi_after(self.start, i)
            while number.value <= self.end:
                yield number
                number = number.next_number()

    @classmethod
    def parse_ranges(cls, ranges: str):
        ranges = ranges.strip().split(',')
        for r in ranges:
            yield cls.from_string(r)
        

class MultiNumber:
    def __init__(self, base_value: int, replica_count: int = 2):
        self._base_value = base_value
        str_base = str(base_value)
        self._value = int(str_base * replica_count)
        self._replica_count = replica_count

    @property
    def value(self):
        return self._value
    
    def next_number(self):
        return MultiNumber(self._base_value + 1, self._replica_count)

    def __repr__(self):
        return f'MultiNumber(value={self.value}, replica_count={self._replica_count})'

    @classmethod
    def first_multi_after(cls, number: int, replica_count: int = 2):
        str_start = str(number)
        if len(str_start) <= replica_count:
            palindrome = cls(1, replica_count)
        else:
            if len(str_start) % replica_count != 0:
                palindrome = cls(int('1' + ('0' * (len(str_start) // replica_count - 1))), replica_count)
            else:
                midpoint = len(str_start) // replica_count
                palindrome = cls(int(str_start[:midpoint]), replica_count)
        while True:
            if (len(str(palindrome.value)) % replica_count == 0) and palindrome.value >= number:
                break
            palindrome = palindrome.next_number()
        return palindrome


def solve_1(ranges: str):
    invalid_ids = set()
    for r in IdRange.parse_ranges(ranges):
        for palindrome in r.all_matching_palindromes():
            invalid_ids.add(palindrome.value)
    return sum(invalid_ids)

EXAMPLE_IN = '11-22,11-29,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'

assert solve_1(EXAMPLE_IN) == 1227775554

with open('inputs/day2.txt') as infile:
    print('Part 1 solution:', solve_1(infile.read()))

def solve_2(ranges: str):
    invalid_ids = set()
    for r in IdRange.parse_ranges(ranges):
        for palindrome in r.all_matching_multi_numbers():
            invalid_ids.add(palindrome.value)
    return sum(invalid_ids)

assert solve_2(EXAMPLE_IN) == 4174379265


with open('inputs/day2.txt') as infile:
    print('Part 2 solution:', solve_2(infile.read()))