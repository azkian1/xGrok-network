"""Build data.json from a People CRM card folder + topics.json.

No owner's interests are hard-coded. Subgroup keys, group-tag aliases and
optional keywords come from topics.json. Rings come from the card `circle`
field (see topics.json → rings) plus two-way contact and old-crew flags.

Privacy: data.json nodes have no handles, only numeric ids. This script does
not call X.

Usage:
  python3 build_data.py --cards /path/to/people --topics topics.json --out data.json
"""
import argparse, glob, json, os, re, sys
from collections import Counter
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))

OLD_CREW_TAGS = {'old crew', 'old team', 'past team', 'past crew'}
PROJECT_TAGS = {'project account', 'project', 'for the algorithm'}
DATE = re.compile(r'^- (\d{4}-\d{2}-\d{2}) ·')


def load_yaml_fm(text):
    if not text.startswith('---'):
        return {}
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}
    d = {}
    for line in parts[1].strip().splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        v = v.strip()
        if v.startswith('['):
            inner = v[1:v.find(']')] if ']' in v else v[1:]
            v = [x.strip().strip("'\"") for x in inner.split(',') if x.strip()]
        elif v.lower() in ('true', 'false'):
            v = v.lower() == 'true'
        d[k.strip()] = v
    return d


def section(text, title):
    sec = re.search(rf'## {re.escape(title)}\n(.*?)(\n## |\Z)', text, re.S | re.I)
    return sec.group(1) if sec else ''


def who_line(text):
    # English template: "- Who: …" under Profile. Also accept a plain "Who:" line.
    m = re.search(r'^- Who:\s*(.*)', text, re.M | re.I)
    if m:
        return m.group(1)
    return ''


def handles_in_list(path, patterns):
    if not path or not os.path.isfile(path):
        return set()
    text = open(path, encoding='utf-8').read()
    found = set()
    for rx in patterns:
        found |= {h for h in re.findall(rx, text, re.M)}
    return found


def build_topic_index(cfg):
    """key -> super, plus alias/keyword lookups."""
    super_of = {}
    aliases = {}  # lower group tag -> subgroup key
    keywords = []  # (key, compiled regex)
    order = []
    for sup in cfg['supers']:
        for sg in sup['subgroups']:
            key = sg['key']
            order.append(key)
            super_of[key] = sup['key']
            aliases[key.lower()] = key
            for g in sg.get('groups') or []:
                aliases[g.strip().lower()] = key
            words = [w for w in (sg.get('keywords') or []) if w]
            if words:
                body = '|'.join(re.escape(w) for w in words)
                keywords.append((key, re.compile(rf'(?i)\b(?:{body})\b')))
    unsorted = (cfg.get('unsorted') or {}).get('key') or 'other'
    super_of[unsorted] = None
    return super_of, aliases, keywords, order, unsorted


def topics_for(groups, who, aliases, keywords):
    found = []
    for g in groups:
        key = aliases.get(str(g).strip().lower())
        if key and key not in found:
            found.append(key)
    blob = who or ''
    for key, rx in keywords:
        if key not in found and rx.search(blob):
            found.append(key)
    return found


def parse_touches(text, handle, owner):
    """Return (outgoing dates, incoming dates) from an English Touch history."""
    touch = section(text, 'Touch history') or section(text, 'History')
    out, inn = [], []
    owner_l = (owner or '').lstrip('@').lower()
    handle_l = (handle or '').lstrip('@').lower()
    for line in touch.splitlines():
        if not line.startswith('- '):
            continue
        dm = DATE.match(line)
        dt = datetime.strptime(dm.group(1), '%Y-%m-%d') if dm else None
        low = line.lower()
        outgoing = bool(re.search(r'·\s*(you|i|me)\s*→', low))
        if owner_l and re.search(rf'·\s*@?{re.escape(owner_l)}\s*→', low):
            outgoing = True
        incoming = bool(re.search(r'→\s*(reply to you|you\b|mention of you|quote of your)', low))
        if handle_l and re.search(rf'·\s*@?{re.escape(handle_l)}\s*→', low):
            incoming = True
        if outgoing:
            out.append(dt)
        elif incoming:
            inn.append(dt)
    return out, inn


def ring_flags(circle, two_way, old_crew, cfg):
    # exported for the renderer; the renderer also applies the same rule
    return {'circle': circle, 'two_way': two_way, 'old_crew': old_crew}


def main():
    ap = argparse.ArgumentParser(description='Build network-map data.json from People CRM cards + topics.json')
    ap.add_argument('--cards', required=True, help='Path to the people card folder (the files @handle.md)')
    ap.add_argument('--topics', default=os.path.join(HERE, 'topics.json'),
                    help='topics.json (defaults to topics.example.json if missing)')
    ap.add_argument('--out', default=os.path.join(HERE, 'data.json'))
    ap.add_argument('--owner', default='', help='Owner handle, used to recognise outgoing touches')
    ap.add_argument('--today', default='', help='YYYY-MM-DD, default: today (local)')
    args = ap.parse_args()

    topics_path = args.topics
    if not os.path.isfile(topics_path):
        example = os.path.join(HERE, 'topics.example.json')
        if os.path.isfile(example):
            topics_path = example
        else:
            sys.exit('No topics file found. Copy topics.example.json to topics.json.')
    cfg = json.load(open(topics_path, encoding='utf-8'))
    super_of, aliases, keywords, order, unsorted = build_topic_index(cfg)

    if args.today:
        today = datetime.strptime(args.today, '%Y-%m-%d')
    else:
        today = datetime.now()
    cut = today - timedelta(days=60)

    cards_dir = os.path.abspath(args.cards)
    files = sorted(glob.glob(os.path.join(cards_dir, '@*.md')))
    # also accept people/@handle.md one level down
    if not files:
        files = sorted(glob.glob(os.path.join(cards_dir, 'people', '@*.md')))
    if not files:
        sys.exit(f'No @*.md cards found in {cards_dir}')

    engaged = handles_in_list(os.path.join(cards_dir, 'ENGAGED.md'),
                              [r'^### \[@(\w+)\]', r'^- \[@(\w+)\]'])
    quar = handles_in_list(os.path.join(cards_dir, 'QUARANTINE.md'),
                           [r'^- \[@(\w+)\]', r'^### \[@(\w+)\]'])

    nodes = []
    n_two_way = n_conn = n_cross = n_warm = n_project = n_old = 0
    for i, path in enumerate(files):
        text = open(path, encoding='utf-8').read()
        meta = load_yaml_fm(text)
        handle = str(meta.get('handle') or os.path.basename(path)[1:-3]).lstrip('@')
        groups = meta.get('group') or []
        if not isinstance(groups, list):
            groups = [groups]
        groups = [str(g) for g in groups]
        who = who_line(text)
        found = topics_for(groups, who, aliases, keywords)
        primary = found[0] if found else unsorted
        span = found if found else [unsorted]
        home_super = super_of.get(primary)
        other = [t for t in span if super_of.get(t) and super_of.get(t) != home_super]
        cross = bool(home_super and other)

        out_t, in_t = parse_touches(text, handle, args.owner)
        two_way = bool(out_t) and bool(in_t)
        recent_out = any(dt and dt >= cut for dt in out_t)
        recent_in = any(dt and dt >= cut for dt in in_t)
        group_l = {g.strip().lower() for g in groups}
        old_crew = bool(group_l & OLD_CREW_TAGS)
        project = bool(group_l & PROJECT_TAGS) or bool(re.search(r'auto:\s*project account', text, re.I))
        connector = (not project) and two_way and recent_out and recent_in
        warm = two_way and len(out_t) >= 2 and len(in_t) >= 1  # 2+ two-way exchanges ~ 2 out + 1 in at least

        node = {
            'primary': primary,
            'super': home_super,
            'connector': connector,
            'condenser': False,
            'bridge': bool(len(span) > 1),
            'cross_bridge': cross,
            'bridge_to': other,
            'span': span,
            'circle': meta.get('circle') or '',
            'warm': warm,
            'two_way': two_way,
            'old_crew': old_crew,
            'past_crew': old_crew,
            'dormant': False,
            'quarantine': handle in quar,
            'out_t': len(out_t),
            'in_t': len(in_t),
            'project': project,
            'id': i,
        }
        nodes.append(node)
        n_two_way += int(two_way)
        n_conn += int(connector)
        n_cross += int(cross)
        n_warm += int(warm)
        n_project += int(project)
        n_old += int(old_crew)

    data = {
        'privacy': 'anonymous-dots; no handles in this file',
        'nodes': nodes,
        'totals': {
            'cards': len(nodes),
            'connectors': n_conn,
            'cross_bridges': n_cross,
            'warm': n_warm,
            'two_way': n_two_way,
            'old_crew': n_old,
            'project': n_project,
        },
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or '.', exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
    print('wrote', args.out)
    print('cards', len(nodes), 'connectors', n_conn, 'cross_bridges', n_cross)
    print('primaries', dict(Counter(n['primary'] for n in nodes)))


if __name__ == '__main__':
    main()
