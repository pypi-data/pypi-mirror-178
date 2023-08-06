import string, random
from dataclasses import dataclass, field


@dataclass
class Uniquecode:

    pattern: str = '' + string.digits + string.ascii_lowercase
    prefix: str = ''
    suffix: str = ''
    _pattern: str = field(init=False, repr=False)
    ln: int = field(init=False, repr=False)
    randomize: bool = True
    limit_size: int = 6
    shift_increment: bool = True
    count_limit: int = field(init=False)
    _size: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._pattern = list(self.pattern)
        self.ln = len(self.pattern)
        if self.randomize:
            random.shuffle(self._pattern)
        if self.limit_size:
            self._size = self.limit_size - len(self.prefix) - len(self.suffix)
            self.count_limit = self.ln ** self._size - 1
        else:
            self.count_limit = None

    def _encode_calc(self, n:int, shift:int) -> tuple:
        r, n = n % self.ln, int(n / self.ln)
        r += shift
        if r >= self.ln:
            r -= self.ln
        return r, n

    def _decode_calc(self, chr:str, pos:int, shift:int) -> int:
        n = self._pattern.index(chr)
        if shift:
            n = n-shift if n > 0 else self.ln - n - shift
        return n * self.ln ** pos

    def encode(self, n: int) -> str:
        if self.count_limit and n > self.count_limit:
            return 'out of range'
        output = '' if n>0 else self._pattern[0]
        shift = 0
        while n>0:
            r, n = self._encode_calc(n, shift)
            output = self._pattern[r] + output
            if self.shift_increment:
                shift += 1
        return self.prefix + output + self.suffix

    def decode(self, codename: str) -> int:
        lp, ls = len(self.prefix), len(self.suffix)
        end = -ls if ls else len(codename)
        prefix, code_string, suffix = codename[0:lp], codename[lp:end], codename[end:]
        result = 0
        if prefix != self.prefix or suffix != self.suffix:
            print('not valid codename')
            return result
        clist = list(code_string)
        pos = 0
        shift = 0
        while clist:
            result += self._decode_calc(clist.pop(), pos, shift)
            pos += 1
            if self.shift_increment:
                shift += 1
        return result
