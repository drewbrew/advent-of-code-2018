#!/usr/bin/env python

test_inputs = [
    int(i) for i in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split(' ')]
real_source = """<paste inputs here>"""
real_inputs = [int(i) for i in real_source.split(' ')]

# LOGIC:
# go depth first
# process first node: does it have kids?
# if so, process the sub-list as a node list (recursion)!
# if not, process the metadata entries (if any) and return
# (metadata_total, remaining list)


def parse_node_list(node_list):
    """convert a node into metadata sum, remaining list"""
    number_of_children = node_list.pop(0)
    metadata_entries = node_list.pop(0)
    metadata_total = 0
    # make a copy of the list so we don't disturb the caller's version
    remaining_list = node_list[:]
    while number_of_children > 0:
        metadata_from_kid, remaining_list = parse_node_list(remaining_list)
        metadata_total += metadata_from_kid
        number_of_children -= 1
    while metadata_entries > 0:
        # we should just have metadata remaining. Pop it
        metadata_total += remaining_list.pop(0)
        metadata_entries -= 1
    return metadata_total, remaining_list


def calc_node_value(node_list):
    """count node value for a node"""
    # Yeah, I don't like the amount of duplicated code either, but I wasn't
    # going for long-term maintainability here.
    number_of_children = node_list.pop(0)
    children_processed = 0
    metadata_entries = node_list.pop(0)
    metadata_total = 0
    remaining_list = node_list[:]
    if number_of_children == 0:
        while metadata_entries > 0:
            # we should just have metadata remaining. Pop it
            metadata_total += remaining_list.pop(0)
            metadata_entries -= 1
        return metadata_total, remaining_list
    # use a dict rather than a list so we don't have to worry about off-by-one
    # errors. It's not quite as memory-efficient, but it gets the job done
    # for this puzzle case.
    child_metadata = {}
    while number_of_children > 0:
        children_processed += 1
        metadata_from_kid, remaining_list = calc_node_value(remaining_list)
        child_metadata[children_processed] = metadata_from_kid
        number_of_children -= 1
    while metadata_entries > 0:
        metadata_value = remaining_list.pop(0)
        try:
            # in part 1 we added this value to a running total
            # whereas in this case, we need to look up the referenced child's
            # node value (which is the sum of metadata *if* it has no children
            # but is otherwise the sum of referenced children's metadata)
            metadata_total += child_metadata[metadata_value]
        except KeyError:
            # child doesn't exist. Don't care
            pass
        metadata_entries -= 1

    # pass whatever data we haven't parsed back to the caller, which can decide
    # whether that data is another node or just metadata
    return metadata_total, remaining_list


if __name__ == '__main__':
    # because each function returns a tuple and the solution only cares about
    # the total, we can ignore the second part, which is guaranteed to be an
    # empty list
    parsed_test = parse_node_list(test_inputs[:])
    assert parsed_test[0] == 138, parsed_test
    test_value = calc_node_value(test_inputs)
    assert test_value[0] == 66, test_value
    print('Day 8, part 1 solution', parse_node_list(real_inputs[:])[0])
    print('Day 8, part 2 solution', calc_node_value(real_inputs)[0])
