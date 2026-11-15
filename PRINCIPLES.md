# PRINCIPLES — the decisions and why they were made

These rules took shape while the kit was tried on a real account with ~350 follows over a couple of days. Each one came out of a concrete problem.

## 1. A card only if you follow them
**Decision.** A full card is created only for the core: mutuals and accounts you follow yourself.
**Why.** These are people you chose. "Everyone who ever liked a post" is noise.

## 2. The core and followers are kept separately
**Decision.** Followers produce exactly three lists, not a card for each person:
- `FOLLOWERS.md` — one roster of every follower (handle, a few words, activity). It is the counter used for "+N new, −M left" and for spotting mutuals.
- `ENGAGED.md` — people who interact with your posts, whether you follow them or not. A full card appears only if you confirm it, or they already gave a clear signal (they replied, mentioned you, or reposted you, you followed them back, or they are clearly in your field).
- `VERIFIED.md` — followers with an X verification badge, blue or higher (blue / X Premium, gold / business, gray / government), built from `verified` / `verified_type` on the same follower read.
**Why.** Followers are almost always weak ties. If there are thousands of them, reviewing each one is impossible, and reading each timeline is very expensive. A roster, a list of people who actually talk to you, and a list of verified accounts are enough.

## 3. On X, read only
**Decision.** The assistant does not post, like, follow, or unfollow. Only you unfollow.
**Why.** This is your voice and your reputation. A bot's mistake on X is visible to everyone and cannot be undone.

## 4. Only a fresh slice
**Decision.** For a card we take ~10 recent posts or 3–7 days, and we look up contact history with search — at most 2 pages per person per direction. For large accounts, the bio and the latest post are enough.
**Why.** Otherwise the daily X limits burn through on the first few dozen people. A fresh slice is enough to understand who they are and what they are doing now.

## 5. The bot fills in the objective, and a best guess for the rest
**Decision.** The assistant writes the profile, the history, the overlaps, and its best guess for value, next step, and group. You only step in to clarify disputed people, and to write notes.
**Why.** A first build that leaves most cards empty waiting for confirmation is too slow. The assistant can classify the obvious cases well enough; you correct the ones that actually need a person.

## 6. Click, don't type
**Decision.** Values are chosen from fixed lists, and each value has a default next step. On the first build the assistant fills `value` and `next_action` for everyone with its best guess and marks the card `auto: …`. When it later shows a disputed person, it may put an alternative in `suggested_value` / `suggested_next` / `suggested_group` for you to click. Answers are accepted in any form: by number, by voice, or as ready-made lines from the table.
**Why.** After a few dozen people, answers start to repeat. The list and the default values turn a clarification into 2–3 minutes a day.

## 7. Auto-classification; the person only sees disputed cases
**Decision.** The assistant classifies everyone automatically in the background, including on the first run. It fills `value`, `next_action`, and `group` with its best guess (noted `auto: …`). It never sets close relationships, collabs, or DMs itself: for those it uses a conservative pair and flags the person as disputed, optionally putting the stronger guess in the suggested fields. It only shows you the disputed ones, later, in small batches, with two-way contacts first.

A person is **disputed** only when the classification is genuinely uncertain or the relationship decision belongs to you:
- 2 or more two-way touches (replies in both directions, or a conversation);
- off-niche, but with a real history (2+ two-way touches, a DM you pasted, or notes that you know them);
- two auto-rules disagree, or the person may be someone you know.

These are **not** disputed:
- a single tag, mention, or one reply, and nothing else;
- active (posted within 14 days, the same threshold as in `FOLLOWERS.md`) but off-niche, with no real history — those go to the unfollow list, or to `bots/` if they look like a farm.

On a first run there are no past decisions, so it relies on the `about_me` niche rules only — but it still classifies everyone, it does not leave niche matches waiting as suggestions.
**Why.** Leaving most of the core empty for a daily review was too slow. Disputed people are few, and decisions about people you talk to stay with you.

## 8. Project accounts are a special type
**Decision.** Official accounts of companies, products, and media (for example, @github) that match your interests get signal and "just read". A collab is never proposed to them. Official accounts that do **not** match your interests get no automatic signal / just-read: they go to the unfollow list as candidates. Touches with a project account are logged only on that project card, not on a person.
**Why.** These are not people: useful updates are worth reading, and there is no need to befriend them. Accounts you followed for a topic you no longer care about should be easy to prune. Replies to a project account belong on that account's card.

## 9. Quarantine is the unfollow list
**Decision.** `QUARANTINE.md` is the unfollow list. The assistant puts only real candidates there and shows them as a single list; you decide. Candidates are:
- long-AFK accounts (silent longer than `silent_after_days`; if nobody reaches that, the fallback is `silent_soft_days`);
- suspected bots (also stored in `bots/`, one cluster named "bots", with a minimal card: handle, why suspected, follower count, last post) — bots go on this list automatically;
- people who no longer match your interests;
- project accounts that do not match your interests.

If there are no candidates, the assistant says so. It does not pad the list with the quietest accounts or "keep" rows. After an unfollow, the card goes to the archive instead of being deleted. Appearing on this list counts as "shown" in `_review-log.json`.
**Why.** "Quiet" does not always mean "useless", and a padded list of mostly-active people is noise. The archive keeps a memory of who they were.

## 10. "Wait for wake-up" is not quarantine
**Decision.** A separate category for sleeping accounts, kept in `WATCHLIST.md`. These are accounts that are quiet now, but if they start posting, something is happening in the field. Every morning they are checked with one batched profile request, using the id of the latest post. If several wake up at once, that is a signal of its own.
**Why.** The most useful finding of the project. Such accounts are easy to unfollow by mistake, and their return is an early indicator. The check is almost free.

## 11. Stay silent if there is nothing to say
**Decision.** In steady mode the assistant writes only if there is a reason: a watchlist account woke up, people from this week's queue, a new substantive engaged person, or disputed accounts to clarify. One improvement question of the day is attached to that message, not sent alone.
**Why.** A daily empty briefing quickly becomes noise, and people stop reading it.

## 12. Every handle is a link
**Decision.** In any list, the handle is given as a link to `https://x.com/handle`.
**Why.** To remember a person, you almost always need to open their profile. One click instead of a search.

## 13. Ask about goals first
**Decision.** On the first run the assistant asks a few short questions: niche and topics, goals for the network, what you want to grow, which people are a priority, the language, and when you want the daily briefing (time, timezone) and the weekly digest (day and time). Defaults: daily 09:00 local, weekly Sunday 18:00. Answers 1–4 go to CONFIG (`about_me`) and drive classification and priority. The language goes to `language`, and the schedule to `schedule.daily` and `schedule.weekly`, and the routines are created with those times.
**Why.** Who matters depends on what you are doing. If you make indie games, people who post quality work in that niche matter more than the biggest accounts in tech. Without goals, the assistant can only guess from follower counts. Briefings should arrive when the owner actually has time to look at them.

## 14. One touch history, filled from your side
**Decision.** Each card has one living Touch history section and a derived `last_touch` date. New touches come from reading your own new posts and mentions (2–3 reads a day), not from each person's timeline. Lookups of past contact are limited to 2 pages per person per direction. Touches with a project account count only on that project card. DMs only if you paste them.
**Why.** "When did we last talk" is the most useful field for keeping relationships alive, and reading it from your own side costs almost nothing.

## 15. A short weekly queue instead of "N new people a day"
**Decision.** Once the first build has classified the core, a weekly queue of 7–10 people worth engaging with is scored by value, next step, niche, your notes, two-way (warm) contact, and days since the last touch (every day-range is covered, with no gaps). Each of your goals adds its own bonus, scaled by the order you gave them — including a bonus for the support goal. The ideas goal must not add `value.ideas` again (that score already lives in `value`). Warm contacts (2+ two-way touches) always outrank strangers. Strangers and other people without a confirmed core card stay out of the queue (they live in `ENGAGED.md` until you confirm a card). If an unconfirmed person has to be mentioned at all, they get a clear marker and are still not scored into the queue. The assistant never sends ready-made text on the owner's behalf. The assistant suggests; you talk. Each morning shows 1–3, with why and an idea of what to write about.
**Why.** After the first build there is little left to classify, but there are always people you meant to reply to and forgot. A short rotating list keeps that manageable, and it should surface people you already talk to before people you do not know.

## 16. Engaged people are a separate light layer
**Decision.** People who interact with your posts (even if you don't follow them) go to `ENGAGED.md`, split into substantive and wow. Strangers — people you don't follow who engage — stay in that list for you to review. They do not enter the contact queue until you confirm a card. The best substantive ones are suggested for a full card. This is the same "signal" that promotes a follower; there is no second rule.
**Why.** New good contacts often come to you first. Splitting substance from applause shows who is worth a look without reviewing every reply or bloating the queue with strangers.

## 17. A weekly digest, not a daily feed
**Decision.** Strong posts from priority people go to the weekly digest, not the morning briefing. Once a week: a data refresh, those posts, sleeping accounts that woke up, top engaged, next week's queue, and 3–5 improvement questions. The same weekly follower read also rebuilds `FOLLOWERS.md` and `VERIFIED.md`. Built from batched lookups that include the latest post.
**Why.** The point of the card file is that good posts from chosen people don't get lost. Weekly is enough, and batched lookups keep it cheap. The morning stays a short action list, not a feed.

## 18. Keep improving with small questions
**Decision.** The daily briefing carries at most one question of the day; the weekly digest ends with 3–5. Both are click cards built from real data (who was useful, who to raise, who could be a partner, disputed accounts, occasionally goals). Asked questions are logged and never repeated.
**Why.** A base built once goes stale. Tiny, regular corrections keep it aligned with what the owner actually values, without a big review session.

## Next (roadmap)
- **Done:** the weekly digest with data refresh and improvement questions, touch history, the priority queue, and the engaged layer.
- **Deferred:** network roles (connector / knowledge holder / bridge), "new follows of your priority people", and cluster visualization. They need a who-talks-to-whom graph or many reads.
- Every N weeks, refresh old cards from a fresh slice.
- Send answers directly from the page, without copying lines.
- Tell a real person from a spam farm more accurately.
