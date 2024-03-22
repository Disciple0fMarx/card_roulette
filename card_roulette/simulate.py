import argparse
import csv
import json
from os import path, makedirs
from uuid import uuid4

from .card_roulette import CardRoulette


ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))

JSON = list[dict[str: str | int]]


def create_results_directory() -> None:
    '''
    Create the 'results' directory if it doesn't exist.
    '''
    results_dir = 'results'
    if not path.exists(results_dir):
        makedirs(results_dir)


def create_player_directory(num_players: int) -> str:
    '''
    Create a directory for the number of players if it doesn't exist.

    Parameters:
        num_players (int): Number of players in each game.

    Returns:
        str: Path to the directory for the number of players.
    '''
    players_dir = path.join(ROOT_DIR, 'results', f'{num_players}_players')
    if not path.exists(players_dir):
        makedirs(players_dir)
    return players_dir


def create_rounds_directory(players_dir: str, num_rounds: int) -> str:
    '''
    Create a directory for the number of rounds if it doesn't exist.

    Parameters:
        players_dir (str): Path to the directory for the number of players.
        num_rounds (int): Number of rounds in each game.

    Returns:
        str: Path to the directory for the number of rounds.
    '''
    rounds_dir = path.join(players_dir, f'{num_rounds}_rounds')
    if not path.exists(rounds_dir):
        makedirs(rounds_dir)
    return rounds_dir


def save_game_results(
        rounds_dir: str,
        game_number: int,
        simulation_id: str, game_scores: list) -> None:
    '''
    Save the results of a game to a CSV file.

    Parameters:
        rounds_dir (str): Path to the directory for the number of rounds.
        game_number (int): Number of the game.
        simulation_id (str): UID of the simulation.
        game_scores (list): Scores of each player in the game.
    '''
    csv_filename = path.join(rounds_dir, f'{simulation_id}.csv')

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([game_number] + game_scores)


def save_accumulated_scores(csv_file_path: str, simulation_id: str, num_players: int, num_rounds: int) -> None:
    """
    Saves accumulated scores from a CSV file to results/total_results.json.

    Args:
        csv_file_path: The path to the CSV file containing the accumulated scores.
        simulation_id: The ID of the simulation.
        num_players: The number of players involved.
        num_rounds: The number of rounds played.

    Raises:
        IOError: If there's an issue opening, reading, or writing the files.
        ValueError: If there's an issue with parsing CSV data or serializing JSON data.
    """
    accumulated_scores: List[int] = [0] * num_players
    num_games: int = 0

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header

        for row in csv_reader:
            scores = [int(score) for score in row[1:]]
            for i, score in enumerate(scores):
                accumulated_scores[i] += score
            num_games += 1

    total_results: Dict[str, Any] = {}
    json_filename: str = os.path.join(RESULTS_DIR, "total_results.json")

    if os.path.exists(json_filename):
        with open(json_filename, 'r') as json_file:
            total_results = json.load(json_file)

    players_key: str = f"{num_players}_players"
    rounds_key: str = f"{num_rounds}_rounds"

    simulation_data: Dict[str, Any] = {
        "simulation_id": simulation_id,
        "num_games": num_games,
        "scores": accumulated_scores
    }

    rounds_data = total_results.setdefault(players_key, {})
    simulations = rounds_data.setdefault(rounds_key, [])
    simulations.append(simulation_data)

    with open(json_filename, 'w') as json_file:
        json.dump(total_results, json_file, indent=4)

    print("JSON data written successfully.")


def save_total_results(num_players: int, num_rounds: int, total_results: JSON):
    '''
    Save the aggregated results of all games to a JSON file.

    Parameters:
        num_players (int): Number of players in each game.
        num_rounds (int): Number of rounds in each game.
        total_results (JSON): Aggregated results of all games.
    '''
    json_filename = path.join(ROOT_DIR, 'results', 'total_results.json')

    # Load existing data if file exists, or initialize as empty dictionary
    if path.exists(json_filename):
        with open(json_filename, 'r') as jsonfile:
            existing_data = json.load(jsonfile)
    else:
        existing_data = {}

    # Calculate total scores for each player across all games
    total_scores = [0] * num_players
    for game_result in total_results:
        for player_scores in game_result['scores']:
            for player_idx, score in enumerate(player_scores):
                total_scores[player_idx] += score

    # Create new entry for current simulation
    new_entry = {
        'simulation_id': total_results[0]['id'],
        'num_games': len(total_results),
        'scores': total_scores
    }

    # Update existing data with new entry
    if f'{num_players}_players' not in existing_data:
        existing_data[f'{num_players}_players'] = {}
    if f'{num_rounds}_rounds' not in existing_data[f'{num_players}_players']:
        existing_data[f'{num_players}_players'][f'{num_rounds}_rounds'] = []
    existing_data[f'{num_players}_players'][f'{num_rounds}_rounds'].append(new_entry)

    # Write updated data to JSON file
    with open(json_filename, 'w') as jsonfile:
        json.dump(existing_data, jsonfile, indent=4)


def play_multiple_games(num_games: int, num_players: int, num_rounds: int):
    '''
    Play multiple games of Card Roulette and save the results.

    Parameters:
        num_games (int): Number of games to simulate.
        num_players (int): Number of players in each game.
        num_rounds (int): Number of rounds in each game.
    '''
    create_results_directory()
    players_dir = create_player_directory(num_players)
    simulation_id = str(uuid4())
    total_results = []

    for game_number in range(1, num_games + 1):
        game = CardRoulette(num_players, num_rounds)
        game.play_game()
        rounds_dir = create_rounds_directory(players_dir, num_rounds)

        # Wrap game.scores in a list
        game_scores = [game.scores]
        save_game_results(rounds_dir, game_number, simulation_id, game_scores)
        total_results.append({'id': simulation_id, 'scores': game_scores})

    save_total_results(num_players, num_rounds, total_results)
    print('All games played. Results saved.')


def main():
    '''
    Main function to parse command-line arguments and start the simulation.
    '''
    parser = argparse.ArgumentParser(description='Simulate multiple games of Card Roulette.')
    parser.add_argument('--num-games', type=int, default=5, help='Number of games to simulate.')
    parser.add_argument('--num-players', type=int, default=3, help='Number of players in each game.')
    parser.add_argument('--num-rounds', type=int, default=3, help='Number of rounds in each game.')
    args = parser.parse_args()

    play_multiple_games(args.num_games, args.num_players, args.num_rounds)


if __name__ == '__main__':
    main()
