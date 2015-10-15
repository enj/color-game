#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from ..api.database import Base

class ColorFeedback(Base):
    '''Represents a color feedback that is stored in the database.
    A feedback is linked to the guess for which it was a response to.
    '''

    # Name of table used by ColorFeedback
    __tablename__ = 'feedback'

    # Each feedback is uniquely keyed
    id = Column(Integer, primary_key=True)

    # The guess for which this feedback was a response to
    guess_id = Column(Integer, ForeignKey('guess.id'))
    guess = relationship('ColorGuess', backref=backref('feedback', order_by=id))

    # The quantity of correct matches
    correct_match = Column(Integer, nullable=False)
    # The quantity of correct matches in the correct positions
    correct_position = Column(Integer, nullable=False)
