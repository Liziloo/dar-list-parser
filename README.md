# DAR List Parser

This repository provides two parsers for DAR Forgotten Patriots state lists:

## 1. Maine-Style Parser
Implements:
- Race extraction (anything with “Indian”, “African American”, etc.)
- Source extraction: ALL-CAPS abbreviations only, prefixed with `DAR,`
- Notes: all remaining text
- Pipe-delimited `.psv` output with no escaping

## 2. Virginia-Style Parser
This is the earlier, simpler parser:
- Surname extracted from text before first comma
- First Name taken from the text after surname
- Source preserved as-is
- No Race separation, no ALL-CAPS extraction, no Notes logic

## Installation
