# SPDX-License-Identifier: GPL-3.0-or-later

import gptc.tokenizer
from gptc.exceptions import InvalidModelError
from typing import Iterable, Mapping, List, Dict, Union
import json


class Model:
    def __init__(
        self,
        weights: Dict[int, List[int]],
        names: List[str],
        max_ngram_length: int,
    ):
        self.weights = weights
        self.names = names
        self.max_ngram_length = max_ngram_length

    def serialize(self) -> bytes:
        out = b"GPTC model v4\n"
        out += (
            json.dumps(
                {
                    "names": self.names,
                    "max_ngram_length": self.max_ngram_length,
                    "has_emoji": True,
                    # Due to an oversight in development, version 3.0.0 still
                    # had the code used to make emoji support optional, even
                    # though the `emoji` library was made a hard dependency.
                    # Part of this code checked whether or not the model
                    # supports emoji; deserialization would not work in 3.0.0
                    # if the model was compiled without this field. Emoji are
                    # always supported with 3.0.0 and newer when GPTC has been
                    # installed correctly, so this value should always be True.
                    # Related: #11
                }
            ).encode("utf-8")
            + b"\n"
        )
        for word, weights in self.weights.items():
            out += word.to_bytes(6, "big") + b"".join(
                [weight.to_bytes(2, "big") for weight in weights]
            )
        return out


def deserialize(encoded_model: bytes) -> Model:
    try:
        prefix, config_json, encoded_weights = encoded_model.split(b"\n", 2)
    except ValueError:
        raise InvalidModelError()

    if prefix != b"GPTC model v4":
        raise InvalidModelError()

    try:
        config = json.loads(config_json.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise InvalidModelError()

    try:
        names = config["names"]
        max_ngram_length = config["max_ngram_length"]
    except KeyError:
        raise InvalidModelError()

    if not (
        isinstance(names, list) and isinstance(max_ngram_length, int)
    ) or not all([isinstance(name, str) for name in names]):
        raise InvalidModelError()

    weight_code_length = 6 + 2 * len(names)

    if len(encoded_weights) % weight_code_length != 0:
        raise InvalidModelError()

    weight_codes = [
        encoded_weights[x : x + weight_code_length]
        for x in range(0, len(encoded_weights), weight_code_length)
    ]

    weights = {
        int.from_bytes(code[:6], "big"): [
            int.from_bytes(value, "big")
            for value in [code[x : x + 2] for x in range(6, len(code), 2)]
        ]
        for code in weight_codes
    }

    return Model(weights, names, max_ngram_length)
