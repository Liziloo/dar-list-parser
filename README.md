# DAR List Parser

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status: Under Active Development](https://img.shields.io/badge/Status-Active-yellow.svg)

Parsers for transforming DAR *Forgotten Patriots* state lists into structured, pipe-delimited data suitable for genealogical research, digital humanities work, archival record-linkage, and computational analysis.

This project provides two related parsing systems:

- an **original/general parser** and  
- a **Virginia-specific parser**, a variant tuned for the formatting quirks of the Virginia section.

Both parsers extract **surname, first name, race, source, and notes** — they just use different rules for how to slice the raw text.

---

## 📚 Source Material (DAR Publication)

All parsed material derives from:

**Forgotten Patriots: African American and American Indian Patriots of the Revolutionary War**  
Daughters of the American Revolution (DAR)  

PDF link (publicly available from DAR):  
https://www.dar.org/sites/default/files/media/library/DARpublications/Forgotten_Patriots_ISBN-978-1-892237-10-1.pdf

Users should consult the original publication for context, editorial notes, and methodology.

---

## 🧩 Overview of the Two Parsers

### 1. Original / General DAR Parser

This is the parser that was in use **before the Virginia-specific adjustments** and is suitable for lists that follow the more typical DAR state formatting (e.g., the Maine work you’ve been doing).

It implements:

- **Surname extraction**  
  Text before the first comma in a line is treated as the surname block (including any slash-delimited variants like `ADERTON/ADDITION`).

- **First name extraction**  
  The first non-race, non-ALL-CAPS token after the surname is treated as the given name block (e.g., `FRANK JOSEPH`, `1st SON`, etc.).

- **Race extraction**  
  Any phrase indicating race or ethnic/national identity is extracted into a dedicated **Race** column.  
  Examples (kept verbatim):  
  - `Maliseet Indian`  
  - `Micmac Indian/St. Johns Indian`  
  - `Passamoquoddy Indian`  
  - `African American`  

- **Source extraction**  
  ALL-CAPS abbreviations and source codes are grouped into the **Source** column, prefixed with:  
  `DAR, `  
  Examples: `MSS`, `SSME`, `MOEM`, `SJ6`, `DHME 14`, `WT76`, `MVBH:371`, etc.

- **Notes extraction**  
  Everything that is not surname, first_name, race, or ALL-CAPS code is preserved in the **Notes** column:  
  - residence: `res Machias`  
  - life details: `married Eunice summer of 1791; died July 7 1843`  
  - alternate names: `also listed as LYON LONDON`  
  - `no residence given`  
  - other free-text editorial hints

- **Output format**  
  Traditional, comma-delimited .csv file or pipe-delimited (`|`) with no escaping or quoting:
  ```text
  surname|first_name|race|source|notes

## 🔧 Installation

To install locally:
pip install .

For editable development mode:
pip install -e .

---

## 🚀 Usage

### Use the original/general DAR parser
dar-parse --original input.txt output.psv

### Use the Virginia-specific parser
dar-parse --virginia input.txt output.psv

### Output Format

All parser outputs are:

- pipe-delimited (|)
- unescaped (no quoting)
- UTF-8 text

Columns produced by both parsers:
surname | first_name | race | source | notes

These load cleanly into Google Sheets using:
Data → Split text to columns → Custom delimiter: |

