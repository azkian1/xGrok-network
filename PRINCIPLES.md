# PRINCIPLES — the decisions and why they were made

These rules took shape while the kit was tried on a real account with ~350 follows over a couple of days. Each one came out of a concrete problem.

## 1. A card only if you follow them
**Decision.** A full card is created only for the core: mutuals and accounts you follow yourself.
**Why.** These are people you chose. "Everyone who ever liked a post" is noise.

## 2. The core and followers are kept separately
**Decision.** Non-mutual followers are stored in a single file, `FOLLOWERS.md`: handle, a few words, activity. A full card appears only if the follower gave a signal: they replied, mentioned you, or reposted you, you followed them back, or they are clearly in your field.
**Why.** Followers are almost always weak ties. If there are thousands of them, reviewing each one is impossible, and reading each timeline is very expensive. Future friends and partners among them can be found by a signal.

## 3. On X, read only
**Decision.** The assistant does not post, like, follow, or unfollow. Only you unfollow.
**Why.** This is your voice and your reputation. A bot's mistake on X is visible to everyone and cannot be undone.

## 4. Only a fresh slice
**Decision.** For a card we take ~10 recent posts or 3–7 days, and we look up contact history with search. For large accounts, the bio and the latest post are enough.
**Why.** Otherwise the daily X limits burn through on the first few dozen people. A fresh slice is enough to understand who they are and what they are doing now.

## 5. The bot fills in the objective, the person fills in the subjective
**Decision.** The assistant writes the profile, the history, and the overlaps. You set the value, the next step, and the notes.
**Why.** A person's value lives in your head, and you cannot guess it from their feed. In return, the assistant invents nothing: if there is little data, it says so.

## 6. Click, don't type
**Decision.** Values are chosen from fixed lists, and each value has a default next step. The assistant writes its suggestion into separate fields (`suggested_value`, `suggested_next`, `suggested_group`) and leaves `value` and `next_action` empty until you confirm or correct it. Auto-rules may fill `value` and `next_action` themselves for obvious cases (official accounts, long-silent accounts, close look-alikes). Review mode is the set of cards whose suggestions are not yet confirmed. Answers are accepted in any form: by number, by voice, or as ready-made lines from the table.
**Why.** After a few dozen people, answers start to repeat. The list and the default values turn the review into 2–3 minutes a day. Keeping the suggestion separate from the confirmed value means a first run does not pretend the owner has already decided.

## 7. Auto-classification; the person only sees disputed cases
**Decision.** The assistant classifies the obvious cases itself: official accounts, long-quiet accounts, and (once you have classified similar people) look-alikes. It only shows you the disputed ones. It never sets close relationships, collabs, or DMs itself. On a first run there are no past decisions, so it relies on the `about_me` niche rules only. A single tag, mention, or one reply is not enough to mark someone disputed; disputed means 2+ two-way touches, a strong conflict between niche fit and activity, or someone off-niche who still has a real history with you.
**Why.** On a real run, more than half of the core was classified automatically, and only ~20 disputed cases out of ~190 were left for manual review. Treating any contact as disputed sent too many people to the owner, some over a single tag. Decisions about people you talk to stay with you.

## 8. Project accounts are a special type
**Decision.** Official accounts of companies, products, and media (for example, @github) always get signal and "just read". A collab is never proposed to them.
**Why.** These are not people: their updates are useful to read, and there is no need to befriend them. There are many such accounts, and they are easy to recognize from the bio.

## 9. Quarantine before unfollowing
**Decision.** The assistant puts dead and useless accounts into "quarantine" and shows them as a single list; you decide. If nobody is quieter than `silent_after_days`, it still shows the quietest N, says so in one line, and suggests quarantine only for accounts that also pass a lower soft threshold and are off-niche; the rest are "keep". After an unfollow, the card goes to the archive instead of being deleted.
**Why.** "Quiet" does not always mean "useless", and that became clear on the very first run. A hard threshold with no fallback left the first cleanup list empty even when some accounts were nearly a year quiet. The archive keeps a memory of who they were.

## 10. "Wait for wake-up" is not quarantine
**Decision.** A separate category for sleeping accounts, kept in `WATCHLIST.md`. These are accounts that are quiet now, but if they start posting, something is happening in the field. Every morning they are checked with one batched profile request, using the id of the latest post. If several wake up at once, that is a signal of its own.
**Why.** The most useful finding of the project. Such accounts are easy to unfollow by mistake, and their return is an early indicator. The check is almost free.

## 11. Stay silent if there is nothing to say
**Decision.** In steady mode the assistant writes only if there is a reason: a watchlist account woke up, people from this week's queue, a new substantive engaged person, or unclear accounts to clarify. One improvement question of the day is attached to that message, not sent alone.
**Why.** A daily empty briefing quickly becomes noise, and people stop reading it.

## 12. Every handle is a link
**Decision.** In any list, the handle is given as a link to `https://x.com/handle`.
**Why.** To remember a person, you almost always need to open their profile. One click instead of a search.

## 13. Ask about goals first
**Decision.** On the first run the assistant asks a few short questions: niche and topics, goals for the network, what you want to grow, which people are a priority, the language, and when you want the daily briefing (time, timezone) and the weekly digest (day and time). Defaults: daily 09:00 local, weekly Sunday 18:00. Answers 1–4 go to CONFIG (`about_me`) and drive classification and priority. The language goes to `language`, and the schedule to `schedule.daily` and `schedule.weekly`, and the routines are created with those times.
**Why.** Who matters depends on what you are doing. If you make indie games, people who post quality work in that niche matter more than the biggest accounts in tech. Without goals, the assistant can only guess from follower counts. Briefings should arrive when the owner actually has time to look at them.

## 14. One touch history, filled from your side
**Decision.** Each card has one living Touch history section and a derived `last_touch` date. New touches come from reading your own new posts and mentions (2–3 reads a day), not from each person's timeline. DMs only if you paste them.
**Why.** "When did we last talk" is the most useful field for keeping relationships alive, and reading it from your own side costs almost nothing.

## 15. A short weekly queue instead of "N new people a day"
**Decision.** Once the core is reviewed, the daily batch is replaced by a weekly queue of 7–10 people worth engaging with, scored by value, next step, niche, your notes, and days since the last touch (every day-range is covered, with no gaps). Each of your goals adds its own bonus, scaled by the order you gave them — not only by which goal comes first. In review mode, scoring uses the suggested fields until you confirm. Each morning shows 1–3, with why and an idea of what to write about. The assistant never sends ready-made text on the owner's behalf. The assistant suggests; you talk.
**Why.** After the review there is nothing left to classify, but there are always people you meant to reply to and forgot. A short rotating list keeps that manageable.

## 16. Engaged people are a separate light layer
**Decision.** People who interact with your posts (even if you don't follow them) go to `ENGAGED.md`, split into substantive and wow. The best substantive ones are suggested for a full card. This is the same "signal" that promotes a follower; there is no second rule.
**Why.** New good contacts often come to you first. Splitting substance from applause shows who is worth a look without reviewing every reply.

## 17. A weekly digest, not a daily feed
**Decision.** Strong posts from priority people go to the weekly digest, not the morning briefing. Once a week: a data refresh, those posts, sleeping accounts that woke up, top engaged, next week's queue, and 3–5 improvement questions. Built from batched lookups that include the latest post.
**Why.** The point of the card file is that good posts from chosen people don't get lost. Weekly is enough, and batched lookups keep it cheap. The morning stays a short action list, not a feed.

## 18. Keep improving with small questions
**Decision.** The daily briefing carries at most one question of the day; the weekly digest ends with 3–5. Both are click cards built from real data (who was useful, who to raise, who could be a partner, unclear accounts, occasionally goals). Asked questions are logged and never repeated.
**Why.** A base built once goes stale. Tiny, regular corrections keep it aligned with what the owner actually values, without a big review session.

## Next (roadmap)
- **Done in this version:** the weekly digest with data refresh and improvement questions, touch history, the priority queue, and the engaged layer.
- **Deferred:** network roles (connector / knowledge holder / bridge), "new follows of your priority people", and cluster visualization. They need a who-talks-to-whom graph or many reads.
- Every N weeks, refresh old cards from a fresh slice.
- Send answers directly from the page, without copying lines.
- Tell a real person from a spam farm more accurately.

## Version history

- **v1.6** (2026-11-15). Fixes from a test install: complete kit file list with a git-clone fallback; cleanup list when nobody reaches `silent_after_days`; first-run classification uses `about_me` (no past decisions yet) and a tighter `disputed_if`; suggestions live in `suggested_*` fields until confirmed; continuous queue day-ranges and per-goal weights; FOLLOWERS.md activity thresholds; state files `_state.json`, `_anchors.json`, `_build-log.md`; explicit X API limits; daily new-follow check against the full stored follow list.
