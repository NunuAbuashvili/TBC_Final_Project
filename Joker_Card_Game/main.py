from game import Game

def main():
    """
    The main entry point of the program.

    This function handles the overall flow of the game: welcomes players, retrieves player names, sets the order of players, plays the sets and hands until the game is complete, also checks for bonuses and determines the overall winner.
    """
    game = Game()
    try:
        game.welcome()    
        game.get_player_names()
        game.print_the_order_of_players()
        game.play_set()
        game.determine_final_winner()
    except KeyboardInterrupt:
        print('\nGame interrupted by the user.')
        exit()
    finally:
        print("Thank you for playing!")

if __name__ == "__main__":
    main()
