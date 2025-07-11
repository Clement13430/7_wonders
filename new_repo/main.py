"""Main file containing the complete execution of the game."""

from personalities import Human, StupidAI
from starter import read_cards_file, read_wonders_file

from game import GameState


def init_games():
    global __all_cards

    global __all_wonders

    __all_cards = read_cards_file("card-descriptions.txt")
    __all_wonders = read_wonders_file("wonders.txt")


init_games()

game = GameState(
    [("alice", Human), ("Bob", StupidAI), ("Frank", StupidAI), ("Tony", StupidAI)]
)
game.logger.card_list = __all_cards
game.setup_age_cards(__all_cards)
game.deal_wonders(__all_wonders)
game.game_loop()
