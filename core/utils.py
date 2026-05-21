"""
Shared UI utility helpers.
"""


def format_kgs(value: float) -> str:
    """Format a float as Kyrgyz som with dot thousands separator.

    Examples:
        48000  → '48.000 с'
        1500   → '1.500 с'
        600    → '600 с'
    """
    formatted = f"{int(round(value)):,}".replace(",", ".")
    return f"{formatted} с"
