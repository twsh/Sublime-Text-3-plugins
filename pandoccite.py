# Display bibliography entries in a quickpanel.
# Insert a Pandoc cite key on selection.

import os
import sublime_plugin
import re
import sys

# Needed to find my functions
sys.path.append('/usr/local/lib/python3.4/site-packages')


from bibtexparser.bparser import BibTexParser

citation_styles =\
    {
        'pandoc': '@{}',
        'mmd': '[][#{}]'
    }

style = 'pandoc'


def remove_biblatex(string):
    """ str -> str
    Remove some ugly features of biblatex.
    >>> remove_biblatex("{This} \emph{is} ``a'' `test': \&.")
    'This is \"a\" \'test\': &.'
    """
    string = re.sub('{|}', '', string)
    string = re.sub('\\\\emph', '', string)
    string = re.sub('``', '"', string)
    string = re.sub("''", '"', string)
    string = re.sub('`', "'", string)
    string = re.sub('\\\\&', '&', string)
    return string


def record_to_tuple(record, bibliography):
    """ dict, dict -> tuple of str
    Take a dictionary representing a biblatex record,
    and one representing a bibliography.
    Return a tuple of a formatted description and its citekey.
    >>> record_to_tuple(
        {
            'year': '1986',
            'id': 'Chomsky1986',
            'type': 'book',
            'booktitle': 'Knowledge of Language',
            'publisher': 'Praeger',
            'location': 'New York, NY',
            'subtitle': 'Its Nature, Origin, and Use',
            'date-modified': '2014-08-28 19:22:11 +0000',
            'author': 'Chomsky, Noam',
            'date-added': '2014-08-28 19:22:11 +0000',
            'title':
            'Knowledge of Language'
        },
        {
            'Chomsky1986':
            {
                'year': '1986',
                'id': 'Chomsky1986',
                'type': 'book',
                'booktitle': 'Knowledge of Language',
                'publisher': 'Praeger',
                'location': 'New York, NY',
                'subtitle': 'Its Nature, Origin, and Use',
                'date-modified': '2014-08-28 19:22:11 +0000',
                'author': 'Chomsky, Noam',
                'date-added': '2014-08-28 19:22:11 +0000',
                'title': 'Knowledge of Language'
            },
            'Chomsky1995a':
            {
                'number': '413',
                'pages': '1--61',
                'id': 'Chomsky1995a',
                'type': 'article',
                'doi': '10.1093/mind/104.413.1',
                'date-modified': '2014-08-28 19:56:06 +0000',
                'read': '0',
                'volume': '104',
                'year': '1995',
                'journaltitle': 'Mind',
                'author': 'Chomsky, Noam',
                'title': 'Language and Nature',
                'date-added': '2014-08-28 19:22:22 +0000'
            },
            'HauserChomskyFitch2002':
            {
                'pages': '1569--1579',
                'id': 'HauserChomskyFitch2002',
                'doi': '10.1126/science.298.5598.1569',
                'type': 'article',
                'date-modified': '2014-08-28 19:55:48 +0000',
                'read': '0',
                'volume': '298',
                'year': '2002',
                'journaltitle': 'Science',
                'author': 'Hauser, Marc D. and Chomsky, Noam and Fitch, W. Tecumseh',
                'title': 'The Faculty of Language: What is it, who Has it, and How Did it Evolve?',
                'date-added': '2014-08-28 19:22:37 +0000'
            },
            'Chomsky2003':
            {
                'crossref': 'AntonyHornstein2003',
                'id': 'Chomsky2003',
                'type': 'incollection',
                'date-modified': '2014-08-28 19:55:53 +0000',
                'read': '0',
                'author': 'Chomsky, Noam',
                'date-added': '2014-08-28 19:23:02 +0000',
                'title': 'Reply to {Ludlow}'
            },
            'AntonyHornstein2003':
            {
                'year': '2003',
                'id': 'AntonyHornstein2003',
                'type': 'book',
                'editor': 'Antony, Louise M. and Hornstein, Norbert',
                'booktitle': '{Chomsky} and His Critics',
                'publisher': 'Blackwell',
                'location': 'Oxford',
                'date-modified': '2014-08-28 19:24:06 +0000',
                'title': '{Chomsky} and His Critics',
                'date-added': '2014-08-28 19:24:06 +0000'
            },
            'Chomsky1995':
            {
                'year': '1995',
                'id': 'Chomsky1995',
                'type': 'book',
                'booktitle': 'The Minimalist Program',
                'publisher': 'MIT Press',
                'location': 'Cambridge, MA',
                'date-modified': '2014-08-28 19:22:52 +0000',
                'author': 'Chomsky, Noam',
                'date-added': '2014-08-28 19:22:52 +0000',
                'title': 'The Minimalist Program'
            },
            'Chomsky1995b':
            {
                'crossref': 'Chomsky1995',
                'id': 'Chomsky1995b',
                'type': 'inbook',
                'read': '0',
                'date-modified': '2014-08-28 19:55:58 +0000',
                'title': 'Categories and Transformations',
                'date-added': '2014-08-28 19:22:50 +0000'
            }
        }
    )
    ('Chomsky, Noam (1986) Knowledge of Language', 'Chomsky1986')
    """
    list_of_parts = []
    if 'author' in record:
        list_of_parts.append(record['author'])
    elif 'editor' in record:
        list_of_parts.append('{} (ed)'.format(record['editor']))
    elif 'crossref' in record:
        crossref_record = bibliography[record['crossref']]
        if 'author' in crossref_record:
            list_of_parts.append(crossref_record['author'])
        elif 'editor' in crossref_record:
            list_of_parts.append('{} (ed)'.format(crossref_record['editor']))
    if 'year' in record:
        list_of_parts.append('({})'.format(record['year']))
    elif 'crossref' in record:
        crossref_record = bibliography[record['crossref']]
        if 'year' in crossref_record:
            list_of_parts.append('({})'.format(crossref_record['year']))
    if 'title' in record:
        list_of_parts.append(record['title'])
    if list_of_parts:
        return remove_biblatex(' '.join(list_of_parts)), record['id']


class insert_keyCommand(sublime_plugin.TextCommand):

    def run(self, edit, key):
        formatted_key = citation_styles[style].format(key)
        point = self.view.sel()[0].begin()
        self.view.insert(edit, point, formatted_key)
        print('I inserted {} at {}.'.format(key, point))


class pdcCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        def on_done(choice):
            if choice < 0:
                return
            # Needed to allow the user to escape.
            else:
                key = list_of_tuples[choice][1]
                # We need a separate command because
                # the edit object has been returned.
                self.view.run_command('insert_key', {'key': key})

        filename = self.view.file_name()
        directory = os.path.split(filename)[0]
        # This gives the filename in the view,
        # so if the console is open it goes wrong.
        list_of_bibfiles =\
            [os.path.join(directory, x) for x in os.listdir(directory)
                if os.path.splitext(x)[1] == '.bib']
        # Make a list of all the paths of files in the same directory
        # as the current view iff their extension is '.bib'.
        if list_of_bibfiles:
            print(
                'I found these bibliography files: {}.'.format(
                    ', '.join(list_of_bibfiles)
                )
            )
            records = {}
            for bibfile in list_of_bibfiles:
                with open(bibfile, 'r', encoding='UTF-8') as file:
                    bibfile_dictionary = BibTexParser(
                        file.read(),
                        ignore_nonstandard_types=False
                    ).entries_dict
                # For some reason it will try for ASCII without the encoding.
                records.update(bibfile_dictionary)
        else:
            raise FileNotFoundError(
                "I couldn't find any bibliography files."
            )
        list_of_tuples = sorted(
            [record_to_tuple(records[x], records) for x in records]
        )
        list_of_strings = [x[0] for x in list_of_tuples]
        self.view.window().show_quick_panel(list_of_strings, on_done)
