# The design system

## Tokens

Everything visual is a CSS custom property at the top of `deck.html`. Rebranding
a whole deck library means editing this block, or overriding it per deck from
`content.json` under `theme`.

| Token | Default | Role |
|---|---|---|
| `--bg` | `#0B0F1F` | slide background |
| `--surface` | `#151D31` | cards, steps, chips |
| `--line` | `rgba(255,255,255,.08)` | hairline borders |
| `--ink` | `#FFFFFF` | primary text |
| `--ink-dim` | 66% white | body copy |
| `--ink-faint` | 38% white | footers, captions |
| `--accent` | `#2DD4BF` | the one thing you want looked at |
| `--alert` | `#EC4899` | the cost of the status quo |

Per-deck override, no template edit needed:

```json
"theme": { "accent": "#7C5CFF", "bg": "#0E0B1A" }
```

## Why dark

Dark decks photograph badly in bright rooms and cost a fortune to print. They
look excellent on a screen share, in a PDF sent by email, and on a projector in a
dimmed room, which is where product decks are actually consumed. If your deck
will be printed or presented in daylight, invert the tokens: `--bg` near-white,
`--ink` near-black, and drop the `wash` gradient.

## The two-colour rule

One accent and one alert is the whole palette. The alert colour marks what the
status quo costs; the accent marks what you do about it. A slide that uses both
is making an argument. A slide that uses neither is context.

Resist adding a third. Every additional colour has to earn a meaning, and readers
can hold about two.

## Type scale

| Element | Size | Weight |
|---|---|---|
| eyebrow | 12px | 700, `.22em` tracking, uppercase |
| `h1` (title slides) | 52px | 800 |
| `h2` (content slides) | 38px | 800 |
| sub | 16px | 400 |
| card title | 15px | 700 |
| card body | 12.5px | 400 |
| footer | 10px | uppercase |

The jump from 38px to 15px is deliberate. Mid-sized text is where decks go to
die: it is too big to skim and too small to land. Either it is a headline or it
is detail.

## Layout

Slides are 960x540 CSS px with a 72px margin, which is 16:9 and maps to
PowerPoint's 13.333 x 7.5in page. Content is vertically centred, so a short
slide and a dense slide both sit correctly without hand-nudging.

The `wash` element is a soft radial gradient in a corner, used only on title,
quote and closing slides. It signals "this is a punctuation slide" without a
different background colour.

## Fonts

The template asks for Inter and falls back to the system UI face. A deck that
must render identically on someone else's machine should either embed the font
with `@font-face` and a base64 `src`, or stick to a system stack. PDFs embed
whatever the browser used at build time, so the PDF is safe either way; it is the
HTML that varies.
