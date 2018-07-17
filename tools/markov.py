#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


''' update_markov_source()
Reads in the entire chat log file, 
and compiles every written line into a single run-on string
which is then written to its own file.
'''
def update_markov_source():
    full_string = ""
    with open("data/mball.txt", "r") as quote_file:
        for line in quote_file:
            if ": " in line and not "http" in line:
                name_removed_line = line[line.index(' ')+1:-1]
                if len(name_removed_line) > 1 and not name_removed_line[1].isupper():
                    name_removed_line = name_removed_line[0].lower() + name_removed_line[1:]
                name_removed_line = name_removed_line.replace(".", "").replace(",", "")
                name_removed_line = name_removed_line.replace("(", "").replace(")", "")
                name_removed_line = name_removed_line.replace("{", "").replace("}", "")
                full_string += name_removed_line + ". "
    quote_file.close()

    with open("data/markov_source2.txt", "w") as markov_source_file:
        markov_source_file.write(full_string)
    markov_source_file.close()

''' generate_markov_dict()
Builds a dict from the markov file.
key: every two words in order added as a key.
value: every word following those two words added as a value to that key.
eg. "The lazy fox jumps over the lazy dog":
the lazy: fox, dog
lazy fox: jumps
fox jumps: over
over the: lazy
lazy dog:
'''
def generate_markov_dict():
    with open("data/markov_source2.txt", "r") as source_file:
        for line in source_file:
            markov_input = line
    source_file.close()

    markov_dict = dict()
    markov_list = markov_input.split(' ')
    
    for i, word in enumerate(markov_list):
        snippet = markov_list[i] + " " + markov_list[i+1]
        try:
            if snippet in markov_dict:
                markov_dict[snippet].append(markov_list[i+2])
            else:
                markov_dict[snippet] = [markov_list[i+2]]
        except IndexError:
            break

    return markov_dict

def markov(phrase):
    markov_dict = generate_markov_dict2()
    output = phrase + " "

    while True:
        if phrase in markov_dict:
            following_word = random.choice(markov_dict[phrase])
            output += following_word + " "
        else:
            break
    
        new_first_word = phrase.split(' ')[1]
        new_second_word = following_word
        phrase = "{} {}".format(new_first_word, new_second_word)

        if output.rstrip().endswith("."):
            break

    if len(output.strip()) == 0:
        return ""

    if len(output.split(' ')) >= 3:
        output = output.split(' ', 2)[2]

    return output.rstrip()
