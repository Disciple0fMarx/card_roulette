import argparse

from .card_roulette import CardRoulette
from .simulate import play_multiple_games
from .__init__ import __version__


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Card Roulette CLI',
        usage='card_roulette <command> [<args>]'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    help_parser = subparsers.add_parser('help', help='Show help message')
    help_parser.add_argument('help_command', nargs='?', help='Command to display help for')

    play_parser = subparsers.add_parser('play', help='Start a card roulette game')
    play_parser.add_argument('--players', type=int, default=3, help='Number of players')
    play_parser.add_argument('--rounds', type=int, default=3, help='Number of rounds')

    simulate_parser = subparsers.add_parser('simulate', help='Simulate multiple card roulette games')
    simulate_parser.add_argument('--games', type=int, default=5, help='Number of games to simulate')
    simulate_parser.add_argument('--players', type=int, default=3, help='Number of players')
    simulate_parser.add_argument('--rounds', type=int, default=3, help='Number of rounds')

    parser.add_argument('--version', action='version', version=f'card_roulette {__version__}', help='Show version information')

    args = parser.parse_args()

    if args.command == 'help':
        if hasattr(args, 'help_command'):
            if args.help_command == 'play':
                play_parser.print_help()
            elif args.help_command == 'simulate':
                simulate_parser.print_help()
            elif args.help_command == None:
                help_parser.print_help()
            else:
                print(f"Unknown command '{args.help_command}'.")
        else:
            help_parser.print_help()
    elif args.command == 'play':
        game = CardRoulette(num_players=args.players, num_rounds=args.rounds)
        game.play_game()
        print('Results:')
        for player, score in enumerate(game.scores):
            print(f'Player {player} - {score} points')
    elif args.command == 'simulate':
        play_multiple_games(num_games=args.games, num_players=args.players, num_rounds=args.rounds)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
