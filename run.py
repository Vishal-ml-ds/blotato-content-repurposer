#!/usr/bin/env python3
"""Blotato Content Repurposer — turn a YouTube video into LinkedIn / X / Instagram posts.

Modes
-----
  --dry-run                       Skip Blotato. Use seed title/content. Real Euri post gen.
  <youtube_url>                   Live mode. Blotato extract -> Euri posts -> Blotato visuals.
  <youtube_url> --publish         Live mode + auto-publish via Blotato.
  --publish-drafts                Publish previously saved drafts from data/drafts.json.

Examples
--------
  python run.py --dry-run
  python run.py --dry-run --seed-title "How to ship FastAPI to Modal" --seed-content "..."
  python run.py https://www.youtube.com/watch?v=VIDEO_ID
  python run.py https://www.youtube.com/watch?v=VIDEO_ID --publish
  python run.py https://www.youtube.com/watch?v=VIDEO_ID --platforms linkedin,x
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from src.config import DATA_DIR, RUNS_DIR, PLATFORMS, DRY_RUN_DEFAULT
from src.client import BlotatoClient
from src.extractor import extract_video
from src.generator import generate_posts, generate_visuals
from src.publisher import publish_all


DRAFTS_PATH = DATA_DIR / "drafts.json"

# Default seed for dry-run (used when --seed-* not supplied). Stays in the
# AIwithVishal voice space so generated posts feel on-brand even on a stub run.
DEFAULT_SEED_TITLE = "How I shipped my first AI agent in 4 hours"
DEFAULT_SEED_CONTENT = (
    "Walkthrough of a small AI agent built with FastAPI + Modal. "
    "Covers cold-start latency (12s -> 800ms after warming), retry logic, "
    "Euri vs OpenAI cost comparison (200K free tokens/day on Euri), and the "
    "exact bug that ate 90 minutes: forgetting to await the async LLM call. "
    "Ends with the 3-file project layout that keeps everything readable."
)


def show_drafts(posts: dict, visuals: dict):
    print("\n" + "=" * 60)
    print("  DRAFT REVIEW")
    print("=" * 60)
    for platform in posts:
        print(f"\n--- {platform.upper()} ---")
        print(f"Text: {posts[platform]['text']}")
        print(f"Visual: {visuals.get(platform, 'None')}")
    print()


def save_drafts(url: str, video_data: dict, posts: dict,
                visuals: dict, platforms: list[str]):
    DRAFTS_PATH.write_text(json.dumps({
        "youtube_url": url,
        "video_data": video_data,
        "posts": posts,
        "visuals": visuals,
        "platforms": platforms,
        "saved_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }, indent=2))
    print(f"Drafts saved to: {DRAFTS_PATH}")


def write_run_log(mode: str, url: str, posts: dict, visuals: dict,
                  platforms: list[str]):
    """Write a markdown summary of the run to runs/YYYY-MM-DD-mode.md."""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    path = RUNS_DIR / f"{stamp}-{mode}.md"
    lines = [
        f"# Repurpose run — {mode}",
        "",
        f"- Timestamp: {stamp}",
        f"- Source: {url}",
        f"- Platforms: {', '.join(platforms)}",
        "",
        "## Generated posts",
        "",
    ]
    for p in platforms:
        post = posts.get(p, {})
        text = post.get("text", "")
        lines.append(f"### {p.upper()}")
        lines.append("")
        lines.append("```")
        lines.append(text)
        lines.append("```")
        lines.append("")
        lines.append(f"- Chars: {len(text)}")
        lines.append(f"- Visual: {visuals.get(p, 'None')}")
        lines.append("")
    path.write_text("\n".join(lines))
    print(f"Run log: {path}")


def publish_drafts(client: BlotatoClient, schedule_time: str | None = None):
    if not DRAFTS_PATH.exists():
        print("Error: No drafts found. Run `python run.py <youtube_url>` first.")
        sys.exit(1)
    drafts = json.loads(DRAFTS_PATH.read_text())
    results = publish_all(
        client, drafts["youtube_url"], drafts["posts"], drafts["visuals"], schedule_time,
    )
    print_results(results)


def print_results(results: dict):
    print("\n" + "=" * 60)
    print("  PUBLISHING COMPLETE")
    print("=" * 60)
    for platform, result in results.items():
        status = result.get("status", "unknown")
        url = result.get("url", "")
        print(f"  {platform.upper()}: {status} {url}")
    print(f"\nFull log: data/posts_log.md")


def main():
    parser = argparse.ArgumentParser(
        description="Repurpose YouTube videos into LinkedIn / X / Instagram posts."
    )
    parser.add_argument("url", nargs="?", help="YouTube video URL")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Skip Blotato (extract + visuals + publish). Use seed title/content. "
             "Real Euri post generation still runs."
    )
    parser.add_argument("--seed-title", default=DEFAULT_SEED_TITLE,
                        help="Title to use in --dry-run mode.")
    parser.add_argument("--seed-content", default=DEFAULT_SEED_CONTENT,
                        help="Content to use in --dry-run mode.")
    parser.add_argument("--publish", action="store_true",
                        help="Auto-publish (skip draft review). Ignored in --dry-run.")
    parser.add_argument("--publish-drafts", action="store_true",
                        help="Publish previously saved drafts from data/drafts.json.")
    parser.add_argument("--platforms", default="linkedin,x,instagram",
                        help="Comma-separated platforms (default: linkedin,x,instagram)")
    parser.add_argument("--schedule", default=None,
                        help="Schedule time in ISO 8601 (e.g., 2026-03-25T15:00:00Z)")
    args = parser.parse_args()

    platforms = [p.strip().lower() for p in args.platforms.split(",")]
    for p in platforms:
        if p not in PLATFORMS:
            print(f"Error: Unknown platform '{p}'. Choose from: {', '.join(PLATFORMS)}")
            sys.exit(1)

    # DRY-RUN PATH (no Blotato calls)
    if args.dry_run or (args.url is None and not args.publish_drafts and DRY_RUN_DEFAULT):
        print(f"Mode: DRY-RUN (no Blotato calls)")
        print(f"Platforms: {', '.join(p.upper() for p in platforms)}")
        print(f"Seed title: {args.seed_title}")

        video_data = {"title": args.seed_title, "content": args.seed_content}
        posts = generate_posts(video_data["title"], video_data["content"], platforms)
        visuals = {p: None for p in platforms}  # Skip Blotato visual generation in dry-run

        show_drafts(posts, visuals)
        save_drafts(args.url or "dry-run://seed", video_data, posts, visuals, platforms)
        write_run_log("dryrun", args.url or "dry-run://seed", posts, visuals, platforms)
        return

    # LIVE PATH (needs Blotato + Euri keys)
    try:
        client = BlotatoClient()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.publish_drafts:
        publish_drafts(client, args.schedule)
        return

    if not args.url:
        parser.print_help()
        sys.exit(1)

    print(f"Repurposing for: {', '.join(p.upper() for p in platforms)}")
    print(f"Mode: {'Auto-publish' if args.publish else 'Draft review'}")

    video_data = extract_video(client, args.url)
    posts = generate_posts(video_data["title"], video_data["content"], platforms)
    visuals = generate_visuals(client, video_data["title"], platforms)

    if args.publish:
        results = publish_all(client, args.url, posts, visuals, args.schedule)
        print_results(results)
        write_run_log("publish", args.url, posts, visuals, platforms)
    else:
        show_drafts(posts, visuals)
        save_drafts(args.url, video_data, posts, visuals, platforms)
        write_run_log("draft", args.url, posts, visuals, platforms)


if __name__ == "__main__":
    main()
