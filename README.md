# Card Roulette

A Python package that simulates a thrilling card game where players draw cards, hoping to avoid the deadly one.

## Description

Card Roulette is a text-based game where players draw cards in rounds.
Each round, players draw cards randomly, and if a player draws the deadly card, they lose the round.
The game introduces a new deadly card with each iteration *(Iteration n's deadly card is card n)*.
If the deadly card is the only one remaining, all players survive.

## Usage

```python
from card_roulette import CardRoulette

# Create a game instance (default settings: 3 players, 3 rounds)
game = CardRoulette()

# Play the game
game.play_game()

# View the results
print('Results:')
for player, score in enumerate(game.scores):
    print(f'Player {player + 1} - {score} points')
```

## Requirements

- Python 3.6 or above

