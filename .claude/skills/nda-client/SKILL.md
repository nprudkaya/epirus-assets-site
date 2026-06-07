---
name: nda-client
description: Create a new NDA access link for a client. Lists available private listings, asks for portfolio name and which listings to include, then updates site/nda.html with the new ref entry and outputs the ready-to-send ?ref= URL.
---

# NDA Client — Create Access Link for a Client

## Step 1 — Read available private listings

List all `.html` files in `site/private/` (skip `.htaccess` and any non-html files).

For each file, extract the property name:
- Read the file
- Look for `<title>` tag → take the part **before** the first ` — ` or ` | ` separator
- Fallback: use the filename without extension, capitalised

Build a numbered list and show it to the user. Example output:
```
Available private listings:
1. CavoBlu Preveza        (cavo.html)
2. Gastro-Eco Ecosystem   (gastro.html)
3. Athens GV Portfolio    (athens.html)
4. Kristalli Ioannina     (kristalli.html)
5. Myticas Seafront       (myticas.html)
```

## Step 2 — Ask the user two questions (ask both at once)

**Question 1 — Portfolio name**
A short label that describes this client's access group. Used as the human-readable label in Formspree logs and in the internal config. Examples:
- "Maria Papadopoulos — Coastal"
- "Ioannina Hotel Investor"
- "Zagori Group Q3"

**Question 2 — Which listings to include**
Ask the user to select from the numbered list shown in Step 1. They can reply with numbers ("1, 3"), names, or filenames. Accept any reasonable format.

Do not proceed until both answers are received.

## Step 3 — Generate the ref key

Transform the portfolio name into a URL-safe key:
- Lowercase
- Remove or transliterate non-ASCII characters (Greek letters → closest Latin, accents dropped)
- Replace spaces, dashes, underscores, and punctuation with single hyphens
- Remove leading/trailing hyphens
- Append the current year (4 digits)

Examples:
- "Maria Papadopoulos — Coastal" → `maria-papadopoulos-coastal-2026`
- "Ioannina Hotel Investor"      → `ioannina-hotel-investor-2026`
- "Zagori Group Q3"              → `zagori-group-q3-2026`

Then read `site/nda.html` and check whether this key already exists inside `NDA_REFS { ... }`.
- If the key already exists: append a letter suffix (`-b`, `-c`, …) until unique.

## Step 4 — Extract property details for each selected listing

For each selected `.html` file in `site/private/`:

**Name:** use what was extracted in Step 1 (from `<title>`).

**Description:** attempt to extract a short description in this order:
1. Content of `<meta name="description">` tag
2. First `<p class="hero-lead">` or `<p class="listing-lead">` text
3. First `<p>` inside `<section class="hero">` or `<div class="hero-text">`
4. If nothing found: leave a placeholder `"Short description."`

Trim to a maximum of **160 characters**. Remove HTML tags if any slipped through.

**URL:** `/private/<filename>.html`

## Step 5 — Show a preview and confirm

Before touching the file, show the user what will be inserted:

```
New ref key: maria-coastal-2026

Properties:
  ● CavoBlu Preveza — "Boutique hotel concept on the Ambracian Gulf..."
  ● Gastro-Eco Ecosystem — "Agritourism complex, 4,200m², Ioannina region..."

Ref URL: https://epirusassets.com/nda.html?ref=maria-coastal-2026
```

Ask: "Does this look correct? Reply yes to update nda.html, or tell me what to change."

If the user requests changes (different description, different name, etc.) — apply them and show the preview again. Repeat until confirmed.

## Step 6 — Update site/nda.html

Read `site/nda.html`. Locate the closing line of `NDA_REFS`:

```javascript
  // To add a new ref:
```

Insert the new entry **immediately before** that comment block. Follow the exact formatting of existing entries — 2-space indentation, trailing comma. Example insertion:

```javascript
  "maria-coastal-2026": {
    label: "Maria Papadopoulos — Coastal",
    properties: [
      {
        name: "CavoBlu Preveza",
        description: "Boutique hotel concept on the Ambracian Gulf. 18 units, fully permitted.",
        url: "/private/cavo.html"
      },
      {
        name: "Gastro-Eco Ecosystem",
        description: "Agritourism complex, 4,200m², Ioannina region. Off-market.",
        url: "/private/gastro.html"
      }
    ]
  },
```

Save the file.

## Step 7 — Output

Reply with:

1. Confirmation that `site/nda.html` was updated
2. The ref key and full URL:
   ```
   ?ref=maria-coastal-2026
   https://epirusassets.com/nda.html?ref=maria-coastal-2026
   ```
3. A one-line reminder:
   > Upload the updated `site/nda.html` to `public_html/` on the server to activate the link.

Do **not** commit or push automatically — the user will do that when ready.

---

## Rules and constraints

- Never modify anything in `NDA_REFS` except inserting the new entry
- Never change `FORMSPREE_ENDPOINT`, `UI_STRINGS`, or any HTML/CSS
- The `url` field must always start with `/private/` — never use a relative path
- Descriptions must be plain text only — no HTML, no quotes that would break the JS string
- If a description contains a double quote `"`, replace it with a single quote `'`
- The ref key must contain only `a-z`, `0-9`, and `-`
