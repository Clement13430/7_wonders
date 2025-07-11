"""All the function used to set up the game at the begining."""

from wonders import Wonder

from cards import Card


def read_cards_file(filename: str) -> list[Card]:
    """Return a 1D list of all the cards from a file."""
    cards = []
    with open(filename) as f:
        content = f.readlines()
        for line in content:
            if line.startswith("#"):
                continue
            values = line.split(",")
            if len(values) != 8:
                continue
            age = int(values[0].strip())
            players = int(values[1].strip())
            name = values[2].strip()
            colour = values[3].strip()
            cost = values[4].strip()
            prebuilt = values[5].strip()
            postbuilt = values[6].strip()
            effect = values[7].strip()
            c = Card(age, players, name, colour, cost, prebuilt, postbuilt, effect)
            if c:
                cards.append(c)
    print("Loaded %d cards" % (len(cards)))
    return cards


def read_wonders_file(filename: str) -> list[Wonder]:
    """Build a list of all the possible wonders."""
    wonders = []

    with open(filename) as f:
        content = f.readlines()
        for line in content:
            if line.startswith("#"):
                continue
            values = line.split(",")
            if len(values) < 5:
                continue

            w = Wonder(values[0], values[1], values[2:])
            wonders.append(w)
    print("Loaded %d wonders" % (len(wonders)))
    return wonders
