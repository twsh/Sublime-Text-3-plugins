# Do a wordcount using wc and insert the result into the metadata

import re
import sublime
import sublime_plugin


class UpdateWordsCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        text = self.view.substr(sublime.Region(0, self.view.size()))
        no_metadata = re.sub(
            '(?s)---.+?\n\.\.\.',
            '',
            text,
            count=1
        )
        words = str(
            len(
                [x for x in no_metadata.split() if not x.startswith('\\')]
            )
        )
        region = self.view.find('words:.+', 0)
        self.view.replace(edit, region, 'words: {}'.format(words))
