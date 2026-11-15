# List templates: QUEUE.md, ENGAGED.md, FOLLOWERS.md, VERIFIED.md, QUARANTINE.md

The assistant generates these files; you don't have to edit them. The handles below are fictional.

## QUEUE.md — who to engage with this week

Only confirmed core cards. Strangers and other people without a confirmed core card stay in `ENGAGED.md` and do not enter this queue.

```markdown
# Engagement queue — week of YYYY-MM-DD

Who it makes sense to interact with this week (reply to a post, quote, write). Only a suggestion: you write on X yourself.

How the score works: see CONFIG section 10 (value, next step, your niche, your notes, two-way / warm contact, continuous day-ranges since the last touch, and a bonus for each of your goals — without double-counting value.ideas). Warm contacts outrank strangers. Unconfirmed people are excluded.

| # | handle | score | value | next_action | last touch | why |
|---|---|---|---|---|---|---|
| 1 | [@example_builder](https://x.com/example_builder) | 8.0 | ideas | reply sometimes | YYYY-MM-DD | your niche, two-way contact, 45 days without a touch |
| 2 | [@example_partner](https://x.com/example_partner) | 7.5 | collab | send a DM | — | your notes: worked together, never touched on X |

## Next 10 (spare)
- [@example_writer](https://x.com/example_writer) — 5.0 — value ideas, 20 days without a touch
```

The assistant keeps a small log of who was in the queue each week and whom it already showed in the morning, so the list rotates and nobody is repeated within a week.

## ENGAGED.md — people who come to you

People who interact with your posts, whether you follow them or not. Strangers (people you don't follow) stay here for you to review and do not enter the contact queue until you confirm a card.

```markdown
# Engaged (last 30 days)

People who interact with your posts (replies, mentions, quotes), even if you don't follow them. Threshold: 2+ interactions in 30 days. Accounts in bots/ are skipped.

### [@example_fan](https://x.com/example_fan) — substantive, 3 in 30 days
- Where now: not followed | in FOLLOWERS.md | has a core card
- Interactions: 3 (substantive 3, wow 0)
- Which posts: https://x.com/your_handle/status/…, https://x.com/your_handle/status/…
  - YYYY-MM-DD reply to you: "The jump in the new build is great, how did you handle…" link
- Status: move to the core (auto)
- Notes:

### [@example_clapper](https://x.com/example_clapper) — wow, 4 in 30 days
- Interactions: 4 (substantive 0, wow 4)
- Status: just active (auto)
- Notes:
```

- **Type:** substantive = a question, a thought, a quote with context (about 6+ words); wow = emoji, "cool", "fire", short reactions. Decided by the majority of interactions.
- **Status:** just active · worth a look · move to the core. "(auto)" marks the assistant's suggestion; once you set a status or a note, it is never overwritten.
- "Move to the core" + your OK = the assistant creates a full card (the follower signal rule). Until then the person stays on this list and out of the queue.

## FOLLOWERS.md — every follower, one roster

The counter and the full roster. Used for "+N new, −M left" and for spotting mutuals. One line each, no cards. Activity: active = posted within 14 days, rare = 15–180, silent = more than 180.

```markdown
# Followers

N people who follow you. Refreshed weekly with the follower reconciliation.

- [@example_reader](https://x.com/example_reader) — writes about indie tools — active
- [@example_quiet](https://x.com/example_quiet) — — silent
```

## VERIFIED.md — followers with an X verification badge

Followers whose profile has a verification badge, blue or higher: blue / X Premium, gold / business, gray / government. Built from the `verified` and `verified_type` fields on the same weekly follower read — no extra timeline reads.

```markdown
# Verified followers

Refreshed weekly with the follower reconciliation.

| handle | badge | followers | follows back | bio |
|---|---|---|---|---|
| [@example_studio](https://x.com/example_studio) | gold (business) | 12800 | mutual | ships indie tools |
| [@example_author](https://x.com/example_author) | blue | 4200 | no | writes about games |
```

## QUARANTINE.md — the unfollow list

Only real candidates. If there are none, the file says so; it is not padded with the quietest accounts or "keep" rows. Appearing here counts as "shown" in `_review-log.json`.

```markdown
# Unfollow list

Candidates for you to unfollow on X yourself. The assistant never unfollows.

| handle | reason | since |
|---|---|---|
| [@example_silent](https://x.com/example_silent) | long AFK (210 days) | YYYY-MM-DD |
| [@example_bot](https://x.com/example_bot) | suspected bot (also in bots/) | YYYY-MM-DD |
| [@example_oldtopic](https://x.com/example_oldtopic) | no longer matches your interests | YYYY-MM-DD |
```
