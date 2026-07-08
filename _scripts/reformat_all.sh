#!/usr/bin/env zsh

set -euo pipefail

for file in resources/codesets/*.ttl; do
    echo $file
    kurra file reformat "$file"
done
