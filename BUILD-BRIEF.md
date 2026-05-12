# Build Brief — Blotato Content Repurposer

> The spec for this repo. Iteration notes + prompts live here.

---

## Goal

Take one YouTube video and produce three platform-native posts (LinkedIn / X / Instagram) plus matching visuals, in the AIwithVishal voice, with a one-command dry-run path so I can demo it without spending Blotato credits.

---

## Requirements

- `.env` with `BLOTATO_API_KEY` + `EURI_API_KEY` (never share in chat, never commit)
- `data/posts_log.{md,json}` — running log of published posts + live URLs (gitignored)
- `src/prompts.py` — every prompt versioned alongside code
- Draft-review mode default; `--publish` is opt-in
- Three distinct visuals per platform (different aspect ratios + tones)
- Voice rules sourced from `brand-assets/AIwithVishal/VOICE-RULES.md` and injected into every prompt
- Dry-run mode that skips Blotato entirely — for CI smoke tests and demos

---

## Voice constraints (per platform)

- **LinkedIn** — beginner-friendly, code-first, hook in line 1-2, 1300 chars max, 3-5 hashtags
- **X** — punchy, one concrete insight, 280 chars max, max 1 hashtag
- **Instagram** — visual-first short caption (3-5 lines), 2-3 emojis, 15-20 hashtags in a separate block

Banned-words list lives in `brand-assets/AIwithVishal/VOICE-RULES.md` — also mirrored in `src/prompts.py::VOICE_HEADER`. When the source changes, update the mirror.

---

## Final prompt library (after iteration)

### 1. LinkedIn post prompt

```
[VOICE_HEADER — see src/prompts.py]

Now create a LinkedIn post from this video content.

Rules:
- Strong hook in the first 2 lines (these show before "see more")
- 3-4 line paragraphs max, line breaks for readability
- 2-3 concrete takeaways from the video (with numbers or code where possible)
- End with a sharp question or CTA
- 3-5 relevant hashtags at the very end
- Max 1300 characters

Video Title: {title}
Video Content: {content}

Return ONLY the post text, nothing else.
```

### 2. X post prompt

```
[VOICE_HEADER]

Now create one X (Twitter) post from this video content.

Rules:
- Lead with the single most surprising or concrete insight
- Conversational, not corporate
- Max 280 characters (hard limit)
- No hashtags unless absolutely relevant (max 1)
- Make people want to reply or quote-tweet

Video Title: {title}
Video Content: {content}

Return ONLY the tweet text, nothing else.
```

### 3. Instagram caption prompt

```
[VOICE_HEADER]

Now create an Instagram caption for a visual post about this video.

Rules:
- Visual-first — caption supports the image, doesn't compete with it
- 3-5 short lines max
- Hook line that stops the scroll
- 2-3 emojis MAX (sparingly)
- End with a save/share/follow CTA
- 15-20 hashtags in a separate block after the caption (mix popular + niche)

Video Title: {title}
Video Content: {content}

Return ONLY the caption text, nothing else.
```

### 4. Visual generation prompts (Blotato /videos/from-templates)

**LinkedIn visual**
```
Clean, dark-mode-first design with the key insight as bold text overlay.
Off-white text on near-black background (cool tint). Subtle accent on the key word only.
Include one subtle icon or graphic related to the topic.
Dimensions: 1200x627. Topic: {title}
```

**X visual**
```
Bold, attention-grabbing image with a short punchy quote overlaid.
Dark background, high contrast, modern. Minimal text, maximum impact.
Dimensions: 1600x900. Topic: {title}
```

**Instagram visual**
```
Scroll-stopping square image, dark-mode-first. Clean typography with the core
message as text overlay. Modern, aesthetic. One accent colour, not a rainbow.
Dimensions: 1080x1080. Topic: {title}
```

---

## Iteration notes

- `{title}` and `{content}` are filled by the YouTube extraction step (Blotato) or by `--seed-*` flags in dry-run.
- Visual prompts go to Blotato `/videos/from-templates` — first available template wins.
- Post-text prompts go to Euri (OpenAI-compatible chat completions).
- Tune by editing `src/prompts.py` directly. The voice header is the high-leverage knob — change it once, all three platforms inherit.
