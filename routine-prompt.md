# Routine prompts

Two scheduled tasks. Paste each to your assistant; it takes the values in `{{…}}` from `CONFIG.md`.

1. **Daily briefing** (morning routine), every day at `{{schedule.daily}}` (`{{timezone}}`).
2. **Weekly digest**, once a week at `{{schedule.weekly}}`, including the weekly data refresh and the improvement questions.

Both times come from the onboarding scheduling question (defaults: daily 09:00 local, weekly Sunday 18:00). Routines are created with those times.

---

## 0. First run only: onboarding

If `CONFIG.md` section 0 (`about_me`) is empty, the assistant does this before anything else:

```text
Before you start, ask me five short questions in one numbered message, and wait for my answers:
1) What is your niche, and which topics do you want to see more of?
2) What do you want from your network, most important first: ideas, collabs, audience growth, or just reading?
3) Which skill or area do you want to grow?
4) What kind of people are a priority for you?
5) When do you want the daily briefing (time, timezone)? Which day and time for the weekly digest?
   Defaults if I skip this: daily 09:00 local, weekly Sunday 18:00.
Accept short and voice answers. Write 1–4 into {{data_folder}}CONFIG.md, section 0 (about_me),
and 5 into timezone, schedule.daily, and schedule.weekly. Leave language as "en". Never ask about language;
if I later ask for another language, switch language in CONFIG.md and write in it from then on.
Create the daily briefing and the weekly digest at those times.
Use about_me from now on: people matching my niche and priority_people get higher priority and the niche group;
clearly off-niche people go to the unfollow list as candidates; the queue weights follow my goals (CONFIG section 10);
the digest picks posts by meaning for my niche and growth area.
```

---

## 1. Daily briefing (morning routine)

```text
Daily People CRM briefing for {{my_handle}}. Time: {{schedule.daily}}, {{timezone}}.
Before you start, re-read {{data_folder}}CONFIG.md (including about_me) and PRINCIPLES.md.
On X, only read: no posts, replies, likes, reposts, follows, unfollows, or DMs.
Every handle in the message is a link to https://x.com/handle.

MODE. After the first build, everyone in the core already has a best-guess value / next_action
(auto: true counts as confirmed for the queue). Only disputed cards are unconfirmed.
The message always uses the canonical order in STEP 6: waking accounts, who to talk to today
(1–3), new engaged, disputed to clarify (up to 3–5), question of the day. Do not lead with
disputed people. Do not skip the queue just because a disputed backlog remains. A person
appears only once: if they are disputed and also in today's queue pick, show them only in
"Who to talk to today", with a short clarify note; do not repeat them in the disputed list.

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
  Keep lines I added by hand (DMs, meetings). Touches with a project account count only on that
  project card, not on a person.
- If I pasted a DM or told you about a meeting, add a "· DM ·" or "· met ·" line yourself.
- Update ENGAGED.md (CONFIG section 11): accounts I already follow with {{engaged.min_interactions}}+
  interactions with my posts in {{engaged.window_days}} days; accounts I do not follow only if they meet
  the sustained bar (interactions on at least 3 different weeks in 60 days, and at least 5 in total — not
  one day, and not a couple of conversations). Type substantive / wow, status, which posts. No "one-off"
  section. Don't overwrite my status or notes. People I don't follow get no card, no queue spot, and no
  disputed review until I follow them or confirm a card.

STEP 3. New people.
- Compare my current follows with the stored follow list in _state.json (every handle
  I follow, not a truncated first-N page). If follow_list_complete is false, only compare
  against the stored subset and say so. Update that list. New follows and mutuals get a card
  using TEMPLATE-card (up to {{batch_steady}} a day; the rest wait for tomorrow).
- A person I do not follow gets a full card only under the single rule in CONFIG section 9 (I follow them,
  or I confirm a card). Other followers stay a line in FOLLOWERS.md (activity: active = posted within
  14 days, rare 15–180, silent > 180) and, if they have a verification badge (blue or higher), a row in
  VERIFIED.md. Do not put non-follows into disputed review.
- Classify new people yourself using auto_rules, about_me, and my past decisions (mark auto: true).
  Fill value / next_action / group with your best guess. Auto-filled fields count as confirmed for the
  queue; only disputed cards are unconfirmed. On a first run there are no past decisions: use about_me
  only, but still classify everyone. Never set {{never_auto}} yourself (use a conservative pair and flag
  the person disputed). Related accounts of the same project get the same decision: if one member is
  disputed, the others are disputed too. Only show me disputed people, two-way contacts first.
  Active (posted within 14 days) but off-niche, with no real history, is not disputed: put them
  on the unfollow list or in bots/. Off-niche project accounts get no automatic signal / just-read.
- Put suspected bots in bots/ (cluster "bots", minimal card) and on QUARANTINE.md automatically.
- Log everyone you showed me in _review-log.json so you don't repeat them. Appearing on the
  unfollow list also counts as shown.

STEP 4. Priority queue.
- If it is {{queue.rebuild_on}} or QUEUE.md is older than 7 days, rebuild it (CONFIG section 10): {{queue.size}} people.
  Only confirmed core cards (auto: true counts as confirmed; only disputed cards are unconfirmed).
  Exclude unconfirmed people and anyone I do not follow; if you must mention one, mark them clearly
  and still do not score them into the queue. Only two-way exchanges count as contact; an outgoing-only
  touch counts for nothing. Warm contacts (2+ two-way exchanges) always outrank people with no two-way contact.
- Pick {{queue.daily_pick}} people from this week's queue whom you haven't shown yet this week.
  For each: one line on why now, their latest post if you already have it (at most 1 read per person),
  and an idea of what to write about (a topic or angle, not a ready-made reply). Never send or post
  any text on my behalf.

STEP 5. Disputed accounts (backlog).
- Keep unresolved disputed people in _review-log.json under "disputed_backlog"
  (a list of {handle, question, suggestion}). Add newly disputed people to that backlog
  instead of dropping them if they don't fit today's message. Do not use a separate "unclear" list:
  disputed is the only review category. Batch order: two-way contacts first, then the rest.
- Pick 3–5 from the backlog whom you haven't asked about recently (or up to {{batch_initial}}
  while the backlog is large), to include in the message, skipping anyone already in today's
  queue pick (they appear only in "Who to talk to today", with a short clarify note). I answer
  by number. After I answer, update the card and remove them from the backlog. Unanswered ones
  stay in the backlog.

STEP 6. Message to me.
- Send one short message only when there is a reason: someone woke up, there are people from the
  queue to show, there is a new substantive engaged person, or there are disputed accounts to clarify.
  If none of that is true — {{stay_silent_if_nothing}}: write nothing (do not send a question alone).
- Otherwise one short message, in this canonical order (do not reorder):
  1) woken watchlist accounts: "@handle woke up (quiet for N months): 'quote' → link";
  2) "Who to talk to today": 1–3 handles from the weekly queue, why, link to a fresh post,
     and an idea of what to write about — never a ready-made text sent on my behalf;
  3) "New engaged": a new substantive person or a "move to the core" suggestion — handle, one quote, "create a card?";
  4) 3–5 disputed accounts from the backlog (two-way contacts first), excluding anyone already shown
     in (2): a number, @handle as a link, who they are in one line, and your suggested value /
     next_action / group; I answer by numbers;
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
- "Create a card" or "I now follow them" for an engaged non-follow — a full card from TEMPLATE-card;
  mark them in ENGAGED.md. Until I follow them or confirm a card, they stay in ENGAGED.md, out of
  the queue, and out of disputed review.
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
- Re-read my following and follower lists. Compare against the stored follow list in
  _state.json (not a truncated first-N page). If follow_list_complete is false, only compare
  against the stored subset and say so. Then update that list. Update follow on cards;
  new follows get a card, new non-mutual followers get a line in FOLLOWERS.md; people who left are noted.
- Rebuild FOLLOWERS.md (the full roster and the +N/−M counter) and VERIFIED.md (followers with
  an X verification badge, blue or higher: blue / X Premium, gold / business, gray / government)
  from the verified and verified_type fields on the same follower read. No extra timeline reads.
  VERIFIED.md columns: handle link, badge type, followers count, follows back / mutual, short bio.
- Re-read profile fields of core accounts in batches of up to 100: name, bio, follower count,
  latest post date, activity. Update the Profile section of each card.
- Suggest quarantine (the unfollow list) only for real candidates: accounts silent longer than
  {{silent_after_days}} days (or {{silent_soft_days}} if nobody reaches that; never for WATCHLIST.md
  accounts), bots, people who no longer match my interests, and project accounts that do not
  match my interests. If there are no candidates, say so in one line. Do not pad the list with
  the quietest accounts or "keep" rows. Log everyone on the list as shown in _review-log.json.
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
  read who quoted them. Append touches, update ENGAGED.md. Touches with a project account count only
  on that project card.

STEP 3. Rebuild QUEUE.md for the new week (CONFIG section 10).
  Only confirmed core cards. Exclude unconfirmed people and anyone I do not follow.

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
  (set collab only if I pick it); clarifications for disputed accounts; and every 3–4 weeks
  one question about my goals and niche.
- Never repeat a question already in _questions-log.json. After I answer, append the questions and
  answers to the log, and update cards, about_me, or queue weights.

Budget: no more than {{weekly_digest.read_budget}} X reads.
```
