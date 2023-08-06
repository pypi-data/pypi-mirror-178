# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Union
import hashlib
import emoji


def tokenize(text: str, max_ngram_length: int = 1) -> List[str]:
    text = text.lower()
    parts = []
    highest_end = 0
    for emoji_part in emoji.emoji_list(text):
        parts += list(text[highest_end : emoji_part["match_start"]])
        parts.append(emoji_part["emoji"])
        highest_end = emoji_part["match_end"]
    parts += list(text[highest_end:])
    converted_text = [part for part in parts if part]

    tokens = [""]

    for char in converted_text:
        if char.isalpha() or char == "'":
            tokens[-1] += char
        elif emoji.is_emoji(char):
            tokens.append(char)
            tokens.append("")
        elif tokens[-1] != "":
            tokens.append("")

    tokens = [string for string in tokens if string]

    if max_ngram_length == 1:
        return tokens
    else:
        ngrams = []
        for ngram_length in range(1, max_ngram_length + 1):
            for index in range(len(tokens) + 1 - ngram_length):
                ngrams.append(" ".join(tokens[index : index + ngram_length]))
        return ngrams


def hash_single(token: str) -> int:
    return int.from_bytes(
        hashlib.sha256(token.encode("utf-8")).digest()[:6], "big"
    )


def hash(tokens: List[str]) -> List[int]:
    return [hash_single(token) for token in tokens]


def normalize(text: str) -> str:
    return " ".join(tokenize(text, 1))
