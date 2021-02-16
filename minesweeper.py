import random
import copy

class MineSweeper:
    def __init__(self, row=3, col=3, mine=3):
        assert isinstance(row, int), f"Row '{row}' is not an integer"
        assert isinstance(col, int), f"Column '{col}' is not an integer"
        assert isinstance(mine, int), f"Mine '{mine}' is not an integer"

        self.row = row
        self.col = col
        self.mine = mine
        self.first_move = True
        self._make_boards()
        self.unknown_fields = row * col - mine
        self.win = False
        
    # Create minesweeper board
    # Player board is what the player sees
    # Hidden board contains all field values after first move
    # -1 - Unknown field
    # 0-8 - Number of mines surrounding that field
    def _make_boards(self):
        self.board = []
        
        for r in range(self.row):
            row = []
            for c in range(self.col):
                row.append(-1)
            
            self.board.append(row)
    
    # Take action
    def action(self, row=-1, col=-1, val=-1):
        if val != -1:
            row, col = self._val_to_rc(val)
            
        assert not (row >= self.row or row < 0), f"Row {row} is not on the board"
        assert not (col >= self.col or col < 0), f"Column {col} is not on the board"
            
        if self.first_move:
            self._make_mines(row, col)
            self.first_move = False

        # Expand field if it's still unknown
        if self.board[row][col] == -1:
            val = self._rc_to_val(row, col)
            # Check if it's mine first
            if val in self.mine_location:
                print("You lose")
                return
                
            neighbors = self._get_neighbors(val)
            mine_count = 0

            for mine in self.mine_location:
                if mine in neighbors:
                    mine_count += 1
            
            # If there is mine around clicked location
            if mine_count != 0:
                self._reveal_loc(row, col, mine_count)
            # If no mine around, expand
            else:
                self._reveal_loc(row, col, 0)
                visited_neighbors = copy.deepcopy(neighbors)
                while neighbors:
                    neighbor_val = neighbors.pop()
                    neighbor_row, neighbor_col = self._val_to_rc(neighbor_val)
                    
                    # Skip if already revealed
                    if self.board[neighbor_row][neighbor_col] != -1:
                        continue
                        
                    cur_neighbors = self._get_neighbors(neighbor_val)
                    neighbor_mine_count = 0

                    for mine in self.mine_location:
                        if mine in cur_neighbors:
                            neighbor_mine_count += 1
                    
                    if neighbor_mine_count != 0:
                        self._reveal_loc(neighbor_row, neighbor_col, neighbor_mine_count)
                    else:
                        self._reveal_loc(neighbor_row, neighbor_col, 0)
                        # Add more neighbors if no mine
                        for neighbor in cur_neighbors:
                            if neighbor not in visited_neighbors:
                                visited_neighbors.add(neighbor)
                                neighbors.add(neighbor)
        
        if self.unknown_fields == 0:
            self.win = True

    def _reveal_loc(self, row, col, mine_count):
        self.board[row][col] = mine_count
        self.unknown_fields -= 1

    def _rc_to_val(self, row, col):
        return (row * self.col) + col

    def _val_to_rc(self, val):
        return val // self.col, val % self.col

    # Determine mine location
    # First move can never be a bomb
    def _make_mines(self, row, col):
        val_rc = self._rc_to_val(row, col)
        fields = list(range(self.row * self.col))
        fields.remove(val_rc)
        
        self.mine_location = set(random.sample(fields, self.mine))
    
    def _get_neighbors(self, val):
        neighbors = []

        # Row above
        if val - self.col >= 0:
            above = val - self.col
            neighbors.append(above)

            # Left
            if above % self.col != 0 and above - 1 >= 0:
                neighbors.append(above-1)
            # Right
            if above % self.col < self.col - 1 and above + 1 < self.col * self.row:
                neighbors.append(above+1)
        
        # Same row
        if val % self.col != 0 and val - 1 >= 0:
            neighbors.append(val-1)
        if val % self.col < self.col - 1 and val + 1 < self.col * self.row:
            neighbors.append(val+1)
        
        # Row below
        if val + self.col < self.row * self.col:
            below = val + self.col
            neighbors.append(below)

            # Left
            if below % self.col != 0 and below - 1 >= 0:
                neighbors.append(below-1)
            # Right
            if below % self.col < self.col - 1 and below + 1 < self.col * self.row:
                neighbors.append(below+1)
        
        return set(neighbors)
    
    def print_board(self):
        border = ("-" * self.col) + ("-" * (self.col-1))
        print(border)
        
        for r in range(self.row):
            row_string = ""
            for c in range(self.col):
                val = self.board[r][c]
                if val == -1:
                    row_string += "o"
                else:
                    row_string += str(val)
                if c != self.col-1:
                    row_string += "|"
            print(row_string)
        
        print(border)
        print(f"unknown: {self.unknown_fields}")