from constants import SUITS, RANKS, CARDS_PER_PLAYER

class Player:
    """
    Represents a player in the card game.
    
    This class provides methods for the functionality of a player in the card game, including selecting a trump suit, bidding, playing cards, and resetting the player's state between hands or sets.
    
    Attributes:
        1) name (str): The name of the player.
        2) cards (list): A list to store the cards in the player's hand.
        3) bid (int): The player's bid for the current hand.
        4) tricks_won (int): The number of tricks won by the player in the current hand.
        5) score (int): The player's cumulative score in the current hand.
        6) hand_scores (list): A list to store the player's scores for each hand in a set.
        7) deserves_bonus (list): A list to store whether the player deserves a bonus for succeeding in every hand of the set.
        8) card_dict (dict): A dictionary to map string representations of cards to Card objects
    """
    
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.bid = 0
        self.tricks_won = 0
        self.score = 0
        self.hand_scores = []
        self.deserves_bonus = []
        self.card_dict = {}
    
    def choose_trump(self) -> str:
        """
        Prompts the player to choose a trump suit or no trump.

        This method displays the player's first three cards and prompts the player
        to enter a valid suit or "None" for no trump. It handles invalid input and
        continues prompting until a valid suit or "None" is entered.

        Returns:
            str: The chosen trump suit or "None" for no trump.
            
        """
        cards_to_choose_from = [str(card) for card in self.cards[:3]]
        print(f"\n{self.name}'s first three cards: {', '.join(cards_to_choose_from)}")
        trump_suit = input('Choose a trump suit ("D" for ♦, "H" for ♥, "S" for ♠, "C" for "♣") or enter "None" for no trump: ').strip().capitalize()
                
        while trump_suit != 'None' and trump_suit not in ['D', 'H', 'S', 'C']:
            trump_suit = input('Please enter a valid suit or "None" for no trump: ').strip().capitalize()
            
        if trump_suit == 'None':
            return 'None'
        else:
            return SUITS[trump_suit]
    
    def place_bid(self):
        """
        Prompts the player to place a bid for the current hand.

        This method continuously prompts the player to enter a bid until a valid
        bid between 0 and the maximum number of cards per player is entered. It
        handles invalid input and displays an error message if the input cannot be converted to an integer.
        
        """   
        while True:
            try:
                self.bid = int(input(f'{self.name}, place your bid: '))
                if 0 <= self.bid <= CARDS_PER_PLAYER:
                    break
                else:
                    print(f'Your bid should be between 0 and {CARDS_PER_PLAYER}.')
            except ValueError:
                print("Invalid input! Please enter an integer.")
    
    def play_card(self):
        """
        Prompts the player to play a card from their hand.

        This method displays the player's current cards and continuously prompts
        the player to enter a card from their hand. It handles invalid input and
        displays an error message if the player attempts to play a card they don't
        have. If a valid card is entered, the method returns the corresponding
        Card object.

        Returns:
            Card: The Card object representing the played card.
            
        """
        # Create a dictionary to map string representations of cards to Card objects
        self.card_dict = {str(card): card for card in self.cards}
        
        while True:
            # Prompt the player to play a card, displaying their current cards
            card_played = input(f'{self.name}, play a card (e.g. "A♦" or "AD") from your deck ({', '.join(self.card_dict.keys())}): ').strip().upper()
            
            # If the played card is not a Joker, transform the input in a more user-friendly format: rank + corresponding suit symbol
            if 'JOKER' not in card_played:
                # Handle case where the card is a 10 of a suit (e.g., "10H")
                if len(card_played) == 3: 
                    if card_played[:2] in RANKS and card_played[2] in ['H', 'D', 'C', 'S']:
                        card_played = card_played[:2] + SUITS[card_played[2]]
                # Handle case where the card is a rank and suit (e.g., "AH")
                elif len(card_played) == 2:
                    if card_played[0] in RANKS and card_played[1] in ['H', 'D', 'C', 'S']:
                        card_played = card_played[0] + SUITS[card_played[1]]
            
            # Check if the card played is in the player's deck
            if card_played in self.card_dict:
                # Return the corresponding Card object
                    return self.card_dict[card_played]
            else:
                # Display an error message if the card is not in the player's deck
                print(f"{self.name}, you do not have this card. Please, choose a card from your deck.")
    
    def reset_for_another_hand(self):
        """
        Resets the player's state for a new hand in the game.

        This method clears the player's hand, and resets their bid, tricks won, and score to 0.
        """
        self.cards = []
        self.bid = 0
        self.tricks_won = 0
        self.score = 0
    
    def reset_for_another_set(self):
        """
        Resets the player's state for a new set of hands.
        
        This method clears the player's hand scores and deserves_bonus lists, preparing the player for a new set of hands in the game.
        """
        self.hand_scores = []
        self.deserves_bonus = []
