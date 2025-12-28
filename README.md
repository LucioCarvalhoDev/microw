# Microw

Microw is a command-line interface (CLI) utility developed in Python to automate the conversion of tabular data (such as CSV or TXT files) into `.ini` configuration files compatible with the *MicroSIP* softphone and its derivatives.

This tool is ideal for VoIP system administrators, technical support teams, and developers who need to perform bulk provisioning of extensions quickly and accurately.

## Features

* **Flexible Mapping:** Define the column order of your input file via the command line.
* **Customizable Templates:** Use custom account templates for different network scenarios.
* **Label Patterns:** Generate dynamic display names (DisplayName) based on input data.
* **Ghost Account:** Option to add a "Disconnected" profile as the first account in the list.
* **Delimiter Support:** Works with commas, tabs (`\t`), semicolons, etc.
* **Sorting:** Sort accounts alphabetically by a specified column.
* **Encoding Support:** Specify input and output file encodings.
* **Call Handling:** Configure automatic call rejection and answering.

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

Assuming you have a file named `your_data.csv` with the format `ramal,label`:

```bash
python3 microw.py --input-file your_data.csv --output-file accounts.ini

```

---

## Argument Reference

| Argument | Default | Description |
| --- | --- | --- |
| `--columns` | `"ramal label"` | Define the column order of the input file. Use variable names (e.g., ramal, password) or '_' to ignore columns. |
| `--input-file` | `./input.txt` | Path to the source file. |
| `--output-file` | `./output.ini` | Path to the generated `.ini` file. |
| `--delimiter` | `,` | Column separator character. |
| `--label-pattern` | `label` | Template for the display name (e.g., `"ramal - label"`). |
| `--add-ghost` | `False` | Adds a 'Disconnected' account at the top. |
| `--set-template` | `None` | Path to a custom account template file. |
| `--set-password` | `None` | Sets a single password for all accounts. |
| `--set-server` | `None` | Sets the server for all accounts. |
| `--read-encoding` | `utf-8` | Encoding for reading the input file. |
| `--write-encoding` | `utf-8` | Encoding for writing the output file. |
| `--sort` | `True` | Sorts the accounts in the final file. |
| `--sort-by` | `ramal` | Column to use for alphabetical sorting. |
| `--deny-incoming` | `button` | Defines if the app will reject calls automatically. Possible values: all, no, server, user, button. |
| `--auto-answer` | `button` | Enables automatic call answering. Possible values: all, no, button. |
| `--help` | `False` | Displays the manual. |

---

## Usage Examples

### 1. CSV Format with Semicolons

If your file follows the pattern `ID;ramal;nome;setor` and you want to ignore the ID:

```bash
python3 microw.py --delimiter ";" --columns "_ ramal nome setor"

```

### 2. Customizing the Display Name

To make the name appear in MicroSIP as `ramal | nome (setor)`:

```bash
python3 microw.py --columns "ramal nome setor" --label-pattern "ramal | nome (setor)"

```

### 3. Using a Specific Account Template

If you need different transport settings (TLS/TCP) or ports, create a template file and point to it:

```bash
python3 microw.py --set-template my_template.txt --input-file extensions.txt

```

---

## License and Credits

Developed by **Lúcio Carvalho Almeida**.

This project is **Open Source**.

**Contact:** [luciocarvalhodev@gmail.com](mailto:luciocarvalhodev@gmail.com)

---

Feel free to contribute with Pull Requests!

---
