# prl_joai_add_harvests

This script is used to programmatically add scheduled harvests to jOAI, eliminating the need to manually fill out and submit a form for each harvest. It functions essentially as a CSV uploader for jOAI.

## System requirements

You need Python 3 to run this script.

## Installation

1. Download the files in this directory to your computer.
1. Create a virtual environment for the third-party dependencies:
    ```bash
    python3 -m venv venv_prl_joai_add_harvests
    ```
1. Activate the virtual environment:
    ```bash
    . venv_prl_joai_add_harvests/bin/activate
    ```
1. Install third-party dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## Usage

Running the script takes the user to a REPL that provides usage hints. The script can be run with no arguments if interacting with the test environment. To interact with the production environment, you must point it to the production jOAI instance.

For usage instructions:
```bash
./prl_joai_add_harvests.py -h
```

The input CSV file should be filled out with a row for each harvest to add to jOAI. Here are the rules:
- The values in the `Repository name`, `Repository base URL`, and `OAI-PMH SetSpec` must be wrapped in single quotes. All other columns must NOT be wrapped in quotes.
- To harvest an entire repository, leave the `OAI-PMH SetSpec` column blank.
- `Harvest every X days` must be an integer.
- `Harvest at time T` must be a datetime formatted like `%H%M` (e.g., `03:00`, `23:59`).
- To skip a row in the CSV, put something in the `skip` column so that it is not empty.

You will probably want to use the CSV file at <https://ucla.app.box.com/file/511596765114>.

## Error logs

The script logs errors to rotating logfiles that are each guaranteed not to exceed 1 MiB in size.

If `prl_joai_add_harvests.debug.log.1` exists, it contains older entries than `prl_joai_add_harvests.debug.log`.
