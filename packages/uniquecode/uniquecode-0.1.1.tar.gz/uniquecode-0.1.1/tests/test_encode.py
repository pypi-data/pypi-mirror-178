from src.uniquecode import Uniquecode
import string, pytest

loop = range(1000)

@pytest.mark.parametrize("x", loop)
def test_encode_hex(x):
    unq = Uniquecode(randomize=False, shift_increment=False, pattern=string.digits + "abcdef", limit_size=0, prefix='0x')
    assert unq.encode(x) == hex(x)

@pytest.mark.parametrize('x', loop)
def test_encode_decode(x):
    unq = Uniquecode()
    assert unq.decode(unq.encode(x)) == x