---
name: xGrok-network
description: Install and run xGrok network (People CRM for X), a personal card file of the user's X network with a daily briefing and a weekly digest. Use when the user says "install this skill/template/system" with a link to this repository, asks to set up a CRM of their X network, or when the morning briefing or weekly digest routine fires.
---

# xGrok network: install and run

You are setting up a personal CRM of the user's network on X for them. They should not copy files or prompts: you do the work, they answer a few short questions, mostly by clicking.

## Hard rules (never break)
- **Read-only on X.** Never post, reply, like, repost, follow, unfollow, or send DMs. Every action on X is the user's.
- Suggest whom to talk to and what about; never write or send messages on the user's behalf.
- The base holds personal notes about real people: keep it private (a private folder, or a private repo only).
- Every handle you show is a clickable link to `https://x.com/<handle>`.
- Prefer clickable choices (buttons, widgets, a table page) over asking the user to type.
- The user's corrections always override your guesses and are never overwritten.

## 1. Get the kit files
Fetch these files from this repository (the GitHub link the user gave you; by default https://github.com/azkian1/xGrok-network; raw files are at `https://raw.githubusercontent.com/<owner>/<repo>/main/<file>`) and save them to a kit folder on your computer:
`SKILL.md`, `README.md`, `PRINCIPLES.md`, `SETUP.md`, `CONFIG.example.md`, `TEMPLATE-card.md`, `TEMPLATE-lists.md`, `routine-prompt.md`, `GITHUB.md`, `gitignore.example`, `LICENSE`.
If a raw fetch fails (404, empty, or blocked), clone the repo with git (`git clone <repo URL>`) and use the files from the clone; do not invent missing files.
Read `PRINCIPLES.md`, `SETUP.md`, `CONFIG.example.md`, and `routine-prompt.md` in full before going on. Save this procedure as a skill if you can, so it survives future conversations.

## 2. Check X access
Make sure you can read X: profiles, posts, search, and the user's follow and follower lists. If a connector or plugin for X is missing or needs sign-in, set it up now (the user's own X connection is needed for their follow lists).

## 3. Onboarding questions (one at a time, clickable where possible)
Ask, in this order, and accept short or voice answers:
1. Their X handle (skip if you already know it).
2. Their niche and the topics they want more of.
3. What they want from their network, most important first: ideas, collabs, audience growth, or just reading.
4. Which skill or area they want to grow.
5. What kind of people are a priority for them.
6. When they want the daily briefing (time and timezone) and which day and time for the weekly digest. Defaults: daily 09:00 local, weekly Sunday 18:00.
7. Optional: do they want the base in a private GitHub repo (and to browse it in Obsidian)? If yes, follow `GITHUB.md`.

Create the base folder, copy `CONFIG.example.md` to `CONFIG.md` there, and write the answers in (about_me, timezone, schedule.daily, schedule.weekly). Leave `language` as `"en"`. Never ask about language; if the owner later asks for another language, switch `language` in CONFIG.md and write in it from then on. Tell the user in one line that the first build runs in the background and takes 20-60 minutes.

## 4. First build
Follow the setup prompt in `SETUP.md` section 4 step by step (cards for everyone they follow, FOLLOWERS.md, VERIFIED.md, touch history, bots, auto-classification of everyone, WATCHLIST, QUARANTINE, ENGAGED, the first QUEUE), within the rate-limit rules of `SETUP.md` section 6 and `daily_read_budget`. People the owner does not follow are not in the network (no card, no queue, no disputed) until the owner follows them or confirms a card — the single rule in CONFIG section 9. For touch-history searches, read page 2 only if page 1 returned a full page. Only two-way exchanges count as contact in the queue; an outgoing-only touch counts for nothing.

Persist the follow list in `_state.json` (every handle they follow, not a truncated first-N page) and set `follow_list_complete: true`. For a capped or test run, set `follow_list_complete: false`; the daily new-follow check then compares only against the stored subset and must say so.

Classify everyone automatically in the background: fill `value` / `next_action` / `group` with your best guess and mark `auto: true`. Auto-filled fields count as confirmed for the queue; only disputed cards are unconfirmed. Do not leave the core waiting for confirmation. Related accounts of the same project get the same decision: if one member is disputed, the others are disputed too. Then show the unfollow list (`QUARANTINE.md`): only real candidates (long-AFK accounts, bots, people or project accounts that no longer match the owner's interests). If there are none, say so; do not pad the list. Log everyone on that list as shown in `_review-log.json`. After that, only genuinely disputed people, in small batches, two-way contacts first.

## 5. Routines
Create two scheduled routines at the times the user chose, using the prompts in `routine-prompt.md`:
- **Daily briefing** (section 1): one short message only when there is a reason, in the canonical order in `routine-prompt.md` (waking accounts, who to talk to today, new engaged, disputed to clarify, question of the day). A person appears only once per briefing.
- **Weekly digest** (section 2): the weekly data refresh, the digest, and 3-5 clickable improvement questions. The same weekly follower read also rebuilds `FOLLOWERS.md` and `VERIFIED.md`.
Tell the user the saved times. They can change them any time ("move the briefing to 8:00").

## 6. Ongoing
Every answer the user gives goes back into the cards, the queue, and the logs (`_review-log.json`, `_questions-log.json`) so nothing is asked twice. "Unfollowed" moves a card to `_unfollowed-archive/`, never deletes it.
