"""This is the "nester.py" module, and it provides one function called print_list_items()
 which prints lists that may or may not include nested lists."""
import sys


def print_list_items(the_list, indent=False, level=0, fh=sys.stdout):
    """This function takes a positional arguments called "the_list","indent" and "level", 'the_list' is
any Python list (of - possibly - nested lists). Each data item in the
provided list is (recursively) printed to the screen on it's own line.
A second argument 'indent' is set to default value 'False', which means indentation or tab-stops are not required
by-default. If user wants to add indentation while printing the nested list it should be set to 'True'.
A Third argument 'level' is used to insert required number of tab_stops when nested list is encountered.
Fourth argument 'fh' is used to specify where the output of this function should write (place to write your
data to), a default value of this argument is sys.stdout so that it continues to write to the screen if no file object
is specified when the function is invoked."""

    for each_item in the_list:
        if isinstance(each_item, list):
            """Each time you process a nested list, you need to increase the value of level by 1 so that tab spaces gets  
            added before printing the list items. Simply increment the value of level 1, 
            each time you recursively invoke the function."""
            print_list_items(each_item, indent, level+1, fh)
        else:
            """ data will be printed in a file with file object print_data_to"""
            if indent:
                """If indent=True, print the tab-stops. by-default indent is set to False"""
                #  for tab_stops in range(level):
                #    print("\t", end='', file=print_data_to)
                """Above for statement can also be written as..."""
                print("\t"*level, end='', file=fh)
            print(each_item, file=fh)

