# Figure out the current header depth.
# The command `header` inserts an ATX header of that depth;
# the command `headerplus` inserts an ATX header one deeper.

import re
import sublime
import sublime_plugin


octothorpe_to_depth =\
    {
        '#': 1,
        '##': 2,
        '###': 3,
        '####': 4,
        '#####': 5,
        '######': 6
    }

depth_to_octothorpe =\
    {octothorpe_to_depth[key]: key for key in octothorpe_to_depth}


def get_depth(text, octothorpe_to_depth):
    """ str, dict -> int between 0 and 6
    Take a string and a dictionary representing a mapping of octothorpes to
    depths; return what the current depth of ATX header is.
    >>> get_depth(
        'foo\n# A header\nbar',
        octothorpe_to_depth
    )
    1
    >>> get_depth(
        'foo\n## A header\nbar',
        octothorpe_to_depth
    )
    2
    >>> get_depth(
        'foo\nbar',
        octothorpe_to_depth
    )
    0
    """
    depth = 0
    lines = text.split('\n')
    for line in lines:
        for header in octothorpe_to_depth:
            if re.match('\s{{0,3}}{}\s'.format(header), line):
                depth = octothorpe_to_depth[header]
                break
    return depth


class headerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # The location of the cursor
        point = self.view.sel()[0].begin()
        # The path to the file
        filename = self.view.file_name()
        # Get all the text so far
        text = self.view.substr(sublime.Region(0, point))
        # Find the depth
        depth = get_depth(text, octothorpe_to_depth)
        if depth:
            self.view.insert(
                edit,
                point,
                '{} '.format(depth_to_octothorpe[depth])
            )
            print(
                'I inserted a header at {} of depth {} in {}.'.format(
                    point,
                    depth,
                    filename
                )
            )
        else:
            print("Depth is 0, so I can't insert a header.")


class headerincrementCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # The location of the cursor
        point = self.view.sel()[0].begin()
        # The path to the file
        filename = self.view.file_name()
        # Get all the text so far
        text = self.view.substr(sublime.Region(0, point))
        # Find the depth
        depth = get_depth(text, octothorpe_to_depth)
        if depth < 6:
            depth += 1
            self.view.insert(
                edit,
                point,
                '{} '.format(depth_to_octothorpe[depth])
            )
            print(
                'I inserted a header at {} of depth {} in {}.'.format(
                    point,
                    depth,
                    filename
                )
            )
        else:
            print("Depth is already 6, so I can't insert a header.")
