# pandoccite.py

I often want to insert a cite key in Pandoc's format. This plugin looks for Biblatex files, i.e. files with the extension `.bib`, in the same directory as the text file being edited and creates a searchable drop-down menu. Selecting an entry inserts its key at the cursor. I based the code on part of the excellent [LaTeXTools](https://sublime.wbond.net/packages/LaTeXTools) package. You will need to have installed the Python [bibtexparser](https://pypi.python.org/pypi/bibtexparser) package. One complication is that installing the package using PIP doesn't automatically make it available to Sublime Text 3. My code adds it to the path assuming that it's where PIP installs it. If you have the package somewhere different you will need to amend the code appropriately.

# headers.py

I use ATX style ('#') headers in my Markdown. This plugin provides two commands. One inserts a heading at the current level, or at level one if the level is zero. The second inserts a heading at one level below the current heading up to to maximum of six.

# sectionreference.py

This plugin creates a searchable drop-down menu of the headers defined in the text file. When selected a link to that header is inserted. It is assumed that the label is the one Pandoc would assign by default.

# updatedate.py

I put a YAML metadata header in my files. This plugin replaces the date field with the current date.

# updatewords.py

This plugin counts the words in the document (excluding YAML metadata) and replaces the current `words:` metadata field with the count. LaTeX is ignored, and references won't be counted.

# examplereference.py

This plugin looks for numbered examples as defined by Pandoc and creates a serachable drop-down menu. Selecting an example inserts that examples label at the cursor.
