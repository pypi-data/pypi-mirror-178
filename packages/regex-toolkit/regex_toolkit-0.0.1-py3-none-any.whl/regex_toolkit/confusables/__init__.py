__all__ = [
    "confusables",
]

from .prepare import parse_confusables

# TODO: Rename the parent folder
confusables: tuple[dict[str, tuple[str, ...]], ...] = parse_confusables()
