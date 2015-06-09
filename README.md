# headers.py

I use ATX style ('#') headers in my Markdown. This plugin provides two commands. One inserts a heading at the current level, or at level one if the level is zero. The second inserts a heading at one level below the current heading up to to maximum of six.

# sectionreference.py

This plugin creates a searchable drop-down menu of the headers defined in the text file. When selected a link to that header is inserted. It is assumed that the label is the one Pandoc would assign by default.

# updatedate.py

I put a YAML metadata header in my files. This plugin replaces the date field with the current date.

# examplereference.py

This plugin looks for numbered examples as defined by Pandoc and creates a serachable drop-down menu. Selecting an example inserts that examples label at the cursor.

# updatewords.py

The script looks for a words field in a YAML metadata block and replaces it with the current word count. A helper bash script `pandocwc.sh` is used which removes YAML and other Pandoc things before counting with `wc`.
