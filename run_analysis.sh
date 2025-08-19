#!/bin/bash

set -e
set -o pipefail

script_directory="$(perl -e 'use File::Basename;
  use Cwd "abs_path";
  print dirname(abs_path(@ARGV[0]));' -- "$0")"
cd "$script_directory" || exit

python3 00-download-data.py

Rscript -e "rmarkdown::render('01-heatmap.Rmd', clean = TRUE)"
