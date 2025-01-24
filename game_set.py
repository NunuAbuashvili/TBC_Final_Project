from prettytable import PrettyTable
from game_hand import PlayHand
from constants import CARDS_PER_PLAYER, HANDS_PER_SET, NUMBER_OF_PLAYERS

class PlaySet():
    """
    Manages the gameplay of a set of hands in a card game.

    This class handles the overall flow of a set of hands, including:
    - Rotating the lead player and dealer for each hand;
    - Resetting player states for each new hand;
    - Dealing cards and taking bids for each hand;
    - Playing tricks within each hand;
    - Updating and printing scores for each hand and the overall set.
    
    Attributes:
        1) players (list): A list of Player objects participating in the set.
        2) lead_player_index (int): The index of the player who leads the current hand.
        3) dealer_index (int): The index of the player who deals the cards.
        4) set_scores (dict): Dictionary to track the cumulative scores for the set.
        5) game_hand (PlayHand): An instance of the PlayHand class to manage individual hands.
        6) game_table (PrettyTable): A table to keep track of the game progress
    """
    def __init__(self, players: list):
        """
        Initializes a new instance of PlaySet.
        
        Args:
            players (list): A list of Player objects representing the players in the game.
        """
        self.players = players
        self.lead_player_index = 0
        self.dealer_index = -1
        self.set_scores = {}
        self.game_hand = PlayHand(self.players)
        self.game_table = PrettyTable([player.name for player in self.players])
    
    def play_hand(self):
        """
        Plays a set of hands in the game.
        """
        for hand in range(HANDS_PER_SET):
            print('\nHAND NO.', hand + 1)
            # Rotate lead player and dealer for each hand
            self.lead_player_index = hand % NUMBER_OF_PLAYERS
            self.dealer_index = (hand - 1) % NUMBER_OF_PLAYERS
            
            # Deal cards to players and let them place their bids
            self.game_hand.deal_cards_and_place_bids(self.lead_player_index, self.dealer_index)
            
            # Play tricks within the hand
            for i in range(CARDS_PER_PLAYER):
                print('\nTrick no.', i + 1)
                self.game_hand.play_trick()
            
            # Update and print scores for the current hand
            self.update_hand_scores()
            # Update cumulative scores for the set
            self.update_set_scores()
            # Update and print the game table
            self.update_game_table(hand)
            
            # Reset player states for a new hand
            for player in self.players:
                player.reset_for_another_hand()
        
    def update_hand_scores(self):
        """
        Updates the scores for the current hand based on the bids and tricks won by each player.
        """
        for player in self.players:
            # In case of a successful bid
            if player.bid == player.tricks_won:
                player.deserves_bonus.append(True)
                # If a player bids to win all the 9 tricks and succeeds,
                # they score 100 points per trick bid.
                if player.bid == CARDS_PER_PLAYER:
                    player.score += player.bid * 100
                # If a player wins the exact number of tricks they bid for,
                # they get a score of 50 times their bid plus 50.
                else: 
                    player.score += (player.bid * 50) + 50
            # In case of an unsuccessful bid
            else:
                player.deserves_bonus.append(False)
                # If a player bids a non-zero number of tricks but does not win any,
                # they get a penalty of -500.
                if player.bid != 0 and player.tricks_won == 0:
                    player.score -= 500
                # If a player's bid does not match their tricks won,
                # they get 10 points for each trick they won.
                else:
                    player.score += player.tricks_won * 10
            
            # Update the player's hand scores list
            player.hand_scores.append(player.score)
    
    def update_set_scores(self):
        """
        Updates the cumulative scores for the set based on the scores from the current hand.
        """
        for player in self.players:
            if player.name in self.set_scores:
                self.set_scores[player.name] += player.score
            else:
                self.set_scores[player.name] = player.score
    
    def update_game_table(self, hand: int):
        """
        Updates the game table with the current bids and scores of the players.

        Args:
            hand (int): The current hand number.

        This method updates the game table by adding a row with the current bids
        and scores of all players. If the current hand is the last hand of the
        set, a divider is added to the row to separate it from the next set.
        """
        self.game_table.padding_width = 5
        print("\nThis hand is over, let's see the results:")
        # Add a divider after the last hand of the set
        divider = (hand == HANDS_PER_SET - 1)
        self.game_table.add_row([f'{player.bid}: {player.score}' for player in self.players], divider = divider)
        print(self.game_table)
