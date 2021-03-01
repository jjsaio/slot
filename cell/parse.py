
import lark

from .util import moduleFile, strWithFileAtPath


INTERPRETER_MODES = [
    "interpreter",
    "interactive",
]


class Parser(object):

    def __init__(self, mode = "interpreter", shortcuts = True):
        assert(mode in INTERPRETER_MODES)
        self.mode = mode
        self.shortcuts = shortcuts
        self.grammar = "start: {}\n".format(self.mode)
        self.grammar += strWithFileAtPath(moduleFile(__file__, 'cell.g'))
        if shortcuts:
            self.grammar += strWithFileAtPath(moduleFile(__file__, 'shortcuts.g'))
        else:
            self.grammar += "syntactic_shortcut: \n"
        self.parser = lark.Lark(self.grammar)

    def parse(self, text, raise_if_not_parseable = True):
        try:
            return ParseTree(self, self.parser.parse(text))
        except lark.ParseError:
            if raise_if_not_parseable:
                raise
            return None

    def parses(self, text):
        return bool(self.parse(text, raise_if_not_parseable = False))


class ParseTree(object):

    def __init__(self, parser, tree):
        self.parser = parser
        self.tree = tree

    def visualize(self, png_path = None, show = False):
        from lark.tree import pydot__tree_to_png
        png_path = png_path or "/tmp/cell.png"
        pydot__tree_to_png(self.tree, png_path)
        if show:
            import subprocess
            subprocess.call(['open', png_path])
