import io
import random

def headcount_write(name, text):
    choices = ["gotcha.","recorded","alrighty","*flush*", "please look forward to it (or don't, i don't care)"]

    with open("/root/raidbot/data/headcount.txt", "r") as headcount_file:
        lines_check = headcount_file.readlines()

    with open("/root/raidbot/data/headcount.txt", "w") as headcount_file:
        for line in lines_check:
            if not line.startswith(name):
                headcount_file.write(line)

    with open("/root/raidbot/data/headcount.txt", "a") as headcount_file:
        if text.startswith("y"):
            headcount_file.write("%s: Attending\n" % (name))
        elif text.startswith("n"):
            headcount_file.write("%s: Not attending\n" % (name))

    return random.choice(choices)

def headcount_display():
    with open("/root/raidbot/data/headcount.txt", "r") as headcount_file:
        headcount_lines = headcount_file.readlines()

    headcount_str = ""
    for i in headcount_lines:
            headcount_str += i

    if headcount_str == "":
        return "headcount data is empty."
    else:
        return headcount_str

def headcount_new():
    with open("/root/raidbot/data/headcount.txt", "w") as headcount_file:
        headcount_file.seek(0)
        headcount_file.truncate()