"""All the functions used to calculate the scores, either at the end of the game or at the end of an age."""

import itertools
import re
from collections import Counter

from common import (
    ALL_COLOURS,
    CARDS_GREEN,
    CARDS_PURPLE,
    CARDS_YELLOW,
    SCIENCE_COMPASS,
    SCIENCE_GEAR,
    SCIENCE_TABLET,
)
from players import Player


def calc_science_score(compass, gear, tablets):
    counts = sorted([compass, gear, tablets], reverse=True)
    total = 0
    for i in range(3):
        total += counts[i] * counts[i]
    return 7 * counts[2] + total


def best_green_symbol_option(compass, gear, tablets, choices):  # WIP
    """Calculate What is the best green symbol to take to maximize the final score of a player."""

    scores = []
    elements = list(range(3))
    combinations = list(itertools.combinations_with_replacement(elements, choices))
    print(combinations)
    for combo in combinations:
        print(combo)
    input()

    # if SCIENCE_COMPASS in choice[0]:
    #     scores.append(find_best_score(compass + 1, gear, tablets, choice[1:]))
    # if SCIENCE_GEAR in choice[0]:
    #     scores.append(find_best_score(compass, gear + 1, tablets, choice[1:]))
    # if SCIENCE_TABLET in choice[0]:
    #     scores.append(find_best_score(compass, gear, tablets + 1, choice[1:]))
    return sorted(scores, key=lambda score: score[1], reverse=True)[0]


def score_science(player):  # WIP
    """Calculate the science score of a player."""

    if player.science_choice == 0:
        score = calc_science_score(
            player.science_symbols[SCIENCE_COMPASS],
            player.science_symbols[SCIENCE_GEAR],
            player.science_symbols[SCIENCE_TABLET],
        )
        # print "%d %d %d -> %d" % (compass, gear, tablets, score)
        return score

    return best_green_symbol_option(
        player.science_symbols[SCIENCE_COMPASS],
        player.science_symbols[SCIENCE_GEAR],
        player.science_symbols[SCIENCE_TABLET],
        player.science_choice,
    )


def score_military(player, west_player, east_player, age):  # WIP
    """Calculate the military score of a player at a timestamp t."""
    if player.shields > west_player.shields:
        west_points = [1, 3, 5][age]
    elif player.shields == west_player.shields:
        west_points = 0
    else:
        west_points = -1

    if player.shields > east_player.shields:
        east_points = [1, 3, 5][age]
    elif player.shields == east_player.shields:
        east_points = 0
    else:
        east_points = -1
    # print "WAR: %s: %d %s %d -> %d\b" % (player.name, my_strength, opponent.name, their_strength, points)
    return (west_points, east_points)


def score_yellow(player: Player, west_player: Player, east_player: Player):
    """Calculate the yellow score of a player at a timestamp t."""
    score = 0
    yellow_card = [c for c in player.get_cards() if c.get_colour() == CARDS_YELLOW]

    for card in yellow_card:
        if re.match("V+{.+} [<v>]+", card.effect) and any(
            colour in card.effect.split("{")[1].split("}")[0] for colour in ALL_COLOURS
        ):
            # print("card colour")
            # input()
            number_of_points = Counter(card.effect.split("{")[0])["V"]
            freq_direction = Counter(card.effect.split("}")[1])
            colours = card.effect.split("{")[1].split("}")[0]
            score += number_of_points * (
                west_player.how_much_colour_card(colours) * freq_direction["<"]
                + player.how_much_colour_card(colours) * freq_direction["v"]
                + east_player.how_much_colour_card(colours) * freq_direction[">"]
            )
        elif re.match("V+{wonder} [<v>]+", card.effect):
            # print("card wonder")
            # input()
            number_of_points = Counter(card.effect.split("{")[0])["V"]
            freq_direction = Counter(card.effect.split("}")[1])
            score += number_of_points * (
                west_player.current_stage_wonder * freq_direction["<"]
                + player.current_stage_wonder * freq_direction["v"]
                + east_player.current_stage_wonder * freq_direction[">"]
            )
    return score


def score_purple(player: Player, west_player: Player, east_player: Player):
    """Calculate the yellow score of a player at a timestamp t."""
    score = 0
    purple_card = [c for c in player.get_cards() if c.get_colour() == CARDS_PURPLE]

    for card in purple_card:
        if re.match("V+{.+} [<v>]+", card.effect) and any(
            colour in card.effect.split("{")[1].split("}")[0] for colour in ALL_COLOURS
        ):
            # print("card colour")
            # input()
            number_of_points = Counter(card.effect.split("{")[0])["V"]
            freq_direction = Counter(card.effect.split("}")[1])
            colours = card.effect.split("{")[1].split("}")[0]
            score += number_of_points * (
                west_player.how_much_colour_card(colours) * freq_direction["<"]
                + player.how_much_colour_card(colours) * freq_direction["v"]
                + east_player.how_much_colour_card(colours) * freq_direction[">"]
            )
        elif re.match("V+{wonder} [<v>]+", card.effect):
            # print("card wonder")
            # input()
            number_of_points = Counter(card.effect.split("{")[0])["V"]
            freq_direction = Counter(card.effect.split("}")[1])
            score += number_of_points * (
                west_player.current_stage_wonder * freq_direction["<"]
                + player.current_stage_wonder * freq_direction["v"]
                + east_player.current_stage_wonder * freq_direction[">"]
            )
