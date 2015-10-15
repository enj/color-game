#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, Integer, Enum

from ..models import colors_short, colors_short_set
from ..api.database import Base

# Number of colors in a pattern
PATTERN_LENGTH = 6

class ColorPattern(Base):
    '''Represents a color pattern that is stored in the database.
    The relations stored in other models give this class context.
    '''

    # Enum to represent the valid one-letter colors
    colors = Enum(*colors_short)

    # Name of table used by ColorPattern
    __tablename__ = 'pattern'

    # Each pattern is uniquely keyed
    id = Column(Integer, primary_key=True)

    # The colors in the pattern
    color_one = Column(colors, nullable=False)
    color_two = Column(colors, nullable=False)
    color_three = Column(colors, nullable=False)
    color_four = Column(colors, nullable=False)
    color_five = Column(colors, nullable=False)
    color_six = Column(colors, nullable=False)

    def __init__(self, colors_list):
        '''Instantiate a color pattern from a list (or tuple) of one-letter colors.

        :param colors_list: a list (or tuple) of one-letter colors
        '''
        self._validate(colors_list)
        colors_iter = iter(colors_list)
        self.color_one = colors_iter.next()
        self.color_two = colors_iter.next()
        self.color_three = colors_iter.next()
        self.color_four = colors_iter.next()
        self.color_five = colors_iter.next()
        self.color_six = colors_iter.next()

    def _validate(self, colors_list):
        '''Validates a list (or tuple) of one-letter colors.
        A ValueError is raised if the list is of the wrong length
        or contains a value that is not a valid one-letter color.

        :param colors_list: a list (or tuple) of one-letter colors
        '''
        if not isinstance(colors_list, (list, tuple)):
            raise TypeError('Pattern must be a list or tuple of colors.')
        if len(colors_list) != PATTERN_LENGTH:
            raise ValueError('Pattern must be composed of %d colors.' % PATTERN_LENGTH)
        for c in colors_list:
            if c not in colors_short_set:
                raise ValueError('Invalid color found in pattern: %s.' % c)
