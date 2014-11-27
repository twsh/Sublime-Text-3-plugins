# Insert a link to an example chosen from a menu.

import sublime
import sublime_plugin
import re
import sys

# Needed to find my functions
sys.path.append('/usr/local/lib/python3.4/site-packages')


def get_examples(text):
    """ str -> list of str
    Take a string (i.e. the text of a document).
    Return a list of strings which are Pandoc numbered examples with references.
    The list is ordered and duplicates are removed.
    (Looks for lines starting with 0--3 spaces,
    '(@', some alphanumeric characters, underscores and hyphens, and ')'.)
    >>> get_examples(
        'A line\n'
        '\n'
        '(@foo) Foo.'
        '\n'
        'A line\n'
        '\n'
        '(@bar) Bar.'
        '\n'
        'A line\n'
        '\n'
        '(@) Zip.'
        '\n'
        'A line\n'
        '\n'
        '(@bar) Bar.'
    )
    ['(@bar) Bar', '(@foo) Foo.']
    """
    lines = text.split('\n')
    return sorted(
        list(
            set(
                [x.strip() for x in lines if re.match('\s{0,3}\(@[A-Za-z0-9_-]+\)', x)]
            )
        )
    )


class insert_refexample(sublime_plugin.TextCommand):

    def run(self, edit, example):
        reference = re.match('\(@[A-Za-z0-9_-]+\)', example).group(0)
        point = self.view.sel()[0].begin()
        self.view.insert(edit, point, reference)
        print('I inserted {} at {}.'.format(reference, point))


class refexampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(choice):
            if choice < 0:
                return
            # Needed to allow the user to escape.
            else:
                example = list_of_examples[choice]
                # We need a separate command because
                # the edit object has been returned.
                self.view.run_command('insert_refexample', {'example': example})
        text = self.view.substr(sublime.Region(0, self.view.size()))
        list_of_examples = get_examples(text)
        self.view.window().show_quick_panel(list_of_examples, on_done)
