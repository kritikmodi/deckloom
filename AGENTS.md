# AGENTS.md

Instructions for any coding agent working in this repository.

Deckloom builds **product decks from code**: pitch decks, investor overviews,
one-pagers, sales decks, technical overviews, brochures. Content is JSON, the
design is one HTML file, headless Chrome renders the PDF.

`SKILL.md` is the full brief and is worth reading before you start. It is written
in Anthropic's Claude Skill format but it is plain Markdown and applies to any
agent.

## The one rule that matters

**Content and design never live in the same file.**

`content.json` holds the words. `deck.html` holds the slide types and brand
tokens. If a slide type cannot express something, add a field to the type. Never
type a headline into the template: it breaks cuts and rebrands, and puts you back
to maintaining parallel decks.

## Commands

```bash
# setup (once)
pip install -r requirements.txt && playwright install chromium

# build
cp templates/deck.html templates/content.example.json .
mv content.example.json content.json
python3 scripts/build.py                       # -> out/deck.pdf
python3 scripts/build.py --cut investor        # a subset of the same content
python3 scripts/build.py --png                 # also one PNG per slide
python3 scripts/export_pptx.py                 # -> out/deck.pptx
```

Every script supports `--help`.

## Match the product's brand from its code

Do not ask for hex codes if a codebase is available:

```bash
python3 scripts/detect_brand.py ../their-product --write content.json
```

Reads tokens, tailwind, CSS variables, JS theme objects and the manifest; also
reports fonts, the icon library and logo files. It skips build output, and
rejects colours that do not cohere (a light-theme surface on a dark background,
a grey "primary" that cannot work as an accent), printing what it rejected.

Show the user the detected palette and the rejections before building.

## Where things live

| Path | Purpose |
|---|---|
| `SKILL.md` | full brief: pipeline, slide types, rules for good decks |
| `references/DESIGN.md` | tokens, type scale, rebranding |
| `references/SLIDE-TYPES.md` | what each slide type is for and how it fails |
| `references/PITFALLS.md` | **read before debugging** |
| `scripts/build.py` | the build |
| `templates/deck.html` | the slide system |

## Conventions

- **Write `content.json` before thinking about layout.** If the argument does not
  hold as a list of plain sentences, no design will rescue it.
- **One idea per slide.** A card needing a comma-spliced sentence is two cards.
- **Numbers, not adjectives.** Every figure should be one a sceptic could check,
  with the measurement conditions on the slide.
- **The accent colour is punctuation.** One accent phrase per headline.
- **Comparison tables must be fair.** Winning every row reads as marketing.
- **Verify the output, do not assume.** Check the page size is 960x540pt, that
  the page corner is slide background rather than white paper, and look at the
  PNGs; slide overflow is clipped silently rather than erroring.

```bash
python3 -c "import pymupdf; d=pymupdf.open('out/deck.pdf'); print(len(d), d[0].rect, d[0].get_pixmap().pixel(2, 2))"
```

## Do not commit

- `out/`, and any generated `.pdf` or `.pptx`
- `/deck.html` and `/content.json` at the repo root: those are a user's working
  copies of the templates. The templates themselves live in `templates/`.

## Style

Plain ASCII in docs and code comments. No em dashes.
