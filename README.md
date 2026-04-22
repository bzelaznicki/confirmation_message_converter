# Confirmation Message Converter

Small CLI utility for converting an HTML email template into a GetResponse confirmation message.

It takes an input HTML file, rewrites the confirmation link to the GetResponse confirmation macro, removes a few template-specific sections, and also generates a plain-text version of the message.

## What It Does

Given an input file like `template.html`, the converter creates:

- `template_converted.html`
- `template_converted.txt`

The HTML conversion currently performs these changes:

- Replaces any `<a>` tag whose `href` exactly matches the provided confirmation URL with the GetResponse confirmation macro shown below
- Removes `<td>` blocks whose class starts with `gr-footer-`
- Removes `<td>` blocks whose class starts with `gr-headerviewonline-`
- Replaces supported dynamic placeholders with GetResponse contact macros

Confirmation macro:

```text
{{LINK `confirm`}}
```

Supported placeholder replacements:

```text
[[firstname]] -> {{CONTACT `subscriber_first_name`}}
[[lastname]]  -> {{CONTACT `subscriber_last_name`}}
[[email]]     -> {{CONTACT `email`}}
[[name]]      -> {{CONTACT `name`}}
```

The plain-text output is generated from the converted HTML and replaces confirmation links with the same GetResponse confirmation macro.

## Requirements

- Python 3.13+
- Optional: `uv`

## Setup

### Option 1: `uv`

Install project dependencies:

```bash
uv sync
```

### Option 2: Standard Python virtual environment

Create a virtual environment and install the project locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage

### With `uv`

```bash
uv run python main.py path/to/template.html
```

With a custom confirmation URL:

```bash
uv run python main.py path/to/template.html --url "https://example.com/confirm"
```

### With standard Python

If you used a virtual environment, activate it first:

```bash
source .venv/bin/activate
```

Basic usage:

```bash
python main.py path/to/template.html
```

With a custom confirmation URL:

```bash
python main.py path/to/template.html --url "https://example.com/confirm"
```

If `--url` is omitted, the script uses this default placeholder URL:

```text
https://getresponse.com/?confirmation_click
```

Only links with an `href` that exactly matches the configured URL are rewritten.

## Example Workflow

Input:

- `welcome.html`

Run:

```bash
uv run python main.py welcome.html --url "https://my-site.example/confirm"
```

Output:

- `welcome_converted.html`
- `welcome_converted.txt`

## Notes

- Output files are written next to the original HTML file.
- The original input file is not modified.
- The converter expects the input to already be valid HTML email markup.
