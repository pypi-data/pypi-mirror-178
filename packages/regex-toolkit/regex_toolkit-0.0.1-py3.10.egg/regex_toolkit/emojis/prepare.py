__all__ = []

import os

# from dataclasses import dataclass, field

# Module root directory
root_dir = os.path.dirname(os.path.abspath(__file__))

# Parent module root directory
parent_dir = os.path.dirname(root_dir)

# @dataclass
# class Emoji:
#     characters: field(default=str)
#     code_points: field(default=str)
#     type_field: field(default=str)
#     description: field(default=str)
#     comments: field(default=str)


def _codepoint_to_ord(codepoint: str) -> int:
    return int(codepoint, 16)


# def parse_emojis() -> tuple[Emoji, ...]:
def parse_emojis() -> tuple[dict[str, tuple[str, ...]], ...]:
    # emoji-sequences.txt and emoji-zwj-sequences.txt
    # from https://unicode.org/Public/emoji/14.0/
    # Format:
    #   code_point(s) ; type_field ; description # comments
    emojis = []
    for file_path in (
        os.path.join(root_dir, "emoji-zwj-sequences.txt"),
        os.path.join(root_dir, "emoji-sequences.txt"),
    ):
        with open(file_path, mode="r", encoding="utf-8") as r:
            for line in r:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Skip comments
                if line[0] == "#":
                    continue

                # Slice code points off of the line
                code_points, line = line.partition(";")[::2]
                code_points = code_points.strip()
                line = line.strip()

                # Slice type field off of the line
                type_field, line = line.partition(";")[::2]
                type_field = type_field.strip()
                line = line.strip()

                # Lastly, slice description and comments off of the line
                description, comments = line.partition("#")[::2]
                description = description.strip()
                comments = comments.strip()

                # Prepare the character representation of the emoji
                if ".." in code_points:
                    characters = "..".join(chr(_codepoint_to_ord(codepoint)) for codepoint in code_points.split(".."))
                else:
                    characters = "".join(chr(_codepoint_to_ord(codepoint)) for codepoint in code_points.split(" "))

                # Store an instance of this emoji
                emojis.append(
                    # Emoji(
                    #     characters,
                    #     code_points,
                    #     type_field,
                    #     description,
                    #     comments,
                    # )
                    {
                        "characters": characters,
                        "code_points": code_points,
                        "type_field": type_field,
                        "description": description,
                        "comments": comments,
                    }
                )

    return tuple(emojis)
