#!/usr/bin/python
import sys
import strip_movie_sentences as strip
import subprocess
import script_line_hits as hits
import top_5k_scores as top5
import tok as tokenization
import feature_analysis as analysis
import math

def output_all(all_info_lines):
    output_name = raw_input("Please name your output file for predictions, with extension")
    output_f = open(output_name, "w")
    for ele in all_info_lines:
        output_f.write(ele)
    output_f.close()

def predict_by_entropy(sentence, in_set, out_of_set, parent_data):
    total = in_set + out_of_set
    child_x = float(in_set)/float(total)
    child_y = (float(out_of_set)/float(total))
    if child_y == 0.0:
        child_y = 0.01
    if child_x == 0.0:
        child_x = 0.01
    entropy_child = (-1.0 * math.log(child_x) * child_x) - (-1.0 *(child_y) * math.log(child_y))
    print entropy_child
    words = sentence.split(" ")
    in_set_parent = 0
    out_of_set_parent = 0
    for word in words:
        if word in parent_data["Memorable"]:
            in_set_parent += parent_data["Memorable"][word]
        else:
            if word in parent_data["Slightly Memorable"]:
                out_of_set_parent += parent_data["Slightly Memorable"][word]
            if word in parent_data["Not Memorable"]:
                out_of_set_parent += parent_data["Not Memorable"][word]
    total_parent = in_set_parent + out_of_set_parent
    if total_parent == 0:
        line = sentence + "\t" + "N/A" + "\t" + "Inconclusive\n"
        return line
    else:
        x = float(in_set_parent)/float(total_parent)
        y = (float(out_of_set_parent)/float(total_parent))
        if y == 0.0:
            y = 1
        if x == 0.0:
            x = 1
        entropy_parent = ( -1.0 * math.log(x) * x) - (-1.0 *y * math.log(y))
        information_gain = entropy_parent - entropy_child
        print information_gain
        line = ""
        if information_gain > 0.075:
            line = sentence + "\t" + str(information_gain) + "\t" + "Not Memorable\n"
        elif information_gain > 0.025:
            line = sentence + "\t" + str(information_gain) + "\t" + "Slightly Memorable\n"
        else:
            line = sentence + "\t" + str(information_gain) + "\t" + "Memorable\n"
        return line


def test_file(file_name, type_of_file):
    print file_name
    if type_of_file == "yahoo":
        f_ = "words_mem_no_annotation_" + file_name
        g_ = "words_memorability_no_annotation.txt"
    elif type_of_file == "manual":
        f_ = "words_mem_with_annotation_" + file_name
        g_ = "words_memorability_with_annotation.txt"
    else:
        print "Error in File Handling"
        return
    data = analysis.main(f_,1)
    parent_data = analysis.main(g_, 1)
    lines_file = open(f_,"r")
    lines = lines_file.read()
    all_lines = lines.split("\n")
    sentence = ""
    temp_in_set = 0
    temp_out_set = 0
    temp_entropy = 0
    all_info_lines = []
    for i in range(len(all_lines)):
        if i != len(all_lines):
            if all_lines[i] != ".":
                line = all_lines[i].split("\t")
                if (len(line) == 3):
                    word = line[0]
                    if word == ".":
                        all_info_lines.append(predict_by_entropy(sentence, temp_in_set, temp_out_set, parent_data))
                        sentence = ""
                    else:
                        memorability_type = line[2]
                        sentence += word + " "
                        if memorability_type == "Memorable":
                            temp_in_set += 1
                        else:
                            temp_out_set += 1
    output_all(all_info_lines)


def do_func(hits_file, annotated_file):
    args = [hits_file, annotated_file]
    tokenization.main(args)
    test_file(hits_file, "yahoo")
    test_file(annotated_file, "manual")

def get_top_5(script):
    top5.main(script, "top_5k_" + script)
    top5_file = "top_5k_" + script
    flag = True
    while (flag == True):
        answer = raw_input("Has your file been annotated? Please answer with yes or no\n")
        if (answer == "yes" or answer == "Yes"):
            annotated_file = raw_input("Please enter the name of your annotated file in the current directory\n")
            do_func(top5_file, annotated_file)
            flag = False
        else:
            question = raw_input("No? Would you like to stop the program? Please answer with yes or no\n")
            if (question == "yes" or question == "Yes"):
                flag = False
                break
            else:
                continue

def main(arguments):
    script_filtered = "scores_" + arguments[1]
    strip.main(arguments[1], script_filtered)
    ## Get script, get filtered movie type
    get_top_5(script_filtered)

if __name__ == "__main__":
    main(sys.argv)
