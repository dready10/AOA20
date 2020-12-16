with open('16input1.txt') as f:
    inputs = [line for line in f.read().split('\n')]
    filters = [line[line.index(': ') + 2:] for line in inputs if ': ' in line]
    my_ticket = [int(x) for x in inputs[inputs.index('your ticket:')+1].split(',')]
    others_tickets = [line for line in inputs[inputs.index('nearby tickets:')+1:]]

    # part 1. i wanted this to be a one-liner, but alas, iterable unpacking isn't legal.
    # this can be a two-liner, but having validity_filters handy in part 2 made things a lot easier.
    # also, substituting validity_filters in line 3 for the expression in line 2 really dings performance.
    # either way, a fun extra challenge.

    # the logic is basically:
    # create a list of all the ranges in the rules
    # create a set of the enumeration of the values in all those ranges
    # sum all the values in others' tickets that aren't in the set of enumerated values
    validity_filters = [range(int(rules.split('-')[0]), int(rules.split('-')[1])+1) for line in filters for rules in line.split(' or ')]
    validity_filters = set([val for rang in validity_filters for val in rang]) 
    print(sum([int(val) for line in others_tickets for val in line.split(',') if int(val) not in validity_filters]))

    # part 2
    # gotta redo some work we were supposed to do in part 1--spit out invalid tickets
    valid_tickets = []
    for ticket in others_tickets:
        ticket = ticket.split(',')
        for val in ticket:
            if int(val) not in validity_filters:
                break
        else:
            valid_tickets.append(ticket)

    # get and parse the ticket fields and field rules that are at the top of the input
    ticket_fields = {}
    for field in inputs[0:inputs.index('your ticket:')-1]:
        field_name = field[0:field.index(':')]
        ticket_fields[field_name] = field[field.index(': ')+2:].split(' or ')
        ticket_fields[field_name] = [range(int(filt.split('-')[0]), int(filt.split('-')[1])+1) for filt in ticket_fields[field_name]]

    # because we're trying to map everything in one column to a field, it's easier to look at this "columnwise"
    transposed_valid_tickets = [[valid_tickets[j][i] for j in range(len(valid_tickets))] for i in range(len(valid_tickets[0]))]

    # check each field / field rule against all the values in a "column" of ticket inputs. if there's an invalid
    # value, then that "column" can't represent that field
    valid_mappings = {}
    for check_field in ticket_fields.keys():
        valid_mappings[check_field] = []
        for i, field in enumerate(transposed_valid_tickets):
            for ticket_val in field: 
                # boy does this 3-nested for make me uncomfortable, but i think this is right.
                # we have to check each (for1) field rule (eg: row: 1-3 or 9-11) against
                # each (for2) value in each (for3) ticket field (eg, 2nd row in ticket)
                ticket_val = int(ticket_val)
                if ticket_val not in ticket_fields[check_field][0] and ticket_val not in ticket_fields[check_field][1]:
                    break
            else:
                valid_mappings[check_field].append(i)

    # now generate the final mapping from the possible mapping. if a field maps to only one "column,"
    # that field must be represented by that column, and no other column can be (so remove them).
    # keep removing already-mapped columns until we get to the final mapping.
    # (assumes that the puzzle input is constructed such that the mapping is unambiguous--ie:
    # that 2 different fields can't be mapped to the same 2 columns, as it'd be undecidable)
    final_mapping = {}
    for i in range(len(ticket_fields.keys())):
        for check_field in ticket_fields.keys():
            if len(valid_mappings[check_field]) == 1:
                final_mapping[check_field] = valid_mappings[check_field][0]
                
                remove_value = valid_mappings[check_field][0]
                for mapping in valid_mappings.keys():
                    if remove_value in valid_mappings[mapping]:
                        valid_mappings[mapping].remove(remove_value)

    # finally, using that mapping, solve part 2.
    part2result = 1
    for mapping in final_mapping.keys():
        if 'departure' in mapping:
            part2result *= my_ticket[final_mapping[mapping]]
    print(part2result)