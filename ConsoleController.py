"""
ConsoleController: User interface for manually solving Anne Hoy's problems
from the console.

move: Apply one move to the given model, and print any error message
to the console.
"""

from TOAHModel import TOAHModel, Cheese, IllegalMoveError
import tkinter as TI
import time


def move(model: TOAHModel, origin: int, dest: int):
    '''
    (TOAHModel, int, int) -> NoneType
    Module method to apply one move to the given model, and print any
    error message to the console.

    model - the TOAHModel that you want to modify
    origin - the stool number (indexing from 0!) of the cheese you want
             to move
    dest - the stool number that you want to move the top cheese
            on stool origin onto.
    REQ: 0 <= origin < self._number_of_stools
    REQ: 0 <= dest < self._number_of_stools
    '''
    # Use the TOAHModel's move method to move the cheese
    model.move(origin, dest)


class ConsoleController:

    def __init__(self: 'ConsoleController',
                 number_of_cheeses: int, number_of_stools: int):
        """
        Initialize a new 'ConsoleController'.

        number_of_cheeses - number of cheese to tower on the first stool,
                            not counting the bottom cheese acting as stool
        number_of_stools - number of stools, to be shown as large cheeses
        """
        # REPRESENTATION INVARIANT
        # self._number_of_cheeses is an integer which represents the number
        # of cheeses in the game
        # self._number_of_stools is an integer which represents the number
        # of stools in the game
        # self._model is a TOAHModel, which represents the game as a whole
        self._number_of_cheeses = number_of_cheeses
        self._number_of_stools = number_of_stools
        self._model = TOAHModel(self._number_of_stools)
        # Fill the first stool with the amount of cheese entered
        self._model.fill_first_stool(self._number_of_cheeses)

    def play_loop(self: 'ConsoleController'):
        '''
        (ConsoleController) -> NoneType
        Console-based game.
        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        '''
        exit = False
        print("Welcome to the TOWER OF ANNE HOY")
        print("To get started, move the top cheese from the first stool.")
        print("To move a cheese from the first stool, enter '1'.")
        print("To move a cheese from the nth stool, enter 'n-1'")
        print("You may only stack smaller cheeses on top of eachother")
        print("To exit the game, type 'END' at any time.")
        # Create a while loop to await user input
        while(exit is False):
            # Get the stool index from the user to move the first cheese
            print("<Enter a stool index to move its' top cheese>")
            origin = input()
            # If the input was "END", then end the game
            if origin == "END":
                exit = True
            # Otherwise continue
            else:
                # Check if the user entered a valid stool index
                if (int(origin) < 0 or
                        int(origin) >= self._model.number_of_stools()):
                    raise IllegalMoveError("Given stool does not exist.")
                # Get the stool index for the destination of the cheese
                print ("<Enter a stool index to place the cheese on>")
                destination = input()
                # Again, check if the user wants to end
                if destination == "END":
                    exit = True
                # If not, then continue the game
                else:
                    # Check if the user entered a valid stool index
                    if (int(destination) < 0 or
                            int(
                            destination) >= self._model.number_of_stools()):
                        raise IllegalMoveError("Given stool does not exit.")
                    # Call the move method
                    move(self._model, int(origin), int(destination))
                    # Print the state of the game
                    print(self._model)


if __name__ == '__main__':
    # Initiate gameplay
    game = ConsoleController(3, 3)
    game.play_loop()
