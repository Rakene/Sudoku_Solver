from sys import argv
script, filename=argv

full = {1, 2, 3, 4, 5, 6, 7, 8, 9}
puzzlecount = 0
rcbmap = {"r1":[11, 12, 13, 14, 15, 16, 17, 18, 19],
          "r2":[21, 22, 23, 24, 25, 26, 27, 28, 29],
          "r3":[31, 32, 33, 34, 35, 36, 37, 38, 39],
          "r4":[41, 42, 43, 44, 45, 46, 47, 48, 49],
          "r5":[51, 52, 53, 54, 55, 56, 57, 58, 59],
          "r6":[61, 62, 63, 64, 65, 66, 67, 68, 69],
          "r7":[71, 72, 73, 74, 75, 76, 77, 78, 79],
          "r8":[81, 82, 83, 84, 85, 86, 87, 88, 89],
          "r9":[91, 92, 93, 94, 95, 96, 97, 98, 99],
          "c1":[11, 21, 31, 41, 51, 61, 71, 81, 91],
          "c2":[12, 22, 32, 42, 52, 62, 72, 82, 92],
          "c3":[13, 23, 33, 43, 53, 63, 73, 83, 93],
          "c4":[14, 24, 34, 44, 54, 64, 74, 84, 94],
          "c5":[15, 25, 35, 45, 55, 65, 75, 85, 95],
          "c6":[16, 26, 36, 46, 56, 66, 76, 86, 96],
          "c7":[17, 27, 37, 47, 57, 67, 77, 87, 97],
          "c8":[18, 28, 38, 48, 58, 68, 78, 88, 98],
          "c9":[19, 29, 39, 49, 59, 69, 79, 89, 99],
          "b1":[11, 12, 13, 21, 22, 23, 31, 32, 33],
          "b2":[14, 15, 16, 24, 25, 26, 34, 35, 36],
          "b3":[17, 18, 19, 27, 28, 29, 37, 38, 39],
          "b4":[41, 42, 43, 51, 52, 53, 61, 62, 63],
          "b5":[44, 45, 46, 54, 55, 56, 64, 65, 66],
          "b6":[47, 48, 49, 57, 58, 59, 67, 68, 69],
          "b7":[71, 72, 73, 81, 82, 83, 91, 92, 93],
          "b8":[74, 75, 76, 84, 85, 86, 94, 95, 96],
          "b9":[77, 78, 79, 87, 88, 89, 97, 98, 99]}

# Cell class represents one cell in the sudoku that has an id, value, and status
class cell:
    def __init__(self, id, val):
        self.id = id
        self.val = val
        self.pos = full
        if val == 0:
            self.status = 'Open'
        else:
            self.status = 'Given'
            self.pos = {self.val}

    def int_pos(self, other):
        if self.status == 'Open':
            self.pos = self.pos & other

    def calc(self):
        if len(self.pos) == 1 and self.status == 'Open':
            for e in self.pos:
                break
            self.val = e
            self.status = 'Solved'
            print(f"Solved Cell {self.id} to {self.val}")
            return 1
        elif len(self.pos) == 0:
            return 99
        else:
            return 0

    def name(self):
        return self.id

    def value(self):
        return self.val

    def in_set(self, value):
        if self.pos.issubset(value):
            return True
        else:
            return False

    def check_status(self):
        return self.status

    def check_pos(self):
        return self.pos

# The rcb class represents a row, column or block of the sudoku board.  Each has an id, list of cells, and list of open cells
class rcb:
    def __init__(self, id, cells):
        self.id = id
        self.cells = cells
        self.remain = full

    def calc(self):
        global rcbmap
        for c in rcbmap[self.id]:
            if self.cells[c].value() != 0:
                self.remain = self.remain - {self.cells[c].value()}
        members = full-self.remain
        for c in rcbmap[self.id]:
            self.cells[c].int_pos(self.remain)
            if self.cells[c].value() != 0:
                if {self.cells[c].value()}.issubset(members) == True:
                    members = members - {self.cells[c].value()}
                else:
                    return 99

#Checking for hidden singles
        for n in self.remain:
            count = 0
            for c in rcbmap[self.id]:
                if self.cells[c].in_set({n}):
                    count += 1
                    hidden_cell = self.cells[c].name()
            if count == 1:
                self.cells[hidden_cell].int_pos({n})
        return 1


# The puzzle class represents the whole sudoku board
class puzzle:
    def __init__(self, layer, pstring, parent):
        global rcbmap
        global puzzlecount
        self.layer = layer
        self.cells={}
        self.rcbs={}
        self.pstring = pstring
        puzzlecount += 1
        if parent == None:

            i = 0
            if len(pstring) == 81 and pstring.isdigit():
                for r in range(1,10):
                    for c in range(1,10):
                        self.cells.update({r*10+c: cell(r*10+c, int(pstring[i]))})
                        i += 1

                for b in rcbmap:
                    self.rcbs.update({b: rcb(b, self.cells)})

            else:
                print("Error: Incorrect Input", pstring)
                exit(1)
        else:
            for id,c in parent.cells.items():
                self.cells.update({id: c})
            for id,b in parent.rcbs.items():
                self.rcbs.update({id: b})

    def disp(self):
        self.pstring = "\n"
        for r in range(1,10):
            for c in range(1,10):
                s = str(self.cells[r*10+c].value())
                if s == '0':
                    s = '.'
                s = s+' '
                self.pstring += s
            self.pstring += "\n"
        print("\n", self.pstring)

    def solve(self):
        import copy
        # Solving for forced results
        change = True
        while change == True:
            change = False
            for r in self.rcbs:
                if self.rcbs[r].calc() == 99:
                    print(f"Layer: {self.layer} Puzzle: {puzzlecount} Duplicate: {self.rcbs[r].id}")
                    self.disp()
                    return False
            for c in self.cells:
                if self.cells[c].calc() == 1:
                    change = True
                elif self.cells[c].calc() == 99:
                    print(f"Layer: {self.layer} Puzzle: {puzzlecount} Zero Cell: {self.cells[c].name()}")
                    return False
        #Printing the puzzle's layers
        print(f"Layer: {self.layer} Puzzle: {puzzlecount}")
        self.disp()

        # Preparing for brute force search and checking for solution
        counter = 0
        min_pos = 9
        min_id = 0
        for c in self.cells:
            if self.cells[c].check_status() == 'Open':
                counter += 1
                if len(self.cells[c].check_pos()) < min_pos:
                    min_id = c
                    min_pos = len(self.cells[c].check_pos())
        if counter == 0:
            print("Yay the sudoku is solved!")
            self.disp()
            return True
        min_set = self.cells[min_id].check_pos()
        for i in min_set:
            new = puzzle(self.layer+1, self.pstring, copy.deepcopy(self))
            new.cells[min_id].int_pos({i})
            if new.solve() == True:
                return True
        return False


# Takes the path to a .txt file as input
def main(filename):
    pstring = ""

    # Opens the .txt file and puts its contents in one long string removing any new lines
    with open(filename, 'r') as txt:
        pstring=txt.read().replace('\n', '')
    txt.close()

    # Initializes a puzzle object from the puzzle string
    p = puzzle(0, pstring, None)

    #Calls the solve function with puzzle object
    p.solve()
    print("Finished!")
    exit(0)

# Passes the second argument from the command line to the main function
main(argv[1])
