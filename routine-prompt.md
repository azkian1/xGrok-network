# Routine prompts

Two scheduled tasks. Paste each to your assistant; it takes the values in `{{…}}` from `CONFIG.md`.

1. **Daily briefing** (morning routine), every day at `{{schedule.daily}}` (`{{timezone}}`).
2. **Weekly digest**, once a week at `{{schedule.weekly}}`, including the weekly data refresh and the improvement questions.

Both times come from the onboarding scheduling question (defaults: daily 09:00 local, weekly Sunday 18:00). Routines are created with those times.

---

## 0. First run only: onboarding

If `CONFIG.md` section 0 (`about_me`) is empty, the assistant does this before anything else:

```text
Before you start, ask me six short questions in one numbered message, and wait for my answers:
1) What is your niche, and which topics do you want to see more of?
2) What do you want from your network, most important first: ideas, collabs, audience growth, or just reading?
3) Which skill or area do you want to grow?
4) What kind of people are a priority for you?
5) Which language should briefings and notes be in?
6) When do you want the daily briefing (time, timezone)? Which day and time for the weekly digest?
   Defaults if I skip this: daily 09:00 local, weekly Sunday 18:00.
Accept short and voice answers. Write 1–4 into {{data_folder}}CONFIG.md, section 0 (about_me), 5 into language,
and 6 into timezone, schedule.daily, and schedule.weekly. Create the daily briefing and the weekly digest at those times.
Use about_me from now on: people matching my niche and priority_people get higher priority and the niche group;
the queue weights follow my goals (CONFIG section 10); the digest picks posts by meaning for my niche and growth area.
```

---

## 1. Daily briefing (morning routine)

```text
Daily People CRM briefing for {{my_handle}}. Time: {{schedule.daily}}, {{timezone}}.
Before you start, re-read {{data_folder}}CONFIG.md (including about_me) and PRINCIPLES.md.
On X, only read: no posts, replies, likes, reposts, follows, unfollows, or DMs.
Every handle in the message is a link to https://x.com/handle.

MODE. Review mode is cards that have suggested_value / suggested_next not yet confirmed
(value / next_action still empty). The message is simply {{batch_initial}} of them with
your suggestions and a link to the table, plus STEP 1 alerts; skip STEPS 4–5.
Once every core card has a confirmed value / next_action (steady mode), follow all steps below.
If you build or score a queue during review mode, use suggested_* fields where value / next_action are empty.

STEP 1. Sleeping accounts (next_action = "wait for wake-up").
- With one batched request, fetch the profiles of everyone in {{data_folder}}WATCHLIST.md
  (it has the handle, the date of the latest post, and the id of the latest post).
  Ask for the latest post to be included in the response, so you usually don't need the timeline.
- Compare the id of the latest post. If it has not changed, do not touch the timeline.
- For those that have moved, one or two sentences about what they posted (a fresh slice of up to
  {{fresh_slice_posts}} posts only if the included post is not enough).
- Update WATCHLIST.md (the new id and date) and add a line to that card's Touch history only if it was about me.
- If {{alert_if_many}} or more woke up at once, mark: "It looks like something is happening in the field."

STEP 2. Touches (cheap: 2–3 reads).
- Read MY posts since the newest one you already have (since_id from _state.json), and MY mentions
  since the newest one you have. Do not read other people's timelines for this.
  After the read, update since_ids and reads used in _state.json.
- For every reply, quote, repost, or mention between me and a person, append a line to that person's
  "Touch history" (newest first, with date and link) and recalculate last_touch. Never duplicate a link.
  Keep lines I added by hand (DMs, meetings).
- If I pasted a DM or told you about a meeting, add a "· DM ·" or "· met ·" line yourself.
- Update ENGAGED.md (CONFIG section 11): people with {{engaged.min_interactions}}+ interactions with my posts
  in {{engaged.window_days}} days, type substantive / wow, status, which posts. Don't overwrite my status or notes.

STEP 3. New people.
- Compare my current follows with the full stored follow list in _state.json (every handle
  I follow, not a truncated first-N page). Update that list. New follows and mutuals get a card
  using TEMPLATE-card (up to {{batch_steady}} a day; the rest wait for tomorrow).
- A follower gets a full card only on a signal: "move to the core" in ENGAGED.md that I confirmed,
  or a clear match with my niche (about_me) and recent activity. Other followers stay a line in FOLLOWERS.md
  (activity: active <= 14 days, rare 15–180, silent > 180).
- Classify the clear cases yourself using auto_rules, about_me, and my past decisions (note "auto: …").
  On a first run there are no past decisions: use about_me only. A single tag, mention, or one reply
  is not enough to mark someone disputed. For obvious auto cases fill value / next_action; otherwise
  write suggested_* and leave value / next_action empty until I confirm.
  Never set these yourself: {{never_auto}}. Only show me disputed and unclear cases.
- Log everyone you showed me in _review-log.json so you don't repeat them.

STEP 4. Priority queue.
- If it is {{queue.rebuild_on}} or QUEUE.md is older than 7 days, rebuild it (CONFIG section 10): {{queue.size}} people.
- Pick {{queue.daily_pick}} people from this week's queue whom you haven't shown yet this week.
  For each: one line on why now, their latest post if you already have it (at most 1 read per person),
  and an idea of what to write about (a topic or angle, not a ready-made reply). Never send or post
  any text on my behalf.

STEP 5. Unclear accounts (backlog).
- Keep unresolved unclear people in _review-log.json under "disputed_backlog"
  (a list of {handle, question, suggestion}). Add newly unclear or disputed people to that backlog
  instead of dropping them if they don't fit today's message.
- Pick 3–5 from the backlog whom you haven't asked about recently, to include in the message.
  I answer by number. After I answer, update the card and remove them from the backlog.
  Unanswered ones stay in the backlog.

STEP 6. Message to me.
- Send one short message only when there is a reason: someone woke up, there are people from the
  queue to show, there is a new substantive engaged person, or there are unclear accounts to clarify.
  If none of that is true — {{stay_silent_if_nothing}}: write nothing (do not send a question alone).
- Otherwise one short message, in this order:
  1) woken watchlist accounts: "@handle woke up (quiet for N months): 'quote' → link";
  2) "Who to talk to today": 1–3 handles from the weekly queue, why, link to a fresh post,
     and an idea of what to write about — never a ready-made text sent on my behalf;
  3) "New engaged": a new substantive person or a "move to the core" suggestion — handle, one quote, "create a card?";
  4) 3–5 unclear accounts from the disputed backlog: a number, @handle as a link, who they are
     in one line, and your suggested value / next_action / group; I answer by numbers;
  5) ONE improvement question of the day, as a click card. Never repeat a question already in
     _questions-log.json (create that file as [] if it is missing). After I answer, append the
     question and my answer to the log, and update cards or queue weights if needed;
  6) a link to the table, if there is one.
- Strong posts from priority people go to the weekly digest, not this morning message.
- Don't use words like "CRM" or "cron", and don't mention file names — write in plain language.

STEP 7. My replies.
- Accept lines `@handle | value=… | next=… | group=… | note=…`, numbers ("3 ok, 5 unfollowed"),
  clicks on the question card, and voice. Write them into the cards. On "unfollowed" — value none,
  update follow, move to _unfollowed-archive/.
- "Create a card" for an engaged person — a full card from TEMPLATE-card; mark them in ENGAGED.md.
- Stories about a person go into "My notes" with a date.

Budget: no more than {{daily_read_budget}} X reads a day; normally 5–15.
```

---

## 2. Weekly digest

```text
Weekly People CRM digest for {{my_handle}}. Time: {{schedule.weekly}}, {{timezone}}.
Re-read {{data_folder}}CONFIG.md (about_me, sections 9–12). On X, only read.
Every handle is a link to https://x.com/handle, every post is a link to the post.

STEP 0. Weekly data refresh (cheap batches, no timelines).
- Re-read my following and follower lists. Compare against the full stored follow list in
  _state.json (not a truncated first-N page) and then update that list. Update follow on cards;
  new follows get a card, new non-mutual followers get a line in FOLLOWERS.md; people who left are noted.
- Re-read profile fields of core accounts in batches of up to 100: name, bio, follower count,
  latest post date, activity. Update the Profile section of each card.
- Suggest quarantine for accounts silent longer than {{silent_after_days}} days (never for WATCHLIST.md accounts).
  If nobody reaches that threshold, a one-line note is enough; the first-build cleanup rule with
  {{silent_soft_days}} applies only to the first cleanup list.
- If the base is a git repo, commit the week's changes (or open a PR, see GITHUB.md).

STEP 1. Priority people's week.
- Take the core with value signal / ideas / collab, without sleeping accounts and project accounts.
- Use the profiles from STEP 0, which include each person's latest post. Compare with last week's
  latest-post ids (keep them in _anchors.json). Skip anyone who has not moved.
- Rank those who moved by priority (CONFIG section 10) and by meaning for my niche, topics, and growth area
  (about_me); likes and bookmarks are only a hint. For the top 10 only, read a fresh slice of this week's
  original posts and pick the single strongest post or idea from each.

STEP 2. Quotes of my posts.
- Read my latest posts once (fresh quote counts). For posts from the last 30 days whose quote count went up,
  read who quoted them. Append touches, update ENGAGED.md.

STEP 3. Rebuild QUEUE.md for the new week (CONFIG section 10).

STEP 4. Message to me:
  "Your network this week"
  0) One line of stats if anything changed: "+N followers, −M left, K new follows".
  1) Strong posts and ideas from priority people: 5–10 lines, @handle — what it is about in one phrase → link.
  2) Sleeping accounts that woke up this week (or one line "the watchlist is quiet").
  3) Top engaged of the week: substantive (handle, count, one quote) and wow (handles in one line);
     who you suggest moving to the core.
  4) Next week's queue: {{queue.size}} handles, one line each on why.
  5) How many X reads you used.
- A quiet week gets a two-line message, not an empty wall of text.

STEP 5. Improvement questions.
- End with ONE click-to-answer card of 3–5 short questions built from this week's data:
  who was actually useful to read; who should get higher priority; who could be a partner
  (set collab only if I pick it); clarifications for unclear accounts; and every 3–4 weeks
  one question about my goals and niche.
- Never repeat a question already in _questions-log.json. After I answer, append the questions and
  answers to the log, and update cards, about_me, or queue weights.

Budget: no more than {{weekly_digest.read_budget}} X reads.
```
