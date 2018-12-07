#!/usr/bin/env python
import string

JOB_DURATION = {i: ord(i) - ord('A') + 1 for i in string.ascii_uppercase}

inputs = """<paste inputs here>""".split('\n')

test_inputs = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split('\n')


input_steps = [(i[5], i[36]) for i in inputs]
test_input_steps = [(i[5], i[36]) for i in test_inputs]
workers = 5
test_workers = 2


def sort_steps(steps):
    """Sort the steps into a form
    {'A': ['B', 'D', 'F']}
    where B, D, and F are the steps A needs to be complete before it can start
    """
    step_dict = {}
    for dependency, step in steps:
        try:
            step_dict[step].append(dependency)
        except KeyError:
            step_dict[step] = [dependency]
        if dependency not in step_dict:
            step_dict[dependency] = []
    return step_dict


def workers_done(active_workers, time_index, test=False):
    """Get a set of all workers who are done"""
    finished = set()
    for index, job in enumerate(active_workers):
        if not job:
            continue
        job_letter, start_time = job
        finish = start_time + JOB_DURATION[job_letter]
        if not test:
            finish += 60
        if time_index >= finish:
            finished.add(index)
    return finished


def get_next_job(job_dict, jobs_done, jobs_in_progress):
    """Get the next job from job_dict whose dependencies are met"""
    for char, dependencies in sorted(job_dict.items()):
        if char in jobs_done | jobs_in_progress:
            continue
        if set(dependencies).issubset(set(jobs_done)):
            return char


def order_steps(sorted_steps):
    """Order steps as if they have zero time to work"""
    # start with steps that have no dependencies
    step_order = list(
        sorted(key for key, val in sorted_steps.items() if not val))
    original_steps = set(sorted_steps)
    steps_seen = set(step_order)
    print('start', step_order)
    # then iterate over each time
    while original_steps != steps_seen:
        next_steps = list(
            sorted(
                key for key, val in sorted_steps.items()
                if set(val).issubset(steps_seen)
                and key not in step_order
            )
        )[:1]
        if not next_steps:
            if original_steps == steps_seen:
                continue
            raise ValueError(
                f'Nothing to do! {original_steps.difference(steps_seen)}')
        steps_seen |= set(next_steps)
        step_order += next_steps
    return step_order


def work_jobs(job_dict, worker_count, test=False):
    time_index = 0
    workers = [None] * worker_count
    # make a copy of the list
    jobs_done = set()
    jobs_to_do = set(job_dict.keys())
    while jobs_to_do != jobs_done:
        # first, iterate over the idle workers and see if there's work
        # available
        for worker_number, active_job in enumerate(workers):
            if not active_job:
                next_job = get_next_job(
                    job_dict, jobs_done,
                    jobs_in_progress=set(i[0] for i in workers if i),
                )
                if next_job:
                    workers[worker_number] = (next_job, time_index)
                    print(
                        'worker', worker_number, 'started',
                        workers[worker_number][0], 'at', time_index)
        # next, who will finish at the START of next turn?
        # because we can have single-second jobs ('A'), we need to do this
        # at the end of the turn
        finished = workers_done(workers, time_index + 1, test)
        for worker_number in finished:
            # but mark them done at the end of the current turn
            print('marking', worker_number, 'done at', time_index)
            # save the job to the set of jobs done
            jobs_done.add(workers[worker_number][0])
            # and mark idle
            workers[worker_number] = None
        time_index += 1
    while any(workers):
        finished = workers_done(workers, time_index, test)
        for worker_number in finished:
            print('marking', worker_number, 'done at', time_index)
            workers[worker_number] = None
        time_index += 1
    # we don't have to worry about off-by-one because the problem wants the
    # time they'll all be idle
    return time_index


if __name__ == '__main__':
    # first, get our dict of first-level dependencies
    sorted_steps = sort_steps(input_steps)
    # then we need to order them for the part 1 solution as if all jobs
    # take zero time
    ordered_steps = order_steps(sorted_steps)
    # take a break and make sure logic is sane with the test input
    assert order_steps(sort_steps(test_input_steps)) == [
        'C', 'A', 'B', 'D', 'F', 'E']
    assert workers_done([('A', 0), ('C', 0)], 1, True) == {0}
    assert work_jobs(sort_steps(test_input_steps), test_workers, True) == 15
    print('Day 7, part 1 solution:', ''.join(ordered_steps))
    # Because time is a factor, we have to go back to the dict of dependencies
    # and work from there
    print('Day 7, part 2 solution:', work_jobs(sorted_steps, workers, False))
