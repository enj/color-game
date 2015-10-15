#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from ..api.database import Base

class ColorGame(Base):
    '''Represents a color game that is stored in the database.
    A game is linked to a pattern that is the correct solution to the game.
    '''

    # Name of table used by ColorGame
    __tablename__ = 'game'

    # Each game is uniquely keyed
    id = Column(Integer, primary_key=True)

    # Has this game been completed yet
    done = Column(Boolean, default=False)

    # The pattern that represents the solution to this game
    pattern_id = Column(Integer, ForeignKey('pattern.id'))
    pattern = relationship('ColorPattern', backref=backref('game', order_by=id))
