__all__ = [
    "emojis",
]

from .prepare import parse_emojis

# TODO: Rename the parent folder
emojis: dict[str, tuple[str, ...]] = parse_emojis()
