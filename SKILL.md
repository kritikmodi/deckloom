---
name: deckloom
description: Build product decks and slide documents from code - pitch decks, investor overviews, product one-pagers, sales decks, technical overviews, brochures and conference talks - by writing content as JSON and rendering an HTML slide system to PDF or PPTX. Use when asked to create, edit, re-cut, re-brand or update any presentation or slide deck.
---

# Deckloom

Decks are content plus a design system, and they are almost never made once. The
same twelve facts get recut as an investor overview, a sales deck, a one-pager
and a technical brief, and within a month the four versions disagree with each
other.

So: keep the content in one JSON file, keep the design in one HTML file, and
render whichever deck you need. The output is a PDF at exactly PowerPoint's 16:9
page size, and a PPTX if someone needs one.

```
content.json ──► deck.html ──► headless Chrome ──► deck.pdf ──► deck.pptx
     (words)      (design)        (layout)          (share)      (optional)
```

## The one idea that matters

**Content and design never live in the same file.**

`content.json` holds the words. `deck.html` holds the slide types and the brand.
Neither knows about the other until build time. That is what makes it possible to
recut a deck for a different audience in seconds, restyle every deck at once by
editing a few CSS variables, and diff a wording change in a pull request.

If you find yourself writing copy inside the HTML, stop. Add a field to the slide
type instead.

## Where the files are

Work in the user's project, not in this folder. `scripts/`, `templates/`, `references/` and `requirements.txt` sit beside this file,
in `${CLAUDE_SKILL_DIR}`; if that shows up unexpanded, it means the folder that
holds this SKILL.md. When that folder is not the working directory, as when this
is installed as a plugin or a skill, put it in front of the paths in the
commands below:

```bash
pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt && playwright install chromium
cp ${CLAUDE_SKILL_DIR}/templates/deck.html .
cp ${CLAUDE_SKILL_DIR}/templates/content.example.json content.json
python3 ${CLAUDE_SKILL_DIR}/scripts/build.py           # -> ./out/deck.pdf
```

The scripts read and write relative to the directory they are run from, so
`content.json`, `deck.html` and `out/` stay in the project. Never write into the skill folder: a plugin
update replaces it.

## Commands

```bash
pip install -r requirements.txt && playwright install chromium

cp templates/deck.html templates/content.example.json .
mv content.example.json content.json

python3 scripts/build.py                       # -> out/deck.pdf
python3 scripts/build.py --cut investor        # a subset, same content file
python3 scripts/build.py --png                 # also one PNG per slide
python3 scripts/export_pptx.py                 # -> out/deck.pptx
```

To see the deck while writing it, open `deck.html` in a browser and reload. It
scrolls as a stack of slides on screen and paginates correctly when printed.

## Match the product's brand automatically

If the product has a codebase, do not ask the user for hex codes and do not
eyedrop a screenshot. Read the brand out of the repo:

```bash
python3 scripts/detect_brand.py ../their-product              # report
python3 scripts/detect_brand.py ../their-product --write content.json
```

It reads design token files, tailwind configs, CSS custom properties, SCSS and
Less variables, JS/TS theme objects and the web manifest, then reports the fonts
in use, the icon library from package.json, and any logo files it found.

Two things make the output trustworthy rather than merely confident:

**Build output is skipped.** A `dist/` folder is full of vendored CSS from
component libraries, and those colours are not the brand.

**The palette is checked for coherence, not just matched by name.** A repo can
define `--surface` for its light theme and `--bg` for its dark one; taking both
gives a white card on a black slide. Values that fail are replaced and the
rejection is printed, never swapped silently:

```
rejected (kept the deck coherent)
  surface #FFFFFF rejected: luma 1.00 vs bg 0.07, not the same theme
  accent #A8B4C2 rejected: saturation 0.13 is too low to read as an accent
```

Treat the result as a strong starting point. Show the user what was detected and
what was rejected, and confirm before sending the deck anywhere. If the repo has
no tokens at all, say so and ask, rather than inventing a palette.

## Slide types

Seven ship in the template. The `type` field on each slide selects one.

| Type | Use it for | Key fields |
|---|---|---|
| `title` | opening claim | `eyebrow`, `title`, `sub`, `chips` |
| `stats` | the problem, in numbers | `items[].stat` `.title` `.body` |
| `flow` | how it works, left to right | `steps[]`, optional `items[]` below |
| `features` | capability grid, up to six | `items[].tag` `.title` `.body` |
| `table` | comparison against alternatives | `columns`, `rows` |
| `quote` | a customer sentence | `quote`, `attrib` |
| `closing` | the ask | `title`, `sub`, `cta` |

Wrap a phrase in `~tildes~` to colour it with the accent, so the copy stays free
of markup. Prefix a table cell with `+` for accent or `-` for alert.

Adding a type is one function in the `TYPES` object in `deck.html`. Page sizing,
footers, numbering and print rules are handled for you.

See `references/SLIDE-TYPES.md` for what each type is good and bad at, and
`references/DESIGN.md` for the design system and how to rebrand it.

## Rules that keep decks good

**One idea per slide.** If a card needs a comma-spliced sentence, it is two
cards. If a slide needs two headlines, it is two slides.

**Numbers beat adjectives.** "2 to 8 GB of heap before the first query" survives
scrutiny; "heavyweight and slow" does not. Every number should be one a sceptic
could check, and the measurement conditions belong on the slide.

**Write for the room you are in.** An investor cut leads with the market and the
wedge; a technical cut leads with the mechanism. Same facts, different order,
which is exactly what `cuts` is for. Never maintain two files.

**The accent colour is punctuation.** One accent phrase per headline. When
everything is highlighted, nothing is.

**Comparison tables must be fair.** A table where you win every row reads as
marketing and invites the audience to find the row you left out. Include a row
you lose, or a row where it depends.

## Building a deck from scratch

1. Write `content.json` first, in plain sentences, before thinking about layout.
   If the argument does not hold as a list of sentences, no design will save it.
2. Assign a `type` to each slide. If nothing fits, the slide is probably trying
   to do two things.
3. Build, look at the PDF, and cut. First drafts are always two slides too long.
4. Define `cuts` once you know which audiences you serve.

For a longer document (a brochure or a leave-behind rather than a presented
deck), the same system works: use fewer, denser slides and expect it to be read
rather than talked over.
