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
6. Which language briefings and notes should be in.
7. When they want the daily briefing (time and timezone) and which day and time for the weekly digest. Defaults: daily 09:00 local, weekly Sunday 18:00.
8. Optional: do they want the base in a private GitHub repo (and to browse it in Obsidian)? If yes, follow `GITHUB.md`.

Create the base folder, copy `CONFIG.example.md` to `CONFIG.md` there, and write the answers in (about_me, language, timezone, schedule.daily, schedule.weekly). Tell the user in one line that the first build runs in the background and takes 20-60 minutes.

## 4. First build
Follow the setup prompt in `SETUP.md` section 4 step by step (cards for everyone they follow, FOLLOWERS.md, touch history, bots, auto-classification, WATCHLIST, QUARANTINE, ENGAGED, the first QUEUE), within the rate-limit rules of `SETUP.md` section 6 and `daily_read_budget`. Persist the complete follow list in `_state.json` (every handle they follow, not a truncated first-N page). Then show the longest-quiet accounts as one cleanup list: if nobody reaches `silent_after_days`, still show the quietest N (see CONFIG). After that, only the unclear cases, in small batches. Write your suggestion in `suggested_value` / `suggested_next` / `suggested_group` and leave `value` / `next_action` empty until the owner confirms, except obvious auto-rule cases.

## 5. Routines
Create two scheduled routines at the times the user chose, using the prompts in `routine-prompt.md`:
- **Daily briefing** (section 1): one short message only when there is a reason.
- **Weekly digest** (section 2): the weekly data refresh, the digest, and 3-5 clickable improvement questions.
Tell the user the saved times. They can change them any time ("move the briefing to 8:00").

## 6. Ongoing
Every answer the user gives goes back into the cards, the queue, and the logs (`_review-log.json`, `_questions-log.json`) so nothing is asked twice. "Unfollowed" moves a card to `_unfollowed-archive/`, never deletes it.
