# Insert a link to a header chosen from a menu.

import re
import sublime
import sublime_plugin


def get_label(header):
    """ str -> str
    Take a string.
    Return the automatic label Pandoc would use for that header:
    http://pandoc.org/README.html#header-identifiers-in-html-latex-and-context
    This function can't check for duplicate identifiers.
    >>> get_label('A header')
    '#a-header'
    >>> get_label('A header!')
    '#a-header'
    >>> get_label('1. A header')
    '#a-header'
    >>> get_label('François')
    '#françois'
    """
    # Make lower case
    header = header.strip().lower()
    # Replace spaces and newlines with hyphens (do this before removing characters)
    header = re.sub('\s', '-', header)
    # Remove everything but alphanumeric characters, hyphens, underscores and periods
    header = re.sub('[^(\w|\-|\.)]', '', header)
    # Find the index of the first letter
    first_letter = re.search('[a-z]', header).start()
    # Make the identifier
    header = header[first_letter:]
    # Return an identifier, or the placeholder if one wasn't made
    if header:
        return '#' + header
    else:
        return '#section'


def get_headers(text):
    """ str -> list of str
    Take a string (i.e. the text of a document).
    Return a list of strings which are the lines in the text that are
    ATX style Markdown headers.
    (A header is 0--3 spaces, 1--6 octothorpes, one or more spaces,
    then one or more non-space characters.)
    Ignore headers marked as unnumbered with '{-}'
    >>> get_headers(
            'This is a line\n'
            '# This is a level one header\n'
            'This is a second line\n'
            '## This is a level two header\n'
            'This is a third line\n'
            '# References {-}'
        )
    ['# This is a level one header', '## This is a level two header']
    """
    lines = text.split('\n')
    return [x.strip() for x in lines if re.match('\s{0,3}#{1,6}\s+\S+', x) and not x.rstrip().endswith('{-}')]


class insert_refheader(sublime_plugin.TextCommand):

    def run(self, edit, header):
        label = get_label(header)
        reference = '[{}]({})'.format(
            header.lstrip('#').strip(),
            label
        )
        point = self.view.sel()[0].begin()
        self.view.insert(edit, point, reference)
        print('I inserted {} at {}.'.format(reference, point))


class refheaderCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(choice):
            if choice < 0:
                return
            # Needed to allow the user to escape.
            else:
                header = list_of_headers[choice]
                # We need a separate command because
                # the edit object has been returned.
                self.view.run_command('insert_refheader', {'header': header})
        text = self.view.substr(sublime.Region(0, self.view.size()))
        list_of_headers = get_headers(text)
        self.view.window().show_quick_panel(list_of_headers, on_done)
