# Pitfalls

## Everything prints white

`print_background` must be true, or Chrome drops every background colour and you
get black text on white pages with the layout intact. It is set in `build.py`;
if you write your own print call, do not forget it.

## The PDF is the wrong physical size

Chrome maps CSS pixels to points at 96dpi, so a 960px-wide slide becomes a
720x405pt page. That is the right aspect ratio but not the standard slide size,
and PowerPoint or Keynote will letterbox it on import.

`build.py` prints at 13.333 x 7.5in with `scale=4/3`, which lands exactly on
960x540pt. Verify after any change:

```bash
python3 -c "import pymupdf; d=pymupdf.open('out/deck.pdf'); print(d[0].rect)"
```

## Slides split across pages

Each slide must be exactly the page height and carry `page-break-after: always`.
If a slide grows past 540px, Chrome paginates it and you get a half-slide
followed by an orphan. Content is vertically centred and does not scroll, so
overflow is silent: it just gets clipped.

Check the PNGs rather than trusting the PDF page count.

## PNG export clips to nothing

Slides stack past the bottom of the viewport, so a page screenshot with a clip
rectangle fails or comes back empty. Screenshot each `.slide` element instead,
which is what `--png` does.

## The em dash and the smart quote

Copy pasted from a doc arrives full of typographic characters that may not exist
in your webfont, and render as a box. Either keep content ASCII, or verify the
font covers the range.

## Content in the template

The moment a headline is typed into `deck.html`, cuts and rebrands stop working
and you are back to maintaining parallel decks. If a slide type cannot express
something, add a field to the type rather than hardcoding the words.

## A deck that only exists as a PDF

The PDF is a build artifact. If someone edits the PPTX and sends it back, that
change is lost on the next build. Say so when you hand the file over: wording
changes go in `content.json`.
