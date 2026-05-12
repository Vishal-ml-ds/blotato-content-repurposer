"""All prompt templates — edit these to tweak tone, length, and style.

Voice rules in VOICE_HEADER are sourced from brand-assets/AIwithVishal/VOICE-RULES.md.
When the active brand changes, update VOICE_HEADER to match the new brand's rules.
"""


# ── Brand Voice Header (prepended to every platform prompt) ───────────

VOICE_HEADER = """Write in the AIwithVishal voice. Hard rules — violate any and the post is rejected:

1. Beginner-friendly first. Talk to the reader the author was 6 months ago. Never talk down.
2. Code-first. Every claim backed by a working example or a concrete number.
3. Daily-life analogies. Frame technical ideas as kitchen / factory / restaurant / traffic. Visual, not abstract.
4. Numbers over buzzwords. "Cut response time from 8s to 1.2s" beats "supercharged performance."
5. Show the failure. Every win post mentions what was broken before. Authenticity comes from struggle, not polish.
6. Short over long. If a sentence is over 25 words, break it.
7. Active voice, first-person. "I shipped X" not "X was shipped by me." Never plural "we" unless an actual team.

BANNED words/phrases — NEVER use any of these:
- excited / thrilled / delighted to share
- leverage / leveraging
- transformative / game-changing
- synergy / synergize
- best-in-class / world-class
- unlock / unlocked
- revolutionary
- empower / empowering
- cutting-edge
- dive deep / let's dive in
- em-dash overload (one is fine, three in a sentence is not)

Test before writing: "What would I say if I were explaining this to my younger brother?"
"""


# ── Post Text Prompts ─────────────────────────────────────────────────

LINKEDIN_POST = VOICE_HEADER + """

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

Return ONLY the post text, nothing else."""


X_POST = VOICE_HEADER + """

Now create one X (Twitter) post from this video content.

Rules:
- Lead with the single most surprising or concrete insight
- Conversational, not corporate
- Max 280 characters (hard limit)
- No hashtags unless absolutely relevant (max 1)
- Make people want to reply or quote-tweet

Video Title: {title}
Video Content: {content}

Return ONLY the tweet text, nothing else."""


INSTAGRAM_POST = VOICE_HEADER + """

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

Return ONLY the caption text, nothing else."""


POST_PROMPTS = {
    "linkedin": LINKEDIN_POST,
    "x": X_POST,
    "instagram": INSTAGRAM_POST,
}


# ── Visual Generation Prompts (sent to Blotato /videos/from-templates) ─

VISUAL_PROMPTS = {
    "linkedin": (
        "Clean, dark-mode-first design with the key insight as bold text overlay. "
        "Off-white text on near-black background (cool tint). Subtle accent on the key word only. "
        "Include one subtle icon or graphic related to the topic. "
        "Dimensions: 1200x627. Topic: {title}"
    ),
    "x": (
        "Bold, attention-grabbing image with a short punchy quote overlaid. "
        "Dark background, high contrast, modern. Minimal text, maximum impact. "
        "Dimensions: 1600x900. Topic: {title}"
    ),
    "instagram": (
        "Scroll-stopping square image, dark-mode-first. Clean typography with the core "
        "message as text overlay. Modern, aesthetic. One accent colour, not a rainbow. "
        "Dimensions: 1080x1080. Topic: {title}"
    ),
}
