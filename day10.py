#!/usr/bin/env python

from matplotlib import pyplot as plt

test_input = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".split('\n')

real_input = """<paste inputs here>""".split('\n')

test_data = []
for line in test_input:
    pos_str, vel_str = line.split('> ')
    pos_x = int(pos_str[10:12].strip())
    pos_y = int(pos_str[13:].strip())
    vel_y = int(vel_str[-3:-1].strip())
    vel_x = int(vel_str[-7:-5].strip())
    test_data.append([pos_x, pos_y, vel_x, vel_y])

real_data = []
for line in real_input:
    pos_str, vel_str = line.split('> ')
    pos_str = pos_str.split('<')[1]
    str_x, str_y = pos_str.split(', ')
    pos_x = int(str_x.strip())
    pos_y = int(str_y.strip())
    str_x, str_y = vel_str.split('<')[1].split(', ')
    vel_x = int(str_x)
    vel_y = int(str_y[:-1])
    real_data.append([pos_x, pos_y, vel_x, vel_y])


def advance_points(vector_list):
    """Advance points one moment in time"""
    for vector in vector_list:
        vector[0] += vector[2]
        vector[1] += vector[3]


def convergence(vector_list):
    sorted_by_x = list(sorted(i[0] for i in vector_list))
    sorted_by_y = list(sorted(i[1] for i in vector_list))
    x_diff = abs(sorted_by_x[0] - sorted_by_x[-1])
    y_diff = abs(sorted_by_y[0] - sorted_by_y[-1])
    return max(x_diff, y_diff)


def print_points(vector_list):
    sorted_by_x = list(sorted(i[0] for i in vector_list))
    sorted_by_y = list(sorted(i[1] for i in vector_list))
    min_x = sorted_by_x[0]
    min_y = sorted_by_y[0]
    max_x = sorted_by_x[-1]
    max_y = sorted_by_y[-1]
    grid = []
    for dummy in range(max_y - min_y + 1):
        grid.append([' '] * (max_x - min_x + 1))
    assert id(grid[0]) != id(grid[1])
    for x, y, dummy1, dummy2 in vector_list:
        grid[y - min_y][x - min_x] = '*'
    for line in grid:
        print(''.join(line))


def guess_at_message(vector_list, plot=False):
    last_convergence = convergence(vector_list)
    last_points = []
    iterations_increasing = 0
    # just picked a really big number here because 10k didn't work
    for count in range(1, 20001):
        advance_points(vector_list)
        new_convergence = convergence(vector_list)
        if new_convergence < last_convergence:
            last_convergence = new_convergence
            # create copies of each inner list
            last_points = [i[:] for i in vector_list]
        elif new_convergence > last_convergence:
            iterations_increasing += 1
        # IDEA: if we've been increasing convergence for 100 straight
        # turns, odds are we've gone well past the solution.
        # Print our saved solution and hope for the best
        if iterations_increasing >= 100:
            print(
                f'Possible Day 10, Part 1 solution found after '
                f'{count - iterations_increasing} iterations:')
            print_points(last_points)
            if plot:
                print(
                    f'Saving to iteration{count - iterations_increasing}.png')
                plot_points(last_points, count - iterations_increasing)
            break
    return count - iterations_increasing


def plot_points(vector_list, iteration=None):
    figure, axes = plt.subplots()
    # need to invert y to reflect that +y is down on the console but
    # up in the plot
    axes.scatter([i[0] for i in vector_list], [-i[1] for i in vector_list])
    axes.set_xlabel('x')
    axes.set_ylabel('y')
    if iteration is not None:
        axes.set_title(f'Iteration #{iteration}')
    axes.grid(True)
    axes.set_aspect('equal', 'datalim')
    plt.savefig(f'iteration{iteration}.png' if iteration else 'plot.png')


if __name__ == '__main__':
    print('running tests')
    test_result = guess_at_message(test_data, True)
    assert test_result == 3
    print('tests passed')
    real_result = guess_at_message(real_data, True)
    print('Day 10, part 2 solution:', real_result)
