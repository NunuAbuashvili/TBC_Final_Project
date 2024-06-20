# Card Game: JOKER

This project is a Python implementation of a card game called "JOKER". The game is played with a standard deck of 36 cards, including two Joker cards that substitute for the two black Sixes. The objective is to maximize your score by bidding and playing cards strategically.

## Game Rules

- The game is played between 4 players.
- There are 4 sets, each consisting of 4 hands.
- In each hand, 9 cards are dealt to each player. In the first hand, the last player deals the cards, and then the dealer role rotates clockwise in subsequent hands.
- The first player after the dealer has the right to choose a trump suit (or no trump) based on the first three cards in their hand.
- Players take turns bidding on the number of tricks they think they can win.
- The player to the dealer's left leads the first trick, and the suit of the lead card determines the suit that must be followed. If a player cannot follow suit, they may play a trump suit card or a Joker card.
- Points are awarded based on the player's bid and the number of tricks won.
- The player with the highest cumulative score across all sets wins the game.
-

## Project Structure

- `main.py`: Entry point of the program.
- `game.py`: Handles the overall game flow, including managing players, sets, and determining the winner.
- `game_set.py`: Manages the gameplay of a set of hands in the card game.
- `game_hand.py`: Manages a single round (hand) of the card game.
- `player.py`: Represents a player in the card game.
- `cards.py`: Defines the `Card` and `Deck` classes for representing cards and a deck of cards.
- `constants.py`: Contains constant values used throughout the game.
- `game_data.JSON`: After each hand, a table is printed displaying the players' names, their bids, and scores. At the end of the game, this table's contents are saved into a JSON file.

## Additional details

### Playing Cards

Cards are unique, meaning that two players cannot hold the same card simultaneously.

### Players

All players should have their unique names, duplicate names are not allowed. Once the order of players is determined at the beginning of the game by a random shuffle, it remains fixed for the entire game.

### Playing a Hand

_Rules for placing a bid:_

- The bid must not be lower than 0 or higher than 9.
- The dealer of the hand cannot place a bid that would make the total sum of all bids equal to 9.

_Rules for playing a card:_

- The first player can play any card they wish.
- Subsequent players must follow suit if able (or play a Joker). If a player cannot follow suit, they must play a trump (or a Joker). If a player has neither a card of the suit led nor a trump, they may play any card.
- A Joker can be played as the leading card. The player who plays the Joker must declare whether they want other players to play their highest card of the specified suit ("High") or aim for another player to win the trick ("Low").
- When a player plays a Joker after the leading card, they should be asked if they want to "Play" or "Give up".

_Winning card:_

There are different scenarios for determining the winning card in a trick:

- If a player chooses to "Play" the Joker, it becomes the winning card. If two Jokers are played in the same trick and both players choose to "Play," the second Joker played wins.
- If the player chooses to "Give up", their Joker is regarded as a card with no value, meaning they cannot win the trick.
- The highest-ranked card in the trump suit wins the trick, unless a Joker is played.
- If all cards in a trick are of the same suit, the card with the highest rank wins, following this descending order: A (Ace) -> K (King) -> Q (Queen) -> J (Jack) -> 10 -> 9 -> 8 -> 7 -> 6.
- When the Joker card is led, in the "High" scenario, the player playing the Joker wins the trick unless a subsequent player plays another Joker or a trump card. In the "Low" scenario, the player whose card has the highest rank in the specified suit wins the trick, unless a trump or another Joker is played.
- A Joker played as "Low" always loses the trick except in one case: if a Joker is led as "Low" and no one else plays the specified suit, a trump, or another Joker, the Joker that was led wins the trick by default.

### Scores

Scores are calculated three times: after each hand, after each set, after the last (fourth) set. Rules for calculating the score:

- A player who wins the exact number of tricks they bid, scores 50 points per trick bid plus 50 bonus points (1 - 100, 2 - 150, 3 - 200, etc.)
- A player who wins more or fewer tricks than they bid, scores 10 points per trick won.
- A player who bids to win all the 9 tricks and succeeds, scores 100 points per trick bid.
- If a player bids one or more tricks but wins none, 500 points are deducted from their score as a penalty.

_Bonus:_

There is a bonus for the player whose bids succeed in every hand during one of four sets. This player gets an additional score equal to the highest amount they scored on any one hand during the set.

_Winner:_

After four sets (sixteen hands), player(s) with the highest score wins the game.

## What I learned

Undertaking the final project for the TBC x USAID course "Intro to Python: Building a Strong Foundation" provided me with the opportunity to apply the knowledge acquired during the course. Working independently, I encountered challenges that allowed me to identify areas where I needed improvement and actively work on enhancing my skills. While initially intimidated by the scale of the project, I successfully broke it down into smaller, manageable problems. However, as a novice, I found it difficult to visualize the entire project and effectively connect these smaller components into a cohesive and efficient final code. Nevertheless, navigating through these challenges offered invaluable insights into the everyday tasks of professional developers.

## Acknowledgments

I would like to express my sincere gratitude to my lecturers Mikheil Lomidze and Tornike Grigalashvili. Their guidance, support, and expertise have been invaluable throughout this learning journey. Thank you for sharing your knowledge and encouraging my growth.
