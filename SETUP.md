# SETUP: step by step

Your part takes about 5 minutes. The assistant does the rest, and the first build usually runs in the background for 20 to 60 minutes.

## 1. What you need

- An AI assistant that can:
  - read X: profiles, posts, search, and follow lists (through an API or a connector);
  - store files (a `people/` folder, or a private repo, see [GITHUB.md](GITHUB.md));
  - run scheduled tasks (routines);
  - ideally, make a web page or a table with buttons.
- This kit.

## 2. Fill in CONFIG

Copy `CONFIG.example.md` to `CONFIG.md`. The only required field is:
- `my_handle`: your X handle.

Everything else can wait. Groups can be filled in now or later (examples for many fields are in the same file). Section 0 (`about_me`), `language`, `timezone`, and `schedule` are filled in by the assistant from your answers in the next step. Defaults: daily briefing at 09:00 local time, weekly digest on Sunday at 18:00.

## 3. Onboarding questions (the assistant asks, you answer)

On the very first run, before it touches X, the assistant asks six short questions. You can answer in a few words or by voice:

1. **Your niche.** What field are you in, and which topics do you want to see more of? ("indie game development", "children's book illustration", "B2B SaaS for dentists")
2. **Goals for your network.** What do you want from it, most important first: ideas, collabs, audience growth, or just reading?
3. **What you want to grow.** One skill or area you want to get better at. ("game design", "writing", "fundraising")
4. **Priority people.** What kind of people matter most to you? ("builders who ship and post their process", "editors at small presses")
5. **Language.** Which language should briefings and notes be in?
6. **Schedule.** When do you want the daily briefing (time and timezone)? Which day and time do you want the weekly digest? Defaults: 09:00 daily, Sunday at 18:00.

Where the answers go:
- Answers 1–4 go to `about_me` (CONFIG section 0). They drive classification and priority. For example, if you make indie games, people who post quality work in that niche get high priority, and generic news accounts get "just read" — or go to the unfollow list if they are off-niche.
- Answer 5 goes to `language`.
- Answer 6 goes to `timezone`, `schedule.daily`, and `schedule.weekly`. The routines are created at those times.

You can redo the questions any time by saying "let's redo the onboarding questions".

## 4. Setup prompt

Copy this into a chat with your assistant:

```text
I want to set up a personal CRM of my network on X. I have attached the People CRM kit files:
README, PRINCIPLES, CONFIG, TEMPLATE-card, TEMPLATE-lists, routine-prompt. Read them and follow them strictly.

My account: {{my_handle}}.

Please do the following:
0. Before anything else, ask me the onboarding questions (routine-prompt.md, section 0) in one short
   numbered message and wait for my answers. Write answers 1–4 into CONFIG.md section 0 (about_me),
   answer 5 into language, answer 6 into timezone, schedule.daily and schedule.weekly.
   Defaults if I skip a question: daily 09:00 local, weekly Sunday 18:00.
1. Create the folder {{data_folder}} and save CONFIG.md there.
2. Take the list of accounts I follow and my followers.
   - The core = mutuals + accounts I follow. Create a card for each one using TEMPLATE-card,
     and keep INDEX.md with one line per card (handle as a link, group, value, next_action).
   - Do NOT turn non-mutual followers into cards. Followers produce exactly three lists
     (see TEMPLATE-lists): FOLLOWERS.md (one roster of every follower: "@handle — a few words
     from the bio — active|rare|silent", using profile fields only, without reading their
     timelines; this is the counter for +N/−M and mutuals), ENGAGED.md (people who interact
     with my posts, follower or not), and VERIFIED.md (followers with an X verification badge,
     blue or higher, from the verified / verified_type fields on the same follower read:
     handle link, badge type, followers count, follows back / mutual, short bio).
   - Fill each card's Touch history and last_touch cheaply: read MY recent posts and MY mentions
     (a few pages), not each person's timeline. Combine touch-history searches into one OR query
     per direction (me → them, and them → me), and limit them to 2 pages per person per direction.
     Touches with a project account count only on that project card, not on a person.
   - Put obvious bots and spam farms in a separate bots/ folder, all in one cluster named "bots",
     with a minimal card (handle, why suspected, follower count, last post). Add them to
     QUARANTINE.md automatically. Mark the reason as a guess.
   - Persist the follow list (every handle I follow) in _state.json, along with
     follow_list_complete (true if every follow is stored; false for a capped or test run),
     since_ids, and reads used. Write a short first-build log to _build-log.md. Keep
     latest-post ids in _anchors.json.
3. Respect X rate limits (SETUP.md section 6): for each card take only a fresh slice
   (the last ~{{fresh_slice_posts}} posts or {{fresh_slice_days}} days), look up our contact history
   with targeted searches (one OR query per direction, at most 2 pages per person per direction),
   and for large accounts ({{big_account_followers}}+) skip the timeline slice — the bio and the
   latest post are enough. Tell me how many reads you used.
4. On X you only read: do not post, reply, like, repost, follow, unfollow, or send DMs.
5. Apply the auto-classification rules from CONFIG section 8. On a first run there are no past
   decisions: use about_me niche rules only, but still classify everyone. Fill value / next_action
   / group with your best guess and mark "auto: …". Never set never_auto values yourself (use a
   conservative pair and flag the person disputed; you may put the stronger guess in suggested_*).
   A person is disputed only if they match disputed_if. Active (posted within 14 days) but
   off-niche, with no real history, is not disputed: they go to the unfollow list or to bots/.
   Off-niche project accounts get no automatic signal / just-read: they go to the unfollow list.
   Put everyone with "wait for wake-up" into WATCHLIST.md: handle, date and id of the latest post.
   QUARANTINE.md is the unfollow list (handle as a link, reason, date): long-AFK accounts
   (quiet > {{silent_after_days}} days, or {{silent_soft_days}} if nobody reaches that), bots,
   people who no longer match my interests, and project accounts that do not match my interests.
   Only real candidates; if there are none, say so. Do not pad the list with the quietest accounts
   or "keep" rows.
6. First, show me the unfollow list. Log everyone on it as shown in _review-log.json.
7. After that, only show me disputed people, in small batches, two-way contacts first.
   For each one: the handle as a link to x.com, one line on who they are, what happened between
   us, and your suggested value / next_action / group (you may use suggested_* for the alternative).
   If you can, make a table page with buttons and a "What will go to chat" block with ready-made lines
   like `@handle | value=… | next=… | group=… | note=…`.
8. Accept short answers: "3 ok", "5 unfollowed", "everyone from {{group}}: vibes, just read",
   including voice messages and typos. Only ask again if something is unclear. Everything I tell you
   about a person goes into "My notes".
9. When I say "unfollowed", set next_action to "unfollowed" and value to none, update follow,
   and move the card to _unfollowed-archive/ (do not delete it).
10. Create ENGAGED.md and the first QUEUE.md (CONFIG sections 10–11 and TEMPLATE-lists).
    Strangers in ENGAGED.md do not enter the queue until I confirm a card.
11. When the first pass is done, create the daily briefing and the weekly digest from routine-prompt.md
    at schedule.daily and schedule.weekly (in timezone).
```

## 5. Adapting it to yourself

### Circles (`circle`)
Circles show how close someone is to you. Defaults: `horizon` (you simply follow them) → `learning` (you read them for value) → `work` (you talk about work) → `friends` (you know them outside X). Rename them if you like, for example "far / near / close".

### Value (`value`)
Value answers why this person matters to you. The defaults are `ideas`, `signal`, `vibes`, `collab`, `support`, and `none`, which is usually enough. You can add your own, for example `clients` for a freelancer or `sources` for a journalist. If you do, add a matching pair to `defaults`.

### Groups (`group`)
Groups are your clusters, and they are the most important setting. Tips:
- one group should be one clear batch of people that you can classify with a single phrase;
- keep the utility groups `project account`, `for the algorithm`, and `bots`, since they are useful for anyone;
- if several groups always get classified the same way, merge them into one (for example "platform A / platform B");
- niche examples for many fields are in `CONFIG.example.md`.

### Sleeping accounts ("wait for wake-up")
These are accounts that are quiet now but whose return would be news in itself: an opinion leader in your field who went quiet, a frozen project, a former competitor, an author who disappeared for a year. This is not quarantine. You don't unfollow them; they go on `WATCHLIST.md`. Checking them is cheap: one batched profile request each morning.

## 6. X rate-limit rules (important)

- Don't download the full history of any account, or you will burn through the daily limit.
- For a card, take a fresh slice: about 10 posts or 3–7 days.
- Look up contact history with search, not by reading timelines. Combine touch-history searches into one OR query per direction (you → them, and them → you). Limit them to 2 pages per person per direction (`touch_history_max_pages`). Touches with a project account count only on that project card.
- For large accounts (50k+ followers by default), skip the timeline slice: the bio and the latest post are enough.
- For followers and sleeping accounts, read only profile fields: bio, post count, and the ID of the latest post. Fetch a timeline only for accounts that have woken up. The weekly follower read also rebuilds `FOLLOWERS.md` and `VERIFIED.md` (from `verified` / `verified_type`); no extra timeline reads.
- On Grok Bot's X tools, each call returns at most 25 results. Large responses may be truncated — write them to a file and read from the file, do not guess the missing part. Pace yourself: about 30 reads per minute, and 1000 reads per day per user. Batch profile lookups (about 100 handles per call) and wait between batches.
- Persist the follow list in `_state.json` and set `follow_list_complete: true` when every handle they follow is stored. The daily new-follow check compares against that stored list, not against a truncated first-N page of the API. If `follow_list_complete` is `false` (a capped or test run), the check only compares against the stored subset and must say so.
- As a rough guide, a first build of 50 follows took about 55 reads and about 11 minutes; about 430 cards cost 300–350 reads. Set your own limit in `daily_read_budget`.

## 7. The routines

Paste [routine-prompt.md](routine-prompt.md) to your assistant. It fills in the values from `CONFIG.md` and creates:

1. **The daily briefing** at `schedule.daily`. One short message, and only when there is a reason. In order, it includes sleeping accounts that woke up; 1–3 people from this week's queue, with why and an idea of what to write about (never ready-made text); new substantive engaged people; 3–5 disputed accounts to answer by number (two-way contacts first); and one improvement question of the day. While a disputed backlog remains, lead with up to {{batch_initial}} of them. If there is nothing to report, the assistant stays silent.
2. **The weekly digest** at `schedule.weekly`. It starts with a data refresh (follows, followers, and profile fields; the same follower read rebuilds `FOLLOWERS.md` and `VERIFIED.md`), then covers strong posts from your priority people, sleeping accounts that woke up, the top engaged (substantive vs wow), and next week's queue, and it ends with 3–5 improvement questions.

### How it stays cheap

- **Touches** come from your side: your new posts and your mentions since the last run, 2–3 reads a day. Quotes of your posts are checked once a week, and only for posts whose quote count went up. Past-contact searches are capped at 2 pages per person per direction.
- **The queue** is computed locally from confirmed core cards (value, next_action, niche, your notes, two-way contact, days since `last_touch`), with no X reads. Strangers in `ENGAGED.md` stay out until you confirm a card.
- **Engaged** comes from the same mentions and quotes, with no extra reads.
- **The digest and refresh** use batched profile lookups that include each person's latest post (about 1 read per 100 people), plus a fresh slice for the top 10 only. `VERIFIED.md` uses fields already on the follower profile.

## 8. FAQ

**Do I need to review followers?** No. Non-mutual followers are almost always weak ties. They live in three lists: a roster (`FOLLOWERS.md`), people who interact with you (`ENGAGED.md`), and verified followers (`VERIFIED.md`). A full card appears only once they show themselves, or you confirm one from the engaged list.

**The assistant put someone I know into bots.** Say "I know this person", and the card moves back to the core and off the unfollow list.

**How do I unfollow from the list?** The assistant gives you a list of links (`QUARANTINE.md`), and you unfollow on X yourself. Then write "unfollowed 1, 4, 7". X does not notify people when they are unfollowed.

**Will the assistant reply to people from the queue for me?** No. It only suggests who to reply to and why. You write on X yourself.

**Why is someone I never talk to in "Engaged"?** Because they interact with your posts. If their replies are substantive, the assistant may suggest moving them to the core. Until you confirm a card, they stay on that list and out of the contact queue. The decision is yours.

**Can I change my goals later?** Yes. Say "let's redo the onboarding questions", and the queue and classification will follow your new answers.

**Can I do this without a table?** Yes. Everything works in chat, with batches of 5 people and answers by number.
