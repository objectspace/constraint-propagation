rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


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
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


grid = '5.9.2..1.4...56...8..9.3..5.87..25..654....82..15684971.82.5...7..68...3.4..7.8..'
print(len(grid))

values = grid_values(grid)
values['D1'] = '39'
values['F1'] = '23'
values['F2'] = '23'



display(values)

twins_dict = {}

def any_in(a, b):
    return any(i in b for i in a)

for key, value in values.items():
    if len(value) == 2:
        twins_dict.setdefault(value, []).append(key)

for no, _boxes in twins_dict.items():
    if len(_boxes) >= 2:
        twins = [box for box in _boxes if any_in(peers[box], _boxes)]
        if len(twins) == 2:
            for peer in set(peers[twins[0]]).intersection(peers[twins[1]]):
                for digit in no:
                    values[peer] = values[peer].replace(digit, '')

display(values)

