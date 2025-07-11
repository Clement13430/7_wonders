"""The information about the class Player, link to every information that can be linked to a player stats."""

from __future__ import annotations

import copy
import re
from collections import Counter
from inspect import signature
from typing import Callable

from common import (
    ACTION_DISCARD,
    ACTION_PLAYCARD,
    ACTION_STAGEWONDER,
    ALL_COLOURS,
    CARDS_BLUE,
    CARDS_BROWN,
    CARDS_GREEN,
    CARDS_GREY,
    CARDS_PURPLE,
    CARDS_RED,
    CARDS_YELLOW,
    RESOURCE_BRICK,
    RESOURCE_GLASS,
    RESOURCE_LOOM,
    RESOURCE_ORE,
    RESOURCE_PAPER,
    RESOURCE_STONE,
    RESOURCE_WOOD,
    find_card,
)

from cards import Card


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 3
        self.resources = []  # resources of the player
        self.half_resources = []  # the resources that have to be chosen between two
        self.yellow_resources = []  # the resources given by the yellow cards
        self.tableau = []  # all the player's played cards
        self.military = []  # war wins/losses
        self.shields = 0  # The number of shields the player has
        self.blue_points = 0  # The number of blue victory points the player has
        self.yellow_score = 0  # The yellow victory points of the player
        self.science_symbols = {"G": 0, "C": 0, "T": 0}
        self.science_choice = 0  # number of card that give the possibility to chose between one of the three science symbol
        self.east_trade_prices = {
            RESOURCE_WOOD: 2,
            RESOURCE_ORE: 2,
            RESOURCE_STONE: 2,
            RESOURCE_BRICK: 2,
            RESOURCE_GLASS: 2,
            RESOURCE_LOOM: 2,
            RESOURCE_PAPER: 2,
        }
        self.west_trade_prices = self.east_trade_prices.copy()
        self.wonder = None
        self.side_a_wonder = True
        self.current_stage_wonder = 0  # from 0 (not started) to 3 (ended)
        self.personality = None

    def set_personality(self, persona):
        self.personality = persona

    def print_info(self):
        cards = {
            CARDS_BROWN: [],
            CARDS_GREY: [],
            CARDS_YELLOW: [],
            CARDS_BLUE: [],
            CARDS_RED: [],
            CARDS_GREEN: [],
            CARDS_PURPLE: [],
        }
        print(f"Stats of the player {self.name}:")
        print("\tYou have $%d" % (self.money))
        print("\tYou have %d shields" % (self.shields))
        print("\tWar points: %s" % (self.military))
        print(f"\twest trading prices: {self.west_trade_prices}")
        print(f"\tEast trading prices: {self.east_trade_prices}")
        print(f"\twonder: {self.wonder.side_a}")
        for c in self.tableau:
            cards[c.colour].append(c)

        biggest_deck = 0
        for colour in cards.keys():
            count = len(cards[colour])
            if count > biggest_deck:
                biggest_deck = count
        print("built cards:")
        for i in range(biggest_deck):
            line = {
                CARDS_BROWN: "\t",
                CARDS_GREY: "\t",
                CARDS_YELLOW: "\t",
                CARDS_BLUE: "\t",
                CARDS_RED: "\t",
                CARDS_GREEN: "\t",
                CARDS_PURPLE: "\t",
            }
            for colour in [
                CARDS_BROWN,
                CARDS_GREY,
                CARDS_YELLOW,
                CARDS_BLUE,
                CARDS_RED,
                CARDS_GREEN,
                CARDS_PURPLE,
            ]:
                if len(cards[colour]) > biggest_deck - 1 - i:
                    line[colour] = "%s" % (
                        cards[colour][biggest_deck - 1 - i].pretty_print_name()
                    )
                else:
                    line[colour] = "        "
            print(
                "\t%s\t%s\t%s\t%s\t%s\t%s\t%s"
                % (
                    line[CARDS_BROWN],
                    line[CARDS_GREY],
                    line[CARDS_YELLOW],
                    line[CARDS_BLUE],
                    line[CARDS_RED],
                    line[CARDS_GREEN],
                    line[CARDS_PURPLE],
                )
            )

    def can_build_with_chain(self, card):
        for precard in card.prechains:
            if find_card(self.get_cards(), precard):
                return (True, 0, 0, 0)
        return (
            False,
            0,
            0,
            0,
        )  # (Can do the card or not, money to the bank, money to west player, money to east player)

    def can_do_card(
        self, resources_needed: list[str], west_player: Player, east_player: Player
    ) -> tuple:
        """Return the following tuple: (True/False if the player can buy the card, the money he has to pay to the bank, the money he has to play to the west player, the money
        he has to pay to the east player)."""
        money_available = copy.copy(self.money)
        money_spent_bank = 0
        cost_west = 0
        cost_east = 0

        yellow_resources_player = copy.copy(self.yellow_resources)
        resources_player = copy.copy(self.resources)
        half_resources_player = copy.copy(self.half_resources)
        resources_west_player = copy.copy(west_player.resources)
        resources_east_player = copy.copy(east_player.resources)
        half_resources_west_player = copy.copy(west_player.half_resources)
        half_resources_east_player = copy.copy(east_player.half_resources)
        card_cost = copy.copy(
            resources_needed
        )  # resources needed to play the card, we will delete step by step the resources that the player have/can pay

        if len(card_cost) == 0:
            return [True, money_spent_bank, cost_west, cost_east]

        cost_num = 0
        # point out the amount of money the player has to pay to the bank
        for cost_num in range(len(card_cost)):
            if card_cost[cost_num] == "$":
                if money_available > 0:
                    money_available -= 1
                    money_spent_bank += 1
                else:
                    return [False, 0, 0, 0]

                card_cost.pop(cost_num)

        if len(card_cost) == 0:
            return [True, money_spent_bank, cost_west, cost_east]

        # Check first if the permenant resources of the player are enough to buy the card

        if len(resources_player) > 0:
            cost_num = 0
            while cost_num < len(card_cost):
                ressource_num = 0
                while ressource_num < len(resources_player):
                    if (
                        cost_num < len(card_cost)
                        and card_cost[cost_num] == resources_player[ressource_num]
                    ):
                        card_cost.pop(cost_num)
                        resources_player.pop(ressource_num)
                        ressource_num = 0

                    else:
                        ressource_num += 1
                cost_num += 1

        if len(card_cost) == 0:
            return [True, money_spent_bank, cost_west, cost_east]

        """================================================================================================================
        # Simple version when we check sequentially between variable resources, yellow resources and neighbours resources if the player can by the card. 
        # A more accurate and complete version of the following code would consider checking at the same time all those solutions."""

        if len(half_resources_player) > 0:
            cost_num = 0
            while cost_num < len(card_cost):
                ressource_num = 0
                while ressource_num < len(half_resources_player):
                    if (cost_num < len(card_cost)) and (
                        card_cost[cost_num] == half_resources_player[ressource_num][0]
                        or card_cost[cost_num]
                        == half_resources_player[ressource_num][1]
                    ):
                        card_cost.pop(cost_num)
                        half_resources_player.pop(ressource_num)
                        ressource_num = 0
                        if len(card_cost) == 0:
                            return [True, money_spent_bank, cost_west, cost_east]
                    else:
                        ressource_num += 1
                cost_num += 1

        if len(yellow_resources_player) > 0:
            cost_num = 0
            while cost_num < len(card_cost):
                ressource_num = 0
                while ressource_num < len(yellow_resources_player):
                    if cost_num < len(card_cost) and (
                        card_cost[cost_num] == yellow_resources_player[ressource_num][0]
                        or card_cost[cost_num]
                        == yellow_resources_player[ressource_num][1]
                        or card_cost[cost_num]
                        == yellow_resources_player[ressource_num][2]
                        or card_cost[cost_num]
                        == yellow_resources_player[ressource_num][3]
                    ):
                        card_cost.pop(cost_num)
                        yellow_resources_player.pop(ressource_num)
                        ressource_num = 0
                        if len(card_cost) == 0:
                            return [True, money_spent_bank, cost_west, cost_east]
                    else:
                        ressource_num += 1
                cost_num += 1

        if len(resources_west_player) > 0:
            cost_num = 0
            while cost_num < len(card_cost):
                ressource_num = 0
                while ressource_num < len(resources_west_player):
                    if cost_num < len(card_cost) and (
                        card_cost[cost_num] == resources_west_player[ressource_num]
                        and money_available
                        > self.west_trade_prices[card_cost[cost_num]]
                    ):
                        money_available -= self.west_trade_prices[card_cost[cost_num]]
                        cost_west += self.west_trade_prices[card_cost[cost_num]]
                        card_cost.pop(cost_num)
                        resources_west_player.pop(ressource_num)
                        ressource_num = 0

                        if len(card_cost) == 0:
                            return [True, money_spent_bank, cost_west, cost_east]
                    else:
                        ressource_num += 1
                cost_num += 1

        if len(half_resources_west_player) > 0:
            cost_num = 0
            while cost_num < len(card_cost):
                ressource_num = 0
                while ressource_num < len(half_resources_west_player):
                    if (
                        cost_num < len(card_cost)
                        and (
                            card_cost[cost_num]
                            == half_resources_west_player[ressource_num][0]
                            or card_cost[cost_num]
                            == half_resources_west_player[ressource_num][1]
                        )
                        and money_available
                        > self.west_trade_prices[card_cost[cost_num]]
                    ):
                        cost_west += self.west_trade_prices[card_cost[cost_num]]
                        money_available -= self.west_trade_prices[card_cost[cost_num]]
                        card_cost.pop(cost_num)
                        half_resources_west_player.pop(ressource_num)
                        ressource_num = 0

                        if len(card_cost) == 0:
                            return [True, money_spent_bank, cost_west, cost_east]
                    else:
                        ressource_num += 1
                cost_num += 1

        if len(resources_east_player) > 0:
            cost_num = 0
            while cost_num < len(card_cost):
                ressource_num = 0
                while ressource_num < len(resources_east_player):
                    if cost_num < len(card_cost) and (
                        card_cost[cost_num]
                        == resources_east_player[  # Check if the neighbour has the resource
                            ressource_num
                        ]
                        and money_available
                        > self.east_trade_prices[card_cost[cost_num]]
                    ):
                        cost_east += self.east_trade_prices[card_cost[cost_num]]
                        money_available -= self.east_trade_prices[card_cost[cost_num]]
                        card_cost.pop(cost_num)
                        resources_east_player.pop(ressource_num)
                        ressource_num = 0

                        if len(card_cost) == 0:
                            return [True, money_spent_bank, cost_west, cost_east]

                    else:
                        ressource_num += 1
                cost_num += 1

        if len(half_resources_east_player) > 0:
            cost_num = 0
            while cost_num < len(card_cost):
                ressource_num = 0
                while ressource_num < len(half_resources_east_player):
                    if (
                        cost_num < len(card_cost)
                        and (  # Check if the neighbour has the resource
                            card_cost[cost_num]
                            == half_resources_east_player[ressource_num][0]
                            or card_cost[cost_num]
                            == half_resources_east_player[ressource_num][1]
                        )
                        and money_available
                        > self.east_trade_prices[card_cost[cost_num]]
                    ):  # Check if the playuer can afford the ressource
                        cost_east += self.east_trade_prices[card_cost[cost_num]]
                        money_available -= self.east_trade_prices[card_cost[cost_num]]
                        card_cost.pop(cost_num)
                        half_resources_east_player.pop(ressource_num)
                        ressource_num = 0

                        if len(card_cost) == 0:
                            return [True, money_spent_bank, cost_west, cost_east]
                    else:
                        ressource_num += 1
                cost_num += 1

        return [False, 0, 0, 0]

        # to check

    def can_do_next_stage(self, west_player, east_player) -> tuple:
        """Return the following tuple: (True/False if the player can do the stage, the money he has to pay to the bank, the money he has to play to the west player, the money
        he has to pay to the east player)."""
        money_to_bank, money_to_west, money_to_right = 0, 0, 0
        if self.current_stage_wonder == 3:
            return [False, money_to_bank, money_to_west, money_to_right]
        if self.side_a_wonder:
            stage = self.wonder.side_a[self.current_stage_wonder]
        else:
            stage = self.wonder.side_b[self.current_stage_wonder]

        resources_needed = stage[0]

        res = self.can_do_card(resources_needed, west_player, east_player)
        return res

    def is_card_in_tableau(self, card):
        return find_card(self.tableau, card.name) is not None

    def play_card(
        self,
        card: Card,
        west_player: Player,
        east_player: Player,
        money_to_pay: list[int, int, int],
    ) -> None:
        """Apply the effects of the card to the current player."""
        self.money -= money_to_pay[0]
        self.money -= money_to_pay[1]
        self.money -= money_to_pay[2]
        west_player.money += money_to_pay[1]
        east_player.money += money_to_pay[2]
        self.add_card(card)
        play_function = self.play_colour_card(card.colour)
        # print(play_function)
        # print(type(play_function))
        # input()
        # print(play_function.__name__)
        # input(5)
        # print(signature(play_function))
        # print(len(signature(play_function).parameters))
        # input(9)
        if len(signature(play_function).parameters) == 3:
            # print(1000000000000)
            play_function(card, west_player, east_player)
            # input()
        else:
            play_function(card)

    def add_card(self, card: Card):
        """Add the card to the list of cards the player has played."""
        self.tableau.append(card)

    def play_red_card(self, card: Card) -> None:
        self.shields += int(card.effect)

    def play_blue_card(self, card: Card) -> None:
        self.blue_points += int(card.effect)

    def play_yellow_card(
        self, card: Card, west_player: Player, east_player: Player
    ) -> None:
        """Apply all the effects of a yellow card."""

        if "trade-$" in card.effect:
            resources = (card.effect.split("{")[1]).split("}")[0]
            resources = [resources[i] for i in range(len(resources))]
            sides = card.effect.split(" ")[1]
            sides = [
                sides[i]
                for i in range(len(sides))
                if (sides[i] == "<" or sides[i] == ">")
            ]
            for side in sides:
                if side == "<":  # West
                    for resource in resources:
                        self.west_trade_prices[resource] = 1
                if side == ">":  # East
                    for resource in resources:
                        self.east_trade_prices[resource] = 1
        elif card.effect[-1] == "$":
            freq = Counter(card.effect.replace(" ", ""))
            if len(freq) == 1:
                self.money += freq["$"]
        elif "+resource{" in card.effect:
            resources = card.effect.split("{")[1].split("}")[0]
            resources = resources.replace("/", "0")

            self.yellow_resources.append(
                tuple([resources[i] for i in range(len(resources))])
            )
        elif re.match("[$V]+{.+} [<v>]+", card.effect) and any(
            colour in card.effect.split("{")[1].split("}")[0] for colour in ALL_COLOURS
        ):
            # print("card colour")
            # input()
            number_of_gold = Counter(card.effect.split("{")[0])["$"]
            freq_direction = Counter(card.effect.split("}")[1])
            colours = card.effect.split("{")[1].split("}")[0]
            self.money += number_of_gold * (
                west_player.how_much_colour_card(colours) * freq_direction["<"]
                + self.how_much_colour_card(colours) * freq_direction["v"]
                + east_player.how_much_colour_card(colours) * freq_direction[">"]
            )
        elif re.match("[$V]+{wonder} [<v>]+", card.effect):
            # print("card wonder")
            # input()
            number_of_gold = Counter(card.effect.split("{")[0])["$"]
            freq_direction = Counter(card.effect.split("}")[1])
            self.money += number_of_gold * (
                west_player.current_stage_wonder * freq_direction["<"]
                + self.current_stage_wonder * freq_direction["v"]
                + east_player.current_stage_wonder * freq_direction[">"]
            )

        else:
            print(re.match("[$V]+{.+} [<v>]+", card.effect))
            print(re.match("[$V]+\{.+\} [<v>]+", card.effect))
            print(re.match("[$v]+{.+} [<v>]+", card.effect))
            print(re.match("[$v]+\{.+\} [<v>]+", card.effect))
            print(f"The following effect is not know: ({card.effect})")
            raise NotImplementedError

    def play_green_card(self, card: Card) -> None:
        self.science_symbols[card.effect] += 1

    def play_brown_card(self, card: Card) -> None:

        if "/" in card.effect:
            self.half_resources.append((card.effect[0], card.effect[2]))
        else:
            for resource in card.effect:
                self.resources.append(resource)

    def play_grey_card(self, card: Card) -> None:
        self.resources.append(card.effect)

    def how_much_colour_card(self, colour: str) -> int:
        return len([card for card in self.tableau if card.colour in colour])

    def play_purple_card(self, card: Card) -> None:
        pass

    def play_colour_card(self, colour: str) -> Callable:
        link_colour_function = {
            "red": lambda card: self.play_red_card(card),
            "blue": lambda card: self.play_blue_card(card),
            "green": lambda card: self.play_green_card(card),
            "brown": lambda card: self.play_brown_card(card),
            "grey": lambda card: self.play_grey_card(card),
            "yellow": lambda card, west_player, east_player: self.play_yellow_card(
                card, west_player, east_player
            ),
            "purple": lambda card: self.play_purple_card(card),
        }
        return link_colour_function[colour]

    def play_hand(self, hand, west_player, east_player):
        """display all the cards and actions that can be done and return the choice of the player"""
        options = []
        for card in hand:

            if not self.is_card_in_tableau(
                card
            ):  # Check if the card is not already played
                res_chain = self.can_build_with_chain(card)
                if res_chain[0]:  # Check if the card can be done using chaining
                    options.append((ACTION_PLAYCARD, card, res_chain[1:4]))
                else:
                    res = self.can_do_card(card.cost, west_player, east_player)

                    if res[0]:  # check if the card can be done
                        options.append(
                            (
                                ACTION_PLAYCARD,
                                card,
                                res[1:4],
                            )
                        )
            options.append((ACTION_DISCARD, card, [0, 0, 0]))
            if (
                self.wonder.built_stages < 3
            ):  # Check if there is still a stage wonder to be done
                stage_res = self.can_do_next_stage(west_player, east_player)
                if stage_res[0]:  # Check if the stage can be done:
                    options.append((ACTION_STAGEWONDER, card, stage_res[1:4]))
        i = 0
        print("-=================-")

        options = sorted(
            options,
            key=lambda x: {
                CARDS_GREY: 0,
                CARDS_BROWN: 1,
                CARDS_YELLOW: 2,
                CARDS_BLUE: 3,
                CARDS_RED: 4,
                CARDS_GREEN: 5,
                CARDS_PURPLE: 6,
            }[x[1].colour],
        )
        for o in options:
            actions = {
                ACTION_PLAYCARD: "Play",
                ACTION_DISCARD: "Discard",
                ACTION_STAGEWONDER: "Stage",
            }
            card = o[1]

            print(
                "[%d]: %s\t%s\t%s\t bank cost: %s \t west cost: %s \t east_cost: %s"
                % (
                    i,
                    actions[o[0]],
                    card.get_cost_as_string(),
                    card.pretty_print_name(),
                    o[2][0],
                    o[2][1],
                    o[2][2],
                )
            )
            i += 1
        print("-=================-")
        # input()
        choice = self.personality.make_choice(options)

        if 0 > choice or choice >= i:
            print(f"Error: please choose a number between 0 and {i-1} included")
            choice = self.personality.make_choice(options)
            if 0 > choice or choice >= i:
                raise Exception(
                    f"Error: please choose a number between 0 and {i-1} included"
                )

        return options[choice]
