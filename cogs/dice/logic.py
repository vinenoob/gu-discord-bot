# dice.py

import random
from typing import Tuple, List

class DiceParseError(Exception):
    """Raised when the notation can't be parsed as XdY."""


def parse_dice_notation(notation: str) -> Tuple[int, int]:
    """
    Parse a string of the form '<quantity>d<sides>' (case-insensitive)
    and return (quantity, sides). Raises DiceParseError if invalid.
    """
    notation = notation.strip().lower()
    if 'd' not in notation:
        raise DiceParseError(f"Invalid format (no 'd'): {notation!r}")
    qty_str, sides_str = notation.split('d', 1)
    try:
        qty = int(qty_str)
        sides = int(sides_str)
    except ValueError:
        raise DiceParseError(f"Non-integer values in: {notation!r}")
    if qty <= 0 or sides <= 0:
        raise DiceParseError(f"Quantity and sides must be positive: {notation!r}")
    return qty, sides


def roll_dice(qty: int, sides: int) -> List[int]:
    """
    Roll `qty` dice, each from 1..`sides` (inclusive),
    and return the list of individual roll results.
    """
    return [random.randint(1, sides) for _ in range(qty)]


def roll_and_sum(notation: str, max_qty: int = 10_000) -> Tuple[List[int], int]:
    """
    Convenience function: parse the notation, enforce max_qty,
    roll the dice, and return (rolls, total).
    Raises:
      - DiceParseError if the notation is malformed.
      - ValueError if qty > max_qty.
    """
    qty, sides = parse_dice_notation(notation)
    if qty > max_qty:
        raise ValueError(f"Too many dice: {qty} > {max_qty}")
    rolls = roll_dice(qty, sides)
    return rolls, sum(rolls)
