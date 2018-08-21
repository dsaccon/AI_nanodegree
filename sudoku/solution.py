assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
#    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag1_units = [[a[0]+a[1] for a in zip(rows, cols)]]
diag2_units = [[a[0]+a[1] for a in zip(rows, cols[::-1])]]

unitlist = row_units + column_units + square_units + diag1_units + diag2_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
#    """
#    Please use this function to update your values dictionary!
#    Assigns a value to a given box. If it updates the board record it.
#    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
#    """Eliminate values using the naked twins strategy.
#    Args:
#        values(dict): a dictionary of the form {'box_name': '123456789', ...}    
    
    for box in boxes: # Take one box
        if len(values[box]) == 2:
            twins = {}
            # Find the twins for each unit for this box
            twins[0] = [i for i in units[box][0] if values[box] == values[i] and i != box]
            twins[1] = [i for i in units[box][1] if values[box] == values[i] and i != box]
            twins[2] = [i for i in units[box][2] if values[box] == values[i] and i != box]
            if len(units[box]) == 4: # Check for boxes that are part of diagonals
                twins[3] = [i for i in units[box][3] if values[box] == values[i] and i != box]
            if len(units[box]) == 5: # Check for the middle box, which is part of both diagonals
                twins[3] = [i for i in units[box][3] if values[box] == values[i] and i != box]
                twins[4] = [i for i in units[box][4] if values[box] == values[i] and i != box]

            for i in range(0, len(units[box])):
                for unit in units[box][i]: # Go through all boxes in each of the units
                    # Take action only on boxes that have more than one digit, where twins exist in the same unit, and which aren't a twin themselves
                    if len(values[unit]) > 1 and len(twins[i]) > 0 and values[unit] != values[box]:  
                        values[unit] = values[unit].replace(values[box][0], '')
                        values[unit] = values[unit].replace(values[box][1], '')
                    else:  # Make no changes to any digits in this pass
                        pass
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    counter = [1 for box in boxes if len(values[box]) == 1]
    if len(counter) == 81:
        return values

#    Choose one of the unfilled squares with the fewest possibilities
    
    length = min([len(values[box]) for box in boxes if len(values[box]) > 1])
    cur_box = min([box for box in boxes if len(values[box]) == length])

    # Now use recurrence to solve each one of the resulting sudokus, and 
    
    for i in values[cur_box]:
        new_values = values.copy()
        new_values[cur_box] = i
        iter = search(new_values)
        if iter:
            return iter

def solve(grid):
    """
#    Find the solution to a Sudoku grid.
#    Args:
#        grid(string): a string representing a sudoku grid.
#            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

#    Returns:
#        The dictionary representation of the final sudoku grid. False if no solution exists.
#    """
    values = grid_values(grid)
    solution = search(values)
    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
