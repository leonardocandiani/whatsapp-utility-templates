<!-- readme-padrao:header -->
<!-- Banner -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1a1a2e,100:00d9ff&height=200&section=header&text=whatsapp-utility-templates&fontSize=54&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Get%20WhatsApp%20templates%20approved%20as%20UTILITY%20by%20Meta%2C%20and%20keep%20them%20there&descAlignY=58&descSize=16" alt="whatsapp-utility-templates" width="100%" />
</div>

<!-- Typing -->
<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=21&duration=2800&pause=900&color=00d9ff&center=true&vCenter=true&width=840&lines=WhatsApp+templates+approved+as+UTILITY%2C+and+kept+there;Checker+calibrated+on+16+real+verdicts%2C+16+of+16+reproduced;Skeleton+for+Meta%2C+sentence+for+the+reader%3A+two+layers;Python+stdlib+only%2C+works+as+a+Claude+Code+skill" alt="WhatsApp templates approved as UTILITY, and kept there" />
</div>

<div align="center">

  <p><strong>Write, check, submit and track WhatsApp Cloud API templates that Meta approves as UTILITY.</strong></p>

  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-00d9ff?style=for-the-badge" alt="License: MIT" /></a>
    <a href="https://docs.claude.com/en/docs/claude-code"><img src="https://img.shields.io/badge/Made%20for-Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Made for: Claude Code" /></a>
    <img src="https://img.shields.io/badge/python-3.8%2B%20stdlib%20only-1a1a2e?style=for-the-badge&logo=python&logoColor=white" alt="python: 3.8+ stdlib only" />
    <img src="https://img.shields.io/badge/corpus-16%20of%2016%20verdicts-00d9ff?style=for-the-badge" alt="corpus: 16 of 16 verdicts" />
    <a href="https://github.com/leonardocandiani/whatsapp-utility-templates/pulls"><img src="https://img.shields.io/badge/PRs-welcome-1a1a2e?style=for-the-badge" alt="PRs: welcome" /></a>
  </p>

  <p>
    <a href="#why-this-exists">Why this exists</a> •
    <a href="#what-is-inside">What is inside</a> •
    <a href="#install">Install</a> •
    <a href="#use">Use</a> •
    <a href="#the-two-layers">The two layers</a> •
    <a href="#license">License</a>
  </p>
</div>

<br>

> **whatsapp-utility-templates** is the difference between a template that opens conversations for months and one that Meta silently moves to MARKETING 25 minutes after approving it: an anchor test, a five part anatomy, a checker that rejects what tends to fall, and a button pair whose click actually lands somewhere.

> Not affiliated with or endorsed by Meta or Anthropic. "WhatsApp" is a Meta trademark; "Claude" and "Claude Code" are Anthropic trademarks.

## What it is

```yaml
product: Claude Code skill plus scripts for WhatsApp Cloud API message templates in the UTILITY category
anchor:  a template talks about a request the reader already has; anything that invites them to start something is MARKETING
anatomy: name and speaker · anchor line · one wide slot with a protocol-style example · closing question · two quick replies
checker: scripts/check.py rejects body, examples and button labels that tend to fall; --corpus replays 16 measured verdicts
buttons: one accept, one decline, both answering the skeleton's question; payload by index so the webhook can route the click
after:   one template per WABA · fail-closed preflight reads the live category before every send
install: git clone into ~/.claude/skills · Python 3.8+, stdlib only
license: MIT
```

<!-- /readme-padrao:header -->

A skill for Claude Code (and any other agent that reads a `SKILL.md`) that teaches how to write, check, submit and track WhatsApp Cloud API message templates so they get approved by Meta as UTILITY and stay there.

## Why this exists

Outside the 24 hour window, only an approved template can open a conversation on WhatsApp. UTILITY templates are cheaper than MARKETING and need no marketing opt-in, but Meta reclassifies an approved UTILITY template to MARKETING the moment the text, the slot examples or the button labels read like a sales pitch. When that happens the name is burned, the template does not come back, and the WABA carries the history.

This repository distills what was measured on a real WABA in September 2026: 33 templates approved and rejected, one batch of four reclassified in 25 minutes, and the three skeletons that were approved right after and never moved. The rules are calibrated against a 16 template corpus, and `scripts/check.py --corpus` reproduces all 16 verdicts.

## What is inside

| Path | What it is |
|---|---|
| `SKILL.md` | The method: the anchor test (utility versus marketing), the anatomy that passes, Meta's parameter rules and the stricter house rules, naming, submission and tracking, what to do after approval |
| `references/approved-pattern.md` | The anonymized catalog of real templates, approved and rejected, each paired with the reason |
| `references/button-pairs.md` | Exactly two quick-reply buttons, one accept and one decline that answer the skeleton's own question, plus the payload contract so the click lands somewhere |
| `references/measured-corpus.json` | The 16 template corpus the checker is calibrated on |
| `scripts/check.py` | Rejects a definition that tends to become MARKETING (exit 1 with reasons); `--corpus` reruns the calibration; `--lang pt|en` picks the word list |
| `scripts/submit.py` | Runs the checker and, only if it passes, submits the definition to a WABA |
| `scripts/status.py` | Reads the live status and category of a template by name |
| `examples/skeleton-followup.json` | A complete definition in the submit format that passes the checker |

## Install

As a Claude Code skill, clone into your skills folder:

```bash
git clone https://github.com/leonardocandiani/whatsapp-utility-templates ~/.claude/skills/whatsapp-utility-templates
```

The scripts need Python 3.8 or newer and nothing outside the standard library.

## Use

Check a definition before it goes anywhere near Meta:

```bash
python3 scripts/check.py examples/skeleton-followup.json
python3 scripts/check.py --corpus
```

Submit and track, with the token and the WABA id taken from the environment (never from a file, never printed):

```bash
export META_TOKEN=...   # system user access token with whatsapp_business_management
export META_WABA=...    # numeric WABA id
python3 scripts/submit.py examples/skeleton-followup.json
python3 scripts/status.py utility_followup_v1
```

The definition format is the one `submit.py` expects: name, language, category, body, footer, slots, protocol-style examples for every slot, and the two buttons. `SKILL.md` section 5 documents every field.

## The two layers

What made the pattern work was separating what Meta approves from what the reader receives. The skeleton that goes to Meta is minimal and protocol-like: name, who is speaking, "about your open request", a wide slot whose example reads like a support desk, a closing question about the pending item. The sentence the operator writes at send time is the real message, and it goes through its own ruler in code, never through Meta's review. `SKILL.md` section 6 covers the ruler and the fail-closed preflight that checks the live category before every send.

## License

MIT. See `LICENSE`.

<!-- readme-padrao:footer -->
<br>

---

<div align="center">
  <p><strong>Built by <a href="https://github.com/leonardocandiani">Leonardo Candiani</a></strong> · More projects at <a href="https://github.com/leonardocandiani?tab=repositories">github.com/leonardocandiani</a></p>
  <p>Leonardo Candiani builds AI agents that talk, decide and close deals. Cofounder of SixQuasar, operating Proteauto, SegSmart and IACall end to end.</p>
  <a href="https://leonardocandiani.com.br">
    <img src="https://img.shields.io/badge/-Website-0d1117?style=for-the-badge&logo=safari&logoColor=00d9ff" alt="Website" />
  </a>
  <a href="https://github.com/leonardocandiani">
    <img src="https://img.shields.io/badge/-GitHub-0d1117?style=for-the-badge&logo=github&logoColor=00d9ff" alt="GitHub" />
  </a>
  <a href="https://instagram.com/leonardocandiani">
    <img src="https://img.shields.io/badge/-Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
  </a>
  <a href="https://youtube.com/@oleonardocandiani">
    <img src="https://img.shields.io/badge/-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" />
  </a>
</div>

<br>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00d9ff,50:1a1a2e,100:0d1117&height=120&section=footer&text=Thanks%20for%20stopping%20by&fontSize=18&fontColor=ffffff&fontAlignY=72" alt="Thanks for stopping by" width="100%" />
</div>
<!-- /readme-padrao:footer -->
