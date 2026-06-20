# TubeScribe - Tokens

## 0. PRIMITIVES

Raw scales derived from the brand. These are the building blocks: semantic tokens reference them.

### Color Ramps

**Neutral** (cool slate)

| Step | Hex | Use |
|------|-----|-----|
| 50 | `#F7F9FC` | Lightest background |
| 100 | `#EEF2F8` | Light surfaces |
| 200 | `#DEE5EF` | Borders, dividers (light) |
| 300 | `#C6D0DF` | Strong borders (light) |
| 400 | `#93A0B5` | Placeholder text |
| 500 | `#69748A` | Muted text |
| 600 | `#4B5568` | Secondary text |
| 700 | `#38404E` | Strong borders (dark) |
| 800 | `#242A34` | Dark surfaces |
| 900 | `#151A21` | Darkest surface |
| 950 | `#0C0F14` | Near-black background |

**Brand** (YouTube red)

| Step | Hex |
|------|-----|
| 50 | `#FEF2F1` |
| 100 | `#FCDDDA` |
| 200 | `#F9BCB6` |
| 300 | `#F28C82` |
| 400 | `#EA5A4D` |
| 500 | `#E3261D` - primary accent |
| 600 | `#C01B13` |
| 700 | `#9C160F` |
| 800 | `#76130E` |
| 900 | `#4F0E0A` |
| 950 | `#2C0705` |

The 500 step is keyed to the logo gradient end (`#E3261D`). This is the one signal color: it points, it never decorates. If two things on a screen are red, one of them is wrong.

**Status Colors**

| Color | 50 (bg tint) | 500 (foreground) | 900 (dark tint) |
|-------|-------------|-----------------|-----------------|
| Red | `#FEF2F2` | `#DC2626` | `#7F1D1D` |
| Green | `#ECFDF5` | `#16A34A` | `#14532D` |
| Amber | `#FFFBEB` | `#D97706` | `#78350F` |

Status red (`#DC2626`) is deliberately a different hue from brand red (`#E3261D`). Brand red is the product's voice; status red is an error. Keep them separate.

### Spacing Primitives

`[0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96]`

### Radii Primitives

`[0, 6, 10, 14, 20, 999]`

Rounded and pill-friendly by design. There is no sharp-corner primitive in active use; the `0` step exists only as a reset. Everything the user touches has softened corners, matching the mascot's personality.

---

## 1. TYPOGRAPHY

### Font Stack

| Role | Font | Fallback | Weight | Use |
|------|------|----------|--------|-----|
| **Display** | `"Shantell Sans"` | `"Comic Sans MS", cursive` | 600 | Screen titles, hero lines, the handwritten warmth |
| **Body / UI** | `"Inter"` | `-apple-system, system-ui, sans-serif` | 400 | Body text, descriptions, UI labels, counts and timestamps |
| **Mono / Code** | `"JetBrains Mono"` | `ui-monospace, "SF Mono", monospace` | 500 | Commands, file paths, format names, video ids, code blocks |

Shantell Sans is the free best-match for the brand's custom marker face (ALK Life). It carries the handwritten side of the tension. JetBrains Mono carries the precision side. Inter is the calm middle that keeps long body copy readable.

### Mono Font Rules

**`mono_for_code`: true** - **`mono_for_metrics`: false**

The whole design tension lives in this split. Mono is reserved for things the user could type, paste, or pipe: shell commands, file paths, format names (`txt` / `srt` / `vtt` / `json`), video ids, and code blocks. That precision is the product's credibility. Numbers that are just information, on the other hand, stay in the friendly Inter sans.

- **`mono_for_code: true`:** Use JetBrains Mono for code blocks, file paths, shell commands, and inline technical tokens (the binary name, flags, format extensions, video ids). This is the signature move; anything a terminal would echo is mono.
- **`mono_for_metrics: false`:** Counts, durations, timestamps, and percentages render in Inter, not mono. A "fetched 42 of 120" progress count is friendly information, not code, so it stays in the sans. Reserving mono for code keeps it meaningful: when you see mono, it is something you could run.

A worked example: in the command preview surface, `tubescribe` and `--format srt` are mono because you would type them; the "12 videos queued" label beside it is Inter because it is just a count.

### Type Scale

| Token | Size | Line Height | Letter Spacing | Weight | Use |
|-------|------|-------------|----------------|--------|-----|
| `--display` | 56px | 1.05 | -0.01em | 600 | Hero lines, marketing titles (Shantell Sans) |
| `--heading` | 30px | 1.15 | -0.01em | 600 | Section headings, screen titles (Shantell Sans) |
| `--subheading` | 19px | 1.3 | 0em | 600 | Card titles, list group headers (Inter) |
| `--body` | 16px | 1.6 | 0em | 400 | Body text, descriptions (Inter) |
| `--body-sm` | 14px | 1.5 | 0em | 400 | Secondary text, notes, list values (Inter) |
| `--caption` | 13px | 1.4 | 0em | 500 | Timestamps, footnotes, mono code default size (JetBrains Mono at this size) |
| `--label` | 11px | 1.3 | 0.02em | 600 | Micro-labels, tag and badge text, metadata (Inter, uppercase optional) |

### Typographic Rules

- Display and heading are the only two roles that use Shantell Sans. Do not set body copy, labels, or UI controls in the display face; at small sizes the marker face hurts legibility and cheapens the warmth.
- Subheading and below are all Inter. Keep the sans calm so the two expressive faces (Shantell, JetBrains) stand out.
- Mono defaults to the `--caption` size (13px). When mono appears inline inside `--body`, let it sit at the body size but keep weight 500 so it reads as a distinct token.
- Negative letter spacing (-0.01em) only on the two large display roles, where it tightens the marker face. Everything else is neutral or slightly open.
- Never mix Shantell Sans and JetBrains Mono in the same line of running text. Pair Shantell with Inter, or Inter with JetBrains; the three-way mix only happens across a layout, not within a phrase.

---

## 2. COLOR SYSTEM (Semantic Tokens)

Semantic tokens reference the primitives above. Components use semantic tokens, never primitives directly.

### Primary Mode (Light)

| Token | Primitive | Hex | Role |
|-------|-----------|-----|------|
| `--background` | `{neutral.50}` | `#F7F9FC` | Page background |
| `--bg` | (alias) | `var(--background)` | Shorthand alias for `--background` |
| `--surface1` | `{neutral.100}` | `#EEF2F8` | Cards, elevated containers |
| `--surface2` | `{neutral.200}` | `#DEE5EF` | Secondary cards, grouped backgrounds, command preview |
| `--surface3` | `{neutral.300}` | `#C6D0DF` | Tertiary surfaces, inset areas, toggle-off track |
| `--border` | `{neutral.200}` | `#DEE5EF` | Subtle dividers, card edges |
| `--border-visible` | `{neutral.300}` | `#C6D0DF` | Stronger borders: inputs, active controls |
| `--text1` | `{neutral.900}` | `#151A21` | Primary text: headings, body |
| `--text2` | `{neutral.600}` | `#4B5568` | Secondary text: descriptions, labels |
| `--text3` | `{neutral.500}` | `#69748A` | Tertiary text: placeholders, timestamps |
| `--text4` | `{neutral.400}` | `#93A0B5` | Disabled text, ghost elements |
| `--accent` | `{brand.500}` | `#E3261D` | Primary accent: interactive elements, CTAs |
| `--accent-hover` | `{brand.600}` | `#C01B13` | Accent hover / pressed |
| `--accent-subtle` | `{brand.100}` | `#FCDDDA` | Tinted backgrounds for accent |
| `--success` | `{green.500}` | `#16A34A` | Confirmed, completed, transcript ready |
| `--warning` | `{amber.500}` | `#D97706` | Caution, pending, throttled |
| `--error` | `{red.500}` | `#DC2626` | Destructive, failed fetch, no captions |

### Secondary Mode (Dark)

| Token | Primitive | Hex | Role |
|-------|-----------|-----|------|
| `--background` | `{neutral.950}` | `#0C0F14` | Page background |
| `--bg` | (alias) | `var(--background)` | Shorthand alias for `--background` |
| `--surface1` | `{neutral.900}` | `#151A21` | Cards, elevated containers |
| `--surface2` | `{neutral.800}` | `#242A34` | Secondary cards, grouped backgrounds, command preview |
| `--surface3` | `{neutral.700}` | `#38404E` | Tertiary surfaces, inset areas, toggle-off track |
| `--border` | `{neutral.800}` | `#242A34` | Subtle dividers, card edges |
| `--border-visible` | `{neutral.700}` | `#38404E` | Stronger borders: inputs, active controls |
| `--text1` | `{neutral.50}` | `#F7F9FC` | Primary text |
| `--text2` | `{neutral.300}` | `#C6D0DF` | Secondary text |
| `--text3` | `{neutral.400}` | `#93A0B5` | Tertiary text |
| `--text4` | `{neutral.500}` | `#69748A` | Disabled text |
| `--accent` | `{brand.400}` | `#EA5A4D` | Primary accent (lifted for dark contrast) |
| `--accent-hover` | `{brand.300}` | `#F28C82` | Accent hover / pressed |
| `--accent-subtle` | `{brand.900}` | `#4F0E0A` | Tinted backgrounds for accent |
| `--success` | `{green.500}` | `#16A34A` | Positive states |
| `--warning` | `{amber.500}` | `#D97706` | Caution states |
| `--error` | `{red.500}` | `#DC2626` | Negative states |

In dark mode the accent steps up to `{brand.400}` (`#EA5A4D`): the 500 red is too dense against near-black and fails contrast on small text. The hover direction also flips, climbing toward the lighter `{brand.300}` instead of darkening.

### Accent & Status Tints

| Token | Primary | Secondary | Usage |
|-------|---------|-----------|-------|
| `--accent-subtle` | `#FCDDDA` | `#4F0E0A` | Tinted backgrounds for accent elements (tags, selected rows) |
| `--success-bg` | `#ECFDF5` | `#14532D` | Success tinted backgrounds |
| `--warning-bg` | `#FFFBEB` | `#78350F` | Warning tinted backgrounds |
| `--error-bg` | `#FEF2F2` | `#7F1D1D` | Error tinted backgrounds |

### Color Usage Rules

- One accent, used sparingly. `--accent` is for the primary action, the binary name in a command, an active tab, and a selected state. It is not a decoration. A typical screen has exactly one or two red elements.
- Text hierarchy is four steps deep: `--text1` for what you read, `--text2` for supporting copy, `--text3` for placeholders and timestamps, `--text4` for disabled. Do not reach past `--text2` for anything load-bearing.
- Surfaces stack by elevation, not by hue. `--background` -> `--surface1` -> `--surface2` -> `--surface3` get progressively more tinted; use them to show depth, never to color-code content.
- Status colors are semantic and exclusive: green for done, amber for in-progress or throttled, status-red for failure. Brand red never means error, and status red never means "primary action."
- The command preview sits on `--surface2` in both modes: a deliberate inset darker than the card it lives in, so the command reads as a distinct terminal surface.
- Always pair a status foreground with its matching `*-bg` tint, never a foreground on a raw surface. `--success` text belongs on `--success-bg`.

---

## 3. SPACING

### Scale (8px base)

| Token | Value | Use |
|-------|-------|-----|
| `--space-2xs` | 2px | Optical adjustments only |
| `--space-xs` | 4px | Icon-to-label gaps, tight padding |
| `--space-sm` | 8px | Component internal padding |
| `--space-md` | 16px | Standard padding, element gaps |
| `--space-lg` | 24px | Card padding, section item gaps |
| `--space-xl` | 32px | Section spacing, generous padding |
| `--space-2xl` | 48px | Major section breaks |
| `--space-3xl` | 64px | Screen section divisions |
| `--space-4xl` | 96px | Hero breathing room |

The scale is `[2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96]` at the primitive level; the semantic tokens above pick the rhythm beats most components need. Reach for `12` and `20` from the primitives only when a layout genuinely needs an intermediate step.

---

## 4. BORDERS & RADII

### Radii Scale (Semantic to Primitive)

| Token | Value | Primitive | Use |
|-------|-------|-----------|-----|
| `--radius-element` | 6px | `{radii[1]}` | Small controls, checkboxes, format pills inside a row |
| `--radius-control` | 10px | `{radii[2]}` | Buttons, inputs, toggles |
| `--radius-component` | 14px | `{radii[3]}` | Cards, panels, list items, command preview |
| `--radius-container` | 20px | `{radii[4]}` | Modals, sheets, popovers |
| `--radius-pill` | 999px | `{radii[5]}` | Tags, chips, badges, pill buttons |

### Border Treatment

| Element | Border |
|---------|--------|
| Cards / Surfaces | `1px solid var(--border)` |
| Buttons | Primary none; Secondary `1px solid var(--border-visible)`; Ghost none |
| Inputs | `1px solid var(--border-visible)`, `var(--accent)` on focus |
| Tags / Chips | None (filled `--accent-subtle`); status tags none |
| Modals / Sheets | None in light; `1px solid var(--border)` in dark for edge definition |

Corners are always rounded and continuous; there are no square corners anywhere in the system. Nest radii so an inner element is one step smaller than its container (a 6px format pill inside a 14px card), keeping the rounding visually concentric.

---

## 5. ELEVATION & SHADOWS

| Level | Light Mode | Dark Mode | Use |
|-------|-----------|----------|-----|
| **0** | None | None | Flat, inline elements, command preview |
| **1** | `0 1px 2px rgba(12,15,20,0.06), 0 1px 3px rgba(12,15,20,0.04)` | `0 1px 2px rgba(0,0,0,0.5)` | Standard cards, containers |
| **2** | `0 4px 12px rgba(12,15,20,0.08), 0 2px 4px rgba(12,15,20,0.04)` | `0 6px 18px rgba(0,0,0,0.55)` | Floating cards, menus, popovers |
| **3** | `0 16px 40px rgba(12,15,20,0.16), 0 4px 12px rgba(12,15,20,0.08)` | `0 20px 48px rgba(0,0,0,0.65)` | Modals, sheets, dialogs |

Elevation strategy is subtle: shadows are soft and low-contrast, tinted with the slate ink (`rgba(12,15,20,...)`) rather than pure black in light mode. Depth comes mostly from surface tinting; shadow is the gentle confirmation, not the main event. In dark mode shadows lean on opacity since tint reads poorly against near-black.

---

## 6. MOTION & INTERACTION

### Personality

Smooth with a bounce. The default is calm and quick; one playful spring shows up on press and on appear, echoing the mascot's friendliness. Motion is never gratuitous: it confirms an action or reveals a surface, then gets out of the way.

### Timing

| Type | Duration | Easing | Use |
|------|----------|--------|-----|
| **Micro** | 140ms | `cubic-bezier(0.2, 0, 0, 1)` | Button press, toggle, color change, copy-confirm flash |
| **Standard** | 240ms | `cubic-bezier(0.4, 0, 0.2, 1)` | Card expand, content transitions, tab switch |
| **Emphasis** | 360ms | `cubic-bezier(0.34, 1.4, 0.64, 1)` | Sheet present, modal appear, the one springy overshoot |

### Interaction States

- **Hover:** color or border shift toward `--accent`, or a `--surface2` background fill for ghost controls. Micro timing.
- **Press:** scale down to ~0.97 and snap back with the emphasis easing on release; this is where the bounce lives.
- **Focus:** a 3px `--accent` ring at ~18% alpha, never a hard outline. Always visible for keyboard users.
- **Disabled:** opacity 0.4, no hover or focus, layout preserved.
- Respect `prefers-reduced-motion`: drop the overshoot to the standard easing and shorten emphasis to micro. The spring is a delight, not a requirement.

---

## 7. ICONOGRAPHY

> **Fallback disclosure.** The icons rendered in the generated preview come from a freely-licensed kit selected as the closest match to the brand's actual icons. They are **not** the brand's real glyphs: the shipped app uses Heroicons (MIT). Swap to Heroicons for an exact match.

### Observed style (the brand's actual icons)

| Attribute | Value |
|-----------|-------|
| Description | The shipped app uses Heroicons (solid for chips/badges, the brand mark is the Heroicons paper-airplane). Geometric, ~1.5px effective weight, rounded corners, balanced density, friendly. |
| Stroke weight | regular |
| Corner treatment | soft |
| Fill style | mixed (solid chips + outline UI icons) |
| Form language | geometric |
| Visual density | balanced |

### Fallback kit (what the preview actually renders)

- **Kit:** Phosphor
- **Weight / variant:** regular
- **Match score:** high
- **Why this kit:** Phosphor regular matches the observed ~1.5px weight, rounded corners, and geometric-but-friendly form language, and its bold/fill variants cover the solid chip icons too. Lucide was the runner-up but reads slightly more clinical than TubeScribe's rounded warmth.
- **CDN:** `https://unpkg.com/@phosphor-icons/web@2/src/regular/style.css`
- **Usage:** `ph ph-`

### Sizes

| Context | Size |
|---------|------|
| Inline with body text | 16px |
| Buttons | 18px |
| Navigation | 20px |

### Color rule

Icons inherit `--text2` by default and `--text1` when they sit beside primary text. Use `--accent` only on active or selected icons (the current tab, a copy-success check). Status icons take their status foreground (`--success`, `--warning`, `--error`). An icon is never red unless it points to the primary action or signals an error.

### Don't

- Do not mix outline and solid icons in the same cluster; pick one fill per context (outline for UI controls, solid for chips and badges).
- Never claim these are the brand's real icons: they are a best-match fallback.
