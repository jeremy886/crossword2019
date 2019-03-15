import re
from pprint import pprint



with open("crosswords_out.txt", "rt") as f:
    crosswords = f.read()

crosswords = "\n".join([line for line in crosswords.splitlines() if line.strip() != ""])
#print(crosswords)
# crosswords = """
#                P
#                L
#            BODMAS
#              E C
#          E   N E
#          Q   O HCF
#       F  U   M O
#     TRAILING I LCD
#       C  V   N D
#       T  A PLACE
#       O  L   T R
#       R  E   O
#          NUMERATOR
#          T A
#            G
#       ROUNDING
#            C
# """

pattern1 = re.compile(r"[A-Z]")
crosswords1 = pattern1.sub("1", crosswords)
pattern2 = re.compile(r"\ ")
crosswords2 = pattern2.sub("0", crosswords1)

# trim the board
board_start = 9999
board_end = 0
for line in crosswords2.splitlines():
    if line.strip() == "":
        continue
    fill_start = line.find("1")
    fill_end = line.rfind("1")
    # print("fill", fill_start, fill_end)
    board_start = fill_start if fill_start < board_start else board_start
    board_end = fill_end if fill_end > board_end else board_end
#print("board", board_start, board_end)


board = []
for line in crosswords2.splitlines():
    if line.strip() == "":
        continue
    board.append(f"{line[board_start:]:0<{board_end-board_start+1}}")

#pprint(board)
# print(board[3][3], board[2][10])

# numbering
# pattern 011, first row and column add 0
# minimal 3 letters: pattern 011 check row in [0: len(row) - 2], column in [0: len(col) - 2]

def head_letter(row, col, board):
    """
    :param row: row number
    :param col: column number
    :param board: existing board
    :return: head_value
        0 not a head letter
        1 is a head letter of a word across
        2 is a head letter of a word down
        3 is a head letter for both a word across and a word down
    """

    # check 11 pattern for first row and column
    # check 011 pattern for other rows and columns

    assert row <= len(board) - 1
    assert col <= len(board[0]) - 1
    head_value = 0
    if board[row][col] == "1":
        # check down word
        if row == 0:
            if board[row+1][col] == "1":
                head_value += 2
        elif board[row-1][col] == "0" and board[row+1][col] == "1":
            head_value += 2
        # check across word
        if col == 0:
            if board[row][col+1] == "1":
                head_value += 1
        elif board[row][col-1] == "0" and board[row][col+1] == "1":
                head_value += 1
    return head_value


for i in range(len(board)-1):
    for j in range(len(board[0])-1):
        if head_letter(i, j, board) > 0:
            print(f"row:{i} col: {j} -->", head_letter(i, j, board))


# Reportlab
