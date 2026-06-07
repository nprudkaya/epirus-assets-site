# Epirus Assets — NDA Gate: Setup & Restructure Guide

## Overview

This guide explains how to deploy the NDA gate system on `epirusassets.com`.
It covers three things: restructuring the file system on the server, setting up
Formspree, and managing the JS configuration going forward.

---

## Part 1 — File System Restructure on the Server

### What needs to happen

On the cPanel server, inside `public_html/`, you will create two new folders
and move the property HTML files into them:

- `/properties/` — public listings (may be linked from the main site)
- `/private/` — private listings (never linked from the site, shared via NDA link only)

### Step-by-step

**Step 1.** Log in to cPanel → File Manager → navigate to `public_html/`.

**Step 2.** Create two new folders:
- `properties`
- `private`

**Step 3.** Move each property file to the correct folder according to the table below.
To move a file in File Manager: right-click → Move → type the new path.

#### File categorisation table

Fill in the "Move to" column before starting. Once decided, do not change a
private listing to public without also removing it from any NDA_REFS entry.

| File                        | Move to            | Notes                             |
|-----------------------------|--------------------|-----------------------------------|
| sivota.html                 | /properties/              | Public listing |
| astoria.html                | /properties/              | Public listing |
| tositsa.html                | /properties/              | Public listing |
| athens.html                 | /private/                 | Private — NDA required |
| cavo.html                   | /private/                 | Private — NDA required |
| gastro.html                 | /private/                 | Private — NDA required |
| kristalli.html              | /private/                 | Private — NDA required |
| myticas.html                | /private/                 | Private — NDA required |

**Step 4.** Upload the new files from this build:

| Local file                    | Upload to (on server)       |
|-------------------------------|-----------------------------|
| `site/nda.html`               | `public_html/nda.html`      |
| `site/private/.htaccess`      | `public_html/private/.htaccess` |

**Step 5.** Update any internal links in `index.html` and `about.html` that
point to property pages. For each moved file, change:

```
href="sivota.html"   →   href="properties/sivota.html"
href="cavo.html"     →   href="private/cavo.html"
```
(adjust per your categorisation table above)

**Step 6.** Verify:
- Open `epirusassets.com/properties/` in a browser — should show a 403 or blank
  page (no directory listing), not a file list.
- Open `epirusassets.com/private/` — same: no directory listing visible.
- Open `epirusassets.com/nda.html` with no `?ref=` param — should show the
  "This link appears to be incomplete" message.
- Open `epirusassets.com/nda.html?ref=sivota-2026` — should show the NDA form.

---

## Part 2 — Formspree Setup

Formspree receives form submissions and sends you an email notification for
each client who signs the NDA. It also stores all submissions in a dashboard
table you can export to CSV, and optionally sync to Google Sheets.

### Steps

**Step 1.** Go to [https://formspree.io](https://formspree.io) and create a
free account (use your work email, e.g. info@epirusassets.com).

**Step 2.** Click **"+ New Form"** → enter a name, e.g. `Epirus NDA Submissions`
→ click **"Create Form"**.

**Step 3.** Copy the form endpoint URL. It looks like:
```
https://formspree.io/f/abcdefgh
```

**Step 4.** Open `nda.html` in a text editor. Find this line near the top of
the `<script>` block:
```javascript
const FORMSPREE_ENDPOINT = "https://formspree.io/f/XXXXXXXX";
```
Replace `XXXXXXXX` with your actual form ID. Save and re-upload the file.

**Step 5.** Formspree will send a confirmation email to the address you
registered with. Click the link in that email to verify the endpoint is active.

**Step 6 (optional — Google Sheets sync).** In the Formspree dashboard, open
your form → **Integrations** tab → **Google Sheets** → click **Connect** →
sign in with your Google account → choose an existing Sheet or create a new one
→ Formspree maps the columns automatically. All future submissions will appear
in the Sheet in real time. This requires the Formspree paid plan ($10/month),
which also removes the 50 submissions/month limit.

### What each submission contains

When a client completes the NDA form, Formspree receives:

| Field        | Example value                         |
|--------------|---------------------------------------|
| name         | Maria Papadopoulos                    |
| email        | maria@example.com                     |
| ref          | sivota-2026                           |
| ref_label    | Sivota Coastal Portfolio              |
| nda_agreed   | Yes                                   |
| gdpr_consent | Yes                                   |
| timestamp    | 2026-06-07T14:22:05.123Z              |
| page_url     | https://epirusassets.com/nda.html?ref=sivota-2026 |

---

## Part 3 — NDA Text (from PDF)

The NDA text is stored in `nda.html` inside the `UI_STRINGS` configuration
block. When you receive the PDF from the client:

1. Copy the English text → paste it into `UI_STRINGS.en.nda_body` (replacing
   the placeholder).
2. Copy the Greek text → paste it into `UI_STRINGS.el.nda_body`.
3. Preserve paragraph breaks by replacing them with `\n\n` between paragraphs.
4. Do **not** rewrite or summarise legal text — paste verbatim.
5. Save and re-upload `nda.html`.

---

## Part 4 — Adding a New Access Group (New ref)

When you want to share a new set of private properties with a client, add a new
entry to the `NDA_REFS` object in `nda.html`.

### Example

Open `nda.html`, find the `NDA_REFS` block, and add:

```javascript
"zagori-villa-2026": {
  label: "Zagori Villa Portfolio",
  properties: [
    {
      name: "Stone Villa Papingo",
      description: "Restored stone villa, 220m², mountain views. Fully permitted.",
      url: "/private/villa-papingo.html"
    }
  ]
}
```

Then save and re-upload `nda.html`.

Send the client this URL:
```
https://epirusassets.com/nda.html?ref=zagori-villa-2026
```

### Rules for ref keys

- Use only lowercase letters, digits, and hyphens: `my-ref-2026`
- Never reuse a ref key for a different client — create a new key instead
- If a client's access should expire, remove their ref from `NDA_REFS` and
  re-upload (old links will then show the "link incomplete" page)

---

## Part 5 — Sending the Link to a Client

The link format is:
```
https://epirusassets.com/nda.html?ref=YOUR-REF-KEY
```

Example:
```
https://epirusassets.com/nda.html?ref=sivota-2026
```

This can be shared via email or WhatsApp. There is no password. The page:
1. Reads the `?ref=` value
2. If valid, shows the NDA form
3. After the client signs, reveals only the property links mapped to that ref

If the `?ref=` is missing or misspelled, the client sees a polite message
asking them to contact you — they cannot guess other refs.

---

## Quick Reference

| Task                          | Where to edit                            |
|-------------------------------|------------------------------------------|
| Add or remove a ref           | `NDA_REFS` block in `nda.html`           |
| Add or update a property link | Inside the `properties` array of the ref |
| Paste NDA text from PDF       | `UI_STRINGS.en.nda_body` / `.el.nda_body` |
| Change Formspree endpoint     | `FORMSPREE_ENDPOINT` in `nda.html`       |
| Change contact phone/email    | Hardcoded in the `<p class="invalid-contact">` block |
