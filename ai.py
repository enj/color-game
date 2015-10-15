#!/usr/bin/env python
# encoding: utf-8

from sys import exit
from collections import deque

from colorgame.models import colors_short, PATTERN_LENGTH

def ai_guess(game, guess):
    '''Helper function for attempting a guess by the computer for
    a game.  It prints dialogs that show the user what is happening.
    Exits the program when the guess is correct.

    :param game: the color game that is being played
    :param guess: the guess to attempt
    :returns: the quantity of correct matches in the correct positions
    '''
    print 'Computer guess:', ' '.join(guess)
    done, _, correct_position = game.guess(guess)
    if done:
        print 'Computer found correct pattern!'
        exit(0)
    return correct_position

def play_game(game):
    '''Algorithm to play the color game.
    Averages 17.5 ± 2.5 guesses to get the correct pattern.

    :param game: the color game that will be played
    '''
    print 'Computer will play the game.'
    print 'The correct pattern is:', ' '.join(game.pattern)
    # The number of valid colors
    total = len(colors_short)
    # How many of each color are in the pattern
    correct = [0 for _ in range(total)]
    for i in range(total):
        guess = [colors_short[i] for _ in range(PATTERN_LENGTH)]
        correct[i] = ai_guess(game, guess)
    # Based on counts in 'correct', what are the colors in this pattern
    # They will most likely be in the wrong order (hence the rest of the code)
    pool = []
    # Determine which color occurs most often in the pattern
    max_count = 0
    max_color = 0
    for i, count in enumerate(correct):
        if count:
            # Add color at index i to pool based on its count
            pool.extend(colors_short[i] for _ in range(count))
            if count > max_count:
                max_count = count
                max_color = colors_short[i]
    # Create a queue of all the colors in the pattern
    # except the color that occurs most frequently
    q = deque(c for c in pool if c != max_color)
    # The current index that we are guessing for
    idx = 0
    # The base guess sets all indexes to the most frequent color
    guess = [max_color for _ in range(PATTERN_LENGTH)]
    # Guard to prevent guessing the wrong color more than once per index
    invalid_color_idx = set()
    # Keep guessing until queue is empty
    while q:
        idx_guess = q.pop()
        # Skip the colors that we already know are not valid
        if idx_guess in invalid_color_idx:
            q.appendleft(idx_guess)
            continue
        # Add new color to guess and check the delta
        guess[idx] = idx_guess
        correct_position = ai_guess(game, guess)
        # The new color was the correct guess
        if correct_position > max_count:
            # Update correct count
            max_count = correct_position
            # Reset invalid colors
            invalid_color_idx.clear()
            # Move to next index
            idx += 1
        # Both the new and old color (the most frequently occurring one)
        # are not the correct colors for this index
        elif correct_position == max_count:
            # Invalidate the new color (the old color will never be guessed again)
            invalid_color_idx.add(idx_guess)
            q.appendleft(idx_guess)
        # The new color lowered the count thus the old color was correct
        else: # correct_position < max_count
            # Put the old color back
            guess[idx] = max_color
            # Put the new color back into the queue
            q.appendleft(idx_guess)
            # Reset invalid colors
            invalid_color_idx.clear()
            # Move to next index
            idx += 1
