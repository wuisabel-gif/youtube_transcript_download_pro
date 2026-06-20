# TubeScribe - Components

Every component traces to the `components:` block in `design-model.yaml`. Source is marked **observed** (lifted from the shipped web app, logo, or mascot) or **derived** (extrapolated from the design rules, with the justification stated). Tokens are semantic; resolve them against `references/platform-mapping.md`.

The throughline: handwritten warmth (Shantell Sans) for titles, calm Inter for UI, JetBrains Mono for anything you could type or run, one YouTube-red accent on cool slate, and rounded pill-friendly corners everywhere.

---

## 1. BUTTONS

**Source:** primary observed, secondary observed, ghost derived. Destructive derived (status-red error token; the shipped app never destroys data, so a destructive weight is extrapolated for delete-from-library actions).

**When to use:** Primary for the single most important action on a surface (Fetch, Download, Add to queue). Secondary for the supporting action beside it (Cancel, Copy, Choose format). Ghost for tertiary, low-stakes actions (a row's overflow, Clear filters). Destructive only for irreversible removal, and never as the default focus.

### Variants

| Variant | Background | Text | Border | Radius | Height |
|---------|-----------|------|--------|--------|--------|
| Primary | `var(--accent)` | `#FFFFFF` | none | 10px | 40px |
| Secondary | `var(--surface1)` | `var(--accent)` | `1px solid var(--border-visible)` | 10px | 40px |
| Ghost | transparent | `var(--text2)` | none | 10px | 36px |
| Destructive | `var(--error)` | `#FFFFFF` | none | 10px | 40px |

### Specs

| Property | Value |
|----------|-------|
| Height (large) | 40px |
| Height (small) | 32px |
| Padding (large) | 10px 18px |
| Padding (small) | 8px 12px |
| Font | `Inter` 600, 15px |
| Min touch target | 44px |

### States

| State | Change |
|-------|--------|
| **Hover** | Primary/Destructive background -> `var(--accent-hover)` / darker error. Secondary border and text -> `var(--accent)`. Ghost background -> `var(--surface2)`, text -> `var(--text1)`. Micro timing (140ms). |
| **Active / Pressed** | Scale to 0.97 then spring back on release with `cubic-bezier(0.34, 1.4, 0.64, 1)`. This is the signature bounce. |
| **Disabled** | Opacity 0.4, no hover/focus, layout preserved. |
| **Focus** | 3px `var(--accent)` ring at ~18% alpha, no hard outline. |

---

## 2. CARDS / SURFACES

**Source:** observed. The shipped library uses bordered cards on the tinted canvas.

**When to use:** Card for any grouped unit (a video in the library list, a settings group, the detail pane). Featured card to lift the currently-selected or hero item. Compact card for dense list rows where 24px padding is too much.

### Variants

| Variant | Background | Border | Radius | Padding | Shadow |
|---------|-----------|--------|--------|---------|--------|
| Standard | `var(--surface1)` | `1px solid var(--border)` | 14px | 24px | Level 1 |
| Featured | `var(--surface1)` + 1px `var(--accent)` left edge or accent ring | `1px solid var(--border-visible)` | 14px | 24px | Level 2 |
| Compact | `var(--surface1)` | `1px solid var(--border)` | 14px | 12px 16px | Level 1 |

### Standard Card

- Background: `var(--surface1)`
- Border: `1px solid var(--border)`
- Radius: 14px (continuous, rounded)
- Padding: 24px
- Shadow: Level 1 (`0 1px 2px rgba(12,15,20,0.06), 0 1px 3px rgba(12,15,20,0.04)` light / `0 1px 2px rgba(0,0,0,0.5)` dark)

### Content Layout

- Title: `--subheading`, `var(--text1)` (Inter 600). Video titles only; do not set in Shantell.
- Description: `--body-sm`, `var(--text2)`
- Metadata (channel, duration, video id): `--caption`, `var(--text3)`. Video id in JetBrains Mono.
- Internal spacing between elements: `--space-sm` (8px)
- Press state: cards that act as a row press to 0.985 scale with `--surface2` fill flash on tap.

---

## 3. INPUTS

**Source:** observed.

**When to use:** The primary input is the URL field (paste a video, playlist, or channel link). Also output-path fields and any free text. Format selection is a chip group, not an input (see Tags / Chips).

### Text Field

| Property | Value |
|----------|-------|
| Height | 40px |
| Background | `var(--surface1)` |
| Border (default) | `1px solid var(--border-visible)` |
| Border (focus) | `1px solid var(--accent)` |
| Border (error) | `1px solid var(--error)` |
| Radius | 10px |
| Padding | 11px 13px |
| Font | `Inter`, `--body`. URLs/paths echo back in `JetBrains Mono` `--caption`. |
| Placeholder color | `var(--text3)` |

### Label

- Position: above field, 6px gap
- Font: `Inter`, `--body-sm`, `var(--text2)`

### States

| State | Treatment |
|-------|-----------|
| **Default** | `1px solid var(--border-visible)` |
| **Focus** | `1px solid var(--accent)`. Plus a 3px `var(--accent)` ring at 18% alpha. |
| **Error** | `1px solid var(--error)`. Error text below in `var(--error)`, `--caption`. |
| **Disabled** | Opacity 0.4, no interaction. |

### Multiline

- Same styling as text field, min-height 100px, auto-grows. Used for pasting multiple URLs (one per line); each line validated independently.

---

## 4. LISTS / LIST ITEMS

**Source:** observed. The library is the app's primary archetype (list-detail).

**When to use:** The video list (left pane) and the transcript segment list (right pane). Each video row carries a title, channel, duration, status badge, and format pills.

### Standard Row

| Property | Value |
|----------|-------|
| Min height | 56px |
| Padding | 12px 16px |
| Divider | `1px solid var(--border)` between rows, or 8px gap if rows are carded |
| Label font | `Inter`, `--body`, `var(--text1)` |
| Value font | `--body-sm`, `var(--text2)`; video id and timestamps in `JetBrains Mono` `--caption` |
| Accessory | status badge + format pills on the right; chevron `var(--text3)` if drillable |

### Interaction States

| State | Treatment |
|-------|-----------|
| **Default** | Transparent background |
| **Pressed** | `var(--surface2)` fill, micro timing |
| **Selected** | `var(--accent-subtle)` background, 2px `var(--accent)` left edge, title stays `var(--text1)` |

### Data Row (Segment: timestamp + text)

- Left: timestamp in `JetBrains Mono` `--caption`, `var(--text3)` (it is a code-like locator).
- Right: segment text in `Inter` `--body`, `var(--text1)`.
- Counts beside the list (e.g. "248 segments") render in Inter, not mono (`mono_for_metrics: false`).

---

## 5. NAVIGATION (HEADER + TABS)

**Source:** header observed; tabs derived from the list-detail archetype and the accent/active conventions.

### Header

| Property | Value |
|----------|-------|
| Height | 56px |
| Background | `var(--surface1)` |
| Border | `1px solid var(--border)` bottom |
| Brand wordmark | "TubeScribe" in Shantell Sans 600, `var(--text1)`, with the paper-airplane mark in `var(--accent)` |
| Title | `--heading`, `var(--text1)` |
| Actions | ghost buttons + one primary (New fetch) on the right |

### Tabs

| Property | Value |
|----------|-------|
| Bar height | 44px |
| Tab padding | 8px 14px |
| Font | `Inter`, `--body-sm`, 600 |
| Gap between tabs | 4px |
| Active indicator | 2px `var(--accent)` underline |
| Bar border | `1px solid var(--border)` bottom |
| Transition | 240ms standard easing on the underline slide |

### Tab States

| State | Treatment |
|-------|-----------|
| **Active** | Text `var(--text1)`, 2px `var(--accent)` underline |
| **Inactive** | Text `var(--text2)`, no underline |
| **Hover** | Text `var(--text1)`, `var(--surface2)` background tint |
| **Disabled** | Opacity 0.4, no interaction |
| **Focus** | 3px `var(--accent)` ring at 18% alpha |

Typical tabs: Library, Queue, Settings. Only one tab is accented at a time, honoring the one-signal-color rule.

---

## 6. TAGS / CHIPS

**Source:** observed.

**When to use:** Format selection (`txt` / `srt` / `vtt` / `json`) is the signature chip group: selectable, mono-labeled chips. Also source-type tags (Video / Playlist / Channel) and filter chips.

| Property | Value |
|----------|-------|
| Height | 24px |
| Padding | 3px 10px |
| Radius | 999px (pill) |
| Font | format chips in `JetBrains Mono` `--caption` 500; label chips in `Inter` `--label` 600 |
| Background | `var(--accent-subtle)` |
| Text color | `var(--accent)` |
| Border | none |

### Selected State

- Background: `var(--accent-subtle)`
- Text: `var(--accent)`
- Border: 1px `var(--accent)` for the chosen format(s)

### Unselected State

- Background: `var(--surface2)`, text `var(--text2)`, no border. Selecting fills it with the accent-subtle treatment.

### Status Variants

Use status colors for semantic tags: `--success-bg` + `--success` (captions found), `--warning-bg` + `--warning` (auto-generated only), `--error-bg` + `--error` (no captions).

Format names always render in JetBrains Mono, even inside a chip: a format is something you could pass to `--format`, so it is code.

---

## 7. BADGES

**Source:** observed (status badges on library rows).

**When to use:** Per-row fetch status. Compact, no interaction, communicates state at a glance.

| Property | Value |
|----------|-------|
| Height | 20px |
| Min width | 20px |
| Padding | 2px 8px |
| Radius | 999px (pill) |
| Font | `Inter`, `--label` 600 |
| Position | inline trailing the row title, or right-aligned in the row |

### Semantic Variants

| Variant | Background | Text |
|---------|-----------|------|
| Neutral (queued) | `var(--surface2)` | `var(--text2)` |
| Success (ready) | `var(--success-bg)` | `var(--success)` |
| Warning (auto-captions) | `var(--warning-bg)` | `var(--warning)` |
| Error (failed) | `var(--error-bg)` | `var(--error)` |

### Status Dot (icon-only)

- Size: 8px circle
- Same semantic color mapping, no text
- Border: 2px `var(--surface1)` halo when overlapping a thumbnail

---

## 8. TOGGLES

**Source:** derived. No toggle exists in the shipped app; the pill track + round thumb follows the rounded radii philosophy and the accent-as-on convention.

**When to use:** Binary settings (Include timestamps, Auto-download on fetch, Dark mode). One concept per toggle; never a toggle for a multi-option choice (use chips).

### Specs

| Property | Value |
|----------|-------|
| Track width | 44px |
| Track height | 26px |
| Track radius | 999px |
| Thumb size | 22px |
| Thumb radius | 999px |
| Thumb offset (from edge) | 2px |
| Label position | left of track |
| Label gap | 12px |
| Label font | `Inter`, `--body`, `var(--text1)` |

### States

| State | Track Background | Thumb |
|-------|-----------------|-------|
| **Off (default)** | `var(--surface3)` | `#FFFFFF` |
| **On** | `var(--accent)` | `#FFFFFF` |
| **Hover** | slight brightness lift on track | thumb scales to 1.05 |
| **Disabled** | Opacity 0.4, no interaction | |
| **Focus** | 3px `var(--accent)` ring at 18% alpha | |

Thumb travel uses the emphasis easing for a small overshoot, echoing the mascot bounce.

---

## 9. OVERLAYS (MODAL + BOTTOM SHEET)

**Source:** derived from the container radius and elevation-3 tokens.

### Modal / Dialog

**When to use:** Focused decisions that block the flow: confirm a large batch fetch, confirm delete, output settings before download. Desktop and wide viewports.

| Property | Value |
|----------|-------|
| Background | `var(--surface1)` |
| Radius | 20px |
| Shadow | Level 3 (`0 16px 40px rgba(12,15,20,0.16), 0 4px 12px rgba(12,15,20,0.08)` light / `0 20px 48px rgba(0,0,0,0.65)` dark) |
| Backdrop | `rgba(12,15,20,0.45)`, blur optional |
| Max width | 480px |
| Padding | 24px |
| Close button | ghost icon (Phosphor `ph-x`) top-right, 20px, `var(--text3)` |
| Title | `--heading` in Shantell Sans, `var(--text1)` |
| Appear | scale 0.96 -> 1 over 360ms with emphasis easing |

### Bottom Sheet

**When to use:** The same decisions on narrow / mobile viewports, and quick format/destination pickers. Drag-to-dismiss.

| Property | Value |
|----------|-------|
| Background | `var(--surface1)` |
| Top radius | 20px |
| Handle | 36px x 4px pill in `var(--surface3)`, centered, 8px from top |
| Backdrop | `rgba(12,15,20,0.45)` |
| Dismiss | drag-to-dismiss, or tap backdrop |
| Present | slide up 360ms emphasis easing |

### Dropdown / Popover

| Property | Value |
|----------|-------|
| Background | `var(--surface1)` |
| Radius | 14px |
| Shadow | Level 2 |
| Border | `1px solid var(--border)` |
| Item height | 36px |
| Selected indicator | `var(--accent)` check (Phosphor `ph-check`), 16px |

---

## 10. COMMAND PREVIEW (signature surface)

**Source:** observed. This is the signature surface: the live-built CLI command. Mono, copy button, accent on the binary name.

**When to use:** Anywhere the GUI choices map to a runnable command, so the user learns the CLI by using the app. Sits below the URL field and format chips, updating live as options change. The whole point of TubeScribe's brand: the GUI and the terminal are the same tool.

### Specs

| Property | Value |
|----------|-------|
| Background | `var(--surface2)` (a deliberate inset darker than the card it lives in; reads as a terminal surface) |
| Text color | `var(--text1)` |
| Font | `JetBrains Mono`, `--caption` (13px) 500 |
| Radius | 14px |
| Padding | 12px 16px (room for the copy button) |
| Shadow | Level 0 (flat, inset feel) |
| Border | none in light; `1px solid var(--border)` in dark |

### Anatomy

| Part | Treatment |
|------|-----------|
| Binary name (`tubescribe`) | `JetBrains Mono`, `var(--accent)` 600. The one red element in the surface. |
| Flags & values (`--format srt`, `--out ./captions`) | `JetBrains Mono`, `var(--text1)` |
| Comment / hint (`# 12 videos`) | `JetBrains Mono`, `var(--text3)` |
| Copy button | ghost icon button (Phosphor `ph-copy`), 18px, `var(--text3)`, top-right or trailing; on success swaps to `ph-check` in `var(--success)` and flashes for 140ms |
| Long commands | wrap with a 2-space hanging indent, or scroll horizontally with a subtle right fade; never truncate the command |

### States

| State | Treatment |
|-------|-----------|
| **Default** | Static command, copy idle |
| **Live update** | changed token cross-fades over 140ms micro timing as options change |
| **Copied** | copy icon -> `ph-check` `var(--success)`, optional "Copied" toast |
| **Hover (copy)** | copy icon -> `var(--text1)` |

Only the binary name is accented. Flags and values stay in `--text1` so the red stays meaningful: it names the tool, it does not highlight everything.

---

## 11. STATE PATTERNS

**Source:** empty observed (the hero/empty state shares the mascot stage); loading, error, disabled derived from the motion and status tokens.

### Empty State

**When to use:** First run, an empty library, a search with no matches.

- Layout: centered, generous top padding (64px+)
- Illustration: the TubeScribe mascot on the soft red-tinted radial stage (the mascot IS the focal point). Previews render a labeled placeholder; drop in `assets/mascot.png` before shipping.
- Headline: `--heading` in Shantell Sans, `var(--text1)` (here the warmth is welcome)
- Description: `--body`, `var(--text2)`, max 2 lines, e.g. "Paste a YouTube link to grab its transcript."
- CTA: primary button (Paste a link), 24px below description
- Mono touch: show a faint example command (`tubescribe <url>`) in JetBrains Mono `var(--text3)` beneath the CTA to teach the CLI.

### Loading (progress count, not skeletons)

TubeScribe shows real progress, not skeletons. Fetching is a countable job (N of M videos), so surface the count.

- Inline: a progress bar (4px track `var(--surface2)`, fill `var(--accent)`, 999px radius) with a live "Fetched 8 of 24" label in `Inter` `--caption` `var(--text2)`. The count is Inter, not mono (`mono_for_metrics: false`).
- Per-row: the row's status badge switches to Neutral "Fetching..." with a 16px spinner in `var(--accent)`.
- Full screen: only for cold start; centered spinner over `var(--background)`, no skeleton shimmer.
- Content appearance: rows fade and rise 4px over 240ms standard easing as each transcript lands.

### Error

**When to use:** A fetch failed, no captions exist, the video is private, or the network dropped. Report the real reason, never a generic failure.

- Inline (field): `var(--error)` text in `--caption` below the element.
- Per-row: Error badge (`--error-bg` + `--error`) with the specific reason on hover/expand (e.g. "No captions available", "Video is private").
- Screen-level: centered, `var(--error)` icon (Phosphor `ph-warning-circle`), `--subheading` `var(--text1)` headline, `--body` `var(--text2)` reason, and a secondary Retry button.
- Tone: plain and specific, never cute. The mascot warmth belongs in empty states, not failures. State what happened and what the user can do.

### Disabled

- Opacity 0.4, no interaction, layout preserved.
- Borders fade to `var(--border)` default.
- No hover/focus states.
- Example: the Fetch button is disabled until a valid URL is entered; the command preview shows a greyed placeholder command at `var(--text4)` until then.
