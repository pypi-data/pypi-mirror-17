#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Mozilla Corporation, Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Convert TikiWiki's language.php files to GetText PO files.

See: http://docs.translatehouse.org/projects/translate-toolkit/en/latest/commands/tiki2po.html
for examples and usage instructions.
"""

from translate.storage import po, tiki


class tiki2po(object):

    def __init__(self, includeunused=False):
        """
        :param includeunused: On conversion, should the "unused" section be
                              preserved?  Default: False
        """
        self.includeunused = includeunused

    def convertstore(self, thetikifile):
        """Converts a given (parsed) tiki file to a po file.

        :param thetikifile: a tikifile pre-loaded with input data
        """
        thetargetfile = po.pofile()

        # For each lang unit, make the new po unit accordingly
        for unit in thetikifile.units:
            if not self.includeunused and "unused" in unit.getlocations():
                continue
            newunit = po.pounit()
            newunit.source = unit.source
            newunit.target = unit.target
            locations = unit.getlocations()
            if locations:
                newunit.addlocations(locations)
            thetargetfile.addunit(newunit)
        return thetargetfile


def converttiki(inputfile, outputfile, template=None, includeunused=False):
    """Converts from tiki file format to po.

    :param inputfile: file handle of the source
    :param outputfile: file handle to write to
    :param template: unused
    :param includeunused: Include the "usused" section of the tiki
                          file? Default: False
    """
    convertor = tiki2po(includeunused=includeunused)
    inputstore = tiki.TikiStore(inputfile)
    outputstore = convertor.convertstore(inputstore)
    if outputstore.isempty():
        return False
    outputstore.serialize(outputfile)
    return True


def main(argv=None):
    """Converts tiki .php files to .po."""
    from translate.convert import convert

    formats = {"php": ("po", converttiki)}

    parser = convert.ConvertOptionParser(formats, description=__doc__)
    parser.add_option("", "--include-unused", dest="includeunused",
                      action="store_true", default=False,
                      help="Include strings in the unused section")
    parser.passthrough.append("includeunused")
    parser.run(argv)


if __name__ == '__main__':
    main()
