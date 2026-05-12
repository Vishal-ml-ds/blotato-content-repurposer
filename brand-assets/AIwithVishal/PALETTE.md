# AIwithVishal Brand Palette

> **Status:** TODO — exact hex values to be locked after first portfolio mockup.
> **Locked preference:** dark mode by default on all UIs (per personal preference, not just visual).

---

## Working draft

### Primary (background / canvas)

| Role | Hex | Notes |
|---|---|---|
| Background dark | `#0A0E14` (TBD) | Near-black, slight cool tint |
| Surface elevated | `#13181F` (TBD) | One step up from background for cards/panels |

### Accent (emphasis / CTA)

| Role | Hex | Notes |
|---|---|---|
| Primary accent | TBD | Decide after first 3 mockups. Pick a distinct identity hue — avoid common AI-brand cyans/violets. |
| Secondary accent | TBD | Used sparingly for warnings or status |

### Neutrals (text / lines)

| Role | Hex | Notes |
|---|---|---|
| Text primary | TBD | Off-white, not pure white (reduces glare) |
| Text secondary | TBD | Mid-grey for captions, metadata |
| Line / divider | TBD | Subtle, near-background |

---

## Usage rules (locked once palette is locked)

- **No off-palette colours in production.** Dev / debug UIs may use vendor defaults; production UIs must use this palette.
- **Accent reserved for action.** Don't decorate with the accent — only CTAs, active states, key emphasis.
- **Dark mode is default.** Light mode is optional, never required.
- **Text contrast minimum:** 4.5:1 for body, 3:1 for large text (WCAG AA).

---

## Decision log

| Date | Decision | Why |
|---|---|---|
| 2026-04-28 | Repo created. Palette deferred. | No design work yet — locking too early creates artificial constraints. |

---

## Next action

When Vishal builds his first portfolio site, lock the palette there → backport to this file.
