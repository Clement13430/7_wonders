"""The Card class containing information about the cards and how we define them."""

from common import (
    ALL_RESOURCES,
    CARDS_BLUE,
    CARDS_BROWN,
    CARDS_GREEN,
    CARDS_GREY,
    CARDS_PURPLE,
    CARDS_RED,
    CARDS_YELLOW,
)


class Card:
    def __init__(self, age, players, name, colour, cost, prebuilt, postbuilt, effect):
        """Create a new card from all the information we got."""
        self.name = name
        self.age = age
        self.players = players
        self.prechains = []
        self.postchains = []
        self.colour = colour

        self.cost = []
        for r in cost:
            if r in ALL_RESOURCES:
                self.cost.append(r)  # ['S', 'W', 'W']
        self.effect = effect

    def __repr__(self) -> str:
        """Display all the information about a card."""
        res = f"name = {self.name} | "
        res += f"age = {self.age} | "
        res += f"players = {self.players} | "
        res += f"prechains = {self.prechains} | "
        res += f"postchains = {self.postchains} | "
        res += f"colour = {self.colour} | "
        res += f"cost = {self.cost} | "
        # return "%s (%s) -> %s" % (self.name, self.get_colour(), self.get_info())
        return res

    def get_cost_as_string(self):
        out = ""
        for r in self.cost:
            out += r
        return out

    def is_resource_card(self) -> bool:  # generally brown/grey and some yellow
        """Check if a card give some resource."""
        if "+resource" in self.effect or self.colour == ("grey" or "brown"):
            return True
        return False

    def is_science_card(self) -> bool:  # generally green
        """Check if a card give some science (T, G, C) bonus."""
        if self.colour == "green" or "+science" in self.effect:
            return True
        return False

    def is_war_card(self) -> bool:  # generally red
        """Check if a card gives shields."""
        if self.colour == "red":
            return True
        return False

    def get_ascii_colour(self) -> str:
        """Give a ascii number to every colour in order to display the cards."""
        return {
            CARDS_BROWN: "\033[33m",
            CARDS_GREY: "\033[37m",
            CARDS_RED: "\033[31m",
            CARDS_GREEN: "\033[92m",
            CARDS_YELLOW: "\033[1;33m",
            CARDS_BLUE: "\033[34m",
            CARDS_PURPLE: "\033[35m",
        }[self.colour]

    def pretty_print_name(self, with_info=True) -> str:
        """Display the name of a card with the corresponding colour."""

        if with_info:
            info = " %s" % (self.effect)
        else:
            info = ""
        return "%s%s%s%s" % (self.get_ascii_colour(), self.name, info, "\033[0m")

