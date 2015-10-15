This game was tested on:

Python 2.7.9
SQLAlchemy 1.0.8
Ubuntu 14.04.3 LTS
3.13.0-55-generic
x86_64

It currently uses a SQLite 3 database to store the games, but this should be easily
modifiable since I used SQLAlchemy's ORM to abstract away the SQL layer.



To run the game:

cd ../color-game
python main.py

To have the computer play the game:

cd ../color-game
python main.py -ai

To run the tests:

cd ../color-game
python -m colorgame.tests -v



Some queries that can be done against the database:

To see the correct pattern for a specific game with id = 4:

SELECT * FROM
    pattern, game
WHERE
    pattern.id = game.pattern_id AND
    game.id = 4

To see all of the guesses and associated feedback for the same game:

SELECT * FROM
    pattern, feedback, guess, game
WHERE
    guess.id = feedback.guess_id AND
    pattern.id = guess.pattern_id AND
    game.id = guess.game_id AND
    game.id = 4
