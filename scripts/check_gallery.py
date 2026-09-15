#!/usr/bin/env python3
"""Run check.py against the gallery corpus (101 anonymized templates from
three real WABAs, UTILITY and MARKETING only, deduplicated by name plus
components; authentication is not present in this capture).

Usage:
    python3 check_gallery.py

Unlike `check.py --corpus`, which runs against the calibrated 16-template
corpus and is the regression test for the rules, this script measures the
checker against data it never saw. It does not change check.py to force a
match, it only reports the real hit rate and lists where it disagrees.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import check


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "references", "gallery-corpus.json")
    with open(path, encoding="utf-8") as f:
        corpus = json.load(f)

    matches = 0
    mismatches = []
    for item in corpus:
        definition = {
            "name": item["name"],
            "category": "UTILITY",
            "allow_category_change": False,
            "components": item["components"],
        }
        reasons = check(definition, lang="en")
        predicted = "MARKETING" if reasons else "UTILITY"
        ok = predicted == item["veredito"]
        if ok:
            matches += 1
        else:
            mismatches.append((item["name"], item["veredito"], predicted, reasons))

    total = len(corpus)
    print(f"{matches}/{total} verdicts match\n")
    if mismatches:
        print("where the checker still disagrees:")
        for name, expected, got, reasons in mismatches:
            why = "; ".join(reasons) if reasons else "no rejection reason found"
            print(f"- {name}: expected={expected} got={got} ({why})")


if __name__ == "__main__":
    main()
