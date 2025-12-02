from typing import NamedTuple

class IdRange(NamedTuple):
    start: int
    end: int

    @classmethod
    def from_string(cls, string):
        start, end = string.split('-')
        return cls(int(start), int(end))

    def starting_palindrome(self):
        return PalindromicNumber.first_palindrome_after(self.start)

    def all_matching_palindromes(self):
        palindrome = self.starting_palindrome()
        while palindrome.value <= self.end:
            yield palindrome
            palindrome = palindrome.next_palindrome()

    @classmethod
    def parse_ranges(cls, ranges: str):
        ranges = ranges.strip().split(',')
        for r in ranges:
            yield cls.from_string(r)
        

class PalindromicNumber:
    def __init__(self, value: int):
        self._value = value
        str_base = str(value)
        self._base_str = list(str_base)

    @property
    def left(self):
        return ''.join(self._base_str[:len(self._base_str) // 2])

    @property
    def value(self):
        return self._value
    
    def next_palindrome(self):
        return PalindromicNumber(int(str(int(self.left) + 1) * 2))

    @classmethod
    def first_palindrome_after(cls, number: int):
        str_start = str(number)
        if len(str_start) == 1:
            palindrome = PalindromicNumber(11)
        else:
            if len(str_start) % 2 == 1:
                str_start = '0' + str_start
            midpoint = len(str_start) // 2
            palindrome = cls(int(str_start[:midpoint] * 2))
        while True:
            if (len(str(palindrome.value)) % 2 == 0) and palindrome.value >= number:
                break
            palindrome = palindrome.next_palindrome()
        return palindrome

    def __repr__(self):
        return f'PalindromicNumber(value={self.value})'

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