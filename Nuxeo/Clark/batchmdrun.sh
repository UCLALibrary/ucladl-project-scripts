#!/bin/bash

# Place script in folder with TSV files to batch load
# Update path to the `meta_from_csv.py` file in your local environment
# This script runs the meta_from_csv.py on the TSV files and should exit if errors are encountered

set -euo pipefail

for f in *.tsv; do
  python /Users/kirschbombe/nuxeo_spreadsheet/csv2dict/meta_from_csv.py --datafile "$f"
done