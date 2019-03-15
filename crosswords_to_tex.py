crosswords = ""
with open("crosswords_out.txt", "rt") as f:
    for line in f:
        if line.strip() != "":
            #print(line.rstrip())
            crosswords += line.rstrip()
            crosswords += "\n"
# crosswords_lines = "\n".join([line for line in crosswords.splitlines() if line.strip() != ""])
crosswords_lines = [line for line in crosswords.splitlines() if line.strip() != ""]
# print(crosswords_lines)
row_num = len(crosswords_lines)
col_num = max([len(line) for line in crosswords_lines])

board_lines = []
filling = "    "
for line in crosswords_lines:
    board_line = ""
    for ch in line:
        if ch == " ":
            board_line += f"|*{filling}"
        else:
            board_line += f"|{ch}{filling}"
    board_line = board_line + f"|*{filling}" * (col_num-len(line)) + "|."
    board_lines.append(board_line)

#pprint(board_lines)


print(r"\begin{Puzzle}{"+ f"{col_num}" + r"}{" + f"{row_num}" + r"}")
for line in board_lines:
    print(line)