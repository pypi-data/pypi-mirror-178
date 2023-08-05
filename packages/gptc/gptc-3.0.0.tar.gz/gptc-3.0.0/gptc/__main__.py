#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import json
import sys
import gptc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="General Purpose Text Classifier", prog="gptc"
    )
    subparsers = parser.add_subparsers(dest="subparser_name", required=True)

    compile_parser = subparsers.add_parser(
        "compile", help="compile a raw model"
    )
    compile_parser.add_argument("model", help="raw model to compile")
    compile_parser.add_argument(
        "--max-ngram-length",
        "-n",
        help="maximum ngram length",
        type=int,
        default=1,
    )
    compile_parser.add_argument(
        "--min-count",
        "-c",
        help="minimum use count for word/ngram to be included in model",
        type=int,
        default=1,
    )

    classify_parser = subparsers.add_parser("classify", help="classify text")
    classify_parser.add_argument("model", help="compiled model to use")
    classify_parser.add_argument(
        "--max-ngram-length",
        "-n",
        help="maximum ngram length",
        type=int,
        default=1,
    )
    group = classify_parser.add_mutually_exclusive_group()
    group.add_argument(
        "-j",
        "--json",
        help="output confidence dict as JSON (default)",
        action="store_true",
    )
    group.add_argument(
        "-c",
        "--category",
        help="output most likely category or `None`",
        action="store_true",
    )

    pack_parser = subparsers.add_parser(
        "pack", help="pack a model from a directory"
    )
    pack_parser.add_argument("model", help="directory containing model")

    args = parser.parse_args()

    if args.subparser_name == "compile":
        with open(args.model, "r") as f:
            model = json.load(f)

        sys.stdout.buffer.write(
            gptc.compile(
                model, args.max_ngram_length, args.min_count
            ).serialize()
        )
    elif args.subparser_name == "classify":
        with open(args.model, "rb") as f:
            model = gptc.deserialize(f.read())

        classifier = gptc.Classifier(model, args.max_ngram_length)

        if sys.stdin.isatty():
            text = input("Text to analyse: ")
        else:
            text = sys.stdin.read()

        if args.category:
            print(classifier.classify(text))
        else:
            print(json.dumps(classifier.confidence(text)))
    else:
        print(json.dumps(gptc.pack(args.model, True)[0]))


if __name__ == "__main__":
    main()
