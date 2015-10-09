# color-game
*Game object: Match, through a series of guessing with feedback, a randomly chosen pattern of colors.*

The computer chooses a pattern comprised of six colors randomly. The user submits guesses of the six colors. The computer scores each guess, stating a) the number of correct matches, and b) the number of correct matches in the correct positions. Play continues until the user submits a guess matching the computer-selected pattern.

- This is a text-mode program.
- The same color can appear in multiple positions in the original pattern.
- The scoring gives no positional indication. Only the quantity of correct matches and the quantity of correct matches in the correct positions are reported. These are two numbers, each 0..6
- Pay attention to usability. As the player, I should be able to enter my guess pattern easily. I should be able to see my pattern history to see if I've tried a particular pattern or position before.

For bonus points:

1. Use and include test-driven development techniques.
2. Include the ability for the game to play itself
3. Store each game in a PostgreSQL
