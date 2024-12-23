import random
from constants import SUITS, RANKS

class Card:
    """
    Represents a single playing card.
    
    Attributes: 
        1) suit (str): The suit of the card (e.g., '♠', '♣', '♥', '♦', or 'JOKER' for Jokers)
        2) rank (str): The rank of the card (e.g., '2', '3', ..., '10', 'J', 'Q', 'K', 'A', and 'RED', 'BLACK' for Jokers).
        3) value (int): The index value of the card rank for comparison purposes.
        
    Returns:
        str: A string representation of the card in the format '{rank}{suit}'.
        
    """
    
    def __init__(self, suit: str, rank: str):
        """
        Initializes a Card instance.

        Args:
            suit (str): The suit of the card.
            rank (str): The rank of the card.

        Note:
            Special cards: 
            - '6♠' is replaced by 'RED JOKER'.
            - '6♣' is replaced by 'BLACK JOKER'.
            
        """
        
        try:
            # Replace '6♠' with RED JOKER and assign it a unique value (-1)
            if rank == '6' and suit == '♠':
                self.suit = 'JOKER'
                self.rank = 'RED '
                self.value = -1
            # Replace '6♣' with BLACK JOKER and assign it a unique value (-1)
            elif rank == '6' and suit == '♣':
                self.suit = 'JOKER'
                self.rank = 'BLACK '
                self.value = -1
            else:
                # Ensure the 'suit' is valid to prevent errors
                if suit in SUITS.values():
                    self.suit = suit
                else:
                    raise ValueError(f'Invalid suit has been passed: {suit}')
                
                # Ensure the 'rank' is valid to prevent errors
                if rank in RANKS:
                    self.rank = rank
                    # In RANKS, ranks of the cards are stored in ascending order, 
                    # so the higher the index, the higher the value of the card.
                    self.value = RANKS.index(rank)
                else:
                    raise ValueError(f'Invalid rank has been passed: {rank}')
        except ValueError as error:
            print(f'Error: {error}')
        
    def __str__(self):
        """
        Returns the string representation of the card.
        """
        return f'{self.rank}{self.suit}'

class Deck:
    """
    Represents a playing deck.
    
    Attributes: 
        1) ranks (list): A list containing the card ranks (e.g., '2', '3', ..., '10', 'J', 'Q', 'K', 'A').
        2) suits (list): A list containing the card suits (e.g., '♠', '♣', '♥', '♦')
        3) cards (list): An empty list to store the card combinations.
        
    Returns:
        list: A list of Card instances.
        
    """
    
    def __init__(self, ranks: list, suits: dict):
        """
        Initializes a Deck object with the specified ranks and suits.

        Args:
            1) ranks (list): A list containing the card ranks (e.g., '2', '3', ..., '10', 'J', 'Q', 'K', 'A').
            2) suits (dict): A dictionary that maps the first letter of each card suit ('D' for Diamonds, 'H' for Hearts, 'S' for Spades, and 'C' for Clubs) to its corresponding symbol ('♦', '♥', '♠', and '♣').
            
        """
        self.ranks = ranks
        self.suits = [suit for suit in suits.values()]
        self.cards = []
            
    def create_deck(self):
        """
        This method populates the 'cards' attribute with a list of Card instances,
        representing all possible combinations of ranks and suits.
        """
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
    
    def shuffle(self):
        """
        This method modifies the 'cards' attribute in-place, randomizing the order
        of the cards in the deck.
        """
        random.shuffle(self.cards)
