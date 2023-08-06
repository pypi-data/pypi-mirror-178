from enum import Enum, auto


class ENDIANNESS(Enum):
    UNKLNOWN = 0
    BIG      = auto()
    LITTLE   = auto()


def get_effective_length_in_bytes(value):
    bit_length = value.bit_length()
    length_bytes = int(bit_length/8)
    if(bit_length%8 > 0):
        length_bytes += 1
    if (length:=int(length_bytes)) == 0:
        return 1
    else:
        return length

def is_bit_set(value, n, endiannes = ENDIANNESS.BIG):
    if endiannes == ENDIANNESS.BIG:
        return ((value >> n & 1) != 0)
    elif endiannes == ENDIANNESS.LITTLE:
        return ((value << n & 1) != 0)
    else:
        raise ValueError("Endianness is not properly set - not able to decite which bit to return")


def get_bit(value, n, endiannes = ENDIANNESS.BIG):
    if value == None:
        raise ValueError(f"Value can not be None")

    size = get_effective_length_in_bytes(value)

    if n == None or n>(size*8-1) or n<0:
        raise ValueError(f"Wrong bit number passed: {n} which is out of curen variable's size range: 0-{size*8}")

    if endiannes == ENDIANNESS.BIG:
        return (value >> n & 1)
    elif endiannes == ENDIANNESS.LITTLE:
        return (value >> (size*8-1)-n & 1)
    else:
        raise ValueError("Endianness is not properly set - not able to decite which bit to return")


def set_bit(value, n, endiannes = ENDIANNESS.BIG):
    if value == None:
        raise ValueError(f"Value can not be None")

    size = get_effective_length_in_bytes(value)
    if n == None or n<0:
        raise ValueError(f"Wrong bit number passed: {n}")

    if endiannes == ENDIANNESS.BIG:
        return value | (1 << n)
    elif endiannes == ENDIANNESS.LITTLE:
        return value | (1 << (size*8-1)-n)
    else:
        raise ValueError("Endianness is not properly set - not able to decide which bit to return")


def clear_bit(value, n, endiannes = ENDIANNESS.BIG):
    if value == None:
        raise ValueError(f"Value can not be None")

    size = get_effective_length_in_bytes(value)

    if n == None or n>(size*8-1) or n<0:
        raise ValueError(f"Wrong bit number passed: {n}")

    if endiannes == ENDIANNESS.BIG:
        return value & ~(1 << n)
    elif endiannes == ENDIANNESS.LITTLE:
        return value & ~(1 << (size*8-1)-n)
    else:
        raise ValueError("Endianness is not properly set - not able to decide which bit to return")


def get_bit_range_as_int(value, start, end, endiannes = ENDIANNESS.BIG):
    if value == None:
        raise ValueError(f"Value can not be None")

    size = get_effective_length_in_bytes(value)

    if start == None or start>(size*8-1) or start < 0:
        raise ValueError(f"Wrong bit number passed: {start}")
    if end == None or end>(size*8) or end < 1:
        raise ValueError(f"Wrong bit number passed: {end}")

    if start >= end:
        AssertionError(f"'end' sall be bigger than 'start', condition {start} >= {end} is not satisfied")

    value_byte = value.to_bytes(length = 1, byteorder = "big")

    mask = 0x00
    if endiannes == ENDIANNESS.BIG:
        for num in range(start, end):
            mask = mask | (1 << num)
    else:
        for num in range((size*8)-end, (size*8)-start):
            mask = mask | (1 << num)

    if endiannes == ENDIANNESS.BIG:
        return (int.from_bytes(value_byte, byteorder = "big") & mask) >> start
    else:
        return (int.from_bytes(value_byte, byteorder = "little") & mask) >> 8-start


def set_bit_range_from_int(target_byte, pos, value, endiannes = ENDIANNESS.BIG):
    if target_byte == None:
        raise ValueError(f"Value can not be None")

    size = get_effective_length_in_bytes(target_byte)
    value_size_in_bits = value.bit_length()

    if pos == None or pos>(size*8-1) or pos < 0:
        raise ValueError(f"Wrong pos passed: {pos} - unable to set bits in a target of size {size*8}")

    if pos+value_size_in_bits >= (size*8):
        AssertionError(f"'end' sall be bigger than 'start', condition {pos+value_size_in_bits} >= {size*8} is not satisfied")

    value_byte = target_byte.to_bytes(length = 1, byteorder = "big")

    mask = 0x00
    if endiannes == ENDIANNESS.BIG:
        value = value << pos
    else:
        value = value << (size*8)-(pos+value_size_in_bits)

    if endiannes == ENDIANNESS.BIG:
        return int.from_bytes(value_byte, byteorder = "big") | value
    else:
        return int.from_bytes(value_byte, byteorder = "little") | value