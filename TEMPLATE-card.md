# Card template

One card is one person, in the file `people/@handle.md`. A header with fields at the top, then four sections. One of them, Touch history, is a living log that the daily routine appends to.

```markdown
---
handle: @handle
circle: horizon            # from CONFIG → circles
follow: i_follow           # mutual | i_follow | follows_me | none
status: passive            # passive | active  (dialogue; not the same as FOLLOWERS activity)
value:                     # from CONFIG → values (the assistant's best guess, or you)
next_action:               # from CONFIG → next_actions (the assistant's best guess, or you)
auto: true                 # true when the assistant filled value / next_action / group; counts as confirmed for the queue. Only disputed cards are unconfirmed. The owner can override anytime.
suggested_value:           # optional alternative, used when a disputed person is shown
suggested_next:            # optional alternative next_action
suggested_group:           # optional alternative group
last_touch:                # date of the newest line in Touch history (derived; empty = never)
group: []                  # from CONFIG → groups, more than one is allowed
related: []                # shared projects and contexts
---

## Profile
- Who: 1–2 phrases from the bio, what they do.
- Account: followers, following, how long they have been on X.
- Activity: how many posts a day from the fresh slice, when the latest post was.
- Recent post (date): "quote…" link

## Overlaps
Shared projects, communities, and acquaintances. If there is nothing, say so.

## Touch history
- YYYY-MM-DD · you → reply · "text…" link
- YYYY-MM-DD · you → quote | repost | mention · "text…" link
- YYYY-MM-DD · @handle → reply to you | mention | quote of your post · "text…" link
- YYYY-MM-DD · DM · what it was about        (only if you pasted the DM yourself)
- YYYY-MM-DD · met · conference / call / chat  (added by hand)
(if nothing is found: "No touches found". Newest first.)

## My notes
- YYYY-MM-DD: how you met, what you agreed on, what is important to remember.
```

## Legend

**Who fills in what**
- The assistant (objective, plus a best guess): handle, follow, status, a preliminary circle, Profile, Overlaps, Touch history, last_touch, and `value` / `next_action` / `group`. On the first build it classifies everyone automatically and marks the card `auto: true`. Auto-filled fields count as confirmed for the queue; only disputed cards are unconfirmed. It invents nothing: if there is little data, it says so.
- You (subjective): corrections to value, next_action, and circle, plus My notes. Usually not by editing the file, but by answering in chat or clicking in a table. You are only asked to clarify disputed people. When a disputed person is shown, the assistant may put an alternative in `suggested_value`, `suggested_next`, and `suggested_group`. After you confirm or correct, the suggestion fields are cleared.

**follow**
- `mutual`: you follow each other (core);
- `i_follow`: you follow them (core);
- `follows_me`: only they follow you. They are not in the network (no card, no queue, no disputed) until you follow them or confirm a card — the single rule in CONFIG section 9. Until then they are only a line in `FOLLOWERS.md`, and they appear in `ENGAGED.md` only if they meet the sustained-engagement bar;
- `none`: neither follows the other. We don't create a card, and after an unfollow the existing card goes to the archive.

**status** (dialogue, not posting frequency)
- `passive`: there is almost no dialogue. That does not mean the person is useless: many valuable people are simply read.
- `active`: there are replies in both directions, or you talk outside X.

Posting frequency uses the same words in `FOLLOWERS.md` with different meanings: **active** = posted within 14 days, rare = 15–180 days, silent = more than 180 days.

**circle, value, next_action, group**: the values are set in `CONFIG.md`. Review mode is the disputed backlog, not every auto-classified card.

**Touch history and last_touch**
- A touch is any direct interaction: your reply, quote, repost, or mention of them; their reply to you, mention of you, or quote of your post. DMs only if you paste them in yourself; meetings and calls by hand.
- Touches with a project account (official company, product, or media) are logged only on that project card, not on a person.
- The daily routine appends new touches cheaply: it reads only *your* new posts and *your* mentions since yesterday (2 reads a day), not each person's timeline. Lookups of past contact are limited to 2 pages per person per direction; read page 2 only if page 1 returned a full page.
- `last_touch` is the date of the newest line. It drives the weekly priority queue ("high-value people you have not touched for N days"). Never type it by hand; the assistant recalculates it.
- Lines you add by hand (DMs, meetings) are never overwritten.

**related**: a shared project or context. If you both worked on the same project but don't know each other, link the project, not a direct connection. Related accounts of the same project (a project circle, not the closeness `circle`) get the same classification decision: if one member is disputed, the others are disputed too, instead of being split onto the unfollow list.

**Notes the assistant adds**: `auto: project account`, `auto: by analogy with …` mean the assistant classified the card itself and you can correct it.

## Bot card (`bots/@handle.md`)

Suspected bots and spam farms are merged into one cluster named `bots` and stored in the `bots/` folder. The card is minimal. Bots are also added to the unfollow list (`QUARANTINE.md`) automatically.

```markdown
---
handle: @handle
group: [bots]
followers: 1234
last_post: YYYY-MM-DD
---

## Why suspected
- One or two lines (template replies, high-volume posting, shilling, clickbait hooks). Always a guess. Numeric hints: posts/day > 50 in the slice; follower/following < 0.01 with following > 2000; default avatar + no bio + < 10 posts. Any two of these → suspected bot.

## Account
- Followers: …
- Latest post: date, or "never posted"
```

If you know the person, say so: the card moves back to the core and off the unfollow list.

## Example (a real public company account, used as a neutral example)

```markdown
---
handle: @github
circle: learning
follow: i_follow
status: passive
value: signal
next_action: just read
auto: true
last_touch:
group: [project account]
related: []
---

## Profile
- Who: GitHub, a platform for developers (official account).
- Large account: the timeline was not downloaded; the bio and the latest post were enough.

## Overlaps
No shared context found.

## Touch history
No touches found.

## My notes
- auto: project account
```
