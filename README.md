# Blotato Content Repurposer

> Turn a YouTube video into platform-native LinkedIn / X / Instagram posts — with custom visuals — in the AIwithVishal voice.
> One command, dry-run by default, GitHub Actions deployable.

[![Repurpose YouTube (dry-run)](https://github.com/Vishal-ml-ds/blotato-content-repurposer/actions/workflows/repurpose-youtube.yml/badge.svg)](https://github.com/Vishal-ml-ds/blotato-content-repurposer/actions/workflows/repurpose-youtube.yml)

---

## What it does

Takes one YouTube URL. Pulls title + transcript via Blotato. Generates three platform-native posts via Euri (OpenAI-compatible LLM, 200K free tokens/day). Generates a platform-optimized visual per channel via Blotato templates. Drops everything in `data/drafts.json` for review. Auto-publishes via Blotato when you flip `--publish`.

**Default stance: dry-run.** No Blotato credits spent, no posts go live until you say so.

---

## Voice

Every post is generated in the **AIwithVishal voice** — beginner-friendly, code-first, daily-life analogies, numbers over buzzwords. Banned-words list and audit checklist live in [`brand-assets/AIwithVishal/VOICE-RULES.md`](brand-assets/AIwithVishal/VOICE-RULES.md). Want a different brand? Drop a new folder into `brand-assets/` and point [`config/brand.yaml`](config/brand.yaml) at it.

---

## Quick start (5 minutes)

```bash
# 1. Clone + venv
git clone https://github.com/Vishal-ml-ds/blotato-content-repurposer.git
cd blotato-content-repurposer
python -m venv .venv
.venv/Scripts/activate           # Windows
# source .venv/bin/activate       # Mac / Linux
pip install -r requirements.txt

# 2. Bootstrap .env (dry-run is on by default)
cp .env.example .env

# 3. Run a dry-run — no Blotato calls, real Euri post generation (if EURI_API_KEY set)
python run.py --dry-run

# 4. See the output
cat data/drafts.json
ls runs/
```

---

## Going live (when you're ready)

1. Add real keys to `.env`:
   - `BLOTATO_API_KEY` — paid, from [blotato.com](https://blotato.com)
   - `EURI_API_KEY` — free 200K tokens/day, from [euron.one](https://euron.one)
2. Verify your Blotato accounts are connected for the channels you want to publish to.
3. Run with a real video:
   ```bash
   python run.py "https://www.youtube.com/watch?v=VIDEO_ID"
   ```
4. Review `data/drafts.json`. When happy, publish:
   ```bash
   python run.py --publish-drafts
   ```
5. Or skip the review step entirely:
   ```bash
   python run.py "https://www.youtube.com/watch?v=VIDEO_ID" --publish
   ```

Compliance baked in:
- `--dry-run` blocks ALL Blotato write calls.
- Draft-first is the default — auto-publish requires explicit `--publish`.
- Voice-rule audit (banned words) is enforced via prompt header on every generation.

---

## Deploy: GitHub Actions (free)

The repo ships with [`.github/workflows/repurpose-youtube.yml`](.github/workflows/repurpose-youtube.yml).

- **Trigger:** manual only (`workflow_dispatch`). No cron — content is too contextual for blind scheduling.
- **Default mode:** `--dry-run` with the built-in seed.
- **Inputs:** optional `youtube_url`, optional `dry_run` toggle (default `true`).
- **Output:** uploaded as a GitHub Actions artifact (`data/drafts.json` + `runs/*.md`) — downloadable for 30 days.

To get real LLM personalization in CI without spending Blotato credits:

```
Repo -> Settings -> Secrets -> Actions -> New repository secret
  Name:  EURI_API_KEY
  Value: <your euron.one key>
```

For full live runs (paid Blotato calls) also add `BLOTATO_API_KEY` and flip `dry_run` to `false`.

---

## Project structure

```
blotato-content-repurposer/
├── run.py                       CLI entry — dry-run + live modes
├── BUILD-BRIEF.md               Spec + iteration notes
├── CLAUDE.md                    Project rules for Claude Code
├── requirements.txt
├── .env.example
├── .gitignore
│
├── config/brand.yaml            Active brand + channel handles
├── brand-assets/AIwithVishal/   Voice rules, pillars, palette, social pages
│
├── src/
│   ├── config.py                Env loader, paths, constants
│   ├── client.py                Blotato HTTP client (poll-based)
│   ├── prompts.py               Voice header + per-platform prompts
│   ├── extractor.py             Blotato YouTube extract
│   ├── generator.py             Euri post gen + Blotato visual gen
│   ├── publisher.py             Blotato publish + log
│   └── logger.py                data/posts_log.{md,json}
│
├── data/                        Drafts + post log (gitignored)
├── runs/                        Per-run markdown summaries (kept in git)
└── .github/workflows/repurpose-youtube.yml
```

---

## Tech stack

| Layer | Tool | Free tier |
|---|---|---|
| YouTube extract | Blotato | No |
| LLM post generation | Euri (OpenAI-compatible) | 200K tokens/day |
| Visual generation | Blotato templates | No |
| Publishing | Blotato `/posts` | No |
| Deploy | GitHub Actions | Unlimited on public repos |

---

## Why this exists

Every video deserves three posts. Doing it manually is two hours of context-switching. This automates the boring part (formatting, hashtag picking, visual specs) and keeps the human part (voice, judgement, what's worth posting) where it belongs — in `prompts.py` + the brand folder, version-controlled, reviewable.

---

## License

MIT.
