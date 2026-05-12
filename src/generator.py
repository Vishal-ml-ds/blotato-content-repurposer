"""Post text and visual generation for each platform.

LLM calls go through Euri (OpenAI-compatible). Visuals go through Blotato.
"""

from openai import OpenAI

from src.client import BlotatoClient
from src.config import EURI_API_KEY, EURI_BASE_URL, LLM_MODEL
from src.prompts import POST_PROMPTS, VISUAL_PROMPTS


def truncate(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def _euri_client() -> OpenAI | None:
    """OpenAI-compatible client pointing at Euri. Returns None if no key."""
    if not EURI_API_KEY or EURI_API_KEY == "your_euri_key_here":
        return None
    return OpenAI(base_url=EURI_BASE_URL, api_key=EURI_API_KEY)


def call_llm(prompt: str) -> str | None:
    """Generate post text via Euri. Returns None if no API key configured."""
    client = _euri_client()
    if client is None:
        return None
    completion = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.7,
    )
    return completion.choices[0].message.content.strip()


def generate_posts(title: str, content: str, platforms: list[str]) -> dict:
    """Generate platform-specific post text using Euri.

    Returns:
        {platform: {"text": str, "prompt_used": str}}
    """
    print("\n[2/4] Generating platform-specific posts...")
    content_short = truncate(content)
    posts = {}

    for platform in platforms:
        prompt = POST_PROMPTS[platform].format(title=title, content=content_short)
        try:
            text = call_llm(prompt)
            if text:
                posts[platform] = {"text": text, "prompt_used": prompt}
                print(f"  {platform.upper()} post generated ({len(text)} chars)")
            else:
                posts[platform] = {
                    "text": f"[No EURI_API_KEY set — prompt ready for manual paste]\n\nTopic: {title}",
                    "prompt_used": prompt,
                }
                print(f"  {platform.upper()} skipped (no Euri key)")
        except Exception as e:
            posts[platform] = {
                "text": f"[LLM error: {e}]\n\nFallback — manually paste prompt into any LLM.",
                "prompt_used": prompt,
            }
            print(f"  {platform.upper()} LLM failed: {e}")

    return posts


def generate_visuals(client: BlotatoClient, title: str, platforms: list[str]) -> dict:
    """Generate platform-optimized visuals via Blotato templates.

    Returns:
        {platform: media_url | None}
    """
    print("\n[3/4] Generating platform-specific visuals...")

    try:
        templates = client.get_templates()
    except Exception as e:
        print(f"  Warning: Could not fetch templates ({e}). Skipping visuals.")
        return {p: None for p in platforms}

    if not templates:
        print("  No templates available. Skipping visuals.")
        return {p: None for p in platforms}

    template_id = templates[0].get("id") if isinstance(templates[0], dict) else templates[0]

    visuals = {}
    for platform in platforms:
        prompt = VISUAL_PROMPTS[platform].format(title=title)
        try:
            result = client.generate_visual(template_id, prompt)
            url = result.get("mediaUrl") or result.get("imageUrls", [None])[0]
            visuals[platform] = url
            print(f"  {platform.upper()} visual: {url}")
        except Exception as e:
            print(f"  {platform.upper()} visual failed: {e}")
            visuals[platform] = None

    return visuals
