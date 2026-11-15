# Network map

On request, the assistant can draw the owner's network as a still picture or a short video: a round map with the owner in the centre, three rings for closeness, and the owner's topics as sectors. There are no lines between people. Membership in a sector and a ring is the relationship — the kit does not parse who knows whom.

The layout is generic. It is not tied to any one niche. Two to four supertopics from the owner's interests (and the groups on their cards) become sectors; colours, labels, and the legend are generated from a config file. The three rings mean the same thing for every owner.

The picture at the top of [README.md](README.md) is one real example of this layout. Handles never appear on the image, only counts.

## What the picture shows

- **YOU** at the centre.
- **Three rings**, from the card `circle` field (plus a two-way exchange, or an old-crew flag, which always place someone in Close):
  - **Close** — support and close useful relationships (default circles: `support`, `friends`).
  - **Productive** — builders and quality information on shared interests (default circles: `productivity`, `work`, `learning`).
  - **Around** — everyone else: projects, signals, the rest (default circles: `development`, `horizon`).
- **Sectors** — one wedge per subgroup, grouped into 2–4 supers, laid out counter-clockwise from north. Adjacent subgroups in `topics.json` share a border. Someone who spans two topics sits on that border, in gold if the two topics belong to different supers.
- **Unsorted** people (no matching topic) form a grey rim on the outer edge.
- **Active connectors** are larger white-cored dots: not a project account, with a two-way exchange in the last 60 days.
- No handles or names. English labels only.

Rename the rings or the circle lists in `topics.json` if the owner's CONFIG uses different circle names. The meaning stays the same.

## Files

| File | What it's for |
|---|---|
| [map/render.py](map/render.py) | Draws `network-map.png` from `topics.json` + `data.json` |
| [map/build_data.py](map/build_data.py) | Reads the card folder and `topics.json`, writes anonymous `data.json` |
| [map/topics.example.json](map/topics.example.json) | A worked example (Sports, Music, Making). Copy to `topics.json` and edit |
| [map/data.example.json](map/data.example.json) | Fictional sample people, so you can render the example without a card folder |

Nothing in `map/` is an owner's real network. Real cards stay in the private base.

## How the assistant should build it

When the owner asks for a picture (or a short video) of their network:

1. **Stay read-only on X.** The map is built only from cards already in the base. Do not fetch new X data just to draw it.
2. **Write `topics.json` from the owner's interests and card groups**, not from a hard-coded niche. Use 2–4 supers, each with subgroups, in counter-clockwise order from north. Put subgroups that often overlap next to each other so they share a border. Copy [map/topics.example.json](map/topics.example.json) as the starting point, then replace the example topics with the owner's. If the owner already has a `topics.json`, update it rather than starting over.
3. **Keep the three rings.** Map the owner's `circle` values into Close / Productive / Around in the `rings` block. Defaults already understand both the kit circles (`friends`, `work`, `learning`, `horizon`) and the common aliases `support`, `productivity`, and `development`. A two-way exchange always goes to Close.
4. **Build the data and draw the still image:**

```text
python3 map/build_data.py --cards /path/to/the/base --topics map/topics.json --out map/data.json --owner @their_handle
python3 map/render.py --topics map/topics.json --data map/data.json --out network-map.png
```

5. **Show the owner the PNG.** If they also asked for a video, say so and render a short clip in the same layout (dots appearing by ring, no lines, about 15–20 seconds). The still image is the default.
6. **Privacy.** `data.json` must not contain handles. The PNG must not contain handles or personal names. Do not commit the owner's `topics.json` or `data.json` to this public kit.

To try the layout without a card folder:

```text
python3 map/render.py --topics map/topics.example.json --data map/data.example.json --out /tmp/example-map.png
```

## Requirements

- Python 3 with **Pillow** and **NumPy**.
- Fonts: Inter and Space Grotesk if they are installed; otherwise DejaVu Sans. You can override paths with `XGROK_FONT_BODY` and `XGROK_FONT_TITLE`.

## topics.json in short

- `supers`: 2–4 items. Each has a `key`, a `label`, optional `color`, and a list of `subgroups`.
- `subgroups`: `key`, `label`, optional `color`, optional `groups` (card `group` tags that map here), optional `keywords` (words in the card's "Who:" line, used only when no group tag matches).
- `unsorted`: leftover people, drawn as a grey rim.
- `rings`: labels and which `circle` values fall into Close / Productive / Around.
- Omit colours to have a hue family assigned per super and shades per subgroup.

`build_data.py` classifies a card by its `group` tags first, then by keywords on the Profile "Who:" line. A person with groups in two different supers is marked as a topic-border (gold) and is placed on the seam. Touch history is read from the English "Touch history" section (`you →` for outgoing, `@handle →` for incoming). Only two-way exchanges count; connectors need both directions dated within the last 60 days.
