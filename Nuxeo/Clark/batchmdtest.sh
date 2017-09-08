#!/bin/bash

# Place script in folder with TSV files to batch load
# Update path to the `meta_from_csv.py` file in your local environment
# This script performs a dry run of the meta_from_csv.py on the TSV files and should exit if errors are encountered

set -euo pipefail

for f in *.tsv; do
  python ~/nuxeo_spreadsheet/csv2dict/meta_from_csv.py --datafile "$f" -d
done