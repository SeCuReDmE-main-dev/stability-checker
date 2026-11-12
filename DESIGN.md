# DESIGN.md

Design rules for the stability-checker interface (`docs/index.html`, served by GitHub Pages).

## Audience

Quebec travellers aged 60 to 80 and the adult children who buy insurance with them. Many read on a tablet, some with low vision.

## Principles

1. **One question, one answer.** The page asks four things (days since the change, age, condition, kind of change) and answers with a list of plans: open or closed.
2. **Readable first.** Base text 18 px, line height 1.6, contrast at least 4.5:1 (WCAG 2.2 AA). No text in images.
3. **Every answer shows its source.** Each plan row links to the policy wording it comes from.
4. **No advice tone.** The disclaimer sits above the result, not in the footer.
5. **Bilingual.** French and English labels side by side; no language switch to hunt for.
6. **Works offline after load.** One static HTML file, no build step, no tracking, no cookies.

## Brand

The page follows the look of the We The Flywheel *Find the Gap* page it was built for: purple `#7C3AED` band, Dosis headings, square inputs and cards with 2 px borders. The We The Flywheel logo is linked from wetheflywheel.com, not copied into this repository, and is used only to name the hackathon. Project marks are `assets/logo.svg` and `assets/mascot.svg`.

## Tokens

| Token | Light | Dark |
|---|---|---|
| `--bg` | `#ffffff` | `#111418` |
| `--text` | `#1b1f24` | `#eef1f4` |
| `--muted` | `#57606a` | `#a4adb6` |
| `--ok` | `#1a7f37` | `#3fb950` |
| `--no` | `#b42318` | `#f47067` |
| `--brand` | `#7c3aed` | `#a78bfa` |
| `--border` | `#d0d7de` | `#30363d` |

Spacing scale: 4, 8, 16, 24, 32 px. Radius: 8 px. Font: system UI stack.

## Components

- **Form:** four labelled inputs, large touch targets (44 px minimum).
- **Result row:** status pill (OPEN / CLOSED), insurer and plan, required days, reason, source link.
- **Summary line:** "N of 10 plans open" in large type at the top of the result.

## Data contract

The page reads `data/clauses.json` (same file as the Python checker) and applies the same rules as `src/stability_checker/checker.py`. A test in `tests/` keeps both in line with the 60-day example.
