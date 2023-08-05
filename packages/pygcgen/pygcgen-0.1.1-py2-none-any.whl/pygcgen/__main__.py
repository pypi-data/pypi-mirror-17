# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re

from .options_parser import OptionsParser
from .generator import Generator


class ChangelogGenerator:
    ''' Class responsible for whole change log generation cycle. '''

    def __init__(self, options=None):
        '''
        @return initialised instance of ChangelogGenerator
        '''

        self.options = OptionsParser(options).options
        self.generator = Generator(self.options)

    def run(self):
        '''
        The entry point of this script to generate change log
        'ChangelogGeneratorError' Is thrown when one
        of the specified tags was not found in list of tags.
        '''
        if not self.options.project or not self.options.user:
            print("Project and/or user missing. For help run:\n  pygcgen --help")
            return

        log = self.generator.compound_changelog()

        def checkname(filename):
            if not os.path.exists(filename):
                return filename
            mtch = re.match(r'(?P<filename>.*?)(?P<nr>\d+)(?P<rest>($|.md)?)',
                            filename)
            if mtch:
                # filename exists, add a number
                nr = int(mtch.group("nr")) + 1
                filename = "{0}{1}{2}".format(mtch.group("filename"), nr,
                                              mtch.group("rest"))
            else:
                # filename exists, but doesn't end with a number -> add one.
                filename = filename.rsplit(".", 1)
                filename = filename[0] + "_1" + (("." + filename[1]) if
                                                 len(filename) > 1 else "")
            return checkname(filename)

        if self.options.no_overwrite:
            out = checkname(self.options.output)
        else:
            out = self.options.output

        with open(out, "w") as fh:
            fh.write(log.encode("utf8"))
        if self.options.verbose:
            print("Done!")
            print("Generated log placed in {0}/{1}".format(
                os.getcwd(), out)
            )


def run():
    ChangelogGenerator(sys.argv[1:]).run()


def run_gui():
    import wx
    from .gui import GeneratorApp, MainFrame
    app = GeneratorApp()
    wx.MessageBox("Not implemented yet.", os.path.basename(sys.argv[0]))
    # win = MainFrame(None).Show()
    # app.MainLoop()

if __name__ == "__main__":
    run()
