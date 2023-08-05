"""
This is the "vscy_nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists.
"""
def print_lol(the_list):
    """
    This function takes one positional argument called "the_list", which is
    any Python list (of - possibly - nested lists). Each data item in the
    provided list is (recursively) printed to the screen on it's own line.
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

if __name__ == '__main__':
    movies = [
        'The Holy Grail', 1975, 'Terry Jones & Terry Gilliam', 91,
        [
            'Garham Chapman',
            [
                'Michael Palin',
                'John Cleese',
                'Terry Gilliam',
                'Eric Idle',
                'Terry Jones'
            ]
        ]
    ]
    print_lol(movies)
