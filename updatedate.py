# Changes the first occurrence of a string of the form 'date: 20 August 2014'
# to one with the current date.

import datetime
import sublime_plugin


class UpdateDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        today = datetime.datetime.now().strftime('%-e %B %Y')
        region = self.view.find('date:\\s*\\d{1,2}\\s\\w*\\s*\\d{4}', 0)
        self.view.replace(edit, region, 'date: {}'.format(today))
