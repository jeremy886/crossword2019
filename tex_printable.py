import os
from string import Template


def crossword_text_to_lines(crossword_text_filename):
    crosswords = ""
    with open(crossword_text_filename, "rt") as f:
        for line in f:
            if line.strip() != "":
                #print(line.rstrip())
                crosswords += line.rstrip()
                crosswords += "\n"
    crosswords_lines = [line for line in crosswords.splitlines() if line.strip() != ""]
    return crosswords_lines


def board_size(crosswords_lines):
    row_num = len(crosswords_lines)
    col_num = max([len(line) for line in crosswords_lines])
    return row_num, col_num


def find_word(crosswords_lines, key, type):
    word = ""
    if type == "across":
        for col, ch in enumerate(crosswords_lines[key[0]]):
            if col < key[1]:
                continue
            if ch != " ":
                word += ch
            else:
                break
    elif type == "down":
        ch = crosswords_lines[key[0]][key[1]]
        row = key[0]
        while True and ch != " ":
            word += ch
            row += 1
            try:
                ch = crosswords_lines[row][key[1]]
            except IndexError:
                break
    return word


def tex_out(crosswords_lines, head_letters):
    row_num, col_num = board_size(crosswords_lines)
    hl = head_letters

    board_lines = []
    fi = " "  # filling
    for nr, line in enumerate(crosswords_lines):
        board_line = ""
        for nc, ch in enumerate(line):
            if ch == " ":
                board_line += f"|*{fi*4}"
            elif (nr, nc) in head_letters:
                no = hl[nr, nc][0]
                board_line += f"|[{no}]{ch}{fi*(2-len(str(no)))}"
            else:
                board_line += f"|{ch}{fi*4}"
        board_line = board_line + f"|*{fi*4}" * (col_num-len(line)) + "|."
        board_lines.append(board_line)

    # print(r"\begin{Puzzle}{"+ f"{col_num}" + r"}{" + f"{row_num}" + r"}")
    # for line in board_lines:
    #     print(line)
    # print(r"\end{Puzzle}")
    with open("crossword_puzzle.tex", "w") as texfile:
        # tex code for puzzle
        texfile.write(r"\begin{Puzzle}{" + f"{col_num}" + r"}{" + f"{row_num}" + r"}")
        texfile.write(os.linesep)
        texfile.writelines(os.linesep.join(board_lines))
        texfile.write(os.linesep)
        texfile.write(r"\end{Puzzle}")
        texfile.write(os.linesep)
        # tex code for clues
        texfile.write(os.linesep)

        clues_across = []
        clues_down = []
        for key, (order, type) in head_letters.items():
            print(key, order, type)
            if type == 0b01:  # across
                clues_across.append((order, find_word(crosswords_lines, key, "across"), ""))
            elif type == 0b10: # down
                clues_down.append((order, find_word(crosswords_lines, key, "down"), ""))
            elif type == 0b11: # across and down
                clues_across.append((order, find_word(crosswords_lines, key, "across"), ""))
                clues_down.append((order, find_word(crosswords_lines, key, "down"), ""))
        print(clues_across)
        print(clues_down)
        texfile.write(r"\begin{PuzzleClues}{\textbf{Across}}")
        texfile.write(os.linesep)
        for clue in clues_across:
            clue_template = Template("\\Clue{$order}{$word}{$clue}")
            texfile.write(clue_template.safe_substitute(order=clue[0], word=clue[1], clue=clue[2]))
            texfile.write(os.linesep)
        texfile.write(r"\end{PuzzleClues}")

        texfile.write(os.linesep)
        texfile.write(r"\begin{PuzzleClues}{\textbf{Down}}")
        texfile.write(os.linesep)
        for clue in clues_down:
            clue_template = Template("\\Clue{$order}{$word}{$clue}")
            texfile.write(clue_template.safe_substitute(order=clue[0], word=clue[1], clue=clue[2]))
            texfile.write(os.linesep)
        texfile.write(r"\end{PuzzleClues}")


def print_tex():
    from headletters import find_heads, build_01_board

    crosswords_lines = crossword_text_to_lines("crosswords_out.txt")
    # print(crosswords_lines)
    board01_lines = build_01_board(crosswords_lines)
    head_letters = find_heads(board01_lines)
    # build cue_list
    # print(head_letters)
    tex_out(crosswords_lines, head_letters)

