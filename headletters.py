import re
from tex_printable import board_size


def build_01_board(crosswords_lines):
    row_num, col_num = board_size(crosswords_lines)
    # print(crosswords_lines)

# with open("crosswords_out.txt", "rt") as f:
#     crosswords = f.read()
#
# crosswords = "\n".join([line for line in crosswords.splitlines() if line.strip() != ""])
#
    pattern = re.compile(r"[A-Z]")
    # crosswords1 = pattern1.sub("1", crosswords)
    # pattern2 = re.compile(r"\ ")
    # crosswords2 = pattern2.sub("0", crosswords1)

    board01_lines = []
    for line in crosswords_lines:
        if len(line) < col_num:
            new_line = "0" * col_num
            new_line = line + new_line[len(line):]
        else:
            new_line = line
        new_line_01 = pattern.sub("1", new_line.replace(" ", "0"))
        board01_lines.append(new_line_01)

    # print(board01_lines)
    return board01_lines


def check_letter(row, col, board):
    """
    check cell in row and col to see if it's a head letter of a word

    :param row: row starting from 0
    :param col: col starting from 0
    :param board: a list consists of 0 and 1 converted from original board
    :return: head_value
        0 not a head letter
        1 or 0b01 is a head letter of a word across
        2 or 0b10 is a head letter of a word down
        3 or 0b11 is a head letter for both a word across and a word down
    """

    # check 11 pattern for first row and first column
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


def find_heads(board01_lines):
    """

    :param board01_lines:
    :return:
        a tuple of (number of the order, across/down status)
    """
    board = board01_lines
    head_letters = {}
    order = 1
    for i in range(len(board)-1):
        for j in range(len(board[0])-1):
            if check_letter(i, j, board) > 0:
                # print(f"row:{i} col: {j} -->", check_letter(i, j, board))
                head_letters[(i, j)] = order, check_letter(i, j, board)
                order += 1
    return head_letters



if __name__ == '__main__':
    board01_lines = build_01_board(crosswords_lines)
    head_letters = find_head_letters(board01_lines)
    print(head_letters)

