#!/usr/bin/env python
# encoding: utf-8

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .api.database import Base
from .api.gameapi import ColorGameAPI
from .models import ColorPattern, ColorGame, ColorGuess, ColorFeedback

# Global scope.  Create session and engine.
engine = create_engine('sqlite:///:memory:', echo=False, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base.query = session.query_property()

class ColorGameTest(unittest.TestCase):
    '''Tests for Color game.'''

    def setUp(self):
        '''Create tables in test database.'''
        Base.metadata.create_all(bind=engine)

    def test_valid_pattern(self):
        '''Test insertion of valid patterns.'''
        patterns = [
                        ['y', 'y', 'y', 'y', 'y', 'y'],
                        ['g', 'w', 'c', 'p', 'o', 'y'],
                        ['y', 'y', 'c', 'r', 'g', 'm'],
                        ['w', 'c', 'w', 'w', 'p', 'r'],
                        ['c', 'o', 'w', 'c', 'r', 'b'],
        ]
        for p in patterns:
            pattern = ColorPattern(p)
            session.add(pattern)
            session.commit()
            self.assertEqual(pattern, ColorPattern.query.get(pattern.id))

    def test_invalid_pattern(self):
        '''Test to make sure invalid patterns cannot be initialized.'''
        patterns = [
                        ['y', 'y', 'y', 'y', 'y', 'x'],
                        ['g', 'w', 'c', 'p', 'o'],
                        ['y', 'y', 'c', 'r', 'g', 1],
                        ['w', 'c', 'w', 'w', 'p', 'R'],
                        ['c', 3.14, 'w', 'c', 'r', 'b'],
                        ['c', 'o', 'w', 'blue', 'r', 'b'],
        ]
        for p in patterns:
            try:
                session.add(ColorPattern(p))
                session.commit()
                self.fail('Should not allow creation of invalid pattern.')
            except ValueError as e:
                pass

    def test_guess(self):
        '''Test responses to guesses.'''
        g = ColorGameAPI(['r', 'm', 'o', 'y', 'w', 'r'], session)
        patterns = [
                        (['y', 'y', 'y', 'y', 'y', 'y'], (False, 6, 1)),
                        (['g', 'm', 'o', 'p', 'o', 'y'], (False, 4, 2)),
                        (['y', 'y', 'c', 'r', 'g', 'm'], (False, 4, 0)),
                        (['w', 'c', 'w', 'w', 'w', 'r'], (False, 5, 2)),
                        (['r', 'm', 'w', 'c', 'w', 'b'], (False, 4, 3)),
                        (['r', 'm', 'o', 'y', 'w', 'r'], (True, 6, 6)),
        ]
        for p, expected in patterns:
            self.assertEqual(expected, g.guess(p))

        try:
            g.guess(['y', 'y', 'c', 'r', 'g', 'm'])
            self.fail('Should not allow guessing for completed games.')
        except ValueError as e:
            pass

    def tearDown(self):
        '''Clean up test database.'''
        Base.metadata.drop_all(engine)

if __name__ == '__main__':
    unittest.main()

# Cleanup
session.remove()
