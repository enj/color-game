#!/usr/bin/env python
# encoding: utf-8

import readline # Allows for history and line-editing
from sys import argv

from colorgame.api.database import init_db
from colorgame.api.gameapi import ColorGameAPI
from colorgame.models import colors_short, colors_long, PATTERN_LENGTH

from ai import play_game

# Create database tables if needed
init_db()

# Create a new game for this play session
game = ColorGameAPI()

# Should the computer play the game
ai_arg = len(argv) == 2 and argv[1] == '-ai'

print \
r'''
 ______  ______  __      ______  ______       ______  ______  __    __  ______
/\  ___\/\  __ \/\ \    /\  __ \/\  == \     /\  ___\/\  __ \/\ "-./  \/\  ___\
\ \ \___\ \ \/\ \ \ \___\ \ \/\ \ \  __<     \ \ \__ \ \  __ \ \ \-./\ \ \  __\
 \ \_____\ \_____\ \_____\ \_____\ \_\ \_\    \ \_____\ \_\ \_\ \_\ \ \_\ \_____\
  \/_____/\/_____/\/_____/\/_____/\/_/ /_/     \/_____/\/_/\/_/\/_/  \/_/\/_____/
'''

if not ai_arg:

    print \
'''
The object of the game is to match, through a series of guessing with feedback,
a randomly chosen pattern of colors.

A pattern is composed of %d colors.  The same color can appear in multiple positions.
The valid colors are: %s.
When prompted to guess a pattern, enter the first letter of each color and
separate each color with a space.  For example, 'c y b w o o' is a valid guess.
As expected, the valid guess colors are: %s.

After each guess the game will respond with two numbers.  The first is the quantity
of correct matches.  The second is the quantity of correct matches in the correct
positions.  '3 0' is an example response.

During a guess prompt, the up / down arrow keys can be used to cycle through
prior guesses.  The left / right arrow keys and the backspace key can be used in
conjunction to edit a previous guess (which can then be submitted by pressing Enter).

Type 'QUIT' as a guess to exit the game early.

Type 'CHEAT' as a guess to have the game print the correct pattern (for testing).
''' % (PATTERN_LENGTH, ', '.join(colors_long), ', '.join(colors_short))

    while True:
        guess = raw_input('Your guess: ')
        if guess == 'QUIT':
            print 'Exiting game early.'
            break
        if guess == 'CHEAT':
            print 'The correct pattern is:', ' '.join(game.pattern)
            continue
        try:
            done, correct_match, correct_position = game.guess(guess.split(' '))
        except ValueError as e:
            print 'Invalid input: %s' % e.message
            continue
        if done:
            print 'Correct guess!'
            break
        else:
            print 'Incorrect guess: %d %d' % (correct_match, correct_position)
else:
    print 'Skipping instructions.'
    play_game(game)
