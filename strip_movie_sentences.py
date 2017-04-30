#!/usr/bin/python
# Use: take screenplays of movies, with various formatting in whitespace and
# extract the sentences into an output file, one sentence per line
import sys
import re
import script_line_hits

def output_text(script, output, score_output, text):
    for line in script:
        output.write(line + "\n")
        score_line = line + ","
        if score_line not in text:
            data = script_line_hits.do_provider_search_with_pause(line, timing=1, reps=0)
            if (data >= 100000):
                score_line = line + "," + data + "\n"
                score_output.write(score_line)
            #elif data == -1:
            #    score_output.write(score_line + "\n")
    output.write("THE END\n")

def remove_extra_spaces(doc):
    for i in range(len(doc)):
        line = doc[i]
        sentence = ""
        for word in line.split(" "):
            word.strip()
            if word != '':
                sentence+= word + " "
        doc[i] = sentence
    return doc

def main():
    file_to_open = "raw_movie_scripts.txt"
    raw_movie_scripts = open(file_to_open, 'r')
    text = raw_movie_scripts.read()
    all_movie_scripts = text.split("THE END")
    output = open("filtered_movie_script_sentences.txt", 'w+');
    score_output = open("movie_script_sentences_scores.txt", 'a+');
    score_output.seek(0)
    text = score_output.read()
    score_output.seek(len(text) - 1)
    for i in range(len(all_movie_scripts) - 1):
        split_text = all_movie_scripts[i].replace("\n", " ")
        sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', split_text)
        filtered_sentences = remove_extra_spaces(sentences)
        output_text(filtered_sentences, output, score_output, text)
    output.close()

if __name__ == "__main__":
    main()
    #sys.exit(main(sys.argv));
