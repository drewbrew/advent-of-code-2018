#!/usr/bin/env python

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

real_input = """<paste inputs here>"""

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


def place_marble(
        current_marble_value, existing_score_line, index_of_last_marble):
    if current_marble_value % 23 == 0:
        return place_special_marble(
            current_marble_value, existing_score_line, index_of_last_marble)
    if len(existing_score_line) == 1:
        # put it at the end of the line and return no points scored
        existing_score_line.append(current_marble_value)
        return 0, 2
    # placement must be two spots higher than the highest previous marble
    placement = index_of_last_marble + 2
    current_length = len(existing_score_line)
    if placement == current_length:
        existing_score_line.append(current_marble_value)
    elif placement > current_length:
        existing_score_line.insert(1, current_marble_value)
        placement = 1
    else:
        existing_score_line.insert(placement, current_marble_value)
    return 0, placement


def place_special_marble(
        current_marble_value, existing_score_line, index_of_last_marble):
    player_score = current_marble_value
    index_to_pop = (index_of_last_marble - 7) % len(existing_score_line)
    player_score += existing_score_line.pop(index_to_pop)
    return player_score, index_to_pop


if __name__ == '__main__':
    for players, marbles, expected_result in test_tuples:
        score_list = [0] * players
        score_line = [0]
        index_of_last_marble = 0
        for turn in range(1, marbles + 1):
            current_player = turn % len(score_list)
            current_score = score_list[current_player]
            score_earned, index_of_last_marble = place_marble(
                turn, score_line, index_of_last_marble)
            current_score += score_earned
            score_list[current_player] = current_score

        assert max(score_list) == expected_result, (
            score_list, expected_result, players)
        if players == 9:
            assert score_line == initial_result, score_line
    print('tests passed')
    score_list = [0] * real_players
    score_line = [0]
    index_of_last_marble = 0
    for turn in range(1, real_marbles + 1):
        current_player = turn % len(score_list)
        current_score = score_list[current_player]
        score_earned, index_of_last_marble = place_marble(
            turn, score_line, index_of_last_marble)
        current_score += score_earned
        score_list[current_player] = current_score
        if not turn % 1000:
            print(
                f'Turn {turn} complete, current high score {max(score_list)}')
    print('Day 9, part 1 solution:', max(score_list))
    score_list = [0] * real_players
    score_line = [0]
    index_of_last_marble = 0
    for turn in range(1, (real_marbles * 100) + 1):
        current_player = turn % len(score_list)
        current_score = score_list[current_player]
        score_earned, index_of_last_marble = place_marble(
            turn, score_line, index_of_last_marble)
        current_score += score_earned
        score_list[current_player] = current_score
        if not turn % 10000:
            print(f'Turn {turn} complete')
