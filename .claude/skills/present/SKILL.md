---
name: present
description: Create stunning, interactive HTML presentations that feel like next-generation experiences. Use when a user asks for a presentation, slide deck, pitch deck, slides, or anything presentation-related. Produces a single self-contained HTML file with animations, interactive elements, and cinematic transitions — no PowerPoint, no dependencies, just open in a browser.
---

# Present — Next-Generation HTML Presentations

Create presentations that make audiences say "how did they do that?" Single self-contained HTML file. No dependencies. Open in any browser.

## Step 0: Read the Brand Book

**Before doing anything else**, check if `presentation/epirus-assets-brand-book.pdf` exists in the working directory.

- If it exists: read it in full using the pdf skill, then apply **every rule** from it — colors, typography, tone of voice, spacing, component behavior. The brand book overrides all default aesthetic decisions in this skill.
- If it does not exist: proceed with the standard workflow below.

The Epirus Assets brand system is embedded below as a reference. If the brand book PDF is available, it is the authoritative source; the embedded spec below is a summary for quick reference.

---

## Epirus Assets Brand System

### Voice & Tone

Write like a private banker who has lived in Epirus for twenty years. Precise. Calm. Speaks only when there is something worth saying.

**Always:**
- Short, declarative sentences for important information
- Specific over general — name the village, cite the figure, state the timeline
- Sentence case for all headings and slide titles (never title case)
- Address the reader directly: "you", not "our clients"
- Acknowledge complexity — permits take months, due diligence has steps
- End with one clear next step — never multiple CTAs

**Never:**
- Superlatives: "the most", "unrivalled", "best-in-class", "exceptional"
- Vague luxury: "prestigious", "opulent", "world-class", "exclusive lifestyle"
- Urgency pressure: "act now", "limited time", "don't miss out"
- Self-congratulation: "we are proud to", "we are pleased to present"
- Title case headings

**The voice test:** "Would a private banker who has lived in Epirus for twenty years say this, without hesitation, to a client they respect?"

### Color Palette

**Core principle:** Light is the default. Dark is type, not surface. Every slide starts on Parchment or White. Epirus Night appears only as text and fine UI elements — never as a background fill. Exception: one full-bleed Night background per presentation (behind a hero image) is permitted.

| Name | Hex | Use |
|---|---|---|
| Parchment | `#F4EFE6` | Default slide background |
| White | `#FFFFFF` | Elevated cards, stat boxes on Parchment |
| Epirus Night | `#1C1C1A` | All text — headings, body, labels. Never backgrounds. |
| Epirus Gold | `#B8924A` | One accent per slide — CTA, active underline, key financial figure |
| Zagori Forest | `#2D6A4F` | Mountain/nature content, eco-luxury angle |
| Ionian Deep | `#1B4965` | Coastal listings, Golden Visa section accent |
| Ioannina Stone | `#7A6A5A` | Captions, metadata, secondary labels |
| Pale Stone | `#E2DDD6` | Card borders, dividers, rule lines |

**Section color logic:**
- Investment slides: Parchment base · Night text · Gold for ROI figures only
- Golden Visa slides: White cards · Ionian Deep text · Gold CTA
- Coastal slides: White cards · Ionian tag · Gold CTA
- Mountain/Zagori slides: Parchment · Forest tag · Stone text
- Agency/About: Parchment base · Night text · Gold accent

### Typography

Two typefaces only. Load both from Google Fonts.

- **Cormorant Garamond** — all display and heading text (humanist serif, Mediterranean character)
- **DM Sans** — all body, UI, data, and labels (geometric sans-serif, precise)

**Type scale for slides:**

| Level | Size | Weight | Font | Use |
|---|---|---|---|---|
| Display | 54pt | 300 | Cormorant Garamond | Hero headlines only |
| H1 | 36pt | 400 | Cormorant Garamond | Slide title — one per slide |
| H2 | 24pt | 400 | Cormorant Garamond | Section headings |
| H3 | 18pt | 500 | DM Sans | Card and subsection titles |
| Body | 18pt | 400 | DM Sans | All prose and descriptions |
| Small | 14pt | 400 | DM Sans | Captions, metadata, dates |
| Label | 13pt | 500 | DM Sans | Uppercase spaced — locations, tags, stat names |

**Capitalisation rules:**
- Sentence case for all slide titles, headings, body copy, bullet points
- Spaced uppercase (`letter-spacing: 0.08em`) for: location labels, stat labels (PRICE, ROI, SIZE), category tags, navigation links
- Never title case

**CSS font stack:**
```css
font-family: 'Cormorant Garamond', Georgia, serif;   /* Headings */
font-family: 'DM Sans', 'Helvetica Neue', Arial, sans-serif;  /* Body */
```

### Layout & Spacing

- Slide safe zone: 40pt from all edges
- Default gap between all elements: 24px (sp-4)
- 8px base unit — all spacing values are multiples of 8px
- Left-align all prose and descriptions — never center body text
- No shadows of any kind — borders and backgrounds do the work
- No pill-shaped elements — 6px radius maximum on cards

**Spacing tokens:**
```css
--sp-1: 4px;   --sp-2: 8px;   --sp-3: 16px;  --sp-4: 24px;
--sp-5: 40px;  --sp-6: 64px;  --sp-7: 96px;
--radius-sm: 3px;  --radius-md: 4px;  --radius-lg: 6px;
```

### UI Components

**Buttons — outlined throughout:**
- Primary: transparent bg · 1px `#B8924A` border · Gold text · hover: Gold fill + Parchment text · 4px radius
- Secondary: transparent bg · 1px `#1C1C1A` border · Night text · hover: Night fill + Parchment text
- One Gold outlined button per slide — never two side by side

**Stat cards:**
- Parchment background · 0.5px Pale Stone border · 6px radius
- Label: 13px DM Sans · uppercase · Stone color · letter-spacing +0.08em
- Value: 22px DM Sans · 500 weight · Night color
- ROI and key financial figures: Gold — one per group, never more

**Dividers:**
- Default: 0.5px `#E2DDD6` (Pale Stone)
- Gold accent rule: 1px `#B8924A` — one per slide maximum, section opener only, never decorative

**Cards:**
- White on Parchment background · 6px radius · 0.5px Pale Stone border at rest · 1px Gold on hover
- No shadows ever

---

## Workflow

### 1. Discover — Understand What They Need

Before writing a single line, clarify:

- **What's the presentation about?** Get the core message and key points.
- **Who's the audience?** Golden Visa seekers, ROI investors, or lifestyle buyers? This determines data treatment and tone.
- **How many slides?** Ask or estimate from the content (~1 slide per key point + title + finale).
- **Vibe within the brand:** The palette and typography are fixed by the brand. Within those constraints, choose the mood:
  - Understated investment memo — data-forward, generous white space, Gold on key figures only
  - Cinematic destination story — full-bleed imagery, large Cormorant headlines, minimal text
  - Structured pitch deck — 2-column grid, stat cards, Gold accents on ROI
  - Custom within brand — describe it and we build it within the brand system

Do NOT start building until you understand the content. A few good questions save hours of revision.

### 2. Architect — Plan the Experience

Think of each slide as a **moment**, not a page. Plan:

- **Opening** — First impressions matter. Terminal boot sequences, dramatic reveals, animated typography. The audience should lean forward before the first word of content.
- **Content slides** — Each one needs a reason to exist. What's the single idea? What's the visual metaphor?
- **Interactive moments** — Where can the audience (or presenter) *do* something? These are the memorable peaks.
- **Closing** — Land the plane. Callback to the opening, clear CTA, or emotional resonance.

Share the slide plan with the user before building. Get buy-in on structure.

### 3. Build — Create the Presentation

Output a **single self-contained HTML file**. All CSS inline in `<style>`, all JS inline in `<script>`. No external dependencies except Google Fonts (loaded via `@import`).

#### Technical Foundation

- Keyboard navigation: Arrow keys + Space to advance, navigation dots on the side
- Slide counter (e.g., "3 / 15") in the corner
- Smooth transitions between slides (opacity, transform — not jarring cuts)
- Responsive for 16:9 screens (the standard presentation ratio)
- Background canvas effects (particles, stars, subtle motion) add depth without distraction

#### The Art: Interactive Elements

This is what separates these presentations from everything else. The following are **starting points, not limits**. Invent new interactions. Surprise the user. Go beyond what they imagined.

**Visual & Motion:**
- Animated typography — words that build, reveal, glitch, or transform
- Parallax layers — foreground/background moving at different speeds
- Particle systems — reactive to mouse movement or slide transitions
- Morphing shapes — SVG paths that transition between forms
- Cinematic reveals — elements that emerge from blur, scale, or rotation
- Progress visualizations — bars, rings, counters that animate on slide entry

**Interactive Elements:**
- Flip cards — click to reveal hidden content on the back
- Expandable sections — click to drill deeper into a topic
- Live code terminals — typing animations that simulate real code execution
- Comparison sliders — drag to compare before/after or two options
- Interactive timelines — scroll or click through chronological events
- Hover-reveal content — details that appear on mouse interaction
- Clickable diagrams — explore parts of a system by clicking nodes
- Chat mockups — simulated conversations that type out in real-time
- Data dashboards — animated charts, metrics that count up
- Voting/polling UI — interactive (visual only) audience engagement

**Audio & Sensory (use sparingly):**
- Ambient sound on slide transitions
- Click/tap sound feedback on interactive elements
- Voice-over integration points

**Structural Patterns:**
- Split layouts — text left, visual right (or vice versa)
- Full-bleed visuals — a slide that's entirely a visual moment
- The "zoom in" — start with the big picture, progressively dive deeper
- The "reveal" — build a complete picture piece by piece across multiple slides
- Quote slides — large typography, minimal decoration, maximum impact

### 4. Iterate — Refine With the User

After the first version:
- Send the file so they can open it immediately
- Ask what slides land and which need work
- Be ready to add, remove, reorder, or completely reimagine slides
- Each iteration should be a complete, working file

## Design Principles

- **Light is the default** — Every slide starts on Parchment (`#F4EFE6`) or White. Night (`#1C1C1A`) is text only — never a background fill, except one full-bleed hero per presentation.
- **Gold is used once per slide** — The single most important figure, CTA, or accent. Never decorative, never repeated.
- **No gradients, no shadows** — The Epirus Assets system uses solid colors, borders, and spacing for depth. Gradients and box-shadows are forbidden.
- **Cormorant for impact, DM Sans for clarity** — Display and heading text is always Cormorant Garamond. Body, data, and labels are always DM Sans. Never reverse this.
- **Space signals confidence** — Generous spacing communicates that the brand is not hard-selling. When in doubt, add more space.
- **Restraint over excess** — Every animation earns its place. A single perfect transition beats ten flashy ones.
- **No superlatives, no urgency** — The voice is that of a private banker. Specific facts persuade. Enthusiasm does not.

## Ambition Level

The goal is not "a nice slide deck." The goal is an experience that makes people ask for the source file. Push creative boundaries. If you've seen it in every presentation tool, it's not enough. Think:

- "What if the slide itself was the demo?"
- "What if the transition told part of the story?"
- "What if the audience could explore, not just watch?"
- "What has nobody done in a presentation before?"

The user came to this skill because they want something extraordinary. Deliver that.
