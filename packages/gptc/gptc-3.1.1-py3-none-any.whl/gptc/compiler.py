# SPDX-License-Identifier: GPL-3.0-or-later

import gptc.tokenizer
import gptc.model
from typing import Iterable, Mapping, List, Dict, Union


def compile(
    raw_model: Iterable[Mapping[str, str]],
    max_ngram_length: int = 1,
    min_count: int = 1,
) -> gptc.model.Model:
    """Compile a raw model.

    Parameters
    ----------
    raw_model : list of dict
        A raw GPTC model.

    max_ngram_length : int
        Maximum ngram lenght to compile with.

    Returns
    -------
    dict
        A compiled GPTC model.

    """

    categories: Dict[str, List[int]] = {}

    for portion in raw_model:
        text = gptc.tokenizer.hash(
            gptc.tokenizer.tokenize(portion["text"], max_ngram_length)
        )
        category = portion["category"]
        try:
            categories[category] += text
        except KeyError:
            categories[category] = text

    word_counts: Dict[int, Dict[str, int]] = {}

    names = list(categories.keys())

    for category, text in categories.items():
        for word in text:
            if word in word_counts:
                try:
                    word_counts[word][category] += 1
                except KeyError:
                    word_counts[word][category] = 1
            else:
                word_counts[word] = {category: 1}

    category_lengths = {
        category: len(text) for category, text in categories.items()
    }

    word_weights: Dict[int, Dict[str, float]] = {
        word: {
            category: value / category_lengths[category]
            for category, value in values.items()
        }
        for word, values in word_counts.items()
        if sum(values.values()) >= min_count
    }

    model: Dict[int, List[int]] = {}
    for word, weights in word_weights.items():
        total = sum(weights.values())
        new_weights: List[int] = []
        for category in names:
            new_weights.append(
                round((weights.get(category, 0) / total) * 65535)
            )
        model[word] = new_weights

    return gptc.model.Model(model, names, max_ngram_length)
