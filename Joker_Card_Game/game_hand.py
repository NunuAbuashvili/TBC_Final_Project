from constants import RANKS, SUITS, CARDS_PER_PLAYER
from cards import Deck

class PlayHand:
    """
    Manages a single round (hand) of a card game.
    
    This class handles the entire flow of a single hand, including:
    - Dealing cards to players;
    - Allowing players to bid;
    - Playing of cards by each player;
    - Determining the winner of each trick.
    
    It also keeps track of the current trump suit, lead card, and cards played by each player.

    The class handles scenarios where the lead card is a regular card
    or a joker, and applies the appropriate rules and validations.
    
    Attributes:
        1) players (list): A list of Player objects.
        2) deck (Deck object): The deck of cards used in the game.
        3) lead_player_index (int): Index of the player who leads the current trick.
        4) dealer_index (int): Index of the player who is responsible for dealing cards.
        5) trump_suit (str): The trump suit for the current hand.
        6) suit_wanted (str): The suit that players are required to play by the lead Joker.
        7) lead_joker_action (str): The action taken when a Joker is the lead card ('High' or 'Low').
        8) lead_card (Card): The card that is leading the current trick.
        9) cards_played (dict): A dictionary to keep track of the cards played by each player, and the action taken when playing a Joker card ('Play', 'Give up', or 'NotApplicable'). 
    
    """
    
    def __init__(self, players: list):
        """
        Initializes a new instance of PlayHand.

        Args:
            players (list): A list of Player objects representing the players in the game.
        """
        self.players = players
        self.deck = Deck(RANKS, SUITS)
        self.lead_player_index = 0
        self.dealer_index = -1
        self.trump_suit = None
        self.suit_wanted = None
        self.lead_joker_action = None
        self.lead_card = None
        self.cards_played = {}
    
    def deal_cards_and_place_bids(self, lead_player_index: int, dealer_index: int):
        """
        Deals cards to the players and allows them to place their bids.

        Args:
            lead_player_index (int): The index of the lead player, who chooses the trump suit of the current hand.
            dealer_index (int): The index of the dealer.
        """
        self.lead_player_index = lead_player_index
        self.dealer_index = dealer_index
        self.deal_cards()
        self.print_cards_and_bid()
        self.print_player_bids()
    
    def deal_cards(self):
        """
        Deal cards to the players from the deck.
        """
        self.deck.create_deck() 
        self.deck.shuffle()
        
        # Deal nine cards to each player, and append them to the Player object
        for _ in range(CARDS_PER_PLAYER):
            for player in self.players:
                player.cards.append(self.deck.cards.pop())
    
    def print_cards_and_bid(self):
        """
        Prints the cards of each player and allows them to place their bids.
        """
        lead_player = self.players[self.lead_player_index]
        dealer = self.players[self.dealer_index]
        
        # Lead player chooses the trump suit of the current hand
        self.trump_suit = lead_player.choose_trump()
        if self.trump_suit == 'None':
            print('There is no trump suit for this hand!')
        else:
            print(f'Trump suit for this hand is {self.trump_suit}.')
        
        # Print the lead player's remaining cards and prompt the player to place a bid
        remaining_cards = [str(card) for card in lead_player.cards[3:]]
        print(f"\n{lead_player.name}'s remaining cards: {', '.join(remaining_cards)}")
        lead_player.place_bid()
        
        # Prompt other users to place their bids
        for player in self.get_following_players():
            print(f"\n{player.name}'s cards: {', '.join(str(card) for card in player.cards)}")
            player.place_bid()
            # Validate the dealer's bid
            if player == dealer:
                self.validate_dealer_bid(dealer)
            
    def validate_dealer_bid(self, dealer: str):
        """
        Validates the dealer's bid and prompts for a new bid if necessary. 

        Args:
            dealer (Player): The dealer Player object.
        """
        total_bids = sum(player.bid for player in self.players)
        remaining_bids = CARDS_PER_PLAYER - total_bids + dealer.bid
        
        # Dealer of the hand has no right to place such a bid, that the sum of the bids becomes nine
        while dealer.bid == remaining_bids:
            print(f'You can place any bid between 0 and {CARDS_PER_PLAYER} except {remaining_bids}.', end = ' ')
            dealer.place_bid()
    
    def print_player_bids(self):
        """
        Prints the bids placed by each player.
        """
        print('\nIn this hand, following bids have been placed:')
        for i, player in enumerate(self.players):
            if i == len(self.players) - 1:
                print(f"{player.name}'s bid is {player.bid}.")
            else:
                print(f"{player.name}'s bid is {player.bid}", end = ', ')
        
    def play_trick(self):
        """
        Plays a single trick in the current hand, determines the winner and updates the game state.
        """
        lead_player = self.players[self.lead_player_index]
        self.lead_card = lead_player.play_card() 
        lead_player.cards.remove(self.lead_card) 
        self.cards_played[lead_player] = (self.lead_card, 'NotApplicable')
        
        # Handle the lead card depending on whether it is a Joker or not
        if 'JOKER' not in str(self.lead_card):
            self.handle_non_joker_lead()
        else:
            self.handle_joker_lead()
        
        winner = self.determine_trick_winner() 
        print(f'{winner.name} is the winner of this trick.') 
        # Update the lead player's index for the following trick
        self.lead_player_index = self.players.index(winner)
        # Reset the dictionary after each trick
        self.cards_played = {}

    def handle_non_joker_lead(self):
        """
        Handles the case when a non-Joker card is led.
        """
        for player in self.get_following_players():
            follow_card, follow_joker_action = self.get_follow_card_for_non_joker_lead(player) # Play a follow card
            player.cards.remove(follow_card) # Remove it from the player's hand
            self.cards_played[player] = (follow_card, follow_joker_action)
    
    def get_follow_card_for_non_joker_lead(self, player: object) -> tuple[object, str]:
        """
        Gets the card played by a player following a non-Joker lead, and the action of playing a Joker card (player can either 'Play' or 'Give up' the Joker card).
        
        Args:
            player (Player object): The player who is following the lead.
                
        Returns:
            Tuple[Card object, str]: A tuple where the Card object represents the card played, and a string represents the action taken when playing a Joker card ('Play', 'Give up' or 'NotApplicable')
        """
        follow_card = player.play_card()
        player_suits = [card.suit for card in player.cards]
        follow_joker_action = 'NotApplicable'
        
        # 1. When playing a Joker card
        if 'JOKER' in str(follow_card):
            # Prompt user to decide whether to 'Play' the Joker or not
            follow_joker_action = self.get_follow_joker_action() 
        
        # 2. When playing a non-Joker card
        else:
            # First scenario: if there is a card with the same suit as the lead card in the player's hand, the player should not be allowed to play a card with another suit
            while self.lead_card.suit in player_suits and follow_card.suit != self.lead_card.suit:
                print(f'You should play a card with the same suit ({self.lead_card.suit}).')
                follow_card = player.play_card()
            
            # Second scenario: if the player is not able to follow the lead suit, then they must play a trump suit, provided there is a trump suit and they have it
            if self.trump_suit != 'None' and self.lead_card.suit not in player_suits:
                while self.trump_suit in player_suits and follow_card.suit != self.trump_suit:
                    print(f'In this case, you should play the trump suit ({self.trump_suit}).')
                    follow_card = player.play_card()
        
        return follow_card, follow_joker_action

    def handle_joker_lead(self):
        """
        Handles the case when a Joker card is led.
        """
        # First, ask the lead player to choose between 'High' or 'Low'
        self.lead_joker_action = self.get_high_low_choice()
        # Then, prompt the player to choose the suit to be played following a Joker lead
        self.suit_wanted = self.get_suit_wanted()
        
        for player in self.get_following_players():
            follow_card, follow_joker_action = self.get_follow_card_for_joker_lead(player)
            player.cards.remove(follow_card)
            self.cards_played[player] = (follow_card, follow_joker_action)
    
    def get_high_low_choice(self) -> str:
        """
        Prompts the player to choose between 'High' or 'Low' action when leading with a Joker card.
        
        Returns:
            str: The player's choice ('High' or 'Low').
        """
        action = input('"High" of "Low"? Choose one of them: ').strip().capitalize()
        while action not in ['High', 'Low']:
            action = input('Invalid action! Choose "High" or "Low": ').strip().capitalize()
        return action
    
    def get_suit_wanted(self) -> str:
        """
        Prompts the player to choose the suit to be played following a Joker lead (the suit they want others to play and win or the suit they want to win with).
        
        Returns:
            str: The suit required to be played.
        """
        if self.lead_joker_action == 'High':
            suit_prompt = f'Which suit would you like others to play? Enter "D" for ♦, "H" for ♥, "S" for ♠, "C" for "♣": '
        else:
            suit_prompt = f'Which suit would you like to win this trick? Enter "D" for ♦, "H" for ♥, "S" for ♠, "C" for "♣": '
            
        suit_wanted = input(suit_prompt).strip().capitalize()
        while suit_wanted not in SUITS.values() and suit_wanted not in SUITS.keys():
            suit_wanted = input('Invalid input! Try again: ').strip().capitalize()
        
        if suit_wanted in SUITS.keys():
            suit_wanted = SUITS[suit_wanted]
            
        return suit_wanted
    
    def get_follow_card_for_joker_lead(self, player: object) -> tuple[object, str]:
        """
        Gets the card played by a player following a Joker lead, and the action of playing another Joker card (player can either 'Play' or 'Give up' the Joker card).
        
        Args:
            player (Player object): The player who is following the lead.
                
        Returns:
            Tuple[Card object, str]: A tuple where the Card object represents the card played, and a string represents the action taken when playing a Joker card ('Play', 'Give up' or 'NotApplicable')
        """
        player_suits = [card.suit for card in player.cards]
        suit_cards = [card for card in player.cards if card.suit == self.suit_wanted]
        follow_card = player.play_card()
        follow_joker_action = 'NotApplicable'
        
        # 1. When playing a Joker card
        if 'JOKER' in str(follow_card):
            # Prompt user to decide whether to 'Play' the Joker or not
            follow_joker_action = self.get_follow_joker_action()
        
        # 2. When playing a non-Joker card
        else:     
            if self.lead_joker_action == 'High':
                highest_card = max(suit_cards, key = lambda card: card.value) if suit_cards else None
                # First scenario: if the player has any cards of the required suit, they must play the highest-ranking card among those cards
                while self.suit_wanted in player_suits and follow_card != highest_card:
                    print(f'You should play the highest card with {self.suit_wanted} suit. Try again!')
                    follow_card = player.play_card()
                # Second scenario: if the player does not have any cards of the required suit, then they must play a trump suit, provided there is a trump suit and they have it
                if self.trump_suit != 'None' and self.suit_wanted not in player_suits:
                    while self.trump_suit in player_suits and follow_card.suit != self.trump_suit:
                        print(f'If you do not have the {self.suit_wanted} card, you should play a trump suit ({self.trump_suit}).')
                        follow_card = player.play_card()
            
            if self.lead_joker_action == 'Low':
                # First scenario: the player must play a card of the required suit if they hold any cards of that suit
                while self.suit_wanted in player_suits and follow_card.suit != self.suit_wanted:
                    print(f'You should play a card with {self.suit_wanted} suit. Try again!')
                    follow_card = player.play_card()
                
                # Second scenario: if the player does not have any cards of the required suit, then they must play a trump suit, provided there is a trump suit and they have it
                if self.trump_suit != 'None' and self.suit_wanted not in player_suits:
                    while self.trump_suit in player_suits and follow_card.suit != self.trump_suit:
                        print(f'If you do not have the {self.suit_wanted} card, you should play a trump suit ({self.trump_suit}).')
                        follow_card = player.play_card()
        
        return (follow_card, follow_joker_action)
    
    def get_follow_joker_action(self) -> str:
        """
        Prompts the player to choose whether to play or give up the Joker card.

        Returns:
            str: The player's choice ('Play' or 'Give up').
        """
        action = input('Would you like to play the JOKER or give it up? Enter "Play" or "Give up": ').strip().capitalize()
        while action not in ['Play', 'Give up']:
           action = input('Invalid input! Please enter "Play" or "Give up": ').strip().capitalize()
        return action
    
    def determine_trick_winner(self) -> object:
        """
        Determines the winner of the current trick based on the cards played.

        Returns:
            Player (object): The Player object who has won the trick.
        """
        if 'JOKER' in str(self.lead_card):
            return self.determine_winner_for_joker_lead()
        else:
            return self.determine_winner_for_non_joker_lead()

    def determine_winner_for_non_joker_lead(self) -> object:
        """
        Determines the winner of a trick led with a non-Joker card.
        
        Returns:
            Player (obect): The player object who has won the trick.
        """
        players_who_played_joker = []
        players_who_played_trump_suit = {}
        highest_card_player = None 
        highest_value = -1
        
        for player, (card, follow_joker_action) in self.cards_played.items():
            # If the player has chosen to 'Play' a Joker card
            if 'JOKER' in str(card):
                if follow_joker_action == 'Play':
                    players_who_played_joker.append(player)
            # If the player's card belongs to the trump suit
            elif card.suit == self.trump_suit:
                players_who_played_trump_suit[player] = card.value
            # If the player's card is of the same suit as the lead card
            elif self.lead_card.suit == card.suit:
                if card.value > highest_value:
                    highest_value = card.value
                    highest_card_player = player
        
        # Joker card is the winner of the trick. If two Jokers are played, the player who played the last Joker wins the trick.
        if players_who_played_joker:
            winner = players_who_played_joker[-1]
        # If no Joker is played, the player who played the highest trump suit card wins the trick.
        elif players_who_played_trump_suit:
            highest_player, _ = max(players_who_played_trump_suit.items(), key = lambda pair: pair[1])
            winner = highest_player
        # If the players' cards are not from the trump suit and are of the same suit as the lead card, the player with the highest-ranking card of that suit wins the trick.
        elif highest_card_player:
            winner = highest_card_player
        # If the lead suit is played, and no other player has a card of the same suit (or a lower-ranking card), a Joker, or a trump suit card, the lead player wins the trick.
        else:
            winner = self.players[self.lead_player_index]
        
        winner.tricks_won += 1
        return winner 
    
    def determine_winner_for_joker_lead(self) -> object:
        """
        Determines the winner of a trick led with a Joker card.
        
        Returns:
            Player (obect): The player object who has won the trick.
        """
        trump_suits_played = {}
        suit_wanted_played = {}
        
        for player, (card, follow_joker_action) in self.cards_played.items():
            # If the player has chosen to 'Play' a Joker card
            if 'JOKER' in str(card):
                if follow_joker_action == 'Play':
                    # As the first Joker has already been played as the lead card, then the second player who chooses to 'Play' their Joker card automatically becomes the winner of that trick
                    player.tricks_won += 1
                    return player
            # If the player's card belongs to the trump suit
            elif card.suit == self.trump_suit:
                trump_suits_played[player] = card.value
            # If the player's card is of the same suit as the suit required
            elif card.suit == self.suit_wanted:
                    suit_wanted_played[player] = card.value
        
        # Track if the suit required to be played is the same as the trump suit
        is_trump_wanted = (self.suit_wanted == self.trump_suit)

        if self.lead_joker_action == 'High':
            # If no Joker is played, and the required suit is the trump suit, the lead player who played the Joker wins the trick.
            if is_trump_wanted:
                winner = self.players[self.lead_player_index]
            # If a suit other than the trump suit is required, the player who played the highest-ranking trump suit card wins the trick.
            elif trump_suits_played:  
                highest_player, _ = max(trump_suits_played.items(), key = lambda pair: pair[1])
                winner = highest_player
            # In all other cases, the lead player who played the Joker wins the trick.
            else:
                winner = self.players[self.lead_player_index]
        
        if self.lead_joker_action == 'Low':
            # The player who played the highest-ranking trump suit card wins the trick.
            if trump_suits_played:
                highest_player, _ = max(trump_suits_played.items(), key = lambda pair: pair[1])
                winner = highest_player
            # The player who played the highest-ranking card of the required suit wins the trick.
            elif suit_wanted_played:
                highest_player, _ = max(suit_wanted_played.items(), key = lambda pair: pair[1])
                winner = highest_player
            # In all other cases, the lead player who played the Joker wins the trick.
            else:
                winner = self.players[self.lead_player_index]
        
        winner.tricks_won += 1
        return winner
    
    def get_following_players(self):
        """
        Returns the list of players who will follow the lead player.
        """
        return self.players[self.lead_player_index + 1:] + self.players[:self.lead_player_index]
