#!/usr/bin/python
#
# Copyright 2015 - Jonathan Gordon
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
# KIND, either express or implied.

import copy
import itertools
from collections import deque

import cards
from common import (
    ACTION_DISCARD,
    ACTION_PLAYCARD,
    ACTION_STAGEWONDER,
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
    RESOURCE_MONEY,
    RESOURCE_ORE,
    RESOURCE_PAPER,
    RESOURCE_STONE,
    RESOURCE_WOOD,
    find_card,
)
from functions import enough_resources


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 3
        self.resources = []  # resources of the player
        self.half_resources = []  # the resources that have to be chosen between two
        self.yellow_resources = []  # the resources given by the yellow cards
        self.tableau = []  # all the players played cards
        self.military = []  # war wins/losses
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
        self.personality = None

    def set_personality(self, persona):
        self.personality = persona

    def get_name(self):
        return self.name

    def get_cards(self):
        return self.tableau

    def add_card(self, card: cards):
        self.tableau.append(card)

    def add_resource(self, resource: str):
        if len(resource) > 1:
            raise Exception(
                f"The lengh of the resource is too long: len(ressources) = {len(resource)}"
            )
        self.resources.append(resource)

    def add_half_resources(
        self, half_resources: str
    ):  # half_resource c'est quand on a accès à qu'une seule ressource par tour sur les deux dispos
        if len(half_resources) > 3:
            return Exception(
                f"The lengh of the half ressource is too long: len(half_ressource) = {half_resources}"
            )
        self.half_resources.append((half_resources[0], half_resources[2]))

    def all_resources_combination_possible(self, with_yellow=True) -> list[list]:
        half_resources_player = copy.copy(self.half_resources)

        if with_yellow:
            yellow_resources_player = copy.copy(self.yellow_resources)
            choice_resources_player = half_resources_player + yellow_resources_player
        else:
            choice_resources_player = half_resources_player

        size_of_vector = 1
        for i in range(len(choice_resources_player)):
            size_of_vector *= len(choice_resources_player[i])
        print(size_of_vector)
        input()
        all_resources_combination = [[] * size_of_vector]

        # add the permanent resources to all the combinations
        for i in range(len(self.resources)):
            for j in range(len(all_resources_combination)):
                all_resources_combination[j].append(self.resources[i])

        print(all_resources_combination)
        input()
        for choice in choice_resources_player:
            for i in range(len(choice)):
                for j in range(
                    size_of_vector / len(choice) * i,
                    size_of_vector / len(choice) * (i + 1),
                ):
                    all_resources_combination[j].append(choice[i])
                    # all_half_resources_combination.append()
        # half resource cost (resources where we have to make a choice which one we use)
        print(all_resources_combination)
        input()
        return all_resources_combination

    def can_buy_card(self, card, west_player, east_player) -> tuple:
        """Return the following tuple: (True/False if the player can buy the card, the money he has to pay to the bank, the money he has to play to the west player, the money
        he has to pay to the east player)."""
        missing = []
        money_available = copy.copy(self.money)
        money_spent = 0
        can_buy_card = False
        cost_west = 0
        cost_east = 0

        options = []
        resources_left_player = self.resources
        resources_left_west_player = west_player.resources
        resources_left_east_player = east_player.resources
        card_cost = copy.copy(card.cost)

        if len(card_cost) == 0:
            return [True, money_spent, cost_west, cost_east]

        u = 0
        # point out the amount of money the player has to pay to the bank
        for u in range(len(card_cost)):
            if card_cost[u] == "$":
                if money_available > 0:
                    money_available -= 1
                    money_spent += 1
                else:
                    return [False, 0, 0, 0]

                card_cost.pop(u)

        if len(card_cost) == 0:
            return [True, money_spent, cost_west, cost_east]

        # Check first if the permenant resources of the player are enough to buy the card
        if len(resources_left_player) > 0:
            i = 0
            while i < len(card_cost):
                j = 0
                while j < len(resources_left_player):
                    if card_cost[i] == resources_left_player[j]:
                        card_cost.pop(i)
                        resources_left_player.pop(j)
                        j = 0
                    else:
                        j += 1
                        i += 1

        if len(card_cost) == 0:
            return [True, money_spent, cost_west, cost_east]

        # Check if the player can buy the card using his own variable resources and/or by paying its neighbours
        money_to_left, monay_to_right = 0, 0
        print(self.yellow_resources)
        # for combinaison in itertools.product(*self.yellow_resources):
        # 	print(combinaison)
        if self.yellow_resources == []:  # aucune ressources gratuite jaune
            return NotImplementedError
        elif (
            len(self.yellow_resources) == 1
        ):  # soir une des 3 ressources grises offerte, soit une des 4 ressources marons offertes
            return NotImplementedError
        elif (
            len(self.yellow_resources) == 2
        ):  # une des 4 ressources marrons offerte et une des 3 ressources grises offertes
            return NotImplementedError
        else:
            print(f"self.yellow_resources = {self.yellow_resources}")
            raise ValueError(
                "Impossible to have more than 2 yellow free resources card."
            )

        # to check

        # size_of_vector = 1
        # for i in range(len(choice_resources_player)):
        #     size_of_vector *= len(choice_resources_player[i])
        # print(size_of_vector)
        # input()
        # all_half_resources_combination = [[] * size_of_vector]
        # for choice in choice_resources_player:
        #     for i in range(len(choice)):
        #         for j in range(
        #             size_of_vector / len(choice) * i,
        #             size_of_vector / len(choice) * (i + 1),
        #         ):
        #             all_half_resources_combination[j].append(choice[i])
        #             all_half_resources_combination.append()
        # half resource cost (resources where we have to make a choice which one we use)
        # print(all_half_resources_combination)
        # input()
        # for resource_combination in all_half_resources_combination:
        #     no_need_to_buy = enough_resources(resource_combination, card_cost)
        #     if no_need_to_buy:
        #         break
        # if not no_need_to_buy:
        # for i in range(len(card_cost)):
        #     cost = deque(card.cost)
        #     cost.rotate(i)
        #     print(cost)
        #     input()
        #     for east_first in [True, False]:
        #         x = self._find_resource_cards(
        #             list(cost),
        #             west_player.get_cards(),
        #             east_player.get_cards(),
        #             east_first,
        #         )
        #         if x and x not in options:
        #             options.append(x)
        # we now remove any of the options which we cant afford to pay for trades
        # legal_options = []
        # for o in options:
        #     cost = o.coins
        #     for c in o.east_trades:
        #         o.east_cost = self.east_trade_prices[c.resource] * c.count
        #         cost += o.east_cost
        #     for c in o.west_trades:
        #         o.west_cost = self.west_trade_prices[c.resource] * c.count
        #         cost += o.west_cost
        #     if cost <= self.money:
        #         o.set_total(cost)
        #         legal_options.append(o)
        #     Setting the total cost is buggy
        # print sorted(legal_options, key=lambda x: x.total_cost)
        # return sorted(legal_options, key=lambda x: x.total_cost)

    def play_hand(self, hand, west_player, east_player):
        """display all the cards and actions that can be done and return the choice of the player"""
        options = []
        for card in hand:
            # print card.get_name(), self.is_card_in_tableau(card)
            if not self.is_card_in_tableau(card):
                if self.can_build_with_chain(card):
                    options.append((ACTION_PLAYCARD, card))
                elif self.can_buy_card(card, west_player, east_player):
                    options.append((ACTION_PLAYCARD, card))
            options.append((ACTION_DISCARD, card))
            if self.wonder.built_stages < 3:  # FIXMEself.wonder.stages:
                options.append((ACTION_STAGEWONDER, card))
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
            }[x[1].get_colour()],
        )
        for o in options:
            actions = {
                ACTION_PLAYCARD: "Play",
                ACTION_DISCARD: "Discard",
                ACTION_STAGEWONDER: "Stage",
            }
            card = o[1]
            print(
                "[%d]: %s\t%s\t%s"
                % (
                    i,
                    actions[o[0]],
                    card.get_cost_as_string(),
                    card.pretty_print_name(),
                )
            )
            i += 1
        print("-=================-")
        choice = self.personality.make_choice(options)
        # print(options)
        # print(choice)
        # print(options[choice])
        # input(1)
        return options[choice]

    def print_tableau(self):
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
        print("\tWar points: %s" % (self.military))
        print(f"\twest trading prices: {self.west_trade_prices}")
        print(f"\tEast trading prices: {self.east_trade_prices}")
        print(f"\twonder: {self.wonder.side_a}")
        for c in self.get_cards():
            cards[c.get_colour()].append(c)

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

    def set_wonder(self, wonder):
        self.wonder = wonder

    def is_card_in_tableau(self, card):
        return find_card(self.get_cards(), card.get_name()) != None

    def can_build_with_chain(self, card):
        for precard in card.prechains:
            if find_card(self.get_cards(), precard):
                return True
        return False

    def can_buy_card(self, card, west_player, east_player):
        """Return True if a card can be put by the player using his own ressources and the ones present in it's neighbours board."""
        missing = []
        money_spent = 0
        trade_east = 0
        trade_west = 0
        options = []
        resources_left_player = self.resources
        resources_left_west_player = west_player.resources
        resources_left_east_player = east_player.resources
        card_cost = copy.copy(card.cost)
        # card_cost.pop(-1)
        # print(card_cost)
        # print(resources_left_player)
        # print(resources_left_west_player)
        # print(resources_left_east_player)
        # input()
        # print(card.cost)
        # input()

        if len(card_cost) == 0:
            return [
                True,
                0,
            ]

        if len(resources_left_player) > 0:
            i = 0
            while i < len(card_cost):
                j = 0
                while j < len(resources_left_player):
                    if card_cost[i] == resources_left_player[j]:
                        card_cost.pop(i)
                        resources_left_player.pop(j)
                        j = 0
                    else:
                        j += 1
                        i += 1
        # input("fin du tet")

        for i in range(len(card_cost)):
            cost = deque(card.cost)
            cost.rotate(i)
            # print(cost)
            # input()
            for east_first in [True, False]:
                x = self._find_resource_cards(
                    list(cost),
                    west_player.get_cards(),
                    east_player.get_cards(),
                    east_first,
                )
                if x and x not in options:
                    options.append(x)
        # we now remove any of the options which we cant afford to pay for trades
        legal_options = []
        for o in options:
            cost = o.coins
            for c in o.east_trades:
                o.east_cost = self.east_trade_prices[c.resource] * c.count
                cost += o.east_cost
            for c in o.west_trades:
                o.west_cost = self.west_trade_prices[c.resource] * c.count
                cost += o.west_cost
            if cost <= self.money:
                o.set_total(cost)
                legal_options.append(o)
            # Setting the total cost is buggy
        # print sorted(legal_options, key=lambda x: x.total_cost)
        return sorted(legal_options, key=lambda x: x.total_cost)

    def play_card(self, card, west_player, east_player):
        missing = []
        money_spent = 0  # money given to the bank
        trade_east = 0
        trade_west = 0
        resources_left_player = copy.copy(self.resources)
        half_resources_player = copy.copy(self.half_resources)
        yellow_resources_player = copy.copy(self.yellow_resources)
        choice_resources_player = half_resources_player + yellow_resources_player
        resources_left_west_player = copy.copy(west_player.resources)
        resources_left_east_player = copy.copy(east_player.resources)
        card_cost = copy.copy(card.cost)
        options = []
        print(f"card_cost = {card_cost}")
        print(f"self.money = {self.money}")
        input()
        if len(card.cost) == 0:
            return [CardPurchaseOption([], 0, [], [])]

        # permanent resource cost
        if len(resources_left_player) > 0:
            i = 0
            while i < len(card_cost):
                j = 0

                while j < len(resources_left_player):
                    if card_cost[i] == resources_left_player[j]:
                        card_cost.pop(i)
                        resources_left_player.pop(j)
                        j = 0
                    else:
                        j += 1
                i += 1

        size_of_vector = 1
        for i in range(len(choice_resources_player)):
            size_of_vector *= len(choice_resources_player[i])
        print(size_of_vector)
        input()
        all_half_resources_combination = [[] * size_of_vector]
        for choice in choice_resources_player:
            for i in range(len(choice)):
                for j in range(
                    size_of_vector / len(choice) * i,
                    size_of_vector / len(choice) * (i + 1),
                ):
                    all_half_resources_combination[j].append(choice[i])
                    # all_half_resources_combination.append()
        # half resource cost (resources where we have to make a choice which one we use)
        print(all_half_resources_combination)
        input()
        for resource_combination in all_half_resources_combination:
            no_need_to_buy = enough_resources(resource_combination, card_cost)
            if no_need_to_buy:
                break
        # if not no_need_to_buy:

        input(3)
        # if len(half_resources_left_player)>0:
        # 	i = 0
        # 	if len(yellow_resources_left_player) > 0:
        # 		while i < len(card_cost):
        # 			j = 0

        # 			while j < len(resources_left_player):
        # 				if card_cost[i]== resources_left_player[j]:
        # 					card_cost.pop(i)
        # 					resources_left_player.pop(j)
        # 					j = 0
        # 				else:
        # 					j += 1
        # 			i += 1
        # print(f'card_cost = {card_cost}')
        # print(f'self.money = {self.money}')
        # input()
        # for i in range(len(card.cost)):
        # 	cost = deque(card.cost)
        # 	cost.rotate(i)
        # 	for east_first in [True, False]:
        # 		x = self._find_resource_cards(list(cost), west_player.get_cards(), east_player.get_cards(), east_first)
        # 		if x and x not in options:
        # 			options.append(x)
        # we now remove any of the options which we cant afford to pay for trades
        # legal_options = []
        # for o in options:
        # 	cost = o.coins
        # 	for c in o.east_trades:
        # 		o.east_cost = self.east_trade_prices[c.resource] * c.count
        # 		cost += o.east_cost
        # 	for c in o.west_trades:
        # 		o.west_cost = self.west_trade_prices[c.resource] * c.count
        # 		cost += o.west_cost
        # 	if cost <= self.money:
        # 		o.set_total(cost)
        # 		legal_options.append(o)
        # 	Setting the total cost is buggy
        # print sorted(legal_options, key=lambda x: x.total_cost)
        # return sorted(legal_options, key=lambda x: x.total_cost)

    def _find_resource_cards(
        self, needed_resources, west_cards, east_cards, east_first=True
    ):
        def __is_card_used(card, used_cards_array):
            for x in used_cards_array:
                if card == x.card:
                    return True
            return False

        def __check_tableau(r, tableau, used_cards, tradeable_only):
            for c in tableau:  # FIXME: WONDER too
                if not __is_card_used(c, used_cards):
                    is_resource, tradeable = c.is_resource_card()
                    if is_resource and (
                        (not tradeable_only) or (tradeable_only == tradeable)
                    ):
                        count = c.provides_resource(r)
                        if count == 0:
                            continue
                        return (c, count)
            return (None, 0)

        used_cards = []
        coins = 0
        east_trades = []
        west_trades = []
        card_sets = [(self.get_cards(), used_cards, False)]
        if east_first:
            card_sets += [
                (east_cards, east_trades, True),
                (west_cards, west_trades, True),
            ]
        else:
            card_sets += [
                (west_cards, west_trades, True),
                (east_cards, east_trades, True),
            ]

        while len(needed_resources):
            r = needed_resources[0]
            found = False
            if r == RESOURCE_MONEY:
                coins += 1
                needed_resources.remove(r)
                continue
            for cards, used, tradeable_only in card_sets:
                card, count = __check_tableau(r, cards, used, tradeable_only)
                if card and count > 0:
                    found = True
                    needed_count = 0
                    for i in range(0, count):
                        if r not in needed_resources:
                            break
                        needed_count += 1
                        needed_resources.remove(r)
                    used.append(CardPurchaseUse(card, r, needed_count))
                    break
            if not found:
                return None
        return CardPurchaseOption(used_cards, coins, west_trades, east_trades)


class CardPurchaseUse:
    def __init__(self, card, resource, count):
        self.card = card
        self.resource = resource
        self.count = count

    def __eq__(self, other):
        return (
            self.resource == other.resource
            and self.count == other.count
            and self.card.get_name() == other.card.get_name()
        )

    def __repr__(self):
        if len(self.card.get_info()) == 1:
            return "%s" % (self.card)
        return "%s -> %s * %d" % (self.card, self.resource, self.count)


class CardPurchaseOption:
    def __init__(self, card, cost_to_the_bank, west_cost, east_cost):
        self.card = card
        self.cost_to_the_bank = cost_to_the_bank
        self.east_cost = east_cost
        self.west_cost = west_cost
        self.total_cost = self.east_cost + self.west_cost + cost_to_the_bank

    def set_total(self, cost):
        self.total_cost = cost

    def __eq__(self, other):
        if self.coins != other.coins:
            return False
        for us, them in [
            (self.cards, other.cards),
            (self.west_trades, other.west_trades),
            (self.east_trades, other.east_trades),
        ]:
            if len(us) != len(them):
                return False
            for x in us:
                if x not in them:
                    return False

        return True

    def __repr__(self):
        return "{ (total: $%d)\n\t%s\n\t$%d\n\tWEST:%s\n\tEAST:%s\n}" % (
            self.total_cost,
            self.cards,
            self.coins,
            self.west_trades,
            self.east_trades,
        )
