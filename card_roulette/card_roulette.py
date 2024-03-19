from random import choice


class CardRoulette:
    '''
    A class representing the Card Roulette game.
    
    This class allows users to simulate multiple rounds of the Card Roulette game,
    track scores for each player, and customize the number of players and rounds.
    '''

    __version__ = '1.0.0'

    def __init__(self, num_players: int | None = 3, num_rounds: int | None = 3):
        '''
        Initialize a CardRoulette instance.

        Parameters:
            num_players (int, optional): The number of players in the game. Defaults to 3.
            num_rounds (int, optional): The number of rounds in the game. Defaults to 3.
        '''
        self.num_players: int = num_players
        self.num_rounds: int = num_rounds
        self.num_cards: int = num_players * num_rounds
        self.reset_cards()
        self.scores: list[int] = [0 for _ in range(num_players)]

    def reset_cards(self) -> None:
        '''Reset the deck of cards for the game.'''
        self.cards: set[int] = {card + 1 for card in range(self.num_cards)}
    
    def play_round(self, first_player: int | None = 1, deadly_card: int | None = 1) -> bool:
        '''
        Perform a round of the game.

        Parameters:
            first_player (int, optional): The index of the first player to draw a card. Defaults to 1.
            deadly_card (int, optional): The card that is deadly. Defaults to 1.

        Returns:
            bool: True if the round is over, False otherwise.
        '''
        round_over: bool = False
        current_player = first_player - 1
        for _ in range(self.num_players):
            if len(self.cards) != 1:
                players_pick = choice(tuple(self.cards))
                print(f'Player {current_player + 1} draws {players_pick}')
                self.cards.remove(players_pick)
                if players_pick == deadly_card:
                    round_over = True
                    print(f'Player {current_player + 1} loses.')
                    self.scores[current_player] += 1
                    break
                current_player = (current_player + 1) % self.num_players
            else:
                print(f'Everyone survives!')
                round_over = True
                break
        return round_over

    def play_iteration(self, first_player: int | None = 1, deadly_card: int | None = 1) -> None:
        '''
        Perform an iteration of the game with a specified deadly card.

        Parameters:
            first_player (int): The index of the first player to draw a card.
            deadly_card (int, optional): The card that is deadly. Defaults to 1.
        '''
        print(f'Iteration {deadly_card}')
        round_over: bool = False
        while not round_over:
            round_over = self.play_round(first_player, deadly_card)
        if round_over:
            self.reset_cards()
    
    def play_game(self):
        '''Play the Card Roulette game.'''
        rounds = range(1, self.num_cards + 1)
        for deadly_card in rounds:
            first_player = (deadly_card - 1) % self.num_players + 1
            self.play_iteration(first_player, deadly_card)
            print()


def main() -> None:
    game = CardRoulette()
    game.play_game()
    print('Results:')
    for player, score in enumerate(game.scores):
        print(f'Player {player + 1} - {score} points')


if __name__ == '__main__':
    main()
