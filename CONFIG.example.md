# CONFIG — People CRM settings

Copy this file to `CONFIG.md` and adapt it to yourself. The assistant reads it before every review and every morning routine. If you change something, just tell it "re-read CONFIG".

## 0. About you (onboarding answers)

On the first run the assistant asks you six short questions (see `SETUP.md`, section 3) and writes answers 1–4 here. You can also fill this in yourself. These answers decide who gets high priority: if you make indie games, people who post quality work in that niche rank above generic news accounts. The language answer goes to `language` and the scheduling answer to `timezone` / `schedule` (both in section 1), not here.

```yaml
about_me:
  niche: ["{{your field}}", "{{a sub-topic}}"]     # e.g. ["indie games"], ["indie publishing"], ["B2B SaaS"]
  topics: ["{{topic 1}}", "{{topic 2}}", "{{topic 3}}"]   # what you want to see more of
  goals:                                            # what you want from your network, most important first
    - ideas            # finding ideas for your work and posts
    - collabs          # people to build or create with
    - audience         # growing your own audience: reply to the right people
    - reading          # just keeping up, no interaction needed
  grow: "{{a skill or area you want to get better at}}"   # e.g. "game design", "writing threads", "fundraising"
  priority_people: "{{who matters most}}"           # e.g. "builders who ship and post their process"
  not_interested: ["{{topic you want to ignore}}"]  # e.g. ["price talk", "politics"]
```

The scheduling question — "When do you want the daily briefing (time, timezone)? Which day and time for the weekly digest?" — is stored in section 1 as `timezone`, `schedule.daily`, and `schedule.weekly`. Defaults if you skip it: daily 09:00 local, weekly Sunday 18:00. Routines are created with those times.

How the assistant uses this:
- **Classification.** A person whose posts match `niche` / `topics` gets value `ideas` or `signal` (filled in automatically, noted `auto: …`) and the group for that niche. Clearly off-niche people, or people matching `not_interested`, go to the unfollow list as candidates (you still decide). On a first run there are no past decisions: use these niche rules only, but still classify everyone.
- **Priority queue.** People in your niche get a bonus (see section 10). Each goal in `goals` adds its own `goal_bonus`, scaled by position (first = full weight, later ones less) — not only the goal that comes first. The ideas goal does not add `value.ideas` again. If `reading` is among the goals, the queue stays shorter and the digest matters more.
- **Digest.** Strong posts are picked "by meaning for you": `niche`, `topics`, and `grow` come first, likes and bookmarks are only a hint.
- Re-answer any time: say "let's redo the onboarding questions".

## 1. Account and time

```yaml
my_handle: "@your_handle"          # your handle on X
timezone: "UTC"                    # your IANA time zone, e.g. "America/New_York" (from the scheduling question)
schedule:
  daily: "09:00"                   # daily briefing time, local; default 09:00
  weekly: "sunday 18:00"           # weekly digest day and time; default Sunday 18:00
language: "en"                     # language for briefings and notes (onboarding question 5)
data_folder: "people/"             # where the assistant stores the cards
```

`schedule.daily` and `schedule.weekly` are set from the onboarding scheduling question. The morning routine and the weekly digest are created at these times. If you change them later, tell the assistant to move the routines.

## 2. Batch sizes and limits

```yaml
batch_initial: 10          # how many disputed people a day while the disputed backlog is being cleared
batch_steady: 5            # max new people a day in steady mode (new follows only; the daily "who to talk to" comes from the queue)
first_cleanup_batch: 30    # max unfollow candidates to show in one list (never pad with non-candidates)
silent_after_days: 365     # quiet longer than this → a unfollow candidate
silent_soft_days: 180      # fallback AFK threshold if nobody reaches silent_after_days
fresh_slice_posts: 10      # how many recent posts to read for a card
fresh_slice_days: "3-7"    # or how many days (fewer for active accounts)
big_account_followers: 50000   # for large accounts, the bio and the latest post are enough
daily_read_budget: 1000    # daily read limit of your X access (set your own)
stay_silent_if_nothing: true   # don't write if nothing is new
touch_history_max_pages: 2 # max search pages per person per direction (you → them, them → you)
```

## 3. Circles (circle): how close someone is

Rename these however you like; the important thing is to have 3–4 circles.

```yaml
circles:
  horizon:  "you simply follow them, you read them occasionally"
  learning: "you read them for ideas, knowledge, and news"
  work:     "you talk about work: colleagues, clients, partners"
  friends:  "you know them outside X: DMs, messenger, real life"
```

## 4. Value (value): why this person matters to me

```yaml
values:
  ideas:   "gives me ideas for my work and posts"
  signal:  "notices what matters in my field earlier than others"
  vibes:   "pleasant to read, my scene, no practical use"
  collab:  "we could make something together"
  support: "supports me, helps, is close as a person"
  none:    "no use"
```

## 5. Next step (next_action): only from this list

```yaml
next_actions:
  - just read
  - reply sometimes
  - send a DM
  - propose a collab
  - do nothing
  - quarantine          # a candidate to unfollow; you decide
  - unfollowed          # you unfollowed them; the card goes to the archive
  - wait for wake-up    # a sleeping account on the watchlist; we watch for activity
```

## 6. Default pairs value → next_action

On the first build the assistant fills `value` / `next_action` / `group` for everyone with its best guess and marks the card `auto: …`. When it later shows a disputed person, it may put an alternative in `suggested_value` / `suggested_next` / `suggested_group` for you to click.

```yaml
defaults:
  none:    quarantine        # if they are someone you know, then "do nothing"
  vibes:   just read
  ideas:   just read
  signal:  just read
  collab:  propose a collab
  support: reply sometimes
```

## 7. Groups (group): your clusters

Groups let you classify people in a batch, for example "everyone from my previous team: vibes, just read". Fill in your own. Below are examples for different fields; keep the ones that fit and delete the rest.

```yaml
groups:
  # general, useful for anyone
  - "{{my team}}"
  - "{{previous job}}"
  - "{{my project}}"
  - "{{my community / course / club}}"
  - "project account"      # utility group, see the rules below
  - "for the algorithm"    # you follow them so the feed shows a topic you care about
  - "bots"                 # suspected bots and spam farms; stored in bots/, also on the unfollow list

# niche examples (uncomment the ones that fit you):
#  design:     "UI/UX", "illustration", "design tools", "art directors"
#  writers:    "editors", "publishers", "literary magazines", "newsletters"
#  founders:   "investors", "founders at my stage", "SaaS", "accelerators"
#  gamedev:    "indie developers", "engines and tools", "game jams"
#  marketing:  "content", "SEO", "growth", "brands"
#  science:    "my lab", "journals", "conferences"
#  AI:         "researchers", "AI tools", "labs"
#  finance:    "analysts", "fintech", "markets"
#  education:  "teachers", "edtech", "researchers"
#  local:      "my city", "local business", "events"
```

## 8. Auto-classification rules

The assistant classifies everyone automatically in the background, including on the first run. It only shows you the disputed cases, later, in small batches.

```yaml
auto_rules:
  classify_everyone: true   # fill value / next_action / group with a best guess; mark "auto: …"
  first_run: "no past decisions yet; use about_me niche / topics / not_interested only, but still classify everyone"

  project_accounts:
    # official accounts of companies, products, platforms, media (example: @github)
    detect: "the bio has 'official', 'we', a product or company name, a product link, and no personal name"
    if_matches_interests: { value: signal, next_action: just read, group: "project account" }
    if_off_niche: { next_action: quarantine, group: "project account" }  # unfollow-list candidate; no automatic signal / just-read
    never: [collab, "propose a collab", "send a DM"]
    touches: "log only on the project card, not on a person"

  silent_long:
    # long-AFK accounts become unfollow candidates
    set: { next_action: quarantine }
    show_as: "as a single unfollow list for confirmation, not one by one"
    threshold: "quiet longer than silent_after_days"
    fallback_threshold: "if nobody reaches silent_after_days, use silent_soft_days"
    exception: "if their return would be news (see watch_for_wakeup), suggest 'wait for wake-up' instead"
    if_none: "say so; do not pad the list with the quietest accounts or 'keep' rows"
    log_as_shown: true      # appearing on the unfollow list counts as shown in _review-log.json

  off_interest:
    # people or project accounts that no longer match about_me.niche / topics, or that match not_interested
    set: { next_action: quarantine }
    not_disputed: true      # this is a cleanup candidate, not a disputed person

  bots:
    detect: "template replies, very high posting volume, shilling, clickbait hooks, mutual engagement pods (see a farm-detector if you have one)"
    store: "bots/ (one cluster named bots)"
    card: "minimal: handle, why suspected, follower count, last post"
    set: { group: "bots", next_action: quarantine }  # automatically on the unfollow list
    always_a_guess: true

  watch_for_wakeup:
    # sleeping accounts: they are quiet, but their return is a signal in itself (kept in WATCHLIST.md)
    enabled: true
    label: "sleeping accounts"      # rename if you like
    examples: "a former opinion leader in your field, a shut-down project, an old competitor, an author who has gone quiet"
    set: { value: signal, status: passive, next_action: wait for wake-up }
    check: "every morning with one batched profile request, compare the id of the latest post"
    alert_if_many: 2     # if ≥ N wake up at once, mark "something is happening in the field"

  by_past_decisions:
    # if similar people have already been classified by you, use the same values
    # On a first run there are no past decisions: skip this rule and classify from about_me only.
    first_run: "no past decisions yet; use about_me only, but still classify everyone"
    confidence: high_only
    note_prefix: "auto: "

  never_auto:
    # the assistant never sets these itself; use a conservative pair (ideas or signal / just read) and flag the person disputed; the stronger guess may go in suggested_*
    values: [collab, support]
    next_actions: ["send a DM", "propose a collab", "unfollowed"]

  disputed_if:
    - "2 or more two-way touches (replies in both directions, or a conversation)"
    - "off-niche, but with a real history (2+ two-way touches, a DM you pasted, or notes that you know them)"
    - "two auto-rules disagree, or the person may be someone you know"
  not_disputed_if:
    - "a single tag, mention, or one reply, and nothing else"
    - "active (posted within 14 days) but off-niche, with no real history — unfollow list or bots/, not disputed"
  batch_order: "two-way contact first, then the rest"
```

"Active" here means posted within 14 days, the same threshold as in section 9. Do not use a separate "very active" label. High-volume off-niche accounts with no real history go to the unfollow list, or to `bots/` if they look like a farm — not to the disputed backlog.

## 9. Followers: three lists

Followers do not each get a card. They produce exactly three lists.

```yaml
followers:
  lists:
    - FOLLOWERS.md        # the roster and the counter: every follower, one line
    - ENGAGED.md          # people who interact with your posts, follower or not (section 11)
    - VERIFIED.md         # followers with an X verification badge, blue or higher
  mode: "one_list"            # FOLLOWERS.md is a single roster, no cards
  line: "@handle — a few words from the bio — active|rare|silent"
  activity:                   # from the latest-post date on the profile, no timeline
    active: "<= 14 days"
    rare: "15-180 days"
    silent: "> 180 days"
  promote_to_card_if:          # when a follower gets a full card
    - "ENGAGED.md status is 'move to the core' and you confirmed it"
    - "they replied to you, mentioned you, or reposted you"
    - "you followed them back"
    - "they are clearly in your field ({{your field}}) and active"
  bulk_review: "once a month, by eye, as a batch"
  refresh: "weekly, with the follower reconciliation in the digest"

verified:
  file: VERIFIED.md
  who: "followers with an X verification badge, blue or higher"
  badges:
    blue: "X Premium / blue check (verified is true, verified_type is empty or blue)"
    gold: "business (verified_type is Business)"
    gray: "government (verified_type is Government)"
  source: "the verified and verified_type fields on the follower profile, from the same weekly follower read — no extra timeline reads"
  refresh: "weekly, with the follower reconciliation"
  columns: ["handle (link to https://x.com/<handle>)", "badge type", "followers count", "follows back / mutual", "short bio"]
```

`FOLLOWERS.md` is the counter used for "+N new, −M left" and for spotting mutuals. `ENGAGED.md` is separate and includes people who interact with you even if they don't follow you. `VERIFIED.md` is only followers with a badge.

## 10. Priority queue: who to engage with this week

Once a week the assistant builds a short list (`QUEUE.md`) of people it makes sense to interact with this week: reply to a post, quote, or write. It only suggests who, why, and an idea of what to write about; it never sends ready-made text on your behalf. Every morning it shows 1–3 of them.

```yaml
queue:
  size: 10                     # people per week (7–10 works well)
  daily_pick: 3                # how many from the queue per morning (1–3)
  rebuild_on: "monday"
  exclude_next_actions: ["do nothing", "quarantine", "unfollowed", "wait for wake-up"]
  exclude_groups: ["project account", "bots"]
  exclude_unconfirmed: true    # no confirmed core card (value empty, or only suggested_*): stay out of the queue
  exclude_strangers: true      # people you don't follow stay in ENGAGED.md until you confirm a card
  score:                       # plain points, added up
    value:       { collab: 3, ideas: 2, support: 2, signal: 1, vibes: 0.5 }
    next_action: { "propose a collab": 3, "send a DM": 3, "reply sometimes": 2 }
    in_my_niche: 1             # groups / topics from about_me.niche
    my_notes: 0.5              # you wrote something about them
    warm_contact: 2            # 2+ two-way touches, or notes that you know each other / talked / worked together
    mutual_or_active: 0.5
    they_engage_with_me: 1     # they are in ENGAGED.md and already have a confirmed core card
    days_since_last_touch:     # continuous ranges, no gaps
      never: 0.5
      "0-6": -2
      "7-13": 0
      "14-29": 1
      "30-59": 2
      "60+": 2.5
    shown_last_2_weeks: -3     # so the list rotates
  # Applied for every goal in about_me.goals, scaled by position
  # (1st = ×1, 2nd = ×0.5, 3rd = ×0.25, 4th = ×0.1). Defined per goal, not per "starts with".
  # Do not add value.ideas again under the ideas goal: that score already lives in value.
  goal_bonus:
    ideas:    { "value.signal": 1 }
    collabs:  { "value.collab": 3, "next_action.propose a collab": 2, "next_action.send a DM": 2 }
    audience: { "next_action.reply sometimes": 2, they_engage_with_me: 1 }
    support:  { "value.support": 2, warm_contact: 1 }
    reading:  { "value.signal": 1, queue_size_factor: 0.7 }
```

In plain words: people who matter more to you, with a "talk to them" next step, from your niche, whom you already have a two-way history with, and whom you have not touched for a while come first. Warm contacts always outrank strangers. Every goal you listed adds its own bonus, strongest for the one you put first — including support. Unconfirmed people, if mentioned at all, get a marker and are still not scored into the queue.

## 11. Engaged: people who come to you

`ENGAGED.md` lists people, followed or not, who interact with your posts. A light card, not a full one. Strangers (people you don't follow) stay on this list for you to review and do not enter the contact queue until you confirm a card.

```yaml
engaged:
  window_days: 30
  min_interactions: 2          # replies, mentions, quotes of your posts within the window
  types:
    substantive: "a question, a thought, a quote with context; about 6+ words"
    wow: "emoji, 'cool', 'fire', very short reactions"
  statuses: ["just active", "worth a look", "move to the core"]
  suggest_move_if: "substantive, 3+ substantive interactions, no core card yet"
  skip: "accounts in bots/"
  keep_manual_fields: true     # status and notes you set are never overwritten
  strangers_stay_here: true    # no queue entry until you confirm a card
```

"Move to the core" is the same signal as in section 9 (followers): there is no separate rule. You decide; then the assistant creates a full card.

## 12. Weekly digest

```yaml
weekly_digest:
  enabled: true
  when: "schedule.weekly"          # use schedule.weekly from section 1; default Sunday 18:00
  who: "core with value signal / ideas / collab, without sleeping accounts and project accounts"
  method: "batched profile lookups with the latest post included; fresh slice only for the top 10"
  sections: ["strong posts and ideas from priority people", "sleeping accounts that woke up this week",
             "top engaged of the week: substantive / wow", "next week's queue"]
  data_refresh: true               # step 0: re-read follow lists and core profile fields in batches, no timelines
  refresh_also: ["FOLLOWERS.md", "VERIFIED.md"]  # same follower read, no extra timeline reads
  improvement_questions: 3-5       # one click card at the end; logged in _questions-log.json, never repeated
  read_budget: 100
```

Strong posts from priority people go here, not in the morning briefing.

## 13. State files the assistant keeps in the base

These are not cards. The assistant creates and updates them; do not edit them by hand.

```yaml
state_files:
  _state.json: "since_ids for your posts and mentions, last run time, reads used today, the stored follow list (every handle you follow, not a truncated first-N page), and follow_list_complete (true when every follow is stored; false for a capped or test run)"
  _anchors.json: "latest post ids for the watchlist and for last week's digest comparison"
  _build-log.md: "the first-build log: reads used, timing, card counts, auto vs disputed"
  _review-log.json: "who has already been shown, including everyone who appeared on the unfollow list, plus the disputed_backlog"
```

The daily new-follow check compares the current following list against the stored follow list in `_state.json`, never against a truncated first-N slice of the API. If `follow_list_complete` is `false` (a capped or test run), the check only compares against the stored subset and must say so in the briefing.

Appearing on the unfollow list (`QUARANTINE.md`) counts as "shown" in `_review-log.json`.

## Deferred ideas

- Network roles (connector / knowledge holder / bridge): needs a who-talks-to-whom graph, which is expensive to read.
- "New follows of your priority people": very expensive on X; if needed, 5–10 people once a week.
- Cluster visualization: a simple chart by group and value is easy; "gaps in a niche" only makes sense together with roles.
