# GITHUB: store and grow your base in a private repo

The kit (this repository) and your people base live **separately**:

| What | Where | Access |
|---|---|---|
| `people-crm-kit`: rules, templates, prompts | can be a public repo or a template | share freely |
| `people-base`: your `@handle.md` cards, INDEX, QUARANTINE, WATCHLIST, FOLLOWERS, QUEUE, ENGAGED, and state files (`_state.json`, `_anchors.json`, `_build-log.md`) | **private repo only** | you and the assistant |

The base holds personal notes about real people. Never make it public.

## Setup (once)

1. Create an empty **private** repository on GitHub, for example `people-base` (with no README).
2. Connect GitHub to your assistant and give it access only to that repo. With Grok Bot (the main agent for this kit), ask it to push the base; it shows a card to connect GitHub, where you choose "Only select repositories" and pick your base repo.
3. Tell the assistant: "Push my People CRM base to <repo URL> and from now on commit changes there."
4. Copy [gitignore.example](gitignore.example) into the base as `.gitignore`. Working caches (downloaded posts, raw JSON) stay out of the repo; they can always be downloaded again.

## How the base grows after that: through pull requests

The most convenient mode is that the assistant does not write to `main` directly, but opens a PR:

- **The daily briefing routine** collects the day's changes (new people, your replies, accounts from the WATCHLIST that woke up, quarantine) into a branch `review/YYYY-MM-DD` and opens a PR.
- **You look at the diff.** That is the review: you can see whose value changed, who went into quarantine, and which notes were added.
- **Merge** = "I agree." Closing the PR = "roll it back." A comment on the PR = a correction, and the assistant will apply it.
- **The weekly digest** commits the data refresh (new follows, profile updates, quarantine suggestions) the same way, as one weekly PR.
- The history of any person is visible through `git log -- @handle.md`: when they appeared, and how the assessment changed.

If reviewing PRs feels like too much, you can let the assistant commit straight to `main`, and keep PRs only for large changes (auto-classification, a quarantine cleanup).

## Reading and editing the base in Obsidian

1. Install [Obsidian](https://obsidian.md) and the community plugin **Obsidian Git**.
2. Clone your private base repo into a new vault with the plugin's "Clone an existing remote repo" command. A private repo needs Git on your computer and a GitHub personal access token (or an SSH key).
3. In the plugin settings, turn on auto-pull (for example every 10 minutes) and auto-commit-and-push for your own edits.
4. Each `@handle.md` card is a note. `INDEX.md`, `QUEUE.md`, `WATCHLIST.md`, and `ENGAGED.md` work as hub pages.
5. Your notes made in Obsidian reach the assistant on its next run. If you use the pull-request mode, merge the assistant's PRs on GitHub and then pull in Obsidian.

On mobile, Obsidian Git is less reliable; desktop is the main way to sync.

## A team setup

If several people keep the base (a team, a community):

- one shared private repo, and each person has their own branch or their own PRs;
- the rule: one card is one person, edits only through a PR, and conflicts are resolved by the owner of the base;
- the `related` field and groups help connect people across bases.

## Updating the kit itself

New versions of the rules and prompts come from `people-crm-kit`. They do not touch the base: you update the kit, then ask the assistant to apply the new rules to the base in a separate PR.
