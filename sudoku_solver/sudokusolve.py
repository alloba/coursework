#These variables are rarely used, to the point that they could be defined each instance, but this helps my sanity
puzzlewidth = 9
puzzleheight = 9
puzzlesize = puzzlewidth * puzzleheight
puzzles = []


def displaypuzzle(puzzlelist):
    displaystring = '---------------------------------\n'
    y = 0
    x = 0
    z = 0
    for i in range(81):
        if x == 0:
            displaystring += '|'

        displaystring += " " + str(puzzlelist[i]) + " "
        x += 1
        y += 1
        z += 1

        if x > 2:
            displaystring += '|'
            x = 0
        if y > 8:
            displaystring += '\n'
            y = 0
        if z > 26:
            displaystring += '---------------------------------\n'
            z = 0
    print(displaystring[:-1]) # get rid of the last character, which is a newline. its just to make it look nicer when printing


def gatherinput(filename):
    """
     take input from a file, with directory specified as a parameter.
     ideally, correct format should be "[num][space][num][space].....[num][newline] * 9"

     can take more than one puzzle from the file
     MAKE SURE each puzzle is separated by ONE blank line ONLY.
    """

    file = open(filename)
    puzzlein = file.read()

    processingpuzzle = puzzlein.split('\n\n')  # get each individual puzzle in the file
    formattedpuzzle = []

    for i in range(len(processingpuzzle)):
        processingpuzzle[i] = processingpuzzle[i].replace('\t', ',').replace('\n', ',').replace(' ', ',').split(',')

    for i in range(len(processingpuzzle)):
        addlist = []
        for cell in processingpuzzle[i]:
                if cell == 0:
                    addlist.append(0)
                else:
                    addlist.append(int(cell))
        formattedpuzzle.append(addlist)

    return formattedpuzzle


def getrowindexes(index):

    """
    given an index, return a list of all indexes in that row.
    """
    row = []
    rowcall = index//puzzlewidth

    for i in range(9):
        row.append(puzzlewidth * rowcall + i)
    return row


def getrowvalues(index, puzzle):
    """
    given an index and a puzzle to work with, return every value that exists on that row in that puzzle
    """
    row = []
    rowcall = index//puzzlewidth

    for i in range(9):
        row.append(puzzle[rowcall * puzzlewidth + i])
    return row


def getcolumnindexes(index):
    column = []
    colcall = index % puzzlewidth

    for i in range(9):
        column.append(colcall + i * puzzlewidth)
    return column


def getcolumnvalues(index, puzzle):
    column = []
    colcall = index % puzzlewidth

    for i in range(9):
        column.append(puzzle[colcall + i * puzzlewidth])
    return column


def getboxindexes(index):
    # a box being the 9 x 9 configuration in puzzles. ninette, square, box, whatever name you want.
    box = []
    boxrow = (index // puzzlewidth) // 3
    boxcolumn = (index % puzzlewidth) // 3

    for i in range(81):
        if (i // puzzlewidth) // 3 == boxrow and (i % puzzlewidth) // 3 == boxcolumn:
            box.append(i)
    return box


def getboxvalues(index, puzzle):
    # what a simple bit of that that i just flat out couldnt come up with.
    # so the bit inside the parenthesis is to get either the row or column.
    # divide each by 3 to deal with having the boxes being 3 by 3

    box = []
    boxrow = (index // puzzlewidth) // 3
    boxcolumn = (index % puzzlewidth) // 3

    for i in range(81):
        if (i // puzzlewidth) // 3 == boxrow and (i % puzzlewidth) // 3 == boxcolumn:
            box.append(puzzle[i])
    return box


def findpossiblevalues(index, puzzle):
        """
        for a given index, in a puzzle,
        find what could possibly go there based on what exists in the row/column/box of the cell
        """
        possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(1,10):
            if i in getboxvalues(index, puzzle) or i in getcolumnvalues(index, puzzle) or i in getrowvalues(index, puzzle):
                possibles.remove(i)
        return possibles


def validatepuzzle(puzzle):
    """
    make sure the puzzle is correct.
    everything filled in, no repeated values (really just no repeated values accomplishes both goals)
    """
    for i in range(81):
        row = getrowvalues(i, puzzle)
        column = getcolumnvalues(i, puzzle)
        box = getboxvalues(i, puzzle)

        # convert each to a set and compare lengths.
        # since sets don't have repeats, this will point out if any conflicts exist
        if len(row) != len(set(row)) or len(column) != len(set(column)) or len(box) != len(set(box)):
            return False
        return True


def makeallguesses(puzzle, level):
    """
    expect results to be reported as booleans in order to keep track of how many numbers are found
    to only solve with certain levels of algorithm, fill optional parameter "level".
    options are 'easy', 'medium', or 'medium_easy' to combine techniques.
    """
    simplecellsfound = 0
    singleinferencecellsfound = 0

    while True:
        holdingpuzzle = puzzle[:]

        if level == 'easy':
            if simpleguess(puzzle):
                simplecellsfound += 1

        if level == 'medium_easy':
            if simpleguess(puzzle):
                simplecellsfound += 1
            if singleinferenceguess(puzzle):
                singleinferencecellsfound += 1

        if level == "medium":
            if singleinferenceguess(puzzle):
                singleinferencecellsfound += 1

        if holdingpuzzle == puzzle:
            return "SimpleGuesses: " + str(simplecellsfound) + "\n" + "SingleInferenceGuesses: " + str(singleinferencecellsfound)


def simpleguess(puzzle):
    """
    makes guesses by just seeing if any cells have only 1 possibility
    just makes use of the 'findpossiblevalues' function really
    """

    for i in range(81):
        if len(findpossiblevalues(i, puzzle)) == 1 and puzzle[i] == 0:
            puzzle[i] = findpossiblevalues(i, puzzle)[0]
            return True
    return False


def singleinferenceguess(puzzle):
    """
    tries to fill in values based on a cell being the only one in a box/row/column that can actually have a value
    (only one cell has a particular possible value in a group)

    man this code is gross and long. and who really knows if it works? Update: totally works
    """

    for i in range(81):
        # all items in the row/col/box that are 0 (modified in the next section to make this the case)
        row = getrowindexes(i)
        column = getcolumnindexes(i)
        box = getboxindexes(i)

        # makes each list above only contain indexes of cells with no value in them (0)
        itercol = column[:]
        for index in itercol:
            if puzzle[index] != 0:
                column.remove(index)

        iterbox = box[:]
        for index in iterbox:
            if puzzle[index] != 0:
                box.remove(index)

        iterrow = row[:]
        for index in iterrow:
            if puzzle[index] != 0:
                row.remove(index)
        ###

        # prepare lists that contain all values that each cell in the row/col/box could possibly be
        possiblerowvalues = []
        for index in row:
            possiblerowvalues.append(findpossiblevalues(index, puzzle))

        possiblecolumnvalues = []
        for index in column:
            possiblecolumnvalues.append(findpossiblevalues(index, puzzle))

        possibleboxvalues = []
        for index in box:
            possibleboxvalues.append(findpossiblevalues(index, puzzle))

        # turn all the 2D lists into 1D
        possiblerowvalues = [x for sublist in possiblerowvalues for x in sublist]
        possiblecolumnvalues = [x for sublist in possiblecolumnvalues for x in sublist]
        possibleboxvalues  = [x for sublist in possibleboxvalues for x in sublist]

        ###

        for value in findpossiblevalues(i, puzzle):
            if possiblerowvalues.count(value) == 1 and puzzle[i] == 0:
                puzzle[i] = value
                return True
            if possiblecolumnvalues.count(value) == 1 and puzzle[i] == 0:
                puzzle[i] = value
                return True
            if possibleboxvalues.count(value) == 1 and puzzle[i] == 0:
                puzzle[i] = value
                return True
    return False

# Finally, the bit that executes, after all those functions.


def getfilelocation():
    global puzzles
    try:
        filelocation = input("Enter Puzzle File Location:\n")
        puzzles = gatherinput(filelocation)
    except FileNotFoundError:
        print("File Not Found\n")
        getfilelocation()


getfilelocation()
method = input("Enter Level of Method to Solve (easy, medium, medium_easy):\n")

for puzzle in puzzles:
    print(makeallguesses(puzzle, method))
    displaypuzzle(puzzle)

    if validatepuzzle(puzzle):
        print("Valid\n\n")  # the newlines are just to get it to print nicely
    else:
        print("Not Valid\n\n")

input("Press Enter to Exit the Program :::")