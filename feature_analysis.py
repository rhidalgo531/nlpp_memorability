#!/usr/bin/python
import sys
import math

def second_pass(data):
    percent_set = []
    for memorability in data:
        print "------------------------ Beginning of " + memorability + "\n"
        max_ = [0,0,0]
        max_pos = ["","",""]
        for pos in data[memorability]:
            percentage = float(data[memorability][pos]) / float(data[memorability]["Total"]) * 100
            for i in range(0,len(max_)):
                if pos != "Total":
                    if max_[i] < percentage:
                        max_[i] = percentage
                        max_pos[i] = pos
                        break

            print "Percentage for " + pos + " in " + memorability + " is " + str(percentage)
        print "------------------------ End of " + memorability + "\n"

def main(file_name, option):
    q = raw_input("Enter any key when words_mem files are finished")
    file1 = open(file_name, "r")
    text = file1.read()
    text_lines = text.split("\n")
    data = {}
    tuples = {}
    data["Memorable"] = {}
    data["Memorable"]["Total"] = 0
    data["Slightly Memorable"] = {}
    data["Slightly Memorable"]["Total"] = 0
    data["Not Memorable"] = {}
    data["Not Memorable"]["Total"] = 0
    for line in text_lines:
        sentence = line.split("\t")
        if (len(sentence) == 3):
            pos = sentence[1]
            if (pos != "."):
                memorability = sentence[2]
                if ("Slightly" in memorability): ## Handle weird cases with whitespace
                    memorability = "Slightly Memorable"
                elif ("Not" in memorability):
                    memorability = "Not Memorable"
                else:
                    memorability = "Memorable"
                if pos in data[memorability]:
                    count = data[memorability][pos] + 1
                    pair = {pos:count}
                    data[memorability][pos] = count
                else:
                    pair = {pos:1}
                    data[memorability].update(pair)
                data[memorability]["Total"] += 1
    if (option == 1):
        return data
    else:
        second_pass(data)


if __name__ == "__main__":
    if (len(sys.argv) == 3):
        main(sys.argv, sys.argv[2])
    else:
        main(sys.argv, 0)
