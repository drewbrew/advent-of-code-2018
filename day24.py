#!/usr/bin/env python
from dataclasses import dataclass
import enum
from copy import deepcopy
from itertools import count
from typing import Set
import re


class System(enum.Enum):
    IMMUNE = enum.auto()
    INFECTION = enum.auto()


@dataclass
class Group:
    units: int
    hit_points: int
    immunities: Set
    weaknesses: Set
    damage_type: str
    attack_points: int
    initiative: int
    system: System

    @property
    def effective_power(self):
        return self.units * self.attack_points

    @property
    def sort_order(self):
        return self.effective_power, self.initiative

    def __str__(self):
        return f'{self.units} units, {self.hit_points} HP, ' \
            f'{self.initiative} initiative'


TEST_INPUT = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""  # noqa


REAL_INPUT = """<paste inputs here>"""  # noqa


def parse_input(puzzle_input):
    immune, infection = puzzle_input.split("\n\n")
    REGEX = re.compile(
        r"(\d+) units each with (\d+) hit points (\([^)]*\) )?with an attack"
        r" that does (\d+) (\w+) damage at initiative (\d+)")
    immune_groups = []
    infection_groups = []
    for system in (System.IMMUNE, System.INFECTION):
        current = immune if system == System.IMMUNE else infection
        for line in current.split('\n')[1:]:
            s = REGEX.match(line)
            units, hit_points, extra, attack_points, damage_type, \
                initiative = s.groups()
            immunities = []
            weaknesses = []
            if extra:
                extra = extra.rstrip(" )").lstrip("(")
                for s in extra.split("; "):
                    if s.startswith("weak to "):
                        weaknesses = s[len("weak to "):].split(", ")
                    elif s.startswith("immune to "):
                        immunities = s[len("immune to "):].split(", ")
                    else:
                        assert False
            group = Group(
                system=system,
                hit_points=int(hit_points),
                weaknesses=set(weaknesses),
                immunities=set(immunities),
                attack_points=int(attack_points),
                damage_type=damage_type,
                initiative=int(initiative),
                units=int(units),
            )
            if current == immune:
                immune_groups.append(group)
            else:
                infection_groups.append(group)
    return immune_groups, infection_groups


def target_selection(army, opposing_army):

    def sort_function(group):
        return group.sort_order

    sorted_army = sorted(army, key=sort_function, reverse=True)

    choices = {}
    for group in sorted_army:
        army_index = army.index(group)
        if group.units <= 0:
            choices[army_index] = None
            continue
        potential_targets = [
            (index, i) for index, i in enumerate(opposing_army)
            if index not in choices.values() and i.units > 0
        ]
        selected_target = None
        selected_index = None
        best_damage = 0
        for target_index, target in potential_targets:
            damage_multiplier = 1
            if group.damage_type in target.immunities:
                # rejected
                continue
            if group.damage_type in target.weaknesses:
                damage_multiplier = 2
            effective_damage = group.effective_power * damage_multiplier
            if effective_damage > best_damage:
                selected_target = target
                selected_index = target_index
                best_damage = effective_damage
            elif effective_damage == best_damage:
                if target.sort_order > selected_target.sort_order:
                    selected_target = target
                    selected_index = target_index
        choices[army_index] = selected_index
    return choices


def attack(attacking_army, defending_army, target_selections):
    for index, army in enumerate(attacking_army):
        target = target_selections.get(index)
        if target is None:
            continue
        damage_multiplier = 1
        target_army = defending_army[target]
        if army.damage_type in target_army.weaknesses:
            damage_multiplier = 2
        effective_damage = army.effective_power * damage_multiplier
        killed, remaining_damage = divmod(
            effective_damage, target_army.hit_points)
        target_army.units -= killed
        if target_army.units < 0:
            target_army.units = 0


def wage_war(infection_army, immune_army):
    turns = 0
    while any(i.units > 0 for i in infection_army) and any(
            i.units > 0 for i in immune_army):
        turns += 1
        before_totals = sum(i.units for i in infection_army), sum(
            i.units for i in immune_army
        )
        immune_targets = target_selection(immune_army, infection_army)
        infection_targets = target_selection(infection_army, immune_army)
        immune_index = None
        infection_index = None
        attack_order = list(sorted(
            (i for i in immune_army + infection_army if i.units > 0),
            key=lambda k: k.initiative, reverse=True,
        ))
        for i in attack_order:
            immune_index = None
            infection_index = None
            target_selections = {}
            arg1 = None
            arg2 = None
            try:
                immune_index = immune_army.index(i)
            except ValueError:
                infection_index = infection_army.index(i)
                target_selections[infection_index] = infection_targets[
                    infection_index]
                arg2 = immune_army
                arg1 = infection_army
            else:
                target_selections[immune_index] = immune_targets[immune_index]
                arg1 = immune_army
                arg2 = infection_army
            attack(arg1, arg2, target_selections)
        after_totals = sum(i.units for i in infection_army), sum(
            i.units for i in immune_army
        )
        if before_totals == after_totals:
            # neither side has enough power to do any damage.
            # Call it a stalemate.
            return


def part_two(puzzle_input):
    counter = count(start=1) if puzzle_input == TEST_INPUT else \
        count(start=1)
    for boost in counter:
        immune, infection = parse_input(puzzle_input)
        for i in immune:
            i.attack_points += boost
        wage_war(infection, immune)
        if sum(i.units for i in immune) != 0 and sum(
                i.units for i in infection) == 0:
            return sum(i.units for i in immune)


if __name__ == '__main__':
    test_immune, test_infection = parse_input(TEST_INPUT)
    test_immune_targets = target_selection(test_immune, test_infection)
    assert test_immune_targets == {0: 1, 1: 0}, test_immune_targets
    test_infection_targets = target_selection(test_infection, test_immune)
    assert test_infection_targets == {0: 0, 1: 1}, test_infection_targets
    wage_war(test_infection, test_immune)
    assert sum(i.units for i in test_infection) == 5216, test_infection
    assert sum(i.units for i in test_immune) == 0, test_immune
    test_part_two = part_two(TEST_INPUT)
    assert test_part_two == 51, test_part_two
    print('tests passed')
    immune_army, infection_army = parse_input(REAL_INPUT)
    wage_war(infection_army, immune_army)
    print(
        f'Part 1: {sum(i.units for i in infection_army)} infection, '
        f'{sum(i.units for i in immune_army)} immune',
    )
    part_two_result = part_two(REAL_INPUT)
    print(f'Part 2: {part_two_result}')
