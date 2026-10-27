#!/usr/bin/env python3
"""Build a deck: content.json + deck.html -> PDF.

The slide design lives in deck.html and never contains content. This reads
content.json, hands it to the page, and prints. Because the browser is doing
the layout, what you see on screen is exactly what lands in the PDF.

    python3 scripts/build.py                          # -> out/deck.pdf
    python3 scripts/build.py --cut investor           # a subset, same source
    python3 scripts/build.py --png                    # also write page images
"""
import argparse, json, pathlib, sys
from playwright.sync_api import sync_playwright, Error as PWError

HERE = pathlib.Path(__file__).resolve().parent.parent
W, H = 960, 540


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--content", default="content.json")
    ap.add_argument("--deck", default="deck.html")
    ap.add_argument("--out", default="out/deck.pdf")
    ap.add_argument("--cut", default="", help="named subset from content.cuts")
    ap.add_argument("--png", action="store_true", help="also write one PNG per slide")
    ap.add_argument("--scale", type=float, default=2.0, help="PNG resolution multiplier")
    a = ap.parse_args()

    content_path = HERE / a.content
    if not content_path.exists():
        sys.exit(f"no content file at {content_path}\n"
                 f"copy templates/content.example.json to {a.content} and edit it")
    content = json.loads(content_path.read_text())

    out = HERE / a.out
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb",
                                    "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H},
                        device_scale_factor=a.scale)
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append("console: " + m.text)
              if m.type in ("error", "warning") else None)
        pg.goto((HERE / a.deck).as_uri())

        try:
            n = pg.evaluate("([c, cut]) => window.__render(c, cut)", [content, a.cut])
        except PWError as e:
            b.close()
            sys.exit(f"render failed: {e}\npage errors:\n  " + "\n  ".join(errors or ["none"]))

        if not n:
            b.close()
            sys.exit(f"nothing rendered. "
                     + (f"cut '{a.cut}' matched no slides" if a.cut else "content.slides is empty"))

        for s in pg.evaluate("window.__slides"):
            print(f"  {s['i']:>2}. {s['type']:<10} {s['title']}")
        for e in errors:
            print(f"  ! {e}", file=sys.stderr)

        # print_background is what keeps the dark theme; without it every
        # slide comes out white with floating text.
        pg.emulate_media(media="print")
        # Chrome maps CSS px to pt at 96dpi, so a 960px slide would land as a
        # 720x405pt page. PowerPoint and Keynote treat 960x540pt (13.333 x 7.5in)
        # as standard 16:9, so scale up to that and these import without
        # letterboxing.
        pg.pdf(path=str(out), width="13.333in", height="7.5in", scale=4 / 3,
               print_background=True, margin={"top": "0", "bottom": "0",
                                              "left": "0", "right": "0"})
        print(f"wrote {a.out}  ({n} slides)")

        if a.png:
            png_dir = out.parent / (out.stem + "_png")
            png_dir.mkdir(exist_ok=True)
            pg.emulate_media(media="screen")
            # Screenshot each slide element. Clipping the page does not work
            # here: the slides stack past the bottom of the viewport.
            slides = pg.locator(".slide")
            for i in range(slides.count()):
                slides.nth(i).screenshot(path=str(png_dir / f"slide_{i+1:02d}.png"))
            shown = png_dir.relative_to(HERE) if png_dir.is_relative_to(HERE) else png_dir
            print(f"wrote {shown}/ ({n} images)")

        b.close()


if __name__ == "__main__":
    main()
