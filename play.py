from cards.helpers import read_cards_file
from game import GameState
from players.personalities import Human, StupidAI
from players.wonders import read_wonders_file


def init_games():
    global __all_cards

    global __all_wonders

    __all_cards = read_cards_file("card-descriptions.txt")
    __all_wonders = read_wonders_file("wonders.txt")


init_games()
game = GameState([("alice", Human), ("Bob", StupidAI), ("Frank", StupidAI)])
game.logger.card_list = __all_cards
game.setup_age_cards(__all_cards)
game.deal_wonders(__all_wonders)
game.game_loop()

# p = game.players[0]
# p.money = 10
# p.tableau += [find_card(__all_cards, "quarry"), find_card(__all_cards, "clay pit"), find_card(__all_cards, "press")]
# game.players[1].tableau += [find_card(__all_cards, "glassworks"), find_card(__all_cards, "sawmill"), find_card(__all_cards, "foundry")]

# p.buy_card(find_card(__all_cards, "fortification"), game.players[1], game.players[2])

# game.players[0].tableau += [find_card(__all_cards, "study"), find_card(__all_cards, "lodge"), find_card(__all_cards, "scientist guild")]
# print helpers.score_science(game.players[0])
