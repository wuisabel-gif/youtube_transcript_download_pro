---
name: tubescribe-design
description: "This skill should be used when the user explicitly says 'TubeScribe style', 'TubeScribe design', '/tubescribe-design', or directly asks to use/apply the TubeScribe design system. NEVER trigger automatically for generic UI or design tasks."
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# TubeScribe

You are a senior product designer. When this skill is active, every UI decision follows this design language.

**Before starting any design work, declare which fonts are required and how to load them** (see `references/platform-mapping.md`). Never assume fonts are already available.

---

## 1. DESIGN PHILOSOPHY

TubeScribe is a friendly developer utility. It turns YouTube videos, playlists, and channels into clean transcript files, and the interface should feel like a helpful desk tool, not an enterprise console.

The whole language lives on one tension: **handwritten warmth against monospace precision.** A casual marker-style display face (Shantell Sans, standing in for the brand's ALK Life headline font) does the welcoming. A calm Inter body does the explaining. JetBrains Mono carries every command, format name, file path, and video id, because the product is fundamentally about producing text artifacts. One YouTube-red signal color (`#E3261D`) does all the pointing, riding on cool-slate neutrals. Everything is rounded and pill-friendly, the same personality as the mascot: a red play button holding a transcript scroll.

The squint test: if you blur the screen, you should see a calm slate page with exactly one warm red moment and one playful headline. If you see red everywhere, or three competing fonts shouting, you have broken it.

---

## 2. CRAFT RULES - HOW TO COMPOSE

**Hierarchy comes from three layers, in this order:**

| Layer | Tool | Example |
|-------|------|---------|
| 1. Structure | Slate neutrals + spacing | Page, cards, list rows on the cool canvas |
| 2. Voice | Shantell Sans display | The hero line, section titles, the one playful note |
| 3. Signal | Red accent, used once per view | The primary action, the active tab, the selected row |

**Font budget: three roles, never more.** Shantell Sans for display and section headings only. Inter for everything that is read as information (body, labels, metadata, buttons). JetBrains Mono for anything a user could copy and paste into a terminal. If a fourth font appears, delete it.

**Mono is for copyable things.** Commands (`tubescribe URL -f srt`), formats (`txt`, `srt`, `vtt`, `json`), file paths, and video ids go in JetBrains Mono. Counts, durations, and timestamps stay in Inter, because they are read, not copied. This is `mono_for_code: true`, `mono_for_metrics: false`.

**Red is a guest, not the wallpaper.** Maximum one red moment per view: the primary CTA, OR the active state, never a page full of red buttons. Tints (`--accent-subtle`) are allowed for tags and selected rows; saturated red fills are rationed.

**Spacing is an 8px grid.** Card padding is `--space-lg` (24px). Element gaps are `--space-md` (16px). Tight icon-to-label pairs are `--space-xs` (4px). Never invent a one-off padding; pick a token.

**Everything rounds.** Buttons and inputs at 10px, cards at 14px, modals at 20px, tags and pills at 999px. There are no sharp corners in TubeScribe. The softness is the friendliness.

**The command preview is the signature surface.** When the UI shows a built CLI command, render it in mono on `--surface2`, with the binary name in accent and a copy button. It is the one place where the developer-tool identity is loudest.

---

## 3. ANTI-PATTERNS - WHAT TO NEVER DO

- No sharp corners. Nothing below 6px radius, ever.
- No second accent hue. Red is the only chromatic color besides semantic success/warning/error.
- No red-on-red walls. One saturated red fill per view, maximum.
- No Shantell Sans in body, labels, inputs, or tables. Display and headings only.
- No mono for prose, counts, or durations. Mono is for copyable code-like strings only.
- No heavy drop shadows. Elevation is subtle (1 to 3px soft offsets); depth otherwise comes from borders and surface steps.
- No gradients on buttons or cards. The only gradient is the soft hero field.
- No pure-black text or pure-black backgrounds. Slate `#151A21` and `#0C0F14`, never `#000`.
- No toast popups for routine confirmations. State changes happen inline (a row turns to done, a count updates).
- No skeleton shimmer screens. Use a calm progress count ("3 of 12 fetched") instead.
- No icon zoo. One kit (Phosphor fallback / Heroicons in product), regular weight, accent or text2 color only.
- No em-dashes in shipped copy. Use hyphens, commas, or colons.

---

## 4. WORKFLOW

1. **Declare fonts** - check `references/platform-mapping.md` for loading instructions.
2. **Set tokens** - paste the canonical `:root` block from `references/platform-mapping.md`.
3. **Build components** - use specs from `references/components.md`.
4. **Check hierarchy** - squint test: one structure layer, one playful headline, one red signal.
5. **Verify both modes** - light and dark must both feel intentional.
6. **Test extremes** - one video, a 100-video playlist, an empty state, a failed fetch.
7. **Platform-adapt** - consult `references/platform-mapping.md` for CSS, Tailwind, and SwiftUI output.

---

## 5. REFERENCE FILES

| File | Contains |
|------|----------|
| `references/tokens.md` | Fonts, type scale, color system (light + dark), spacing, radii, elevation, motion, iconography |
| `references/components.md` | Cards, buttons, inputs, lists, navigation, tags, overlays, the command preview, state patterns |
| `references/platform-mapping.md` | HTML/CSS canonical `:root`, React/Tailwind, SwiftUI - platform code and font loading |
| `design-model.yaml` | The single source of truth all of the above derive from |
