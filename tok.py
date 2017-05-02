#!/usr/bin/python
# Get sentences based off of each corpus
# Extract words and their status as memorable depending on the sentence it is in
import nltk
import sys

def tokenize(sentence, memorability, outputFileName):
    output_file = open(outputFileName, "a+")
    text = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(text)
    for pair in tagged_words:
        new_pair = pair[0] + "\t" + pair[1] + "\t" + memorability + "\n"
        output_file.write(new_pair)
    output_file.close()

def _hits(fileName, outputFileName):
    input1 = open(fileName, "r")
    text = input1.read()
    text = text.split("\n")
    i=0
    for line in text:
       if line != "":
            sent = line.split("\t")
            sentence = sent[0]
            memorability = sent[2]
            tokenize(sentence, memorability, outputFileName)
    input1.close()

def main():
    _hits("top_5k.txt", "words_memorability_no_annotation.txt")
    _hits("top_5k_annotated.txt", "words_memorability_with_annotation.txt")


if __name__ == "__main__":
    main()
