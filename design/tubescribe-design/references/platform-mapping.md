# TubeScribe - Platform Mapping

Copy-paste-ready token code. The CSS `:root` block below is the canonical source of truth for every preview and product surface. Light is the primary mode; `[data-theme="dark"]` overrides it.

## Font loading (declare before any design work)

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Shantell+Sans:ital,wght@0,500;0,600;0,700;1,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
<!-- Icons (fallback kit): Phosphor -->
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2/src/regular/style.css" />
```

- **Display / heading:** Shantell Sans (free best-match for the brand's marker face). Fallback `"Comic Sans MS", cursive`.
- **Body / UI:** Inter. Fallback `-apple-system, system-ui, sans-serif`.
- **Mono / code:** JetBrains Mono. Fallback `ui-monospace, "SF Mono", monospace`.

## CSS custom properties (canonical `:root`)

```css
:root {
  /* color - light (primary mode) */
  --background: #F7F9FC;
  --bg: var(--background);
  --surface1: #EEF2F8;
  --surface2: #DEE5EF;
  --surface3: #C6D0DF;
  --border: #DEE5EF;
  --border-visible: #C6D0DF;
  --text1: #151A21;
  --text2: #4B5568;
  --text3: #69748A;
  --text4: #93A0B5;
  --accent: #E3261D;
  --accent-hover: #C01B13;
  --accent-subtle: #FCDDDA;
  --success: #16A34A;
  --warning: #D97706;
  --error: #DC2626;
  --success-bg: #ECFDF5;
  --warning-bg: #FFFBEB;
  --error-bg: #FEF2F2;

  /* type families */
  --font-display: "Shantell Sans", "Comic Sans MS", cursive;
  --font-body: "Inter", -apple-system, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", monospace;

  /* type scale */
  --text-display: 56px;
  --text-heading: 30px;
  --text-subheading: 19px;
  --text-body: 16px;
  --text-body-sm: 14px;
  --text-caption: 13px;
  --text-label: 11px;

  /* spacing (8px base) */
  --space-2xs: 2px;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
  --space-4xl: 96px;

  /* radii */
  --radius-element: 6px;
  --radius-control: 10px;
  --radius-component: 14px;
  --radius-container: 20px;
  --radius-pill: 999px;

  /* elevation */
  --shadow-1: 0 1px 2px rgba(12,15,20,0.06), 0 1px 3px rgba(12,15,20,0.04);
  --shadow-2: 0 4px 12px rgba(12,15,20,0.08), 0 2px 4px rgba(12,15,20,0.04);
  --shadow-3: 0 16px 40px rgba(12,15,20,0.16), 0 4px 12px rgba(12,15,20,0.08);

  /* motion */
  --ease-micro: cubic-bezier(0.2, 0, 0, 1);
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-emphasis: cubic-bezier(0.34, 1.4, 0.64, 1);
  --dur-fast: 140ms;
  --dur-normal: 240ms;
  --dur-slow: 360ms;
}

[data-theme="dark"] {
  --background: #0C0F14;
  --bg: var(--background);
  --surface1: #151A21;
  --surface2: #242A34;
  --surface3: #38404E;
  --border: #242A34;
  --border-visible: #38404E;
  --text1: #F7F9FC;
  --text2: #C6D0DF;
  --text3: #93A0B5;
  --text4: #69748A;
  --accent: #EA5A4D;
  --accent-hover: #F28C82;
  --accent-subtle: #4F0E0A;
  --success: #16A34A;
  --warning: #D97706;
  --error: #DC2626;
  --success-bg: #14532D;
  --warning-bg: #78350F;
  --error-bg: #7F1D1D;

  --shadow-1: 0 1px 2px rgba(0,0,0,0.5);
  --shadow-2: 0 6px 18px rgba(0,0,0,0.55);
  --shadow-3: 0 20px 48px rgba(0,0,0,0.65);
}
```

## React / Tailwind (`tailwind.config.js` extend)

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        surface1: "var(--surface1)",
        surface2: "var(--surface2)",
        surface3: "var(--surface3)",
        border: "var(--border)",
        "border-visible": "var(--border-visible)",
        text1: "var(--text1)",
        text2: "var(--text2)",
        text3: "var(--text3)",
        text4: "var(--text4)",
        accent: "var(--accent)",
        "accent-hover": "var(--accent-hover)",
        "accent-subtle": "var(--accent-subtle)",
        success: "var(--success)",
        warning: "var(--warning)",
        error: "var(--error)",
      },
      fontFamily: {
        display: ["Shantell Sans", "Comic Sans MS", "cursive"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      borderRadius: {
        element: "6px", control: "10px", component: "14px", container: "20px", pill: "999px",
      },
    },
  },
};
```

## SwiftUI (Color + Font extensions)

```swift
extension Color {
  static let background   = Color(hex: "F7F9FC")   // dark: 0C0F14
  static let surface1     = Color(hex: "EEF2F8")   // dark: 151A21
  static let text1        = Color(hex: "151A21")   // dark: F7F9FC
  static let text2        = Color(hex: "4B5568")   // dark: C6D0DF
  static let accent       = Color(hex: "E3261D")   // dark: EA5A4D
  static let accentSubtle = Color(hex: "FCDDDA")   // dark: 4F0E0A
  static let success      = Color(hex: "16A34A")
  static let warning      = Color(hex: "D97706")
  static let errorRed     = Color(hex: "DC2626")
}

extension Font {
  // Shantell Sans / Inter / JetBrains Mono must be bundled in the app target.
  static func display(_ size: CGFloat = 56) -> Font { .custom("ShantellSans-SemiBold", size: size) }
  static func bodyUI(_ size: CGFloat = 16)  -> Font { .custom("Inter", size: size) }
  static func mono(_ size: CGFloat = 13)    -> Font { .custom("JetBrainsMono-Medium", size: size) }
}
```

Use `RoundedRectangle(cornerRadius: 14, style: .continuous)` for cards on iOS so corners match the rounded radii philosophy.
