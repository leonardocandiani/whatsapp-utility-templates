#!/usr/bin/env python3
"""Check a WhatsApp template definition against what Meta reclassifies.

Usage:
    python3 check.py definition.json              # exit 0 passes, 1 fails, 2 usage
    python3 check.py definition.json --lang en     # use the English word lists
    python3 check.py --corpus                      # run the measured corpus, print the scorecard

Rules calibrated on a real WABA (see references/approved-pattern.md): the
templates that Meta approved and then silently reclassified to MARKETING fail
here, the ones that stayed UTILITY pass. references/measured-corpus.json is
the regression test for these rules, run with --corpus.

Two word lists ship side by side, Portuguese and English, selectable with
--lang (default: pt). The measured corpus is in Portuguese, so `--corpus`
always runs against the pt list, regardless of the --lang flag you pass.
"""

import json
import os
import re
import sys

# Sales language in the fixed body text, in an example, or on a button: Meta
# reads all three at approval time, and a single one of these words has
# pushed an otherwise clean template into MARKETING.
SALES_WORDS = {
    "pt": [
        r"cota[cç][aã]o", r"cota[cç][oõ]es", r"proposta", r"consultor[a]?", r"vendedor[a]?",
        r"caminh[aã]o", r"prote[cç][aã]o", r"seguro", r"plano", r"valor(es)?", r"pre[cç]o",
        r"ligar", r"liga[cç][aã]o", r"te passo", r"detalhes", r"conhecer", r"aproveit",
        r"oferta", r"promo", r"desconto", r"condi[cç][aã]o", r"vaga", r"gr[aá]tis", r"novidade",
        r"benef[ií]cio", r"vantagem", r"melhor", r"especial",
    ],
    "en": [
        r"\bquote[sd]?\b", r"\bproposal\b", r"\bconsultant\b", r"\bsales(person|rep)?\b",
        r"\btruck\b", r"\bvehicle\b", r"\bprotection\b", r"\binsurance\b", r"\bplan\b",
        r"\bprice[sd]?\b", r"\bcost[s]?\b", r"\bcall you\b", r"\bi.?ll call\b", r"\bi.?ll send\b",
        r"\bdetails\b", r"\blearn more\b", r"\btake advantage\b", r"\boffer\b", r"\bpromo\b",
        r"\bdiscount\b", r"\bspecial deal\b", r"\bslot[s]?\b", r"\bfree\b", r"\bnew\b",
        r"\bbenefit\b", r"\badvantage\b", r"\bbest\b", r"\bspecial\b",
    ],
}

# Re-engagement close: an invitation to pick the conversation back up, instead
# of a question about something already pending. "Can we keep talking here?"
# is the exact phrase that got reclassified in the case study.
REENGAGEMENT_WORDS = {
    "pt": [
        r"continuar", r"retomar", r"dar continuidade", r"seguir com", r"voltar a falar",
        r"podemos conversar", r"quero ver", r"saber mais", r"ver mais",
    ],
    "en": [
        r"\bcontinue\b", r"\bresume\b", r"\bkeep talking\b", r"\bcatch up\b",
        r"\bget back to\b", r"\bcan we talk\b", r"\bwant to see\b", r"\blearn more\b",
        r"\bsee more\b",
    ],
}

# A button that invites the reader to see or start something pushes the
# template toward MARKETING. A button that confirms something the reader
# already has ("Yes, ..."), acknowledges ("Got it"), or declines ("Not now")
# holds it in UTILITY.
BAD_BUTTON_WORDS = {
    "pt": [r"quero", r"\bver\b", r"saber", r"conhecer", r"continuar", r"ligar", r"mandar", r"mais"],
    "en": [r"\bwant\b", r"\bsee\b", r"\bknow\b", r"\blearn\b", r"\bcontinue\b", r"\bcall\b", r"\bsend\b", r"\bmore\b"],
}

# The free slot's example needs to read like a service-desk note, not a sales
# pitch. One of these words in the example is the signal that held the good
# batches in UTILITY.
PROTOCOL_ANCHOR_WORDS = {
    "pt": [r"protocolo", r"atendimento", r"solicita[cç][aã]o", r"cadastro", r"agendamento", r"registro"],
    "en": [r"\bticket\b", r"\bcase\b", r"\brequest\b", r"\baccount\b", r"\bappointment\b", r"\brecord\b"],
}

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _find(patterns, text):
    lowered = text.lower()
    for pattern in patterns:
        match = re.search(pattern, lowered)
        if match:
            return match.group(0)
    return None


def _check_contract(definition: dict, components: list, text: str) -> list:
    """Meta/house contract fields that have nothing to do with wording."""
    reasons = []
    if definition.get("category") != "UTILITY":
        reasons.append("category must be UTILITY")
    if definition.get("allow_category_change") is not False:
        reasons.append("allow_category_change must be false")
    if not NAME_PATTERN.match(definition.get("name", "")):
        reasons.append("name must be lowercase snake_case starting with a letter")
    if any(c.get("type", "").upper() == "HEADER" for c in components):
        reasons.append("header does not belong in the utility pattern")
    if EMOJI.search(text):
        reasons.append("emoji in the body")
    return reasons


def _check_wording(fixed_text: str, lang: str) -> list:
    """The two closes that read as marketing to Meta: sales words and re-engagement."""
    reasons = []
    found = _find(SALES_WORDS[lang], fixed_text)
    if found:
        reasons.append(f"sales word in the fixed text: {found}")
    found = _find(REENGAGEMENT_WORDS[lang], fixed_text)
    if found:
        reasons.append(f"re-engagement close: {found}")
    return reasons


def _check_slot_format(text: str, numbers: list) -> list:
    reasons = []
    if numbers != list(range(1, len(numbers) + 1)):
        reasons.append("variables out of sequence")
    if re.search(r"\{\{\d+\}\}\s*$", text.strip()):
        reasons.append("body ends in a variable (INVALID_FORMAT)")
    return reasons


def _check_example_values(example_values: list, expected_count: int, lang: str) -> list:
    reasons = []
    if len(example_values) != expected_count:
        reasons.append("example does not cover every variable")

    for value in example_values:
        found = _find(SALES_WORDS[lang], value)
        if found:
            reasons.append(f"sales word in the example: {found}")

    free_values = [v for v in example_values if len(v.split()) >= 5]
    if free_values and not any(_find(PROTOCOL_ANCHOR_WORDS[lang], v) for v in free_values):
        reasons.append("free slot example has no ticket/case anchor")
    return reasons


def _check_variables(text: str, body: dict, lang: str) -> list:
    """Slot numbering, format, and the free slot's example."""
    slots = re.findall(r"\{\{(\d+)\}\}", text)
    if not slots:
        return []

    numbers = [int(s) for s in slots]
    examples = (body.get("example") or {}).get("body_text") or [[]]
    example_values = examples[0] if examples else []

    return (
        _check_slot_format(text, numbers)
        + _check_example_values(example_values, len(numbers), lang)
    )


def _check_buttons(components: list, lang: str) -> list:
    buttons = next((c for c in components if c.get("type", "").upper() == "BUTTONS"), None)
    if not buttons:
        return []

    reasons = []
    for button in buttons.get("buttons", []):
        label = button.get("text", "")
        if len(label) > 20:
            reasons.append(f"button over 20 characters: {label}")
        found = _find(BAD_BUTTON_WORDS[lang], label)
        if found:
            reasons.append(f"button invites the reader to see or start something: {label}")
    return reasons


def check(definition: dict, lang: str = "pt") -> list:
    """Return the list of rejection reasons. Empty means it passes."""
    if lang not in SALES_WORDS:
        raise ValueError(f"unknown lang: {lang}")

    components = definition.get("components") or []
    body = next((c for c in components if c.get("type", "").upper() == "BODY"), None)
    if body is None:
        return ["missing BODY component"]
    text = body.get("text", "")
    fixed_text = re.sub(r"\{\{\d+\}\}", " ", text)

    return (
        _check_contract(definition, components, text)
        + _check_wording(fixed_text, lang)
        + _check_variables(text, body, lang)
        + _check_buttons(components, lang)
    )


def run_corpus() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "references", "measured-corpus.json")
    with open(path, encoding="utf-8") as f:
        corpus = json.load(f)
    errors = 0
    for item in corpus:
        definition = {
            "name": item["name"],
            "category": "UTILITY",
            "allow_category_change": False,
            "components": item["components"],
        }
        reasons = check(definition, lang="pt")
        predicted = "MARKETING" if reasons else "UTILITY"
        ok = predicted == item["verdict"]
        errors += 0 if ok else 1
        suffix = f" ({'; '.join(reasons)})" if reasons else ""
        print(f"{'ok  ' if ok else 'FAIL'} {item['name']}: expected={item['verdict']} got={predicted}{suffix}")
    print(f"\n{len(corpus) - errors}/{len(corpus)} verdicts match")
    return 0 if errors == 0 else 1


def main() -> None:
    args = sys.argv[1:]
    lang = "pt"
    if "--lang" in args:
        idx = args.index("--lang")
        try:
            lang = args[idx + 1]
        except IndexError:
            print("usage: --lang expects a value (pt|en)", file=sys.stderr)
            sys.exit(2)
        del args[idx:idx + 2]

    usage = "usage: python3 check.py <definition.json> [--lang pt|en] | --corpus"
    if args == ["--corpus"]:
        sys.exit(run_corpus())
    if args in (["--help"], ["-h"]):
        print(usage)
        sys.exit(0)
    if len(args) != 1 or args[0].startswith("-"):
        print(usage, file=sys.stderr)
        sys.exit(2)

    with open(args[0], encoding="utf-8") as f:
        definition = json.load(f)
    reasons = check(definition, lang=lang)
    if reasons:
        print("rejected: this template tends to become MARKETING")
        for reason in reasons:
            print(f"- {reason}")
        sys.exit(1)
    print("passes: within the pattern that stayed UTILITY")


if __name__ == "__main__":
    main()
