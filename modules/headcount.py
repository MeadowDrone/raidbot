import io
import random

def headcount_write(name, text):
    yes_choices = ["HYPE","OMG SO HYPE","GET FUKEN HYPED SON","AAAAAAH I CAN'T WAIT", "YAY HYYYYYPE", "WE'RE GONNA CLEAR THIS SHIT SON", "\"PLEASE LOOK FORWARD TO IT???\" MY GOD YOU HAVE NO IDEA"]
    no_choices = ["gotcha.","recorded","i don't care, i'm just a toilet","*flush*", "seeya next time"]

    if name.lower() == "erika":
        alias = "Arelle Doomraix"
    elif name.lower() == "faissal":
        alias = "Black Swordsman"
    elif name.lower() == "una":
        alias = "Una Ventful"
    elif name.lower() == "velcio":
        alias = "Velcio Datari"
    elif name.lower() == "mymla":
        alias = "T'sun Dere"
    elif name.lower() == "nikita":
        alias = "Leone Larsefauceais"
    elif name.lower() == "andreas":
        alias = "Alethea Morne"
    elif name.lower() == "alexander":
        alias = "Hisa Moriyama"
    elif name.lower() == "bruce":
        alias = "Shevi Ventus"
    else:
        alias = "erika you borked %s's name FIX IT PLEASE" % (name)

    with open("/root/raidbot/data/headcount.txt", "r") as headcount_file:
        lines_check = headcount_file.readlines()

    with open("/root/raidbot/data/headcount.txt", "w") as headcount_file:
        for line in lines_check:
            print(line + " " + alias)
            if not line.startswith(alias):
                headcount_file.write(line)

    with open("/root/raidbot/data/headcount.txt", "a") as headcount_file:

        if text.startswith("y"):
            attending = "Attending"
            choices = yes_choices
        elif text.startswith("n"):
            attending = "Not Attending"
            choices = no_choices
            
        headcount_file.write("%s: %s\n" % (alias, attending))

    return random.choice(choices)

def headcount_display():
    with open("/root/raidbot/data/headcount.txt", "r") as headcount_file:
        headcount_lines = headcount_file.readlines()

    headcount_str = ""
    headcount_num = 0
    for i in headcount_lines:
            headcount_str += i
            if "Not" not in i:
            	headcount_num += 1.0

    hype_level = (headcount_num / 8.0) * 100.0
    headcount_str += "---\nhype levels at " + str(int(hype_level)) + "%!!!"
    if headcount_str == "":
        return "headcount data is empty."
    else:
        return headcount_str

def headcount_new():
    with open("/root/raidbot/data/headcount.txt", "w") as headcount_file:
        headcount_file.seek(0)
        headcount_file.truncate()