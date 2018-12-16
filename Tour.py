
from ConsoleController import ConsoleController
from GUIController import GUIController
from TOAHModel import TOAHModel

import time
NUM_CHEESES = 3


def _find_i(num_cheese):
    '''
    (int) -> int
    Find the optimal value of variable, i, which determines how much cheese
    should be left over to move from the origin stool to the destination stool
    after moving num_cheese - i to a temporary stool.
    REQ: num_cheese >= 2
    '''
    # The formula to find i comes from the summation of k, where k is some
    # real number; i(i+1)/2 = num_cheese, which was found from the formula
    # to calculate the amount of steps required to solve TOAH with 4 stools
    i = (((8*num_cheese+1)**.5)-1)/2
    # Round down the value to the nearest integer and return
    return int(i)


def three_stool_hanoi(model, num_cheese, stl0, stl1, stl2, ani):
    '''
    (TOAHModel, int, int, int, int) -> NoneType
    Solve the Tower of Hanoi for 3 stools, given num_cheese cheese's.
    REQ: Atleast 1 cheese in the game
    '''
    # Base Case
    if (num_cheese == 1):
        # if there is only 1 cheese, move it to the destination
        model.move(stl0, stl2)
        # if animation option is true, then print the current model
        if (ani is True):
            print(model)
    # Recursive Decomposition
    else:
        # Otherwise, we want to move num - 1 cheese to a temporary stool
        three_stool_hanoi(model, num_cheese - 1, stl0, stl2, stl1, ani)
        # Call the model's move method
        model.move(stl0, stl2)
        # Move the rest to the destination stool
        three_stool_hanoi(model, num_cheese - 1, stl1, stl0, stl2, ani)


def four_stool_hanoi(model, num_cheese, stl0, stl1, stl2, stl3, ani):
    '''
    (TOAHModel, int, int, int, int, int, int) -> NoneType
    Given 4 stools, num_cheese cheese's and an integer i, which will determine
    how much cheese to move at a given step, solve the tower to that all
    the cheese ends up from the first stool to fourth stool.
    NOTE: the variable stl0,stl1,stl2,stl3 are just integers
    REQ: Atleast 1 cheese in the game
    '''
    # Base Case 1:
    if (num_cheese == 1):
        # If there is only 1 cheese, move it to the destination
        model.move(stl0, stl3)
        # if animation option is true, then print the current model
        if (ani is True):
            print(model)
    # Recursive Decomposition:
    else:
        # Find the i value, which differs for each number of cheeses
        i = _find_i(num_cheese)
        # we move n-1 cheese using 4 stools first
        four_stool_hanoi(model, num_cheese - i, stl0, stl3, stl1, stl2, ani)
        # Call the function to move with 3 stools, such that stool 2 is ignored
        # we're now moving i cheeses using 3 stools to the desired stool
        three_stool_hanoi(model, i, stl0, stl1, stl3, ani)
        # now move the rest from the temporary stool to the desired stool
        four_stool_hanoi(model, num_cheese - i, stl2, stl0, stl1, stl3, ani)


def tour_of_four_stools(model: TOAHModel, delay_btw_moves: float=0.5,
                        console_animate: bool=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

       model - a TOAHModel with a tower of cheese on the first stool
                and three other empty stools
       console_animate - whether to use ConsoleController to animate the tour
       delay_btw_moves - time delay between moves in seconds IF
                         console_animate == True
                         no effect if console_animate == False
    """
    # Call helper functions to move the cheese
    # If console_animate is true, print each step
    if (console_animate is True):
        # Pass true in the parameter to print
        four_stool_hanoi(model, model.number_of_cheeses(), 0, 1, 2, 3,
                         True)
    # Otherwise don't print it
    else:
        four_stool_hanoi(model, model.number_of_cheeses(), 0, 1, 2, 3,
                         False)


if __name__ == '__main__':
    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses = 5)

    tour_of_four_stools(four_stools,
                        console_animate=False,
                        delay_btw_moves=0.5)

    print(four_stools.number_of_moves())
