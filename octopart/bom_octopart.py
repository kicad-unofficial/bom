# Generate an Octopart compatible BOM from a KiCad netlist.

"""
    @package Generates an Octopart compatible BOM from a KiCad netlist.

    Octopart's CSV format uses a "query" column to find components. This column
    is generated from the (non-standard) "Octopart Query" field on each
    component.

    The symbols in https://github.com/kicad-unofficial/symbols include the
    "Octopart Query" field wherever possible. However, be aware that components
    with packing alternatives (reel vs tray, for example) are often listed
    separately on Octopart, which is not accounted for.

    If the component does not have an "Octopart Query" field, the built-in
    "Value" field is used. A custom "Octopart Query" field can be added on a
    per-component basis in the schematic editor.
"""

import kicad_netlist_reader
import sys
import csv

inputFile = sys.argv[1]
outputFile = sys.argv[2]


def getOctopartQuery(component):
    return component.getField("Octopart Query") or component.getValue()


# Modify the component comparison to only consider components equal if they use
# the same Octopart query string.
eq = kicad_netlist_reader.comp.__eq__
kicad_netlist_reader.comp.__eq__ = lambda a, b: \
    eq(a, b) and getOctopartQuery(a) == getOctopartQuery(b)


net = kicad_netlist_reader.netlist(inputFile)

out = csv.writer(
    open(outputFile, 'w'),
    lineterminator='\n',
    delimiter=',',
    quotechar='\"',
    quoting=csv.QUOTE_ALL,
)

out.writerow([
    'Query',
    'Qty',
    'Description',
    'Schematic Reference',
])

for group in net.groupComponents():
    component = group[0]
    refs = ", ".join(c.getRef() for c in group)

    out.writerow([
        getOctopartQuery(component),
        len(group),
        component.getDescription(),
        refs,
    ])
