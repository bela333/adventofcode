class Board:
    def __init__(self, board) -> None:
        self.board = board
        self.marks = [[False]*5 for _ in range(5)]
    
    def mark(self, number):
        for y in range(5):
            for x in range(5):
                if self.board[y][x] == number:
                    return self._mark(x, y)
        return False

    def check(self, x, y):
        #Look at column of y
        if all(self.marks[y]):
            return True
        #Look at row of x
        if all([a[x] for a in self.marks]):
            return True
        return False

    def _mark(self, x, y):
        self.marks[y][x] = True
        return self.check(x, y)
    def unmarked_sum(self):
        return sum([sum([m for n, m in zip(a, b) if not n]) for a, b in zip(self.marks, self.board)])

def main():
    with open("input.txt") as f:
        numbers = [int(a) for a in f.readline().strip().split(",")]
        lines = f.read().splitlines()
        wins = [-1]*(len(lines)//6)
        boards = [None for _ in wins]
        for i in range(1, len(lines), 6):
            board = [[int(number) for number in line.split()] for line in lines[i:i+5]]
            board = Board(board)
            boards[(i-1)//6] = board
            for j in range(len(numbers)):
                num = numbers[j]
                if board.mark(num):
                    wins[(i-1)//6] = j
                    break
        #One line change LMAO
        winning_pos = max([a for a in wins if a >= 0])
        winning_num = numbers[winning_pos]
        winning_board = boards[wins.index(winning_pos)]
        print(winning_board.unmarked_sum() * winning_num)
        

if __name__ == "__main__":
    main()