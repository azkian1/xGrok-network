"""Render network-map.png from data.json + topics.json.

Generic: the renderer does not hard-code any owner's interests.
Supertopics, subgroups, colours and labels come from topics.json (2-4 supers,
laid out counter-clockwise from north). If a colour is omitted, a hue family
is assigned per super and shades per subgroup.

The three rings Close / Productive / Around are fixed CRM meaning, from the
card `circle` field (plus old-crew / two-way flags for Close).

Privacy: anonymous dots only; no handles or names. No edges — membership in a
sector and ring is the relationship; we do not parse who knows whom.
Static image only.
"""
import json, math, os, sys, colorsys
from collections import Counter, defaultdict
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, S = 1920, 1080, 2
HERE = os.path.dirname(os.path.abspath(__file__))

def _pick(*paths):
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None

FI = _pick(
    os.environ.get('XGROK_FONT_BODY'),
    '/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf',
    '/usr/share/fonts/truetype/inter/Inter-VariableFont_opsz,wght.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
)
FS = _pick(
    os.environ.get('XGROK_FONT_TITLE'),
    '/usr/share/fonts/truetype/sand-box/google/Space Grotesk/SpaceGrotesk-VariableFont_wght.ttf',
    '/usr/share/fonts/truetype/space-grotesk/SpaceGrotesk-VariableFont_wght.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    FI,
)
def _arg(flag, default):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default

def load_inputs():
    """Load topics + data. Copy topics.example.json / data.example.json if needed."""
    topics_path = _arg('--topics', os.path.join(HERE, 'topics.json'))
    data_path = _arg('--data', os.path.join(HERE, 'data.json'))
    if not os.path.isfile(topics_path):
        example = os.path.join(HERE, 'topics.example.json')
        if os.path.isfile(example):
            topics_path = example
        else:
            raise SystemExit('No topics.json found. Copy topics.example.json to topics.json and edit it.')
    if not os.path.isfile(data_path):
        example = os.path.join(HERE, 'data.example.json')
        if os.path.isfile(example):
            data_path = example
        else:
            raise SystemExit('No data.json found. Run build_data.py on your card folder, or copy data.example.json.')
    return json.load(open(data_path)), json.load(open(topics_path))

import sys
D, CFG = load_inputs()

_fc = {}


def font(path, size, wght):
    k = (path, size, wght)
    if k not in _fc:
        if not path:
            f = ImageFont.load_default()
            _fc[k] = f
            return f
        f = ImageFont.truetype(path, int(size * S))
        try:
            vals = []
            for a in f.get_variation_axes():
                nm = a['name'].decode() if isinstance(a['name'], bytes) else a['name']
                if nm.lower().startswith('weight'):
                    vals.append(wght)
                elif nm.lower().startswith('optical'):
                    vals.append(min(max(28, a['minimum']), a['maximum']))
                else:
                    vals.append(a['default'])
            f.set_variation_by_axes(vals)
        except Exception:
            pass
        _fc[k] = f
    return _fc[k]


def tup(c):
    return tuple(int(x) for x in c)

def mix(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))

# Auto palette if a super/subgroup has no colour: one hue family per super.
AUTO_HUES = [0.12, 0.55, 0.33, 0.78, 0.04, 0.66]

WHITE = (240, 244, 255)
MUTED = (140, 150, 175)
GOLD = tup(CFG.get('bridge_color') or [255, 214, 110])
MINT = tup(CFG.get('old_crew_color') or [90, 240, 170])
UNS = CFG.get('unsorted') or {'key': 'other', 'label': 'Unsorted', 'color': [125, 138, 165]}
UNS_KEY = UNS['key']
UNS_COL = tup(UNS.get('color') or [125, 138, 165])

supers_cfg = CFG['supers']
assert 1 <= len(supers_cfg) <= 4, 'topics.json must list 1-4 supers'

for si, sup in enumerate(supers_cfg):
    hue = AUTO_HUES[si % len(AUTO_HUES)]
    if not sup.get('color'):
        r, g, b = colorsys.hsv_to_rgb(hue, 0.55, 0.82)
        sup['color'] = [int(r * 255), int(g * 255), int(b * 255)]
    nsub = max(1, len(sup['subgroups']))
    for j, sg in enumerate(sup['subgroups']):
        if not sg.get('color'):
            lit = 0.95 - 0.18 * (j / max(nsub - 1, 1))
            sat = 0.55 + 0.25 * (j % 2)
            r, g, b = colorsys.hsv_to_rgb(hue, sat, lit)
            sg['color'] = [int(r * 255), int(g * 255), int(b * 255)]

COL = {UNS_KEY: UNS_COL}
SUPER_OF = {UNS_KEY: None}
SUPER_COL = {}
LABEL = {UNS_KEY: UNS.get('label') or 'Unsorted'}
for sup in supers_cfg:
    SUPER_COL[sup['key']] = tup(sup['color'])
    for sg in sup['subgroups']:
        COL[sg['key']] = tup(sg['color'])
        SUPER_OF[sg['key']] = sup['key']
        LABEL[sg['key']] = sg['label']

nodes = D['nodes']
total = D['totals']['cards']
pri_count = Counter(n['primary'] for n in nodes)


# --- rings (fixed CRM meaning, not owner-specific) -------------------------
# Close:      configured close circles, or old crew, or a two-way exchange
# Productive: configured productive circles
# Around:     everyone else
DEFAULT_RING_CIRCLES = {
    'close': ['support', 'friends'],
    'productive': ['productivity', 'work', 'learning'],
    'around': ['development', 'horizon'],
}

def _ring_circles(name):
    entry = (CFG.get('rings') or {}).get(name) or {}
    return [c.strip().lower() for c in entry.get('circles') or DEFAULT_RING_CIRCLES[name]]

def ring_of(n):
    if n.get('old_crew') or n.get('two_way'):
        return 'close'
    c = (n.get('circle') or '').strip().lower()
    if c in _ring_circles('close'):
        return 'close'
    if c in _ring_circles('productive'):
        return 'productive'
    return 'around'

for n in nodes:
    n['ring'] = ring_of(n)

def _ring_label(name, default):
    entry = (CFG.get('rings') or {}).get(name) or {}
    return entry.get('label') or default

RING_ORDER = [
    ('close', _ring_label('close', 'Close')),
    ('productive', _ring_label('productive', 'Productive')),
    ('around', _ring_label('around', 'Around')),
]
RING_COUNT = Counter(n['ring'] for n in nodes)

# --- disc geometry (y-up angles: 0=east, 90=north) -------------------------
CX, CY = 690.0, 575.0
R_MAX = 355.0
RINGS = {
    'close':      (58.0, 125.0),
    'productive': (140.0, 232.0),
    'around':     (246.0, 322.0),
}
R_UNS = (330.0, 354.0)
GUIDES = [125.0, 232.0, 322.0]

rng = np.random.default_rng(11)
GA = math.pi * (3 - math.sqrt(5))
TWO_PI = 2 * math.pi


def polar(ang, r):
    return (CX + r * math.cos(ang), CY - r * math.sin(ang))


def wrap(a):
    a = a % TWO_PI
    return a if a >= 0 else a + TWO_PI


def ang_diff(a, b):
    """Smallest signed difference a-b in (-π, π]."""
    return (a - b + math.pi) % TWO_PI - math.pi


def unwrap_near(ang, target):
    k = round((target - ang) / TWO_PI)
    return ang + k * TWO_PI


# Equal angular share per super, CCW from north (π/2).
# Within a super, subgroups share the arc in list order, proportional to size,
# with a minimum wedge so a small group stays readable.
n_sup = len(supers_cfg)
SUPER_SPAN = TWO_PI / n_sup
SECTOR = {}          # key -> (lo, hi) unwrapped radians
SUPER_ARC = {}       # super key -> (lo, hi)
SUPER_SEAMS = []     # (angle, key_a, key_b) at the end of key_a
cursor = math.pi / 2
MIN_FRAC = 0.16      # minimum share of a super's arc per subgroup

for sup in supers_cfg:
    keys = [sg['key'] for sg in sup['subgroups']]
    weights = np.array([max(pri_count.get(k, 0), 1) for k in keys], dtype=np.float64)
    raw = weights / weights.sum()
    raw = np.maximum(raw, MIN_FRAC)
    raw /= raw.sum()
    start = cursor
    acc = 0.0
    for k, w in zip(keys, raw):
        lo = cursor + acc * SUPER_SPAN
        hi = cursor + (acc + w) * SUPER_SPAN
        SECTOR[k] = (lo, hi)
        acc += w
    SUPER_ARC[sup['key']] = (start, cursor + SUPER_SPAN)
    nxt = supers_cfg[(supers_cfg.index(sup) + 1) % n_sup]
    SUPER_SEAMS.append((cursor + SUPER_SPAN, sup['key'], nxt['key']))
    cursor += SUPER_SPAN


def mid_ang(lo, hi):
    return (lo + hi) / 2.0


def sectors_adjacent(a, b):
    lo_a, hi_a = SECTOR[a]
    lo_b, hi_b = SECTOR[b]
    for x, y in ((hi_a, lo_b), (hi_b, lo_a)):
        if abs(ang_diff(x, y)) < math.radians(2.8):
            return True
    return False


def shared_border(a, b):
    lo_a, hi_a = SECTOR[a]
    lo_b, hi_b = SECTOR[b]
    cands = []
    for x, y in ((hi_a, lo_b), (hi_b, lo_a)):
        if abs(ang_diff(x, y)) < math.radians(2.8):
            cands.append(x)
    return cands[0] if cands else mid_ang(*SECTOR[a])


def nearest_super_seam(home_super, other_super, home_mid):
    seams = [s for s in SUPER_SEAMS if set(s[1:]) == {home_super, other_super}]
    if not seams:
        seams = SUPER_SEAMS
    return min(seams, key=lambda s: abs(ang_diff(s[0], home_mid)))[0]


def border_for(n):
    """Cross-super people sit on the seam toward their other topic. Intra-super
    multi-tags stay in their primary sector — being in the same super is the link.
    """
    if not n.get('cross_bridge'):
        return None
    home = n.get('primary') if n.get('primary') in SECTOR else None
    home_super = SUPER_OF.get(home)
    others = []
    for t in list(n.get('span') or []) + list(n.get('bridge_to') or []):
        if t in SECTOR and SUPER_OF.get(t) and SUPER_OF.get(t) != home_super and t not in others:
            others.append(t)
    if not home or not others:
        return None
    for t in others:
        if sectors_adjacent(home, t):
            return shared_border(home, t), (home, t)
    other_super = SUPER_OF[others[0]]
    ang = nearest_super_seam(home_super, other_super, mid_ang(*SECTOR[home]))
    return ang, (home, others[0])


def liveliness(n):
    if n.get('connector'):
        return 3
    if n.get('two_way'):
        return 2
    if n.get('warm'):
        return 1
    return 0


def node_style(n):
    if n.get('connector'):
        return 'connector', 4.8
    if n.get('cross_bridge'):
        return 'bridge', 3.3
    if n.get('old_crew') or n.get('past_crew'):
        return 'crew', 3.0
    if liveliness(n) >= 2:
        return 'twoway', 3.5
    if liveliness(n) == 1:
        return 'warm', 3.0
    if n.get('primary') == UNS_KEY:
        return 'unsorted', 2.7
    if n.get('dormant') or n.get('quarantine'):
        return 'faint', 2.1
    return 'plain', 2.55


for n in nodes:
    n['_border'] = border_for(n)


# --- pack dots in (ring × sector) cells, no overlaps -----------------------
def pack_annulus(mem, r0, r1, a0, a1, min_d=8.5):
    """Fill an annular sector with a jittered, staggered lattice — not concentric shells."""
    n = len(mem)
    if n == 0:
        return
    span = a1 - a0
    full = span >= TWO_PI - 1e-6
    if span <= 1e-6:
        mid = (a0 + a1) / 2.0
        span = math.radians(8)
        a0, a1 = mid - span / 2, mid + span / 2
        full = False
    mem = sorted(mem, key=lambda n: (-liveliness(n),
                                     n.get('dormant') or n.get('quarantine') or False,
                                     n['id']))
    # How many staggered radial rows fit in this band?
    band = max(r1 - r0, min_d)
    n_rows = max(1, int(round(band / (min_d * 1.05))))
    if n == 1:
        n_rows = 1
    # People per row, proportional to the row's radius (more on the outside)
    row_r = [r0 + (i + 0.5) / n_rows * band for i in range(n_rows)]
    weights = np.array(row_r, dtype=np.float64)
    raw = weights / weights.sum() * n
    counts = np.maximum(np.floor(raw), 0).astype(int)
    # spread the remainder so we place exactly n points
    while counts.sum() < n:
        frac = raw - counts
        counts[int(np.argmax(frac))] += 1
    while counts.sum() > n:
        counts[int(np.argmax(counts))] -= 1
    # If the sector is a thin rim or a thin wedge, prefer one well-filled row
    mid_r = (r0 + r1) / 2.0
    arc = mid_r * span
    if band < min_d * 1.6 or (not full and arc / max(n, 1) > band * 1.8 and n <= 8):
        n_rows = 1
        counts = np.array([n])
        row_r = [mid_r]

    pts = []
    for ri, (rr, k) in enumerate(zip(row_r, counts)):
        if k <= 0:
            continue
        m = 0.0 if full else min(0.08, span * 0.08)
        usable = TWO_PI if full else max(span - 2 * m, 1e-3)
        offset = (0.5 * usable / k) if (ri % 2) else 0.0
        for j in range(k):
            if full:
                ang = (j / k) * TWO_PI + offset
            else:
                ang = a0 + m + offset + (j + 0.5) * (usable / k)
            # organic jitter — enough to break the row, not enough to overlap
            ang += float(rng.normal(0, 0.22 * (usable / max(k, 1))))
            r = float(np.clip(rr + rng.normal(0, min_d * 0.32), r0 + 1.8, r1 - 1.8))
            pts.append([r * math.cos(ang), r * math.sin(ang)])

    P = np.array(pts, dtype=np.float64)
    # Light repulsion so dots do not sit on top of each other, but do not
    # crystallise into concentric shells (keep iterations low, then re-jitter).
    for _ in range(14):
        if len(P) < 2:
            break
        d = P[:, None, :] - P[None, :, :]
        dist = np.sqrt((d * d).sum(-1) + 1e-6)
        hit = (dist < min_d) & (dist > 0)
        if not hit.any():
            break
        w = np.where(hit, (min_d - dist) / dist, 0.0)
        P += 0.40 * (w[:, :, None] * d).sum(1)
        r = np.sqrt((P * P).sum(1))
        ang = np.arctan2(P[:, 1], P[:, 0])
        r = np.clip(r, r0 + 1.5, r1 - 1.5)
        if not full:
            mid = (a0 + a1) / 2.0
            eps = min(0.02, span * 0.04)
            for i in range(len(P)):
                a = unwrap_near(ang[i], mid)
                a = min(max(a, a0 + eps), a1 - eps)
                ang[i] = a
        P[:, 0] = r * np.cos(ang)
        P[:, 1] = r * np.sin(ang)
    # Tiny frozen noise so a lattice does not read as dashed rings
    if len(P):
        P += rng.normal(0, min_d * 0.12, P.shape)
        r = np.clip(np.sqrt((P * P).sum(1)), r0 + 1.2, r1 - 1.2)
        ang = np.arctan2(P[:, 1], P[:, 0])
        if not full:
            mid = (a0 + a1) / 2.0
            eps = min(0.015, span * 0.03)
            for i in range(len(P)):
                a = unwrap_near(ang[i], mid)
                ang[i] = min(max(a, a0 + eps), a1 - eps)
        P[:, 0] = r * np.cos(ang)
        P[:, 1] = r * np.sin(ang)
    for node, (x, y) in zip(mem, P):
        node['xy'] = (CX + float(x), CY - float(y))
        node['_r0'], node['_r1'] = r0, r1
        node['_a0'], node['_a1'] = (None, None) if full else (a0, a1)


# 1) single-home people, by ring
cells = defaultdict(list)
borders = defaultdict(list)
close_unsorted = []
for n in nodes:
    if n.get('_border'):
        borders[(n['ring'], n['_border'][0])].append(n)
        continue
    if n['primary'] == UNS_KEY or n['primary'] not in SECTOR:
        if n['ring'] == 'around':
            cells[('around', '__unsorted__')].append(n)
        else:
            close_unsorted.append(n)  # Close/Productive but untagged
        continue
    cells[(n['ring'], n['primary'])].append(n)

for (ring, topic), mem in cells.items():
    if topic == '__unsorted__':
        pack_annulus(mem, *R_UNS, 0.0, TWO_PI, min_d=9.2)
        continue
    pack_annulus(mem, *RINGS[ring], *SECTOR[topic], min_d=8.8)

# Close/Productive unsorted: their ring, all around (grey)
by_ring = defaultdict(list)
for n in close_unsorted:
    by_ring[n['ring']].append(n)
for ring, mem in by_ring.items():
    pack_annulus(mem, *RINGS[ring], 0.0, TWO_PI, min_d=9.0)

# 2) cross-super people: same ring, stacked along the shared seam
for (ring, ang0), mem in borders.items():
    pack_annulus(mem, *RINGS[ring],
                 ang0 - math.radians(11.0), ang0 + math.radians(11.0), min_d=9.0)

# leftover safety
for n in nodes:
    if 'xy' not in n:
        r0, r1 = RINGS[n['ring']]
        n['xy'] = polar(float(rng.uniform(0, TWO_PI)), (r0 + r1) / 2)
        n['_r0'], n['_r1'] = r0, r1
        n['_a0'], n['_a1'] = None, None

# light global separation, staying inside each node's cell
P = np.array([[n['xy'][0] - CX, CY - n['xy'][1]] for n in nodes], dtype=np.float64)
for _ in range(8):
    d = P[:, None, :] - P[None, :, :]
    dist = np.sqrt((d * d).sum(-1) + 1e-6)
    min_d = 8.4
    hit = (dist < min_d) & (dist > 0)
    if not hit.any():
        break
    w = np.where(hit, (min_d - dist) / dist, 0.0)
    P += 0.35 * (w[:, :, None] * d).sum(1)
    for i, n in enumerate(nodes):
        r0, r1 = n.get('_r0', RINGS[n['ring']][0]), n.get('_r1', RINGS[n['ring']][1])
        r = math.hypot(P[i, 0], P[i, 1])
        ang = math.atan2(P[i, 1], P[i, 0])
        r = min(max(r, r0 + 1.2), r1 - 1.2)
        a0, a1 = n.get('_a0'), n.get('_a1')
        if a0 is not None:
            mid = (a0 + a1) / 2.0
            a = unwrap_near(ang, mid)
            a = min(max(a, a0 + 0.015), a1 - 0.015)
            ang = a
        P[i, 0] = r * math.cos(ang)
        P[i, 1] = r * math.sin(ang)
for n, (x, y) in zip(nodes, P):
    n['xy'] = (CX + float(x), CY - float(y))


# --- background ------------------------------------------------------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
dist = np.sqrt(((xx - CX) / W) ** 2 + ((yy - CY) / H) ** 2)
BG = np.array([11, 13, 20], np.float32) * (1 - np.clip(dist * 0.9, 0, 1))[..., None] + np.array([7, 8, 12], np.float32)
BG = BG + np.random.default_rng(3).uniform(-1.2, 1.2, (H, W, 1)).astype(np.float32)


def northmost_inward(lo, hi):
    """Angle inside (lo, hi) closest to north, nudged off a seam."""
    mid = (lo + hi) / 2.0
    # candidate norths: π/2 + 2π k
    best = mid
    best_d = 1e9
    k0 = int(math.floor((lo - math.pi / 2) / TWO_PI)) - 1
    for k in range(k0, k0 + 4):
        north = math.pi / 2 + k * TWO_PI
        if lo <= north <= hi:
            return north + (0.18 * (hi - lo) if abs(north - lo) < 1e-6
                            else -0.18 * (hi - lo) if abs(north - hi) < 1e-6
                            else 0.0)
        d = min(abs(north - lo), abs(north - hi))
        if d < best_d:
            best_d = d
            best = lo + 0.18 * (hi - lo) if abs(north - lo) <= abs(north - hi) else hi - 0.18 * (hi - lo)
    return best


def render(draw_people=True):
    G = 2
    glow = Image.new('RGB', (W // G, H // G))
    gd = ImageDraw.Draw(glow, 'RGBA')

    def gc(xy, r, col, a):
        if a <= 0:
            return
        x, y, r = xy[0] / G, xy[1] / G, r / G
        gd.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(255 * min(a, 1)),))

    # One weak shared wash for the whole disc, plus a hint of each super
    gc((CX, CY), R_MAX * 0.95, (40, 50, 70), .11)
    for si, sup in enumerate(supers_cfg):
        mid = math.pi / 2 + (si + 0.5) * SUPER_SPAN
        px, py = polar(mid, R_MAX * 0.48)
        gc((px, py), R_MAX * 0.58, tup(sup['color']), .07)
    crew = [n for n in nodes if n.get('past_crew') or n.get('old_crew')]
    if crew:
        mx = sum(n['xy'][0] for n in crew) / len(crew)
        my = sum(n['xy'][1] for n in crew) / len(crew)
        gc((mx, my), 36, MINT, .07)
    for n in (nodes if draw_people else []):
        kind, _ = node_style(n)
        col = GOLD if n.get('cross_bridge') else COL.get(n['primary'], UNS_COL)
        xy = n['xy']
        if kind == 'connector':
            gc(xy, 14, WHITE, .48)
            gc(xy, 8, col, .36)
        elif kind == 'bridge' or n.get('cross_bridge'):
            gc(xy, 9, GOLD, .42)
        elif kind == 'crew':
            gc(xy, 7, MINT, .16)
        elif kind == 'unsorted':
            gc(xy, 7, mix(UNS_COL, WHITE, .2), .16)
        elif kind == 'faint':
            gc(xy, 5, col, .10)
        else:
            gc(xy, 6.5, col, .20)
    gc((CX, CY), 30, (160, 200, 255), .48)

    glow = glow.filter(ImageFilter.GaussianBlur(12)).resize((W, H), Image.BILINEAR)
    im = Image.fromarray(np.clip(BG + np.asarray(glow, np.float32) * 0.85, 0, 255).astype(np.uint8))
    im = im.resize((W * S, H * S), Image.BILINEAR)
    d = ImageDraw.Draw(im, 'RGBA')

    def circ(xy, r, col, a=1.0, outline=None, ow=1.0):
        x, y, rr = xy[0] * S, xy[1] * S, r * S
        d.ellipse((x - rr, y - rr, x + rr, y + rr),
                  fill=(col + (int(255 * a),)) if col else None,
                  outline=(outline + (int(255 * a),)) if outline else None,
                  width=int(ow * S) if outline else 0)

    def text(xy, s, f, fill, anchor='la', a=1.0):
        if a > .01:
            d.text((xy[0] * S, xy[1] * S), s, font=f,
                   fill=fill + (int(255 * min(a, 1)),), anchor=anchor)

    def scrim(cx, cy, w, h, pad=7, radius=7):
        d.rounded_rectangle(((cx - w / 2 - pad) * S, (cy - h / 2 - pad) * S,
                             (cx + w / 2 + pad) * S, (cy + h / 2 + pad) * S),
                            radius=radius * S, fill=(8, 12, 22, 215))

    # Very faint concentric ring guides — not a hard outline of the disc
    for r in GUIDES:
        bbox = ((CX - r) * S, (CY - r) * S, (CX + r) * S, (CY + r) * S)
        d.ellipse(bbox, outline=(180, 190, 210, 30), width=max(1, int(1.1 * S)))

    # Nodes only. No lines.
    for n in (nodes if draw_people else []):
        xy = n['xy']
        col = GOLD if n.get('cross_bridge') else COL.get(n['primary'], UNS_COL)
        fade = n.get('dormant') or n.get('quarantine')
        a = .50 if fade else .96
        if n.get('primary') == UNS_KEY:
            col = mix(UNS_COL, WHITE, .22)
            a = .58 if fade else .92
        kind, rad = node_style(n)
        if kind == 'connector':
            circ(xy, rad, (255, 255, 255), a)
            circ(xy, rad + 2.5, None, a, outline=col, ow=1.5)
        elif kind == 'bridge' or n.get('cross_bridge'):
            circ(xy, rad, GOLD, a)
            circ(xy, rad + 1.6, None, .8, outline=mix(GOLD, WHITE, .3), ow=0.9)
        elif kind == 'crew':
            circ(xy, rad, mix(col, MINT, .25), a)
            circ(xy, rad + 1.5, None, .55, outline=MINT, ow=0.85)
        elif kind == 'twoway':
            circ(xy, rad, mix(col, WHITE, .2), a)
        else:
            circ(xy, rad, col, a)

    # YOU — exact centre
    circ((CX, CY), 15, (235, 245, 255), 1)
    circ((CX, CY), 20, None, .65, outline=(150, 200, 255), ow=1.6)
    text((CX, CY + 1), 'YOU', font(FS, 13, 700), (10, 16, 30), 'mm')

    # Ring labels along a quiet bearing (just west of north), with a tiny scrim
    ring_lab_ang = math.radians(102)
    for key, lab in RING_ORDER:
        r0, r1 = RINGS[key]
        lx, ly = polar(ring_lab_ang, (r0 + r1) / 2)
        f = font(FS, 13, 600)
        bb = d.textbbox((0, 0), lab, font=f, anchor='mm')
        scrim(lx, ly, (bb[2] - bb[0]) / S, (bb[3] - bb[1]) / S, pad=5, radius=5)
        text((lx, ly), lab, f, (200, 208, 222), 'mm', .95)

    used_boxes = []  # (x0,y0,x1,y1) in screen px, to keep labels apart

    def add_box(x, y, w, h):
        used_boxes.append((x - w / 2, y - h / 2, x + w / 2, y + h / 2))

    def overlaps(x, y, w, h):
        x0, y0, x1, y1 = x - w / 2, y - h / 2, x + w / 2, y + h / 2
        for a, b, c, e in used_boxes:
            if x0 < c and x1 > a and y0 < e and y1 > b:
                return True
        return False

    # Super titles: towards the north of each super, outside the disc
    super_pos = {}
    for si, sup in enumerate(supers_cfg):
        lo, hi = SUPER_ARC[sup['key']]
        ang = northmost_inward(lo, hi)
        size = sum(pri_count.get(sg['key'], 0) for sg in sup['subgroups'])
        # Prefer a high placement; if the arc tops out near the equator or south,
        # sit just outside the rim at that angle.
        ux, uy = math.cos(ang), math.sin(ang)
        if uy > 0.15:
            side = 1 if ux > 0 else -1
            lx = CX + side * 0.82 * R_MAX
            ly = 150
            anchor = 'ma'
        else:
            lx, ly = polar(ang, R_MAX + 78)
            lx = min(max(lx, 90), 1340)
            ly = min(max(ly, 200), 980)
            anchor = ('l' if ux > 0.35 else 'r' if ux < -0.35 else 'm') + 'a'
        super_pos[sup['key']] = (lx, ly, anchor, size)
        text((lx, ly), sup['label'], font(FS, 36, 700),
             mix(tup(sup['color']), WHITE, .15), anchor)
        count_y = ly + 38
        text((lx, count_y), f"{size} people", font(FI, 18, 450),
             mix(tup(sup['color']), (200, 200, 210), .55), anchor)
        # rough box so subgroup labels keep clear
        add_box(lx, ly + 16, 180, 70)

    # Subgroup labels just outside the disc at the sector mid-angle
    for key, (lo, hi) in SECTOR.items():
        ang = mid_ang(lo, hi)
        r_lab = R_MAX + 46
        lx, ly = polar(ang, r_lab)
        ux, uy = math.cos(ang), math.sin(ang)
        ah = 'l' if ux > 0.35 else ('r' if ux < -0.35 else 'm')
        av = 'a'
        if uy < -0.45:
            ly += 4
        elif uy > 0.45:
            ly -= 6
        # stay on canvas and off the right-hand legend / top title
        lx = min(max(lx, 70), 1348)
        ly = min(max(ly, 220), 988)
        # nudge out if we sit on a super title
        tw = 8 * max(len(LABEL[key]), 4)
        th = 44
        tries = 0
        while overlaps(lx, ly + 12, tw, th) and tries < 8:
            r_lab += 16
            lx, ly = polar(ang, r_lab)
            lx = min(max(lx, 70), 1348)
            ly = min(max(ly, 220), 988)
            tries += 1
        text((lx, ly), LABEL[key], font(FI, 21, 620), COL[key], ah + av)
        text((lx, ly + 24), f"{pri_count.get(key, 0)}", font(FI, 15, 450),
             (185, 192, 212), ah + av)
        add_box(lx, ly + 12, tw, th)

    # Unsorted caption near the lower-left rim
    text((80, 992), UNS.get('label') or 'Unsorted', font(FS, 18, 650), UNS_COL, 'la')
    text((80, 1016), f"{pri_count.get(UNS_KEY, 0)} people", font(FI, 14, 450),
         (150, 158, 175), 'la')

    # Title
    title = CFG.get('title') or 'Inside my X network'
    n_sup_lab = f"{len(supers_cfg)} topic{'s' if len(supers_cfg) != 1 else ''}"
    text((64, 44), title, font(FS, 50, 700), WHITE, 'la')
    text((66, 108), f"{total} people  ·  {n_sup_lab}  ·  built from my People CRM",
         font(FI, 20, 420), (170, 180, 205), 'la')

    # Right-hand legend — generated from config + counts
    PX = 1435
    text((PX, 150), 'THE NETWORK', font(FS, 15, 700), MUTED, 'la')
    y = 178
    for si, sup in enumerate(supers_cfg):
        size = sum(pri_count.get(sg['key'], 0) for sg in sup['subgroups'])
        text((PX, y), sup['label'], font(FS, 28, 700), tup(sup['color']), 'la')
        text((PX + 200, y + 4), str(size), font(FS, 28, 700), WHITE, 'la')
        y += 40
        for sg in sup['subgroups']:
            c = pri_count.get(sg['key'], 0)
            circ((PX + 7, y + 10), 5, tup(sg['color']), 1)
            text((PX + 22, y), sg['label'], font(FI, 17, 500), (220, 225, 235), 'la')
            text((PX + 200, y), str(c), font(FS, 18, 600), (230, 235, 245), 'la')
            n_conn = sum(1 for n in nodes if n['primary'] == sg['key'] and n.get('connector'))
            if n_conn:
                word = 'connector' if n_conn == 1 else 'connectors'
                text((PX + 248, y), f"· {n_conn} {word}", font(FI, 14, 450), (180, 190, 205), 'la')
            y += 28
        y += 8

    text((PX, y), UNS.get('label') or 'Unsorted', font(FI, 18, 600), UNS_COL, 'la')
    text((PX + 200, y), str(pri_count.get(UNS_KEY, 0)), font(FS, 20, 600), (200, 205, 215), 'la')
    y += 48

    text((PX, y), 'RINGS', font(FS, 15, 700), MUTED, 'la')
    y += 26
    for key, lab in RING_ORDER:
        text((PX, y), lab, font(FI, 18, 600), (220, 225, 235), 'la')
        text((PX + 200, y), str(RING_COUNT[key]), font(FS, 20, 600), WHITE, 'la')
        y += 28

    y += 22
    text((PX, y), 'ROLES', font(FS, 15, 700), MUTED, 'la')
    y += 26
    n_conn = D['totals'].get('connectors', sum(1 for n in nodes if n.get('connector')))
    n_cross = sum(1 for n in nodes if n.get('cross_bridge'))
    text((PX, y), str(n_conn), font(FS, 56, 700), WHITE, 'la')
    text((PX + 90, y + 10), 'Active connectors', font(FI, 22, 650), WHITE, 'la')
    text((PX + 90, y + 40), 'two-way exchange in the last 60 days', font(FI, 15, 420), (150, 160, 180), 'la')
    y += 92
    text((PX, y), str(n_cross), font(FS, 56, 700), GOLD, 'la')
    text((PX + 90, y + 10), 'On a topic border', font(FI, 22, 650), WHITE, 'la')
    text((PX + 90, y + 40), 'people spanning two topics', font(FI, 15, 420), (150, 160, 180), 'la')

    # Bottom key
    ly, lx = 1030, 300
    lc = (190, 198, 218)
    circ((lx + 7, ly + 1), 4.6, (255, 255, 255), 1)
    circ((lx + 7, ly + 1), 7.0, None, 1, outline=(56, 214, 255), ow=1.5)
    text((lx + 22, ly - 11), 'active connector', font(FI, 16, 450), lc, 'la')
    circ((lx + 200, ly + 1), 3.2, GOLD, 1)
    text((lx + 212, ly - 11), 'topic border', font(FI, 16, 450), lc, 'la')
    circ((lx + 360, ly + 1), 2.2, mix(UNS_COL, WHITE, .22), .9)
    text((lx + 374, ly - 11), 'unsorted', font(FI, 16, 450), lc, 'la')

    text((W - 60, 1018), 'xGrok network', font(FS, 18, 600), (150, 160, 185), 'ra')
    return im.reduce(S)


if __name__ == '__main__':
    out = _arg('--out', os.path.join(HERE, 'network-map.png'))
    render().save(out, optimize=True)
    print('wrote', out)
    print('RINGS', dict(RING_COUNT))
    print('BORDERS', sum(1 for n in nodes if n.get('_border')))
    print('CROSS_SUPER', sum(1 for n in nodes if n.get('cross_bridge')))
    bc = Counter((round(n['_border'][0], 3), n['_border'][1]) for n in nodes if n.get('_border'))
    for k, v in bc.most_common():
        print('  border', k, v)
    # seam angles in degrees for the report
    print('SEAMS deg', [(round(math.degrees(a) % 360, 1), x, y) for a, x, y in SUPER_SEAMS])
    print('SECTORS deg')
    for k, (lo, hi) in SECTOR.items():
        print(' ', k, round(math.degrees(lo) % 360, 1), '->', round(math.degrees(hi) % 360, 1),
              'span', round(math.degrees(hi - lo), 1))
