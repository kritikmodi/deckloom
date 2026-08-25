# Slide types

What each one is for, and the failure mode it invites.

## `title`

The opening claim. One sentence a stranger could repeat afterwards.

```json
{ "type": "title", "eyebrow": "Product name",
  "title": "All your data.<br>~One SQL engine.~",
  "sub": "One sentence of what and for whom.",
  "chips": [{ "tag": "01", "label": "Proof point" }] }
```

Fails when the headline is a category rather than a claim. "A modern data
platform" says nothing; "Query 55 sources with one statement" says everything.
Chips are optional and should be checkable facts, not adjectives.

## `stats`

Three cards, each a number and what it costs. This is the problem slide.

Numbers render in the alert colour by default because this type usually
describes the status quo. Set `"good": true` on an item to flip it to accent, or
`"highlight": true` to outline the card.

Fails when the numbers are unsourced or suspiciously round. "10x faster" invites
"than what, measured how?" Put the conditions in the body text.

## `flow`

Left-to-right steps with arrows, optionally with stat panels underneath. Use it
for the mechanism: what goes in, what you do, what comes out.

```json
{ "type": "flow", "steps": [{ "title": "Your query", "body": "one statement" }],
  "items": [{ "stat": "0.8%", "body": "overhead versus querying directly" }] }
```

Four steps is the ceiling. Five is a process diagram and belongs in an appendix.
Mark the step that is you with `"highlight": true`.

## `features`

Two-column grid, up to six capabilities. The "what it does" slide.

Fails by becoming a feature list nobody reads. Six is the maximum a viewer takes
in at a glance; if you have twelve, you have two slides or, more likely, six
features and six details.

## `table`

Comparison against alternatives. Prefix a cell with `+` for accent, `-` for
alert.

Fails when you win every row. Reviewers scan for the row you omitted, and a
single honest "it depends" row buys more credibility than three ticks.

## `quote`

One customer sentence, large. Works because it is the only slide where someone
other than you is talking.

Fails when the quote is a testimonial rather than a problem statement. "They're
great to work with" persuades nobody. "We had four people maintaining ETL nobody
trusted" makes a prospect recognise themselves.

## `closing`

The ask. Specific beats polite: "Book a technical deep dive" over "Get in touch".

## Adding a type

One function in `TYPES` in `deck.html`, taking `(slideEl, data)`:

```js
timeline(s, d){
  if (d.eyebrow) s.appendChild(el('div','eyebrow', d.eyebrow));
  s.appendChild(el('h2','', acc(d.title)));
  // ...build your layout from d
}
```

Footers, numbering, page sizing and print rules are applied for you. Use the
`acc()` helper on any field that should support `~accent~` marks.
