# Blotato Content Repurposer — Project Rules

> Turn a YouTube video into platform-optimized LinkedIn / X / Instagram posts in the AIwithVishal voice.
> Blotato handles extraction + visuals + publishing. Euri handles LLM post generation.

---

## Stack

| Layer | Tool |
|---|---|
| YouTube extraction | Blotato `/source-resolutions-v3` |
| LLM post generation | Euri (OpenAI-compatible) — `gemini-2.5-flash` default (free tier) |
| Visual generation | Blotato `/videos/from-templates` |
| Publishing | Blotato `/posts` |
| Voice rules | `brand-assets/AIwithVishal/VOICE-RULES.md` |
| Deploy | GitHub Actions (`workflow_dispatch`) |

---

## Architecture

```
blotato-content-repurposer/
├── run.py                       CLI entry point — dry-run + live modes
├── BUILD-BRIEF.md               Original spec + iteration notes
├── CLAUDE.md                    This file
├── requirements.txt             Python deps
├── .env.example                 Required keys + DRY_RUN_DEFAULT switch
├── .gitignore                   .env, drafts, posts_log, .venv, .tmp
│
├── config/
│   └── brand.yaml               Active brand + channel handles (swappable)
│
├── brand-assets/
│   └── AIwithVishal/            Active brand
│       ├── VOICE-RULES.md       Banned words, sentence rules, audit checklist
│       ├── CONTENT-PILLARS.md   5 pillars + monthly mix
│       ├── PALETTE.md           Dark-mode-first colours
│       └── SOCIAL-PAGES.md      Channel handles + statuses
│
├── src/
│   ├── __init__.py
│   ├── config.py                Env loader, paths, constants
│   ├── client.py                Blotato HTTP client (poll-based)
│   ├── prompts.py               Voice header + per-platform prompts
│   ├── extractor.py             Blotato YouTube extract
│   ├── generator.py             Euri post gen + Blotato visual gen
│   ├── publisher.py             Blotato publish + log
│   └── logger.py                data/posts_log.{md,json}
│
├── data/                        Runtime drafts + post log (gitignored)
├── runs/                        Per-run markdown summaries (kept in git)
└── .github/workflows/
    └── repurpose-youtube.yml    Manual workflow_dispatch — dry-run by default
```

---

## Workflow

```
[ DRY-RUN ]                            [ LIVE ]
seed title + content                   YouTube URL
        |                                   |
        v                                   v
   (skip Blotato)                  Blotato extract -> title + transcript
        |                                   |
        +--------> Euri post gen <----------+
        |                                   |
        v                                   v
   no visuals                       Blotato visuals
        |                                   |
        v                                   v
   data/drafts.json                 data/drafts.json (review)  OR  Blotato publish
   runs/<stamp>-dryrun.md           runs/<stamp>-draft|publish.md
```

---

## Usage

```bash
# Dry-run (safe — no Blotato calls, real Euri post gen)
python run.py --dry-run

# Dry-run with custom seed
python run.py --dry-run --seed-title "How I cut cold starts to 800ms" --seed-content "..."

# Live — draft review (no auto-publish)
python run.py https://www.youtube.com/watch?v=VIDEO_ID

# Live — auto-publish all platforms
python run.py https://www.youtube.com/watch?v=VIDEO_ID --publish

# Specific platforms only
python run.py https://www.youtube.com/watch?v=VIDEO_ID --platforms linkedin,x

# Schedule
python run.py https://www.youtube.com/watch?v=VIDEO_ID --publish --schedule "2026-05-20T15:00:00Z"
```

---

## Blotato API reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/users/me` | GET | Verify API key |
| `/users/me/accounts` | GET | List connected social accounts |
| `/users/me/accounts/{id}/subaccounts` | GET | LinkedIn page IDs |
| `/source-resolutions-v3` | POST | Extract YouTube video content |
| `/source-resolutions-v3/{id}` | GET | Poll extraction status |
| `/videos/templates` | GET | List visual templates |
| `/videos/from-templates` | POST | Generate platform visuals |
| `/videos/creations/{id}` | GET | Poll visual generation status |
| `/posts` | POST | Create / publish / schedule a post |
| `/posts/{id}` | GET | Poll publish status |

Auth: `blotato-api-key` header. Base URL: `https://backend.blotato.com/v2`

---

## Hard rules

1. **Never log API keys.** Keys live in `.env` only. Logs and run summaries auto-mask.
2. **All prompts live in `src/prompts.py`.** Voice header is the single source for brand voice — do not scatter voice rules into other files.
3. **Voice header sync.** `src/prompts.py::VOICE_HEADER` mirrors `brand-assets/AIwithVishal/VOICE-RULES.md`. When VOICE-RULES.md changes, update VOICE_HEADER.
4. **Draft-first by default.** Auto-publish requires explicit `--publish`. CI defaults to `--dry-run`.
5. **Lowercase platform names** throughout: `linkedin`, `x`, `instagram`. Never `LinkedIn`, `Twitter`, `IG`.
6. **Blotato scheduling.** `scheduledTime` goes at payload ROOT, not inside `post` object.
7. **Polling is required.** All Blotato operations are async — always poll for `completed` / `done` / `published`.
8. **LinkedIn pages.** Fetch subaccounts for company-page posting; omit `pageId` for personal.
9. **Brand swap.** To add a new brand: create `brand-assets/<NewBrand>/` with the same 4 files, update `config/brand.yaml::active_brand`, refresh `src/prompts.py::VOICE_HEADER`.
10. **No upstream-author names in code, comments, configs, or commits.**
