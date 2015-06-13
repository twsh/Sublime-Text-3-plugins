#!/bin/sh

# Assumptons: There is only one YAML block and it's at the start

tr '\n' ' ' < "$1" | perl -pe 's/---.+?\.\.\.//' | perl -pe 's/{[>>|\-\-].+?[<<|\-\-]}//g' | perl -pe 's/{\+\+(.+?)\+\+}/\1/g' | perl -pe 's/\[@.+?\][[:punct:]]?|@\w+\s?(\[.+?\])?[[:punct:]]?//g' | perl -pe 's/\[.+?\]\(#.+?\)//' | wc -w
