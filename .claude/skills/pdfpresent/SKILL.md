# Skill: pdfpresent

Full pipeline: PDF property brochure → extracted images → listing description → HTML presentation.

## Usage

User provides a folder path containing a single PDF file (developer brochure for a Golden Visa or investment property). The skill runs three sequential steps and asks for approval at the end of each step before continuing.

```
/pdfpresent <folder-path>
```

Example:
```
/pdfpresent C:\Users\nprud\epirus-assets\presentation\GV-Cosmo
```

---

## Step-by-step instructions

### Step 1 — Extract images from the PDF

1. Locate the PDF file in the specified folder (there is usually exactly one).
2. Run a Python script to extract all embedded images using `pypdf`:

```python
from pypdf import PdfReader

reader = PdfReader('file.pdf')
count = 0
for page_num, page in enumerate(reader.pages, 1):
    if '/XObject' not in page.get('/Resources', {}):
        continue
    xobj = page['/Resources']['/XObject'].get_object()
    img_num = 0
    for name, obj in xobj.items():
        o = obj.get_object()
        if o.get('/Subtype') == '/Image':
            img_num += 1
            try:
                data = o.get_data()
                ft = o.get('/Filter', '')
                fname = f'img_p{page_num:02d}_{img_num:02d}'
                fname += '.jpg' if ('DCT' in str(ft) or 'JPX' in str(ft)) else '.png'
                with open(fname, 'wb') as f:
                    f.write(data)
                count += 1
            except:
                pass
```

3. After extraction, report to the user:
   - How many images were extracted
   - A list of the largest images by file size (these are typically renders and photos, not icons)
   - Recommend which image to use as the **hero** (largest portrait or landscape render, typically on the cover page — `img_p01_01.*` or similar)
   - Recommend which image to use for the **contact slide** panel (second large render, or a wide interior shot)

4. **Ask for user approval before continuing.** Show the image list and suggested picks. Wait for confirmation or corrections (user may specify different images).

---

### Step 2 — Extract text and create listing description

1. Extract full text from the PDF using `pypdf`:

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pypdf import PdfReader
reader = PdfReader('file.pdf')
text = ''
for i, page in enumerate(reader.pages):
    t = page.extract_text()
    if t:
        text += f'--- PAGE {i+1} ---\n{t}\n'
print(text)
```

2. Parse the extracted text to identify:
   - Property name
   - Location (district, city, address if present)
   - Unit count and types
   - Floor layout
   - Unit sizes (internal m², total with balcony/terrace)
   - Price (if stated)
   - Energy class
   - Amenities and features
   - Any financial figures mentioned

3. Invoke the `/listing-description` skill, passing all extracted data as arguments along with:
   - The financial parameters the user has confirmed (or use defaults: price from €250,000, ROI ~3%, CAPEX €0 turn-key)
   - The output file path: `<folder-path>/<PropertyName>.md`

4. If financial data (price, ROI, CAPEX) is missing from the PDF and was not previously established, **stop and ask the user** before calling `/listing-description`.

5. After `/listing-description` completes, show the result to the user and **ask for approval** before continuing to Step 3.

---

### Step 3 — Create the HTML presentation

1. Once the listing description is approved, invoke the `/present` skill with:
   - The property name and source `.md` file
   - The hero image path confirmed in Step 1
   - The output path: `<parent-of-folder>/PropertyName.html`

Example argument format:
```
Property: Cosmo I. Source files: C:\...\Cosmo.md. Hero image: C:\...\img_p01_01.jpg (building cover photo). Output: C:\...\Cosmo.html
```

2. The `/present` skill will build the full 9-slide HTML presentation following the Epirus Assets brand system.

---

## Default financial parameters

These defaults apply when the property PDF does not state financial figures and the user has not provided them:

| Parameter | Default |
|---|---|
| Starting price | from €250,000 |
| CAPEX | €0 (turn-key delivery included in price) |
| Gross yield | ~3% |
| Annual income (min.) | from €7,500 / unit |
| Payback period | ~33 years |
| Furnished package | optional, extra cost, not included in CAPEX |

If the project is not Golden Visa eligible or the price differs significantly from €250,000, stop and confirm with the user before proceeding.

---

## Notes

- Run each step to completion before starting the next. Do not skip the approval gates.
- The image extraction script must be written to a `.py` file and executed — do not pass base64 or large data as a command-line argument.
- Images are saved into the same folder as the PDF.
- The listing description `.md` file is saved into the same folder as the PDF.
- The final `.html` presentation is saved one level up (into `presentation/`), named after the property.
- If the folder contains images already (from a previous run), skip extraction and go directly to showing the image list for user approval.
