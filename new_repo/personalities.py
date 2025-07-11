"""File containing the differents personalities that can be used in the game."""


class Personality:
    def __init__(self):
        pass

    def make_choice(self, options):
        pass


class StupidAI(Personality):
    def __init__(self):
        pass

    def make_choice(self, options):
        return 0


class Human(Personality):
    def __init__(self):
        pass

    def make_choice(self, options):
        choice = input("Please enter your choice: \n")
        return int(choice)
        # return int(stdin.readline())
