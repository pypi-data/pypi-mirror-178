__all__ = []

import os

# from dataclasses import dataclass, field

# Module root directory
root_dir = os.path.dirname(os.path.abspath(__file__))

# Parent module root directory
parent_dir = os.path.dirname(root_dir)


def print_blocks(blocks):
    msg = ""
    for block in blocks:
        if msg:
            msg += "\n"

        msg += "<------- START BLOCK --------"
        if isinstance(block, tuple):
            for block_part in block:
                # if isinstance(block_part, tuple):
                #     for chunk in block_part:
                #         msg += f"\n    {chunk}"
                # else:
                msg += f"\n    {block_part}"
        else:
            msg += f"\n    {block}"

        msg += "\n-------- END BLOCK --------"

    print(msg)


def _char_from_instructs(instructs: str) -> str:
    return instructs.removeprefix("(\u200E ").removesuffix(" \u200E)")


def parse_confusables() -> dict[str, tuple[str, ...]]:
    # confusablesSummary.txt
    # from https://www.unicode.org/Public/security/latest/
    with open(
        os.path.join(root_dir, "confusablesSummary.txt"),
        mode="r",
        encoding="utf-8",
    ) as r:
        raw = r.read()

    # Preprocess
    #     Expects no surrounding newlines
    raw = raw.strip("\n")
    #     Remove header and footer
    raw = raw.partition("#\n\n")[2]
    raw = raw.rpartition("\n\n#")[0]

    # Split into each character's block
    blocks = tuple(raw.split("\n\n#"))
    print_blocks(blocks)

    confusables = {}
    for block in blocks:
        if not block:
            # Skip empty lines
            continue

        # Separate parts of the single block
        rows = tuple(block.split("\n"))

        # Skip first row that is a comment for users
        src_row, confus_rows = rows[1], rows[2:]
        assert src_row.startswith("\t") and all((row.startswith("←\t") for row in confus_rows))

        # Clean row separation sequences
        src_row = src_row.removeprefix("\t")
        confus_rows = tuple(map(lambda row: row.removeprefix("←\t"), confus_rows))

        # Extract source char from instructions in first group
        src_char = _char_from_instructs(src_row.partition("\t")[0])
        # print(f"Source char: {src_char}")

        # Init Key
        if src_char not in confusables:
            confusables[src_char] = []
            # print(f"Initialized key: {src_char}")

        # Store corresponding confusable chars
        for row in confus_rows:
            # Extract the confusable character (from instructions in first group)
            confus_char = _char_from_instructs(row.partition("\t")[0])
            if confus_char not in confusables[src_char]:
                confusables[src_char].append(confus_char)
                # print(f'"{confus_char}" is confusable for "{src_char}"')

        # Convert all lists to tuples
        for col in list(confusables):
            confusables[col] = tuple(confusables[col])

    return confusables
