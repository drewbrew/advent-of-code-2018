#!/usr/bin/env python
from collections import deque
# (players, marbles, expected_result)
test_inputs = """9 players; last marble is worth 25 points: high score is 32
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305"""

initial_result = [
    0, 16, 8, 17, 4, 18, 19, 2, 24, 20, 25, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3,
    14, 7, 15]

real_input = """476 players; last marble is worth 71657 points"""

test_lines = [i.split(' ') for i in test_inputs.split('\n')]
test_inputs = []
for line in test_lines:
    if not line:
        continue
    test_inputs.append((int(line[0]), int(line[6]), int(line[-1])))
test_tuples = [
    (int(line[0]), int(line[6]), int(line[-1]))
    for line in test_lines if line
]
split_input = real_input.split(' ')
real_players = int(split_input[0])
real_marbles = int(split_input[6])


def place_marble(current_marble_value, existing_score_line):
    if current_marble_value % 23 == 0:
        # get the value 7 back
        existing_score_line.rotate(7)
        score_earned = current_marble_value + existing_score_line.pop()
        existing_score_line.rotate(-1)
        return score_earned
    # put it at the end of the line and return no points scored
    existing_score_line.rotate(-1)
    existing_score_line.append(current_marble_value)
    return 0


def play_game(game_players, game_marbles):
    score = deque([0])
    scores = [0] * game_players
    for marble in range(1, game_marbles + 1):
        score_earned = place_marble(marble, score)
        scores[marble % game_players] += score_earned
    return scores


if __name__ == '__main__':
    for players, marbles, expected_result in test_tuples:
        scores = play_game(players, marbles)
        assert max(scores) == expected_result, (
            scores, expected_result, players)
    print('tests passed')
    scores = play_game(real_players, real_marbles)
    print('Day 9, part 1 solution:', max(scores))
    scores = play_game(real_players, real_marbles * 100)
    print('Day 9, part 2 solution:', max(scores))
