#!/usr/bin/env python

from lodestone import FFXIVScraper, DoesNotExist
import json
import io

def ffxiv_char(first_name, last_name, server):
    try:
        s = FFXIVScraper()
        
        data = s.validate_character(server, "%s %s" % (first_name, last_name))
        if data is not None:
            ret = s.scrape_character(data.get('lodestone_id'))
            with open("data/debug.txt", "a") as quote_file:
                   quote_file.write(str(ret))
            quote_file.close()
            
            name = ret.get('name')
            title = ret.get('title')
            race = ret.get('race')
            clan = ret.get('clan')
            img = ret.get('portrait_url')
            classes = ret.get('classes')
            if ret.get('free_company') is not None:
                fc = ret.get('free_company').get('name')
            else:
                fc = "No Free Company"
            if ret.get('grand_company') is not None:
                gc = ret.get('grand_company')
            else:
                gc = ["No Grand Company"]
                
            current_class = ret.get('current_class')
            weapon = ret.get('weapon')
            weapon_ilvl = ret.get('weapon_ilvl')
            ilevel = ret.get('ilevel')
            jobbed = ret.get('jobbed')
            
            if jobbed == "Yes":
                if current_class == "Conjurer":
                    current_class = "White Mage"
                elif current_class == "Arcanist":
                    current_class = "Scholar"
                elif current_class == "Gladiator":
                    current_class = "Paladin"
                elif current_class == "Marauder":
                    current_class = "Warrior"
                elif current_class == "Thaumaturge":
                    current_class = "Black Mage"
                elif current_class == "Lancer":
                    current_class = "Dragoon"
                elif current_class == "Pugilist":
                    current_class = "Monk"
                elif current_class == "Rogue":
                    current_class = "Ninja"
                elif current_class == "Archer":
                    current_class = "Bard"
            elif jobbed == "SMN":
                current_class = "Summoner"
            
            level_sixties = "Level 60 Classes: "            
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
                
            if level_sixties != "Level 60 Classes: ":
                level_sixties = level_sixties[:-2]
            else:
                level_sixties = ""

            if title:
                # pic name title race clan fc, gc 60s 
                return_string = "%s\n%s (%s)\n%s (i%s)\nWeapon: %s (i%s)\n\n%s (%s)\n%s\n%s\n\n%s" % (
                        img, name, title, current_class, ilevel, weapon, weapon_ilvl, 
                        race, clan, 
                        fc, gc[0], level_sixties)
            else:
                # name fc race clan gc 60s pic
                return_string = "%s\n%s\n%s (i%s)\nWeapon: %s (i%s)\n\n%s (%s)\n%s\n%s\n\n%s" % (
                        img, name, current_class, ilevel, weapon, weapon_ilvl,
                        race, clan, 
                        fc, gc[0], level_sixties)
                
            return return_string
        else:
            return "couldn't find character. usage: /char [first name] [last name] [server]"

    except DoesNotExist, AttributeError:
        return "couldn't find character. usage: /char [first name] [last name] [server]"