#!/usr/bin/env python
# encoding: utf-8

from collections import namedtuple

def _create_named_tuple(name, values):
    '''Helper function for creating a named tuple with the first
    letter of each of the values as the names of its fields.

    :param name: the name of the class that is generated
    :param values: the values to instantiate the named tuple with
    :returns: a named tuple
    '''
    return namedtuple(name, (v[0] for v in values))(*values)

# Using a named tuple guarantees the order of the colors
Color = _create_named_tuple('Color',
    ('red', 'green', 'yellow', 'blue', 'white', 'magenta', 'cyan', 'orange', 'purple'))

# The one-letter representations of the colors
colors_short = Color._fields
colors_short_set = set(colors_short)

# The full names of the colors
colors_long = Color._asdict().values()
