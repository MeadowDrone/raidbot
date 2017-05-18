#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def generate_markov_source():
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
                full_string += name_removed_line + " "
    quote_file.close()

    with open("data/markov_source.txt", "w") as markov_source_file:
        markov_source_file.write(full_string)
    markov_source_file.close()
    return("updated!")


def generate_markov_dict():
    with open("data/markov_source.txt", "r") as source_file:
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
        except IndexError as e:
            break

    return markov_dict


def markov(phrase):
    not_ending_words = ['and', 'or', 'that', 'i', 'he', 'she', 'they', 'we',
            'but', 'the', 'a', 'an', 'the',
            'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 
            'amid', 'among', 'around', 'as', 'at', 'before', 'behind', 'below',
            'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'considering',
            'despite', 'down', 'during', 'except', 'excluding', 'following', 
            'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'of', 'off',
            'on', 'onto', 'outside', 'over', 'past', 'regarding', 'since', 
            'than', 'though', 'to', 'toward', 'under', 'underneath', 'until',
            'up', 'upon', 'verses', 'with', 'within', 'without']
    comma_words = ['and', 'or', 'then', 'but', 'because', 'however', 'although', 'except',
            'amid', 'among', 'around', 'as', 'before', 'behind', 'below',
            'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'considering',
            'despite', 'down', 'during', 'except', 'excluding', 'following', 
            'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'off',
            'on', 'onto', 'outside', 'over', 'past', 'regarding', 'since', 
            'than', 'though', 'toward', 'under', 'underneath', 'until',
            'up', 'upon', 'verses', 'with', 'within', 'without']
    markov_dict = generate_markov_dict()
    output = phrase + " "

    for i in range(random.randint(3,40)):
        if phrase in markov_dict:
            following_word = random.choice(markov_dict[phrase])

            if following_word in comma_words and random.randint(1,5) == 1:
                output = output[:-1] + ", " + following_word + " "
            else:
                output += following_word + " "
        else:
            break
    
        new_first_word = phrase.split(' ')[1]
        new_second_word = following_word
        phrase = "%s %s" % (new_first_word, new_second_word)

        for words in not_ending_words:
            if new_second_word.lower().strip() == words.lower():
                i -= 1

    ending_rng = random.randint(1,10)
    if ending_rng < 7:
        ending = "."
    elif ending_rng < 9:
        ending = "!"
    else:
        ending = "?"

    output = output[0].upper() + output[1:-1] + ending

    return(output.rstrip())
