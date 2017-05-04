#!/usr/bin/python
import sys

def shuffle_board(sent_board, score_board):
    for i in range(1, len(score_board) - 1):
        for j in range(i):
            if score_board[j] < score_board[i]:
                temp = score_board[i]
                score_board[i] = score_board[j]
                score_board[j] = temp
                temp2 = sent_board[i]
                sent_board[i] = sent_board[j]
                sent_board[j] = temp2


def get_top_5k(sent_board, score_board, file5k):
    shuffle_board(sent_board, score_board)
    output_file = open(file5k, "w+")
    length = len(sent_board)
    i = 0
    if (length < 5000):
        lower_bound = length * .25
        mid_bound = length * .75
        upper = length
    else:
        lower_bound = 1250
        mid_bound = 3750
        upper = 5000
    while (i < upper): #only get the top 5 thousand scores
        if (i < lower_bound):
            output_file.write(sent_board[i] + "\t" + str(score_board[i]) + "\t" + "Memorable\n")
        elif (i < mid_bound):
            output_file.write(sent_board[i] + "\t" + str(score_board[i]) + "\t" + "Slightly Memorable\n")
        else:
            output_file.write(sent_board[i] + "\t" + str(score_board[i]) + "\t" + "Not Memorable\n")
        i+= 1
    output_file.close()

def handle_line(line):
    sentence = ""
    if len(line) == 2:
        sentence = line[0]
    else :
        for i in range(len(line) - 1):
            if i == len(line) - 1:
                sentence += line[i]
            else:
                sentence += line[i] + ","
    return sentence

def main():
    get_text = open("movie_script_sentences_scores.txt","r")
    lines = get_text.read()
    docs = lines.split("THE END")
    sent_board = []
    score_board = []
    for movie in docs:
        script = movie.split("\n")
        for ele in script:
            if ele == "":
                continue
            else:
                line = ele.split(",")
                score_index = len(line) - 1
                if line[score_index] != "":
                    score = int(line[score_index])
                    sentence = handle_line(line)
                    score_board.append(score)
                    sent_board.append(sentence)
    get_text.close()
    get_top_5k(sent_board, score_board, "top_5k.txt")

def main(args1, args2):
    get_text = open(args1,"r")
    lines = get_text.read()
    docs = lines.split("THE END")
    sent_board = []
    score_board = []
    for movie in docs:
        script = movie.split("\n")
        for ele in script:
            if ele == "":
                continue
            else:
                line = ele.split(",")
                score_index = len(line) - 1
                if line[score_index] != "":
                    score = int(line[score_index])
                    sentence = handle_line(line)
                    score_board.append(score)
                    sent_board.append(sentence)
    get_text.close()
    get_top_5k(sent_board, score_board, args2)


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        main()
    elif (len(sys.argv) > 1):
        main(sys.argv)
    else:
        print "Error"
