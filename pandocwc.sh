#!/bin/sh

# This won't count words in references
# Add a `--bibliography` option if you want that

pandoc --to plain "$1" | wc -w
