#!/usr/bin/env python

import datetime

source = """<paste inputs here>""".split('\n')

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M'


def parse_input(source):
    """Convert input into a sorted list of (timestamp, event)"""
    result = []
    for line in source:
        raw_timestamp, event = [i.strip() for i in line.split(']')]
        # trim the leading [
        timestamp = datetime.datetime.strptime(
            raw_timestamp[1:], TIMESTAMP_FORMAT)
        result.append((timestamp, event))
    # and sort by timestamp
    return sorted(result)


def parse_awake_asleep(event_list):
    """Parse the event list to determine when each guard is awake/asleep for
    a given day"""
    guards = {}
    last_guard = None
    last_timestamp = None
    last_state = None
    for timestamp, event in event_list:
        if event.startswith('Guard #'):
            # Guard #x begins shift
            last_guard = int(event.split(' ')[1][1:])
            continue
        if last_guard is None:
            raise ValueError(
                'Unknown guard! Event %s, timestamp %s' % (event, timestamp))
        try:
            guard_calendar = guards[last_guard]
        except KeyError:
            guards[last_guard] = {}
            guard_calendar = guards[last_guard]
        # first, just log the events in order
        try:
            today = guard_calendar[(timestamp.month, timestamp.day)]
        except KeyError:
            guard_calendar[(timestamp.month, timestamp.day)] = {}
            today = guard_calendar[(timestamp.month, timestamp.day)]
        # event is either 'wakes up' or 'falls asleep'
        # just in case of whitespace, use `in` instead of equality
        state = 'wakes up' in event
        today[timestamp.minute] = state
    # now go through and convert them into a list of minutes using booleans
    # to represent awake/asleep
    awake_asleep = {
        i: {} for i in guards
    }
    for guard, calendar in guards.items():
        for (month, day), event_dict in calendar.items():
            last_state = None
            last_time = None
            today = {}
            # NOTE: if you're running this on python < 3.7[1], this *WILL* fail
            # because dict insertion order is not preserved
            # [1] This will work for CPython 3.6 because insertion order
            # preservation was added as an implementation detail, but other
            # implementations of Python 3.6 will fail. Guido mandated that
            # insertion order is preserved in Python 3.7 for all
            # implementations.
            for minute, event in event_dict.items():
                if last_state is None:
                    # assume the state is inverted for the start of the hour
                    # so if the first event is 'wakes up', then the guard
                    # was asleep at the start of the shift (and is probably
                    # named Homer Jay Simpson)
                    last_state = not event
                    last_time = 0
                # mark everything from the previous timestamp up to the
                # previous minute with the prior state
                for timestamp in range(last_time, minute):
                    today[timestamp] = last_state
                last_time = minute
                last_state = event
            else:
                # use this to fill in the rest of the hour
                for timestamp in range(last_time, 60):
                    today[timestamp] = last_state
            assert len(today) == 60, today
            awake_asleep[guard][(month, day)] = today
    return awake_asleep


def max_asleep_time(guards_awake_asleep):
    asleep_time = {i: 0 for i in guards_awake_asleep}
    for guard, calendar in guards_awake_asleep.items():
        asleep_time[guard] = sum(
            sum(not event for event in event_dict.values())
            for (month, day), event_dict in calendar.items()
        )
    return sorted(
        ((guard_number, time) for guard_number, time in asleep_time.items()),
        key=lambda k: k[1],
        reverse=True,
    )[0]


def minute_most_asleep(guards_awake_asleep, guard_number):
    """Calculate on which minute the guard was most often asleep"""
    calendar = guards_awake_asleep[guard_number]
    times_asleep = [0] * 60
    for dummy, events in calendar.items():
        for minute, event in events.items():
            if not event:
                times_asleep[minute] += 1
    most_times_asleep = max(times_asleep)
    minute_asleep = times_asleep.index(most_times_asleep)
    return minute_asleep


def guard_most_frequently_asleep_on_same_minute(guards_awake_asleep):
    """Calculate which guard is asleep the most on the same minute"""
    result = {}
    for guard, calendar in guards_awake_asleep.items():
        guard_minutes = {i: 0 for i in range(60)}
        for (month, day), event_dict in calendar.items():
            for minute, state in event_dict.items():
                if not state:
                    guard_minutes[minute] += 1
        # now we've gone through the calendar, so figure out which minute has
        # the most
        max_asleep = sorted(
            guard_minutes.items(), key=lambda k: k[1], reverse=True)[0]
        result[guard] = max_asleep
    # so result is of the form {guard number: (minute, times asleep)}
    # sort by times asleep, descending to get the right result
    minutes = sorted(result.items(), key=lambda k: k[1][1], reverse=True)
    return minutes[0]


if __name__ == '__main__':
    events = parse_input(source)
    parsed = parse_awake_asleep(events)
    guard_number, time_asleep = max_asleep_time(parsed)
    min_most_asleep = minute_most_asleep(parsed, guard_number)
    print(
        f'Day 4, part 1 solution: Guard {guard_number} (asleep {time_asleep} '
        f'min total) most likely asleep at minute {min_most_asleep}, so '
        f'solution is {min_most_asleep * guard_number}'
    )
    guard_number, (minute_most_often_asleep, times_asleep) = \
        guard_most_frequently_asleep_on_same_minute(parsed)
    print(f'Day 4, part 2 solution: {guard_number * minute_most_often_asleep}')
