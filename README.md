# Microw

Microw is a command-line interface (CLI) utility developed in Python to automate the conversion of tabular data (such as CSV or TXT files) into `.ini` configuration files compatible with the *MicroSIP* softphone and its derivatives.

This tool is ideal for VoIP system administrators, technical support teams, and developers who need to perform bulk provisioning of extensions quickly and accurately.

## Features

* **Flexible Mapping:** Define the column order of your input file via the command line.
* **Customizable Templates:** Use custom account templates for different network scenarios.
* **Label Patterns:** Generate dynamic display names (DisplayName) based on input data.
* **Ghost Account:** Option to add a "Disconnected" profile as the first account in the list.
* **Delimiter Support:** Works with commas, tabs (`\t`), semicolons, etc.

## How to Use

### Prerequisites

* Python 3.x installed.

### Installation

Simply clone the repository or download the `microw.py` file:

```bash
git clone https://github.com/LucioCarvalhoDev/microw.git
cd microw

```

### Basic Execution

Assuming you have a file named `your_data.csv` with the format `extension,label`:

```bash
python3 microw.py --input your_data.csv --output accounts.ini

```

---

## Argument Reference

| Argument | Default | Description |
| --- | --- | --- |
| `--format` | `"extension label"` | Column order (use `_` to ignore columns). |
| `--input` | `./input.txt` | Path to the source file. |
| `--output` | `./output.ini` | Path to the generated `.ini` file. |
| `--delimiter` | `,` | Column separator character. |
| `--label-pattern` | `label` | Template for the display name (e.g., `"extension - label"`). |
| `--add-ghost` | `False` | Adds a 'Disconnected' account at the top. |
| `--set-template` | `None` | Path to a custom account template file. |

---

## Usage Examples

### 1. CSV Format with Semicolons

If your file follows the pattern `ID;Extension;Name;Department` and you want to ignore the ID:

```bash
python3 microw.py --delimiter ";" --format "_ extension label department"

```

### 2. Customizing the Display Name

To make the name appear in MicroSIP as `Extension | Name (Department)`:

```bash
python3 microw.py --format "extension label department" --label-pattern "extension | label (department)"

```

### 3. Using a Specific Account Template

If you need different transport settings (TLS/TCP) or ports, create a template file and point to it:

```bash
python3 microw.py --set-template my_template.txt --input extensions.txt

```

---

## License and Credits

Developed by **Lúcio Carvalho Almeida**.

This project is **Open Source**.

**Contact:** [luciocarvalhodev@gmail.com](mailto:luciocarvalhodev@gmail.com)

---

Feel free to contribute with Pull Requests!

---
