# Looks at section references and tries to find the section referred to.
# The number of that section in the reference is then updated.

import re
import sublime
import sublime_plugin


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


def dict_headers(l):
    """ list -> dict
    Take a list representing the ATX headers in a document,
    return a dictionary of the labels for the headers to a tuple
    representing the section numbers.
    >>> dict_headers(
        [
            '# This is a level one header',
            '## This is a level two header'
        ]
    )
    {
        '#this-is-a-level-one-header': ((1,), 'This is a level one header'),
        '#this-is-a-level-two-header': ((1, 1) 'This is a level two header')
    }
    """
    output = {}
    h1 = 0
    h2 = 0
    h3 = 0
    h4 = 0
    h5 = 0
    h6 = 0
    for header in l:
        sec = len(header[:header.rfind('#')+1].strip())
        title = header[header.rfind('#')+1:].strip()
        if sec == 1:
            h1 += 1
            h2 = 0
            h3 = 0
            h4 = 0
            h5 = 0
            h6 = 0
            tup = (h1,)
        elif sec == 2:
            h2 += 1
            h3 = 0
            h4 = 0
            h5 = 0
            h6 = 0
            tup = (h1, h2)
        elif sec == 3:
            h3 += 1
            h4 = 0
            h5 = 0
            h6 = 0
            tup = (h1, h2, h3)
        elif sec == 4:
            h4 += 1
            h5 = 0
            h6 = 0
            tup = (h1, h2, h3, h4)
        elif sec == 5:
            h5 += 1
            h6 = 0
            tup = (h1, h2, h3, h4, h5)
        elif sec == 6:
            h6 += 1
            tup = (h1, h2, h3, h4, h5, h6)
        output[get_label(title)] = tup, title
    return output


def get_sec_string(t):
    """ tuple -> str
    Take a tuple representing a section number,
    return a string representation.
    >>> get_sec_string((1, 2))
    '§1.2'
    """
    return '§' + '.'.join([str(i) for i in t])


class UpdateSectionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = self.view.substr(sublime.Region(0, self.view.size()))
        headers = dict_headers(get_headers(text))
        # The matches must be lazy
        matches = self.view.find_all('\[§.+?\]\(#.+?\)')
        non_referrers = set()
        for match in matches:
            # This could be cleaner with a neat regex
            try:
                match_text = text[match.begin():match.end()]
                ref = match_text[match_text.find('(')+1:match_text.find(')')]
                replace = '[{}]({})'.format(
                    get_sec_string(headers[ref][0]),
                    ref
                )
                self.view.replace(edit, match, replace)
            except KeyError:
                non_referrers.add(match_text)
        if non_referrers:
            print("I couldn't find sections corresponding to these labels:")
            for label in non_referrers:
                print(label)
