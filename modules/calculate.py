from __future__ import division
import random
import re
import shlex

def calculate(text, first_name):
        head, sep, tail = text.partition('/')
        input_nums = tail.replace('calc', '')
        input_nums = input_nums.replace('\'', '')
        
        if ' ' in input_nums[1:]:
            spaces = True
        else:
            spaces = False
            
        finalexp = shlex.split(input_nums)
        exp = finalexp[0]
        
        if not exp:
            return "this isn't a valid expression, %s. *FLUSH*" % (first_name.lower())
        elif re.search('[a-zA-Z]', exp):
            return "that's not maths, %s." % (first_name.lower())
        else:
            if spaces:
                bot.sendMessage(
                    chat_id=chat_id,
                    text=str(calculate(exp)) +
                    "\nnote: don't use spaces in your expression")
            else:
                return eval(exp)