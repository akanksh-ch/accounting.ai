<div align="center">

# accounting.ai

**From trial balance to financial statements, with a little help from AI.**

Read an Excel workbook. Classify accounts. Generate statements.

![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Model: MiniLM](https://img.shields.io/badge/model-MiniLM-FFD21E?style=flat-square)
![Format: Excel](https://img.shields.io/badge/input%20%2F%20output-.xlsx-217346?style=flat-square)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-7C3AED?style=flat-square)](LICENSE)

[Usage](#usage) · [Installation](#installation) · [Workbook format](#workbook-format) · [Contributing](#contributing)

</div>

---

**accounting.ai** is a Python command-line project that turns a trial balance into a **Profit and Loss** statement and a **Statement of Financial Position**. It compares account names with reference examples using sentence embeddings, then groups the balances into formatted Excel worksheets.

```text
                         accounting.ai
                              │
  Trial balance (.xlsx) ───────┤
                              ▼
                    Classify account names
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Profit and Loss          Statement of
                                 Financial Position
                 └────────────┬────────────┘
                              ▼
                   Financial statements (.xlsx)
```

> **Project status:** Early development. Account types are inferred from names; review the classifications and generated statements before relying on them.

## Table of contents

- [Features](#features)
- [Usage](#usage)
- [Installation](#installation)
- [Workbook format](#workbook-format)
- [How it works](#how-it-works)
- [Custom configuration](#custom-configuration)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

| | What you get |
| :--- | :--- |
| 🧠 **Account classification** | Matches account names to assets, liabilities, capital, revenue, or expenses. |
| 📊 **Two statements** | Writes Profit and Loss and Statement of Financial Position sheets into one workbook. |
| 🧮 **Balance check** | Includes the difference between assets and liabilities plus equity. |
| ✨ **Readable spreadsheets** | Applies bold totals, fixed column widths, frozen panes, and two-decimal number formatting. |
| 💻 **Local inference** | Runs MiniLM on the CPU after the model is downloaded. No API key is required. |

## Usage

[↑ Back to top](#accountingai)

After [installation](#installation), run these commands from the repository root.

### Generate statements

Try the included [sample trial balance](sample.xlsx):

```bash
uv run python -m accounting_ai sample.xlsx statements.xlsx
```

On success:

```text
Financial statements saved to statements.xlsx
```

Or supply your own input and output paths:

```bash
uv run python -m accounting_ai "trial balance.xlsx" "financial statements.xlsx"
```

The first argument is the source workbook; the second is the destination. Choose a different output path to preserve your input. An existing destination file is overwritten, and its parent directory must already exist.

### Show command help

```bash
uv run python -m accounting_ai --help
```

### Classify a single account

```bash
uv run python -m accounting_ai.classify "Cash"
```

This prints the suggested account type: `asset`, `liability`, `capital`, `revenue`, or `expenses`.

## Installation

[↑ Back to top](#accountingai)

You need **Python 3.14 or newer** and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone https://github.com/akanksh-ch/accounting.ai.git
cd accounting.ai
uv sync
```

Then follow the [usage examples](#usage). The first classification run needs internet access to download `sentence-transformers/all-MiniLM-L6-v2`; later runs can use the cached model.

> Use `uv run python -m accounting_ai` for now. The `accounting-ai` console script is declared in the package metadata, but its target is not yet wired to the CLI implementation.

## Workbook format

[↑ Back to top](#accountingai)

The reader uses the **first worksheet**, skips row 1 as a header, and reads the first three columns in this order:

| Account Title | Debit | Credit |
| :--- | ---: | ---: |
| Cash | 16,200 | |
| Supplies | 1,300 | |
| Prepaid Insurance | 550 | |
| Equipment | 5,300 | |
| Notes Payable | | 5,200 |
| Accounts Payable | | 2,900 |

*Excerpt from [sample.xlsx](sample.xlsx); this is not the complete trial balance.*

- Put the account name in column **A**, debit in **B**, and credit in **C**. Header wording is flexible; column order is fixed.
- Use numeric Excel cells for amounts, with one populated amount per row. Leave the unused side blank; a debit of `0` still counts as a populated debit.
- Keep the data contiguous, without blank rows, subtotals, or a grand-total row. Every row after the header is treated as an account.
- Supply amounts as values rather than formulas. The reader does not evaluate Excel formulas.

If both debit and credit are populated, the current reader takes the debit. Extra worksheets and columns are ignored.

## How it works

[↑ Back to top](#accountingai)

1. **Read.** `openpyxl` extracts account names and debit or credit amounts from the workbook.
2. **Classify.** MiniLM embeds each name and compares it with representative account names using cosine similarity. The closest reference determines the account type.
3. **Group.** Assets and expenses use debit as their normal side; liabilities, capital, and revenue use credit. Entries on the opposite side reduce their category total.
4. **Export.** The report builder writes both statements, carries the period's profit or loss into equity, and adds a balance check.

| Worksheet | Contents |
| :--- | :--- |
| **Profit and Loss** | Revenue, expenses, category totals, and profit or loss for the period. |
| **Statement of Financial Position** | Assets, liabilities, capital, period profit or loss, total equity, and a balance check. |

The balance check is **assets − liabilities − capital − profit** and should be zero for a balanced result. A zero check does not establish that every account was classified correctly. The classifier always chooses its closest match; there is currently no confidence threshold or review prompt.

## Custom configuration

[↑ Back to top](#accountingai)

Classification settings currently live in [classify.py](src/accounting_ai/classify.py):

| Setting | Purpose |
| :--- | :--- |
| `MODEL_NAME` | Selects the Sentence Transformer model. |
| `ACCOUNT_EXAMPLES` | Defines the reference account names for each category. |

To adapt classification to your chart of accounts, add representative names to the appropriate category in `ACCOUNT_EXAMPLES`. Restart the command after editing; reference embeddings are cached for the lifetime of the process.

## Project structure

```text
accounting.ai/
├── src/accounting_ai/
│   ├── __main__.py         # Command-line arguments and workflow
│   ├── excel.py            # Trial balance reader
│   ├── classify.py         # MiniLM account classification
│   ├── build_report.py     # Statement generation and formatting
│   └── types/
│       └── ledger.py       # Ledger model and account enums
├── sample.xlsx             # Example trial balance
├── pyproject.toml          # Package metadata and dependencies
├── uv.lock                 # Dependency lockfile
└── LICENSE                 # GNU GPL v3
```

## Contributing

[↑ Back to top](#accountingai)

Issues and pull requests are welcome. Useful areas to improve include account classification, workbook validation, and report formatting.

For a bug report, include the command you ran, the expected result, and a small example using fictional account data. For changes, explain the behavior and how you verified it.

[Report an issue](https://github.com/akanksh-ch/accounting.ai/issues) · [Open a pull request](https://github.com/akanksh-ch/accounting.ai/pulls)

## License

Licensed under the [GNU General Public License v3.0](LICENSE).

---

<div align="center">

Built by <a href="https://github.com/akanksh-ch">Akanksh Chitimalla</a>.<br>
README layout inspired by <a href="https://github.com/athityakumar/colorls">colorls</a>.

</div>
