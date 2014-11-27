# Insert a link to a header chosen from a menu.

import re
import sublime
import sublime_plugin
import sys

# Needed to find my functions
sys.path.append('/usr/local/lib/python3.4/site-packages')


def get_headers(text):
    """ str -> list of str
    Take a string (i.e. the text of a document).
    Return a list of strings which are the lines in the text that are
    ATX style Markdown headers.
    (A header is 0--3 spaces, 1--6 octothorpes, one or more spaces,
    then one or more non-space characters.)
    >>> get_headers(
            'This is a line\n'
            '# This is a level one header\n'
            'This is a second line\n'
            '## This is a level two header\n'
            'This is a third line'
        )
    ['# This is a level one header', '## This is a level two header']
    """
    lines = text.split('\n')
    return [x.strip() for x in lines if re.match('\s{0,3}#{1,6}\s+\S+', x)]


def get_header_content(line):
    """ str -> str
    Take a string containing an ATX style header.
    Return a string with just the content i.e. with octothorpes stripped.
    (A simple substitution would fail with escaped octothorpes.)
    >>> get_header_content('# This is a header')
    'This is a header'
    >>> get_header_content('## This is a header ##')
    'This is a header'
    >>> get_header_content('## This is a header #')
    'This is a header'
    >>> get_header_content('# This is a \# header')
    'This is a \# header'
    >>> get_header_content('# This is a # header #')
    'This is a # header'
    >>> get_header_content('# This is a # header')
    'This is a # header'
    """
    content_begins = re.match('#{1,6}', line).end()
    return re.sub(
        '(?<!\\\\)#{0,6}(?!\s*\S)',
        ' ',
        line[content_begins:]
    ).strip()


def get_label(header):
    """ str -> str
    Take a string.
    Return the automatic label Pandoc would use for that header:
    http://johnmacfarlane.net/pandoc/README.html#header-identifiers-in-html-latex-and-context
    >>> get_label('A header')
    '#a-header'
    >>> get_label('A header!')
    '#a-header-'
    >>> get_label('1. A header')
    '#a-header'
    """
    header = header.strip().lower()
    first_letter = re.search('[a-z]', header).start()
    return '#' + re.sub('[^a-z0-9-_\.]', '-', header[first_letter:])


class insert_refheader(sublime_plugin.TextCommand):

    def run(self, edit, header):
        reference = '[{}]({})'.format(
            get_header_content(header),
            get_label(header)
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
