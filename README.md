# DAR List Parser

Tools for parsing Revolutionary War–era compiled lists (especially the **DAR Forgotten Patriots** volume) into structured CSV files suitable for genealogical work, including WikiTree and similar projects.

This repository currently supports:

- A **general DAR-style parser** (`original_parser.py`)
- A **Virginia-specific parser** (`virginia_parser.py`)
- A **PDF → text extractor** tuned for DAR pages (`pdf_to_text.py`)
- A simple **web interface** for non-technical users (`webapp.py`)
- A basic **OpenRefine import schema** for post-processing

MIT licensed.

---

## Output schema (columns)

All parsers output the same 9 columns in this order:

1. `Wiki-ID of Member Working` — left blank for now (for your project to fill)
2. `Wiki-ID` — left blank for now
3. `Surname`
4. `First Name`
5. `Race`  
   - African-descended entries are normalized to `AA`
   - More detailed race text (e.g. `African American (“a man of colour”)`) is preserved in **Notes** as `Race detail: ...`
6. `Owner`  
   - Phrases like `enslaved man of`, `slave of`, `property of`, `hired by`, etc.
7. `Service`  
   - Terms like `Soldier`, `Private`, `Pvt`, `Patriotic Service`, `Seaman`, `Drummer`, etc.
8. `Source`  
   - Codes like `M881`, `MKM:4:43`, `SFPPV:32`, always prefixed with `DAR, ...`
9. `Notes`  
   - Locations (`res. York`, `no residence given`, `1790MD Charles Co.`),
   - Parenthetical notes,
   - Race details if collapsed to `AA`,
   - Anything not clearly race, owner, service, or source.

---

## For genealogists (non-technical users)

### Easiest: use the web interface

Your project admin (Liz!) can host this tool on a home server.

From the genealogist side, you:

1. Go to the URL Liz gives you (something like `https://<server>/`).
2. On the page **DAR List Parser**:
   - Either **upload** a PDF or TXT file,  
   - OR paste the text of the list into the big text box.
3. Choose:
   - **General parser** (most lists like Maine, Maryland, etc.), or  
   - **Virginia parser** (for the Virginia chapter content).
4. Choose output format:
   - Pipe-delimited (`|`) is recommended for use with OpenRefine and Excel.
5. Click **Process**.
6. Your browser will download a file called `parsed_output.csv`.
7. Open that CSV in:
   - Excel
   - Google Sheets
   - LibreOffice
   - Or import into OpenRefine (see below).

You **do not** need to install Python, Docker, or anything else if the web tool is hosted for you.

---

## For power users: CLI usage

### Requirements

- Python 3.10+  
- `pip install pymupdf` (for PDF extraction)

You can optionally install Flask if you want to run the web app locally:

```bash
pip install flask pymupdf
