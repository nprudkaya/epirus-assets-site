# Skill: listing-description

Analyze real estate listing files and generate investor-focused property descriptions.

## Usage

User will specify one or more listing files from the `listings/` folder. Process each file and save results to `presentation/`.

Optional: user may specify output language. Default is **English**. Supported: `english`, `russian`, `greek`, `turkish`.

## Step-by-step instructions

### 1. Read the listing file(s)

Use the appropriate method based on file format:
- `.md` / `.txt` — use Read tool directly
- `.docx` — use `/docx` skill
- `.pdf` — use `/pdf` skill

If the user specifies multiple files, process each one independently.

### 2. Extract financial data

Look for the following values in the listing:
- **Selling price** (purchase price)
- **CAPEX** (renovation / fit-out budget)
- **Annual rental income** (gross)
- **ROI** (if not stated, calculate: `annual income / (price + CAPEX) × 100%`)
- **Payback period** (if not stated, calculate: `(price + CAPEX) / annual income`)

If any of the above **cannot be found** in the file, stop and ask the user to provide the missing values before continuing.

### 3. Generate the output

Produce the following sections in the specified language (default: English):

---

#### 🏷️ Marketing Name
A creative, investor-appealing property name. No street address. Evokes lifestyle, location character, or investment potential.
*Example: "Sunset Boutique Residences — Corfu Old Town"*

---

#### 📝 Property Overview
2–3 sentences. Highlight property type, location appeal, condition, and key feature. Written for a sophisticated investor audience.

---

#### 💰 Financial Summary

| Metric | Value |
|---|---|
| Selling Price | €... |
| CAPEX (estimated) | €... |
| Total Investment | €... |
| Gross Annual Income | €... |
| ROI | ...% |
| Payback Period | ... years |

If ROI or payback period were calculated (not taken from the listing), add a note: `* calculated based on provided figures`.

---

#### ⚖️ Legal & Investment Profile

- **Investment Type:** (e.g. Buy-to-let / Short-term rental / Development / Mixed)
- **Golden Visa Eligible:** Yes / No / Likely (explain briefly if relevant — threshold, zone restrictions, etc.)
- **Ownership Structure:** (freehold / leasehold / other — if stated)
- **Any legal notes:** (e.g. listed building, heritage zone, permit status — if mentioned)

---

#### ⭐ Unique Selling Points
1–2 concise bullet points. Focus on what makes this asset stand out for an investor: yield, location scarcity, upside potential, lifestyle premium, etc.

---

### 4. Save the output

- Create folder `presentation/` if it does not exist
- Save the result as: `presentation/<original-filename>-description.md`
  - Example: `listings/villa-corfu.pdf` → `presentation/villa-corfu-description.md`
- If processing multiple files, save each as a separate file

### 5. Confirm

After saving, tell the user:
- Which files were processed
- Where the output was saved
- Flag any missing data that was assumed or skipped

## Notes

- Tone: professional, concise, investor-facing. Avoid tourist/holiday language.
- Do not invent financial figures. Only calculate derived metrics (ROI, payback) from data present in the file or provided by the user.
- If the listing is in a language other than the output language, translate and adapt — do not transliterate.
