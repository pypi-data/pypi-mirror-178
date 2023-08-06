from functools import cache

import os


"""Module Root Directory"""
root_dir = os.path.dirname(os.path.abspath(__file__))

"""Parent Module Root Directory"""
parent_dir = os.path.dirname(root_dir)

# TODO: Need to account for confusables whose confusing value is more than one char
#           User may want to provide expected chars as a list/tuple? or iterate the confusing chars and check that way


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


# class ConfusablesMap:
#     def __init__(self) -> None:
#         self._confusable_map = {}
#
#     def __setattribute__(self, __name: str, __value: Any) -> None:
#         if "__name" == "_confusable_map":
#             raise AttributeError("confusable_map is a reserved name")
#
#         self._confusable_map[__name] = __value
#
#     def __getattribute__(self, __name: str) -> Any:
#         return self._confusable_map[__name]


class Confusables:
    # def update(
    #     url="https://www.unicode.org/Public/security/latest/confusablesSummary.txt"
    # ):
    #     pass

    @staticmethod
    def _char_from_instructs(instructs: str) -> str:
        """Parse Character Surrounded by Left-to-Right Marks"

        "(‎ !! ‎)" -> "!!"

        Args:
            instructs (str): Instructions expressing a character.

        Returns:
            str: Character expressed by instructions.
        """
        assert instructs.startswith("(\u200E ") and instructs.endswith(" \u200E)")
        return instructs.removeprefix("(\u200E ").removesuffix(" \u200E)")

    def _clean_row(row: str, is_source: bool) -> str:
        if is_source:
            assert row.startswith("\t")
            # Remove tab seperating rows
            # "	(‎ !! ‎)	0021 0021	 EXCLAMATION MARK, EXCLAMATION MARK"
            # to
            # "(‎ !! ‎)	0021 0021	 EXCLAMATION MARK, EXCLAMATION MARK"
            row = row.removeprefix("\t")
        else:
            assert row.startswith("←\t")
            # "←	(‎ ‼ ‎)	203C	 DOUBLE EXCLAMATION MARK"
            # to
            # "(‎ ‼ ‎)	203C	 DOUBLE EXCLAMATION MARK"
            row = row.removeprefix("←\t")

        # Remove everything after the instructions
        # "(‎ !! ‎)	0021 0021	 EXCLAMATION MARK, EXCLAMATION MARK"
        # to
        # "(‎ !! ‎)"
        row = row.partition("\t")[0]
        # Extract source character from instructions
        # "(‎ !! ‎)" -> "!!"
        return Confusables._char_from_instructs(row)

    def confusables(confusables_summary_path: str) -> dict[str, set[str]]:
        with open(confusables_summary_path, mode="r", encoding="utf-8") as r:
            raw = r.read()

        # Preprocess
        # # - Expects no surrounding newlines, but remove anyways
        # raw = raw.strip("\n")
        # - Expects no surrounding newlines
        assert not raw.startswith("\n") and not raw.endswith("\n")
        # - Remove header
        raw = raw.partition("#\n\n")[2]
        # - Remove footer
        raw = raw.rpartition("\n\n#")[0]

        # Split into each character's block
        blocks = tuple(filter(bool, raw.split("\n\n#")))
        print_blocks(blocks)

        # Build the confusables mapping
        confusables = {}
        for block in blocks:
            # Separate parts of the single block
            # """#	!!	‼
            # 	(‎ !! ‎)	0021 0021	 EXCLAMATION MARK, EXCLAMATION MARK
            # ←	(‎ ‼ ‎)	203C	 DOUBLE EXCLAMATION MARK"""
            # to
            # ["#	!!	‼",
            #  "	(‎ !! ‎)	0021 0021	 EXCLAMATION MARK, EXCLAMATION MARK",
            #  "←	(‎ ‼ ‎)	203C	 DOUBLE EXCLAMATION MARK"]
            rows = block.split("\n")
            # Remove comment for user in first row
            # ["#	!!	‼",
            #  "	(‎ !! ‎)	0021 0021	 EXCLAMATION MARK, EXCLAMATION MARK",
            #  "←	(‎ ‼ ‎)	203C	 DOUBLE EXCLAMATION MARK"]
            # to
            # ["	(‎ !! ‎)	0021 0021	 EXCLAMATION MARK, EXCLAMATION MARK",
            #  "←	(‎ ‼ ‎)	203C	 DOUBLE EXCLAMATION MARK"]
            rows.pop(0)

            # Extract source character
            src_char: str = Confusables._clean_row(rows[0])

            # Should not be existing entries
            assert src_char not in confusables

            # Store corresponding confusable chars
            confusables[src_char] = set(map(Confusables._clean_row, rows[1:]))
        return confusables

    def make_confusable_dict(text: str) -> dict[str, tuple[str, ...]]:
        # Non-repeating list of all chars present
        known_chars = set(text)

        # Prepare empty result dict
        result = {char: set() for char in known_chars}

        for known_char in known_chars:
            # Skip if never confusable
            if known_char not in Confusables.confusables:
                continue

            # Add if each known character is in the confusables set of any other known chars
            # Add if character will not be used in a different context
            known_confusables = Confusables.confusables[known_char]
            for known_confus in known_confusables.difference(known_char):
                # 2. Char is does not conflict with another confusable
                is_conflicting = False
                for known_char in (
                    known_chars
                    # Excluding current char
                    .difference({known_char})
                    # Only chars in confusables
                    .difference(set(Confusables.confusables))
                ):
                    # Flag if correcting conflicts with confusables of 'known_char'
                    if known_confus in Confusables.confusables[known_char]:
                        is_conflicting = True
                        break

                if is_conflicting:
                    continue

                # Store final confusable char
                result[known_char].add(known_confus)

        # Convert all lists to tuples
        for col in list(result):
            result[col] = tuple(result[col])

        # Convert all lists to tuples
        return result

