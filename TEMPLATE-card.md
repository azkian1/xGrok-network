# Card template

One card is one person, in the file `people/@handle.md`. A header with fields at the top, then four sections. One of them, Touch history, is a living log that the daily routine appends to.

```markdown
---
handle: @handle
circle: horizon            # from CONFIG → circles
follow: i_follow           # mutual | i_follow | follows_me | none
status: passive            # passive | active
value:                     # from CONFIG → values (you confirm this, or an auto-rule fills it)
next_action:               # from CONFIG → next_actions (you confirm this, or an auto-rule fills it)
suggested_value:           # assistant's suggestion; leave value empty until you confirm
suggested_next:            # assistant's suggested next_action
suggested_group:           # assistant's suggested group (optional)
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
- The assistant (objective): handle, follow, status, a preliminary circle, Profile, Overlaps, Touch history, last_touch, and the suggested fields. It invents nothing: if there is little data, it says so.
- You (subjective): value, next_action, the final circle, My notes. Usually not by editing the file, but by answering in chat or clicking in a table. Until you confirm (or an auto-rule confirms an obvious case), `value` and `next_action` stay empty and the assistant's guess lives in `suggested_value`, `suggested_next`, and `suggested_group`. After you confirm, the suggestion fields are cleared.

**follow**
- `mutual`: you follow each other (core);
- `i_follow`: you follow them (core);
- `follows_me`: only they follow you. There is no full card, only a line in `FOLLOWERS.md`, until they give a signal;
- `none`: neither follows the other. We don't create a card, and after an unfollow the existing card goes to the archive.

**status**
- `passive`: there is almost no dialogue. That does not mean the person is useless: many valuable people are simply read.
- `active`: there are replies in both directions, or you talk outside X.

**circle, value, next_action, group**: the values are set in `CONFIG.md`. Review mode is cards that still have `suggested_*` filled and `value` / `next_action` empty.

**Touch history and last_touch**
- A touch is any direct interaction: your reply, quote, repost, or mention of them; their reply to you, mention of you, or quote of your post. DMs only if you paste them in yourself; meetings and calls by hand.
- The daily routine appends new touches cheaply: it reads only *your* new posts and *your* mentions since yesterday (2 reads a day), not each person's timeline.
- `last_touch` is the date of the newest line. It drives the weekly priority queue ("high-value people you have not touched for N days"). Never type it by hand; the assistant recalculates it.
- Lines you add by hand (DMs, meetings) are never overwritten.

**related**: a shared project or context. If you both worked on the same project but don't know each other, link the project, not a direct connection.

**Notes the assistant adds**: `auto: project account`, `auto: by analogy with …` mean the assistant classified the card itself and you can correct it.

## Example (a real public company account, used as a neutral example)

```markdown
---
handle: @github
circle: learning
follow: i_follow
status: passive
value: signal
next_action: just read
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
