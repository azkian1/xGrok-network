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
- Answers 1–4 go to `about_me` (CONFIG section 0). They drive classification and priority. For example, if you make indie games, people who post quality work in that niche get high priority, and generic news accounts get "just read".
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
   - Do NOT turn non-mutual followers into cards: put them in a single file FOLLOWERS.md,
     one line "@handle — a few words from the bio — active|rare|silent",
     using profile fields only, without reading their timelines.
   - Fill each card's Touch history and last_touch cheaply: read MY recent posts and MY mentions
     (a few pages), not each person's timeline. Combine touch-history searches into one OR query
     per direction (me → them, and them → me).
   - Put obvious bots and spam farms in a separate bots/ folder and mark them as a "guess".
   - Persist the complete follow list (every handle I follow) in _state.json, along with since_ids
     and reads used. Write a short first-build log to _build-log.md. Keep latest-post ids in _anchors.json.
3. Respect X rate limits (SETUP.md section 6): for each card take only a fresh slice
   (the last ~{{fresh_slice_posts}} posts or {{fresh_slice_days}} days), look up our contact history with targeted
   searches (one OR query per direction), and for large accounts ({{big_account_followers}}+) skip the
   timeline slice — the bio and the latest post are enough. Tell me how many reads you used.
4. On X you only read: do not post, reply, like, repost, follow, unfollow, or send DMs.
5. Apply the auto-classification rules from CONFIG section 8 (project accounts, long-silent accounts,
   "wait for wake-up"). On a first run there are no past decisions: use about_me niche rules only.
   A single tag, mention, or one reply is not enough to mark someone disputed (see disputed_if).
   For obvious auto cases, fill value / next_action and mark "auto: …". For everyone else, write
   suggested_value, suggested_next, and suggested_group, and leave value / next_action empty until I confirm.
   Put everyone with "wait for wake-up" into WATCHLIST.md: handle, date and id of the latest post.
   Keep quarantine as a list in QUARANTINE.md (handle as a link, reason, date).
6. First, show me the {{first_cleanup_batch}} longest-quiet accounts as a single list.
   If nobody is quieter than {{silent_after_days}} days, still show the quietest N, tell me that
   in one line, and suggest quarantine only for those quieter than {{silent_soft_days}} days
   AND off-niche; the rest are "keep".
7. After that, only show me disputed or unclear cases (review mode = cards with suggestions
   not yet confirmed). For each one: the handle as a link to x.com, one line on who they are,
   what happened between us, and your suggested value / next_action / group.
   If you can, make a table page with buttons and a "What will go to chat" block with ready-made lines
   like `@handle | value=… | next=… | group=… | note=…`.
8. Accept short answers: "3 ok", "5 unfollowed", "everyone from {{group}}: vibes, just read",
   including voice messages and typos. Only ask again if something is unclear. Everything I tell you
   about a person goes into "My notes".
9. When I say "unfollowed", set next_action to "unfollowed" and value to none, update follow,
   and move the card to _unfollowed-archive/ (do not delete it).
10. Create ENGAGED.md (CONFIG section 11) and the first QUEUE.md (CONFIG section 10), using TEMPLATE-lists.
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
- keep the utility groups `project account` and `for the algorithm`, since they are useful for anyone;
- if several groups always get classified the same way, merge them into one (for example "platform A / platform B");
- niche examples for many fields are in `CONFIG.example.md`.

### Sleeping accounts ("wait for wake-up")
These are accounts that are quiet now but whose return would be news in itself: an opinion leader in your field who went quiet, a frozen project, a former competitor, an author who disappeared for a year. This is not quarantine. You don't unfollow them; they go on `WATCHLIST.md`. Checking them is cheap: one batched profile request each morning.

## 6. X rate-limit rules (important)

- Don't download the full history of any account, or you will burn through the daily limit.
- For a card, take a fresh slice: about 10 posts or 3–7 days.
- Look up contact history with search, not by reading timelines. Combine touch-history searches into one OR query per direction (you → them, and them → you).
- For large accounts (50k+ followers by default), skip the timeline slice: the bio and the latest post are enough.
- For followers and sleeping accounts, read only profile fields: bio, post count, and the ID of the latest post. Fetch a timeline only for accounts that have woken up.
- On Grok Bot's X tools, each call returns at most 25 results. Large responses may be truncated — write them to a file and read from the file, do not guess the missing part. Pace yourself: about 30 reads per minute, and 1000 reads per day per user. Batch profile lookups (about 100 handles per call) and wait between batches.
- Persist the complete follow list in `_state.json`. The daily new-follow check compares against that full stored list, not against a truncated first-N page of the API.
- As a rough guide, a first build of 50 follows took about 55 reads and about 11 minutes; about 430 cards cost 300–350 reads. Set your own limit in `daily_read_budget`.

## 7. The routines

Paste [routine-prompt.md](routine-prompt.md) to your assistant. It fills in the values from `CONFIG.md` and creates:

1. **The daily briefing** at `schedule.daily`. It has two modes:
   - **Review mode**, while the core still has cards whose suggestions are not yet confirmed (`value` / `next_action` empty): {{batch_initial}} people a day, plus a table.
   - **Steady mode**, once the core is done: one short message, and only when there is a reason. In order, it includes sleeping accounts that woke up; 1–3 people from this week's queue, with why and an idea of what to write about (never ready-made text); new substantive engaged people; 3–5 unclear accounts to answer by number; and one improvement question of the day. If there is nothing to report, the assistant stays silent.
2. **The weekly digest** at `schedule.weekly`. It starts with a data refresh (follows, followers, and profile fields), then covers strong posts from your priority people, sleeping accounts that woke up, the top engaged (substantive vs wow), and next week's queue, and it ends with 3–5 improvement questions.

### How it stays cheap

- **Touches** come from your side: your new posts and your mentions since the last run, 2–3 reads a day. Quotes of your posts are checked once a week, and only for posts whose quote count went up.
- **The queue** is computed locally from the cards (value, next_action, niche, your notes, days since `last_touch`), with no X reads.
- **Engaged** comes from the same mentions and quotes, with no extra reads.
- **The digest and refresh** use batched profile lookups that include each person's latest post (about 1 read per 100 people), plus a fresh slice for the top 10 only.

## 8. FAQ

**Do I need to review followers?** No. Non-mutual followers are almost always weak ties. They live in a single list and only get a full card once they show themselves.

**The assistant put someone I know into bots.** Say "I know this person", and the card moves back.

**How do I unfollow from quarantine?** The assistant gives you a list of links, and you unfollow on X yourself. Then write "unfollowed 1, 4, 7". X does not notify people when they are unfollowed.

**Will the assistant reply to people from the queue for me?** No. It only suggests who to reply to and why. You write on X yourself.

**Why is someone I never talk to in "Engaged"?** Because they interact with your posts. If their replies are substantive, the assistant may suggest moving them to the core. The decision is yours.

**Can I change my goals later?** Yes. Say "let's redo the onboarding questions", and the queue and classification will follow your new answers.

**Can I do this without a table?** Yes. Everything works in chat, with batches of 5 people and answers by number.
