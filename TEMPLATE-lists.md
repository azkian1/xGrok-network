# List templates: QUEUE.md and ENGAGED.md

The assistant generates both files; you don't have to edit them. The handles below are fictional.

## QUEUE.md — who to engage with this week

```markdown
# Engagement queue — week of YYYY-MM-DD

Who it makes sense to interact with this week (reply to a post, quote, write). Only a suggestion: you write on X yourself.

How the score works: see CONFIG section 10 (value, next step, your niche, your notes, continuous day-ranges since the last touch, and a bonus for each of your goals).

| # | handle | score | value | next_action | last touch | why |
|---|---|---|---|---|---|---|
| 1 | [@example_builder](https://x.com/example_builder) | 8.0 | ideas | reply sometimes | YYYY-MM-DD | your niche, your notes, 45 days without a touch |
| 2 | [@example_partner](https://x.com/example_partner) | 7.5 | collab | send a DM | — | your notes: worked together, never touched on X |

## Next 10 (spare)
- [@example_writer](https://x.com/example_writer) — 5.0 — value ideas, 20 days without a touch
```

The assistant keeps a small log of who was in the queue each week and whom it already showed in the morning, so the list rotates and nobody is repeated within a week.

## ENGAGED.md — people who come to you

```markdown
# Engaged (last 30 days)

People who interact with your posts (replies, mentions, quotes), even if you don't follow them. Threshold: 2+ interactions in 30 days. Accounts in bots/ are skipped.

### [@example_fan](https://x.com/example_fan) — substantive, 3 in 30 days
- Where now: not followed | in FOLLOWERS.md | has a core card
- Interactions: 3 (substantive 3, wow 0)
- Which posts: https://x.com/your_handle/status/…, https://x.com/your_handle/status/…
  - YYYY-MM-DD reply to you: "Love the jump from v1 to this, how did you handle…" link
- Status: move to the core (auto)
- Notes:

### [@example_clapper](https://x.com/example_clapper) — wow, 4 in 30 days
- Interactions: 4 (substantive 0, wow 4)
- Status: just active (auto)
- Notes:
```

- **Type:** substantive = a question, a thought, a quote with context (about 6+ words); wow = emoji, "cool", "fire", short reactions. Decided by the majority of interactions.
- **Status:** just active · worth a look · move to the core. "(auto)" marks the assistant's suggestion; once you set a status or a note, it is never overwritten.
- "Move to the core" + your OK = the assistant creates a full card (the follower signal rule).
