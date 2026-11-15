# List templates: QUEUE.md, ENGAGED.md, FOLLOWERS.md, VERIFIED.md, QUARANTINE.md

The assistant generates these files; you don't have to edit them. The handles below are fictional.

## QUEUE.md — who to engage with this week

Only confirmed core cards (people you follow, or an engaged non-follow you have explicitly confirmed). Auto-filled cards (`auto: true`) count as confirmed; only disputed cards are unconfirmed. People you do not follow stay out of this queue until you follow them or confirm a card.

```markdown
# Engagement queue — week of YYYY-MM-DD

Who it makes sense to interact with this week (reply to a post, quote, write). Only a suggestion: you write on X yourself.

How the score works: see CONFIG section 10 (value, next step, your niche, your notes, two-way / warm contact, continuous day-ranges since the last two-way exchange, and a bonus for each of your goals — without double-counting value.ideas). Only two-way exchanges count as contact; an outgoing-only touch counts for nothing. Warm contacts (2+ two-way exchanges) always outrank people with no two-way contact, even with the conservative auto pair (ideas / just read). Unconfirmed (disputed) people and people you do not follow are excluded.

| # | handle | score | value | next_action | last touch | why |
|---|---|---|---|---|---|---|
| 1 | [@example_builder](https://x.com/example_builder) | 8.0 | ideas | reply sometimes | YYYY-MM-DD | your niche, two-way contact, 45 days without a touch |
| 2 | [@example_partner](https://x.com/example_partner) | 7.5 | collab | send a DM | — | your notes: worked together, never touched on X |

## Next 10 (spare)
- [@example_writer](https://x.com/example_writer) — 5.0 — value ideas, 20 days without a touch
```

The assistant keeps a small log of who was in the queue each week and whom it already showed in the morning, so the list rotates and nobody is repeated within a week.

## ENGAGED.md — people who come to you

People who interact with your posts. Accounts you follow enter at 2+ interactions. People you do not follow enter only if they interact often and over time (at least 5 interactions, on at least 3 different weeks, within 60 days — not one day, and not a couple of conversations). There is no "one-off worth a look" section. Engaged non-follows get no card, no queue spot, and no disputed review until you follow them or confirm a card (CONFIG section 9).

```markdown
# Engaged (last 30 days)

People who interact with your posts (replies, mentions, quotes). Accounts you follow: 2+ interactions in 30 days. Accounts you do not follow: at least 5 interactions, on at least 3 different weeks, within 60 days. Accounts in bots/ are skipped.

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
- "Move to the core" is a status on this list. When someone gets a full card is the single rule in CONFIG section 9. A person you do not follow stays on this list and out of the queue until you follow them or confirm a card.

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
