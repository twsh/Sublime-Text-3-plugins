# Do a wordcount and insert the result into the metadata

import sublime
import sublime_plugin
import subprocess


class UpdateWordsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print(self.view.file_name())
        command = '~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Sublime-Text-3-plugins/pandocwc.sh {}'.format(self.view.file_name())
        b = subprocess.check_output([command], shell=True)
        words = b.decode(encoding='utf-8').split()[0].strip()
        region = self.view.find('words:.+', 0)
        self.view.replace(edit, region, 'words: {}'.format(words))
