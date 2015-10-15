#!/usr/bin/env python
# encoding: utf-8

from random import SystemRandom
from atexit import register

from .database import db_session
from ..models import ColorPattern, ColorGame, ColorGuess, ColorFeedback, PATTERN_LENGTH, colors_short

class ColorGameAPI(object):
    '''Provides the API needed to interact with a color game.
    It coordinates the model classes to make sure
    that the game is stored in the database.
    '''

    def __init__(self, known_pattern=None, session=db_session):
        '''Instantiates a color game based on a random color pattern.

        If known_pattern is specified, this color pattern is used to create the game
        instead of a random pattern.  This should only be used for testing purposes.

        If session is specified, this DB session is used instead of the standard session.

        :param known_pattern: a list (or tuple) of one-letter colors (default: None)
        :param session: the DB session (default: standard color game session)
        '''
        # Make sure to cleanup database resources on exit
        register(self._cleanup)

        # Set up DB session
        self.s = session

        if known_pattern is None:
            sr = SystemRandom()
            self.pattern = [sr.choice(colors_short) for _ in range(PATTERN_LENGTH)]
        else:
            self.pattern = known_pattern
        self.pattern_set = set(self.pattern)
        self.game = ColorGame(pattern=ColorPattern(self.pattern))
        self.s.add(self.game)
        self.s.commit()

    def guess(self, pattern_guess):
        '''Attempts the given pattern guess for this game.

        :param pattern_guess: a list (or tuple) of one-letter colors
        :returns: a tuple with three items - a boolean representing if the game is completed,
            the quantity of correct matches, and correct matches in the correct positions
        '''
        if self.game.done:
            raise ValueError('Game is already completed.  No more guesses are allowed.')

        guess = ColorGuess(game=self.game, pattern=ColorPattern(pattern_guess))

        # Could do the calculations in the feedback model
        # but I try to avoid logic in such classes

        # Calculate the quantity of correct matches
        correct_match = sum(1 for c in pattern_guess if c in self.pattern_set)

        # Calculate the quantity of correct matches in the correct positions
        correct_position = sum(1 for i in range(PATTERN_LENGTH) if pattern_guess[i] == self.pattern[i])

        done = correct_position == PATTERN_LENGTH # Avoid unnecessary SQL SELECT on return
        if done: # Avoid unnecessary SQL UPDATE
            self.game.done = done

        feedback = ColorFeedback(guess=guess, correct_match=correct_match, correct_position=correct_position)
        self.s.add(feedback)
        self.s.commit()
        return done, correct_match, correct_position

    def _cleanup(self):
        '''Helper function for cleaning up database resources.  All connections are
        returned to their connection pool and any transactional state is rolled back.
        '''
        self.s.remove()
