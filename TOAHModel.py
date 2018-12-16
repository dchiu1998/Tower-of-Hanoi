"""
TOAHModel:  Model a game of Towers of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Towers of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


class TOAHModel:
    """Model a game of Towers Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.  Note that
    large, aged, cheeses at the bottom of each pile serve as stools, and
    these may not be moved!

    fill_first_stool - put an existing model in the standard starting config
    move - move cheese from one stool to another
    add - add a cheese to a stool
    cheese_location - index of the stool that the given cheese is on
    number_of_cheeses - number of cheeses in this game
    number_of_moves - number of moves so far
    number_of_stools - number of stools in this game
    get_move_seq - MoveSequence object that records the moves used so far
    """

    def __init__(self, num_stools):
        '''
        (TOAHModel, int, int) -> NoneType
        Create a TOAHModel to play Tower of Anne Hoy.
        REQ: cheeses > 0 and stools > 0
        '''
        # REPRESENTATION INVARIANT
        # self._number_of_stools is an integer representing the number of
        # stools in the game
        # self._number_of_cheese is an integer representing the number of
        # cheese in the game
        # self._number_of_moves is an integer tracking how many moves have
        # been made in the game
        # self._stools is a list holding lists which act as containers
        # for cheese
        # if len(self._stools) == 3:
        #     then self._number_of_stools == 3 and
        #     there are three stools in the game
        # if len(self._stools[0]) == 4:
        #     then there are 4 cheeses on the first stool (using 0 indexing)
        #     cheese at self._stools[0] has size 4
        #     cheese at self._stools[-1] has size 1
        self._number_of_stools = num_stools
        self._number_of_cheese = 0
        self._number_of_moves = 0
        self._move_seq = MoveSequence([])
        self._stools = []
        # Intitialize the number of requested stools as lists
        for i in range(0, num_stools):
            self._stools.append([])

    def cheese_location(self, cheese):
        '''
        (TOAHModel, Cheese) -> int
        Return the index of the stool the given cheese is on.
        REQ: The cheese exists in the current model
        '''
        result = None
        for i in range(0, self.number_of_stools()):
            if cheese in self._stools[i]:
                result = i
        return result

    def fill_first_stool(self: 'TOAHModel', number_of_cheeses: int):
        """
        (TOAHModel, int) -> NoneType
        Put number_of_cheeses cheeses on the first (i.e. 0-th) stool, in order
        of size, with a cheese of size == number_of_cheeses on bottom and
        a cheese of size == 1 on top.
        REQ: number_of_cheeses > 0
        """
        # Use a for loop to create and add cheeses
        for i in range(0, number_of_cheeses):
            cheese = Cheese(number_of_cheeses - i)
            self._stools[0].append(cheese)
            # Raise cheese count
            self._number_of_cheese += 1

    def add(self, stool_number, cheese):
        '''
        (TOAHModel, int) -> NoneType
        Add a cheese to the stool_number'th stool.
        REQ: Cheese has a size < the current top Cheese on the stool
        '''
        # If the user attempts to add a larger cheese on top, raise an error
        if (self._stools[stool_number] != [] and
                cheese.size >= self._stools[stool_number][-1].size):
            raise IllegalMoveError("Can only stack cheese of smaller sizes.")
        # If the stool does not exist, raise an error
        if (stool_number < 0 or stool_number >= self._number_of_stools):
            raise IllegalMoveError("Invalid stool index.")
        # Add the cheese to the top of the selected stool
        self._stools[stool_number].append(cheese)
        # Raise cheese count
        self._number_of_cheese += 1

    def move(self, curr_stool, dest_stool):
        '''
        (TOAHModel, int, int) -> NoneType
        Move a cheese from curr_stool to dest_stool.
        REQ: The cheese to be moved has size < dest_stool's top cheese
        '''
        # If the user enters a non-existing stool number, raise an error
        if (curr_stool < 0 or dest_stool < 0 or
            curr_stool >= self._number_of_stools or
                dest_stool >= self._number_of_stools):
            raise IllegalMoveError("Invalid stool index.")
        # Increase the amount of moves
        self._number_of_moves += 1
        # If the current stool has no cheese to be moved, raise an error
        if (self._stools[curr_stool] == []):
            raise IllegalMoveError("There is no cheese to be moved.")
        # If the cheese from current is larger or equal in size, raise error
        if (self._stools[dest_stool] != [] and
            self._stools[curr_stool][-1].size >=
                self._stools[dest_stool][-1].size):
            raise IllegalMoveError("Impossible to stack a larger cheese on top.")
        # Move the cheese from curr_stool to dest_stool
        self._stools[dest_stool].append(self._stools[curr_stool].pop())
        # Add it to the move sequence history
        self._move_seq.add_move(curr_stool, dest_stool)

    def number_of_cheeses(self):
        '''
        (TOAHModel) -> int
        Return the amount of cheeses in the current model.
        REQ: None
        '''
        return self._number_of_cheese

    def number_of_moves(self):
        '''
        (TOAHModel) -> int
        Return the amount of moves made so far.
        REQ: None
        '''
        return self._number_of_moves

    def number_of_stools(self):
        '''
        (TOAHModel) -> int
        Return the amount of stools in the game.
        REQ: None
        '''
        return self._number_of_stools

    def top_cheese(self, stool_index):
        '''
        (TOAHModel, int) -> Cheese
        Return the top cheese at the given stool.
        REQ: 0 <= stool_index < number_of_stools
        '''
        # Raise an error if invalid stool index is given
        if (stool_index < 0 or stool_index >= self.number_of_stools()):
            raise IllegalMoveError("Given stool does not exist.")
        return self._stools[stool_index][-1]

    def _cheese_at(self: 'TOAHModel', stool_index,
                   stool_height: int) -> 'Cheese':
        """
        (TOAHModel, int) -> Cheese
        If there are at least stool_height+1 cheeses
        on stool stool_index then return the (stool_height)-th one.
        Otherwise return None.
        REQ: 0 <= stool_index < number_of_stools
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        result = None
        if (stool_index >= 0 and stool_index < self.number_of_stools() and
                stool_height < len(self._stools[stool_index])):
            result = self._stools[stool_index][stool_height]
        return result

    def get_move_seq(self: 'TOAHModel') -> 'MoveSequence':
        '''
        (TOAHModel) -> MoveSequence
        Return out the players' move history.
        REQ: User started the game
        '''
        return self._move_seq

    def __eq__(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        (TOAHModel, TOAHModel) -> bool
        We're saying two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,3)
        >>> m2.move(0,2)
        >>> m2.move(3,2)
        >>> m1 == m2
        True
        REQ: None
        """
        # If the other object is not a TOAHModel, raise an error
        if (type(other) is not TOAHModel):
            raise IllegalMoveError("Must compare 2 TOAHModels.")
        # Return if self is equivalent to the other TOAHModel
        return self == other

    def __str__(self: 'TOAHModel') -> str:
        """
        (TOAHModel) -> str
        Depicts only the current state of the stools and cheese.
        REQ: None
        """
        stool_str = "=" * (2 * (self.number_of_cheeses()) + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.number_of_stools()

        def cheese_str(size: int):
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = cheese_str(int(c.size))
                else:
                    s = cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines


class Cheese:
    def __init__(self: 'Cheese', size: int):
        """
        Initialize a Cheese to diameter size.

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __repr__(self: 'Cheese') -> str:
        """
        Representation of this Cheese
        """
        return "Cheese(" + str(self.size) + ")"

    def __eq__(self: 'Cheese', other: 'Cheese') -> bool:
        """Is self equivalent to other? We say they are if they're the same
        size."""
        return isinstance(other, Cheese) and self.size == other.size


class IllegalMoveError(Exception):
    '''
    An error to be raised when the user attempts to make an invalid move.
    '''
    pass


class MoveSequence(object):
    def __init__(self: 'MoveSequence', moves: list):
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self: 'MoveSequence', i: int):
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self: 'MoveSequence', src_stool: int, dest_stool: int):
        self._moves.append((src_stool, dest_stool))

    def length(self: 'MoveSequence') -> int:
        return len(self._moves)

    def generate_TOAHModel(self: 'MoveSequence', number_of_stools: int,
                           number_of_cheeses: int) -> 'TOAHModel':
        """
        An alternate constructor for a TOAHModel. Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in move_seq.
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model

    def __repr__(self: 'MoveSequence') -> str:
        return "MoveSequence(" + repr(self._moves) + ")"


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
