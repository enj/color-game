#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from ..api.database import Base

class ColorGuess(Base):
    '''Represents a color guess that is stored in the database.
    A guess is linked to a pattern and a game.  The pattern was the
    actual value of the guess, and the game is the color game for which
    the guess was attempted.
    '''

    # Name of table used by ColorGuess
    __tablename__ = 'guess'

    # Each guess is uniquely keyed
    id = Column(Integer, primary_key=True)

    # The game that this guess was attempted for
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('ColorGame', backref=backref('guess', order_by=id))

    # The pattern that represents the actual value of this guess
    pattern_id = Column(Integer, ForeignKey('pattern.id'))
    pattern = relationship('ColorPattern', backref=backref('guess', order_by=id))
