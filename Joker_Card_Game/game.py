import random
import json
from player import Player
from constants import CARDS_PER_PLAYER, NUMBER_OF_PLAYERS, NUMBER_OF_SETS, HANDS_PER_SET
from game_set import PlaySet

class Game:
    """
    Handles the overall game flow, including managing players, sets, and determining the winner.
    
    Attributes:
        players (list): List to store Player objects.
        set_scores (dict): Dictionary to track the cumulative scores for each player across sets.
    """
    def __init__(self):
        """
        Initializes a new instance of the Game class.
        """
        self.players = []
        self.set_scores = {}
    
    def welcome(self):
        """
        Displays a welcome message with game details.
        """
        print(f'Welcome to the game! \nThis game consists of {NUMBER_OF_SETS} sets, with {HANDS_PER_SET} hands per set. There will be {CARDS_PER_PLAYER} cards dealt to each player during each hand.')
        print()
    
    def get_player_names(self) -> list:
        """
        Gets the names of the players and creates Player objects. 

        Returns:
            list: A list of Player objects representing the players in the order they will play.
        """
        for i in range(1, NUMBER_OF_PLAYERS + 1):
            # Prompt user to enter the player's name
            name = input(f'Enter the name of player {i}: ').strip().title()
            
            # Validate the name input (duplicated or empty names are not allowed)
            while not name or name in [player.name for player in self.players]:
                if not name:
                    print('Name cannot be empty.', end = ' ')
                elif name in [player.name for player in self.players]:
                    print('Name already exists.', end = ' ')
                name = input('Please enter another name: ').strip().title()
            
            self.players.append(Player(name))
        
        # Shuffle the order of players
        random.shuffle(self.players)
    
    def print_the_order_of_players(self):
        """
        Prints the order of players and the starting dealer.
        """
        players = [player.name for player in self.players]
        print(f'\nWe have {NUMBER_OF_PLAYERS} players in this order: {', '.join(players)}. Please take turns to deal the cards starting from {self.players[-1].name}.')
        
    def play_set(self):
        """
        Plays a set of hands in the game.
        """
        # Initialize a PlaySet instance
        game_set = PlaySet(self.players)
        
        # Play each set
        for _set in range(NUMBER_OF_SETS):            
            print(f'\n{'*' * 54} SET NO. {_set + 1} {'*' * 54}')
            # Play the hands of the set
            game_set.play_hand() 
            print()
            # Check for bonus after each set
            self.check_bonus(game_set)
            # Print the scores after each set
            print("\nThis set is over. Let's see the results:")
            self.update_table_after_set(game_set)
            # Reset player states for a new set
            for player in self.players:
                player.reset_for_another_set()
        
        # Update the overall set scores
        self.set_scores = game_set.set_scores
        # Write the table data to a JSON file
        self.write_table_to_json(game_set)
                
    def check_bonus(self, game_set: object):
        """
        Checks if any player deserves a bonus for successfully bidding in all hands of the set.

        Args:
            game_set (PlaySet): The current PlaySet object representing the set of hands.
        """
        bonus_awarded = False
        
        for player in self.players:
            # If the player has successfully bid in all hands of a set
            if False not in player.deserves_bonus:
                # Bonus is an additional score equal to the highest amount the player has scored on any one hand during the set
                bonus_score = max(player.hand_scores)
                game_set.set_scores[player.name] += bonus_score
                print(f"{player.name} earned a bonus of {bonus_score} for successfully bidding in all hands of this set.")
                bonus_awarded = True
        
        # If no player has successfully bid in all hands of a set
        if not bonus_awarded:
            print('No player earned a bonus in this set.')
    
    def update_table_after_set(self, game_set: object):
        """
        Updates the game table with the scores for the completed set.

        Args:
            game_set (PlaySet): An object representing the completed set of the game.

        This method updates the game table by adding a row with the scores
        for each player in the completed set. A divider is added to separate
        this row from the next set.
        """
        game_set.game_table.add_row([score for score in game_set.set_scores.values()], divider = True)
        print(game_set.game_table)
    
    def write_table_to_json(self, game_set: object):
        """
        Converts the table data into a dictionary and writes it to a JSON file.
        """
        field_names = [player.name for player in self.players]
        
        with open('game_data.json', 'w') as file:
            json.dump([{field: row[i] for i, field in enumerate(field_names)} for row in game_set.game_table.rows], file, indent = 4)
    
    def determine_final_winner(self):
        """
        Determines and announces the overall winner of the game based on the cumulative set scores.
        """
        highest_score = 0
        final_winner = None
        tie = False

        for player, score in self.set_scores.items():
            if score > highest_score:
                highest_score = score
                final_winner = player
                tie = False
            elif score == highest_score:
                tie = True

        if final_winner and not tie:
            print(f"\nThe overall winner of the game is {final_winner} with a score of {highest_score}!")
        elif tie:
            winners = [player for player, score in self.set_scores.items() if score == highest_score]
            print(f"\nThere was a tie between {', '.join(winners)} with a score of {highest_score}.")
