from __future__ import division
import random
import re
import shlex


def calculate(text, first_name):
    head, sep, tail = text.partition('/')
    input_nums = tail.replace('calc', '')
    input_nums = input_nums.replace('\'', '')

    spaces = True if ' ' in input_nums[1:] else False
    there_are_spaces = "don't use spaces in your expression (eg. 6*9-3)"

    finalexp = shlex.split(input_nums)
    exp = finalexp[0]

    if not exp:
        return "this isn't a valid expression, %s. *FLUSH*" % (
            first_name.lower())
    elif re.search('[a-zA-Z]', exp):
        return "that's not maths, %s." % (first_name.lower())
    else:
        return there_are_spaces if spaces else eval(exp)
