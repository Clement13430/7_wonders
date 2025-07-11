"""All the information about the Wonder class and how we define it."""

from common import ALL_RESOURCES


class Wonder:
    def __init__(self, name: str, freeslot: str, effects: list[str]):
        self.name = name
        self.freeslot = freeslot
        self.side_a, self.side_b = self.build_effects(effects)  # (cost, action)

        self.built_stages = 0
        self.discred_cards = (None, None, None)

    def build_effects(self, effects: list[str]):
        size_side_a = int(effects[0])
        side_a, side_b = [], []

        for stage_num in range(size_side_a):
            resources_needed = []
            for resource in effects[stage_num * 2 + 1]:
                if resource in ALL_RESOURCES:
                    resources_needed.append(resource)
            side_a.append((resources_needed, effects[stage_num * 2 + 2]))

        size_side_b = int(effects[size_side_a * 2 + 1])
        for stage_num in range(size_side_b):
            resources_needed = []

            for resource in effects[size_side_a * 2 + stage_num * 2 + 2]:
                if resource in ALL_RESOURCES:
                    resources_needed.append(resource)
            side_b.append(
                (resources_needed, effects[size_side_a * 2 + 1 + stage_num * 2 + 2])
            )

        return side_a, side_b
