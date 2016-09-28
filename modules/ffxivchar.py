#!/usr/bin/env python
'''
Usage:
  /char (<lodestone_id> | <server_name> <first_name> <last_name>)
  /char free_company <lodestone_id>
  /char verify <server_name> <first_name> <last_name> <key>
  /char validate <server_name> <first_name> <last_name>
  /char topics
  /char help
'''

from lodestone import FFXIVScraper, DoesNotExist
#from docopt import docopt
import json

def ffxiv_char(first_name, last_name, server):

    s = FFXIVScraper()

    try:
        data = s.validate_character(server, "%s %s" % (first_name, last_name))
        if data is not None:
            ret = s.scrape_character(data.get('lodestone_id'))
            
            name = ret.get('name')
            title = ret.get('title')
            race = ret.get('race')
            clan = ret.get('clan')
            gc = ret.get('grand_company')
            fc = ret.get('free_company').get('name')
            img = ret.get('portrait_url')
            classes = ret.get('classes') 
            level_sixties = "Level 60 Classes:\n"
            
            if classes.get('Gladiator').get('level') == 60:
                level_sixties += ("GLD, ")
            if classes.get('Dark Knight').get('level') == 60:
                level_sixties += ("DRK, ")
            if classes.get('Marauder').get('level') == 60:
                level_sixties += ("WAR, ")
            if classes.get('Conjurer').get('level') == 60:
                level_sixties += ("WHM, ")
            if classes.get('Astrologian').get('level') == 60:
                level_sixties += ("AST, ")
            if classes.get('Arcanist').get('level') == 60:
                level_sixties += ("SCH, SMN, ")
            if classes.get('Thaumaturge').get('level') == 60:
                level_sixties += ("BLM, ")
            if classes.get('Lancer').get('level') == 60:
                level_sixties += ("DRG, ")
            if classes.get('Pugilist').get('level') == 60:
                level_sixties += ("MNK, ")
            if classes.get('Rogue').get('level') == 60:
                level_sixties += ("NIN, ")
            if classes.get('Archer').get('level') == 60:
                level_sixties += ("BRD, ")
            if classes.get('Machinist').get('level') == 60:
                level_sixties += ("MCH, ")
            if classes.get('Miner').get('level') == 60:
                level_sixties += ("MNR, ")
            if classes.get('Botanist').get('level') == 60:
                level_sixties += ("BTN, ")
            if classes.get('Fisher').get('level') == 60:
                level_sixties += ("FSH, ")
            if classes.get('Goldsmith').get('level') == 60:
                level_sixties += ("GSM, ")
            if classes.get('Carpenter').get('level') == 60:
                level_sixties += ("CRP, ")
            if classes.get('Leatherworker').get('level') == 60:
                level_sixties += ("LTW, ")
            if classes.get('Culinarian').get('level') == 60:
                level_sixties += ("CUL, ")
            if classes.get('Blacksmith').get('level') == 60:
                level_sixties += ("BSM, ")
            if classes.get('Weaver').get('level') == 60:
                level_sixties += ("WVR, ")
            if classes.get('Armorer').get('level') == 60:
                level_sixties += ("ARM, ")
                
            if level_sixties != "":
                level_sixties = level_sixties[:-2]

            if title:
                # pic name title race clan fc, gc 60s 
                return_string = "%s\n-----------\n%s: %s\n-----------\n%s (%s)\n%s\n%s\n%s" % (
                        img, name, title, 
                        race, clan, 
                        fc, gc[0], level_sixties)
            else:
                # name fc race clan gc 60s pic
                return_string = "%s\n-----------\n%s\n-----------\n%s (%s)\n%s\n%s\n%s" % (
                        img, name, 
                        race, clan, 
                        fc, gc[0], level_sixties)
                
            return return_string
        else:
            return "couldn't find character. usage: /char [first name] [last name] [server]"

        '''if a.get('verify'):
            ret = s.verify_character(a['<server_name>'], "%s %s" % (a['<first_name>'], a['<last_name>']), a['<key>'])

        if a.get('validate'):
            ret = s.validate_character(a['<server_name>'], "%s %s" % (a['<first_name>'], a['<last_name>']))

        if a.get('char'):
            if a['<lodestone_id>']:
                ret = s.scrape_character(a['<lodestone_id>'])
            else:
                #data = s.validate_character(a['<server_name>'], "%s %s" % (a['<first_name>'], a['<last_name>']))
                data = s.validate_character(server, "%s %s" % (first_name, last_name))
                ret = s.scrape_character(data.get('lodestone_id'))
                print(str(ret))

        if a.get('free_company'):
            ret = s.scrape_free_company(a['<lodestone_id>'])

        if a.get('topics'):
            ret = s.scrape_topics()

        if ret:
            print json.dumps(ret, indent=4)'''

    except DoesNotExist, AttributeError:
        return "couldn't find character. usage: /char [first name] [last name] [server]"