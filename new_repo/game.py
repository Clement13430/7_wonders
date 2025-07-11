"""Information about the game in itself and the set up of the game."""

import random

import logger
from common import ACTION_DISCARD, ACTION_PLAYCARD, ACTION_STAGEWONDER, CARDS_PURPLE
from players import Player
from score import score_military, score_purple, score_science, score_yellow


class GameState:
    """Global class that contains informations about the game, only one instance is meant to be created per game."""

    def __init__(self, players: list[tuple[str, type]]):
        self.player_count = len(players)
        self.players = []
        self.ages_cards = []
        self.decks = [[]] * len(players)
        self.discard_pile = []
        self.logger = logger.Logger()
        for i in range(len(players)):
            name, persona = players[i]

            self.players.append(Player(name))
            self.players[i].set_personality(persona())

    def setup_age_cards(self, cards):
        """Shuffle and prepare the cards for every age depending on the number of players."""
        age_1 = [c for c in cards if c.age == 1 and c.players <= self.player_count]
        age_2 = [c for c in cards if c.age == 2 and c.players <= self.player_count]
        age_3 = [
            c
            for c in cards
            if c.age == 3
            and c.colour != CARDS_PURPLE
            and c.players <= self.player_count
        ]
        purple = [
            c
            for c in cards
            if c.age == 3
            and c.colour == CARDS_PURPLE
            and c.players <= self.player_count
        ]

        random.shuffle(age_1)
        random.shuffle(age_2)
        random.shuffle(purple)
        age_3 += purple[0 : self.player_count + 2]
        random.shuffle(age_3)

        self.ages_cards = [age_1, age_2, age_3]

    def deal_wonders(self, wonders):
        """Shuffle all the wonders and gives one to every player."""
        random.shuffle(wonders)
        for i in range(self.player_count):
            self.players[i].wonder = wonders[i]
            self.players[i].side_wonder_a = random.choice([True, False])

    def deal_age_cards(self, age):
        """Deal (distribuer) all the cards of an age to each player."""
        cards = self.ages_cards[age][0:]
        p = 0
        for i in range(self.player_count):
            self.decks[i] = []
        while len(cards):
            self.decks[p].append(cards[0])
            p += 1
            p %= self.player_count
            cards = cards[1:]

    def _get_west_player(self, playerid):
        """Return the west player of the chosen player."""
        return self.players[(playerid + self.player_count - 1) % self.player_count]

    def _get_east_player(self, playerid):
        """Return the east player of the chosen player."""
        return self.players[(playerid + 1) % self.player_count]

    def game_loop(self):
        print("beginning of the game")
        for age in range(3):
            print(f"Age {age+1}")
            self.logger.log_age_header(age)
            self.deal_age_cards(age)
            offset = 0  # le numéro du tour de jeu actuel au sein d'un age
            while (
                len(self.decks[0]) > 1
            ):  # until each player has only 1 card left in his deck
                self.play_turn(offset)
                offset = (
                    offset + [1, self.player_count - 1, 1][age]
                ) % self.player_count
            # everyone discards the last card
            for p in range(self.player_count):
                self.discard_pile.append(self.decks[p][0])

            # score military
            for p in range(self.player_count):
                west = self._get_west_player(p)
                east = self._get_east_player(p)
                player = self.players[p]
                player.military.append(score_military(player, west, east, age))
            print(f"End of age {age}")

        for i in range(self.player_count):
            player = self.players[i]
            west = self._get_west_player(i)
            east = self._get_east_player(i)
            greenscore = score_science(player)
            redscore = 0
            for military in player.military:
                redscore += military[0] + military[1]
            moneyscore = player.money / 3
            yellowscore = score_yellow(player, west, east)
            purplescore = score_purple(player, west, east)
            input()
            totalscore = (
                self.blue_points
                + greenscore
                + redscore
                + yellowscore
                + purplescore
                + moneyscore
            )
            text = (
                "Final score: Blue: %d, Green: %d, red: %d, yellow: %d, purple: %d, $: %d, total: %d"
                % (
                    self.blue_points,
                    greenscore,
                    redscore,
                    yellowscore,
                    purplescore,
                    moneyscore,
                    totalscore,
                )
            )
            self.logger.log_freetext(player.get_name() + " " + text)
            print(text)

        logfile = open("logfile.txt", "w")
        self.logger.dump(logfile)
        logfile.close()

    def play_turn(self, offset):
        """Make each player play its next turn."""
        for i in range(self.player_count):
            player = self.players[i]
            west_player = self._get_west_player(i)
            east_player = self._get_east_player(i)
            deckid = (i + offset) % self.player_count
            # input(1)
            player.print_info()
            # input("pause")
            # This loop is actually wrong.
            # Everyone should choose the card they will play, server
            # validates the move is legal, then each player plays the card
            # Then each player adds the new card to their tableau
            # action, card = can_buy_card(self.decks[deckid], west_player, east_player)

            action, card, money_to_pay = player.play_hand(
                self.decks[deckid], west_player, east_player
            )  # action c'est le numéro de l'action (entre 0 et 2), card la carte and money to pay the money to give in the format [money to bank, money to west, money to east]
            # print(type(card))
            # input()
            # print(action)
            # print(card)
            # input(2)
            if action == ACTION_PLAYCARD:
                player.play_card(card, west_player, east_player, money_to_pay)
            elif action == ACTION_DISCARD:
                self.discard_pile.append(card)
                player.money += 3
            elif action == ACTION_STAGEWONDER:
                raise NotImplementedError
                # make sure we can do that
            # 	input("pause1")
            # input("pause2")
            self.decks[deckid].remove(card)
