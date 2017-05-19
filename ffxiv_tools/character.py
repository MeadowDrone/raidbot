#!/usr/bin/env python

from lodestone import FFXIVScraper, DoesNotExist
import json
import io

def get_job(ffxiv_class, is_jobbed):
    if is_jobbed == "Yes":
        if ffxiv_class == "Conjurer":
            return "White Mage"
        elif ffxiv_class == "Arcanist":
            return "Scholar"
        elif ffxiv_class == "Gladiator":
            return "Paladin"
        elif ffxiv_class == "Marauder":
            return "Warrior"
        elif ffxiv_class == "Thaumaturge":
            return "Black Mage"
        elif ffxiv_class == "Lancer":
            return "Dragoon"
        elif ffxiv_class == "Pugilist":
            return "Monk"
        elif ffxiv_class == "Rogue":
            return "Ninja"
        elif ffxiv_class == "Archer":
            return "Bard"
    elif is_jobbed == "SMN":
        return "Summoner"
    else:
        return ffxiv_class


def get_level_sixties(classes):
    level_sixties = "\n\nLevel 60s: "

    if classes.get('Gladiator').get('level') == 60:
        level_sixties += "Paladin, "
    if classes.get('Dark Knight').get('level') == 60:
        level_sixties += "Dark Knight, "
    if classes.get('Marauder').get('level') == 60:
        level_sixties += "Warrior, "
    if classes.get('Conjurer').get('level') == 60:
        level_sixties += "White Mage, "
    if classes.get('Astrologian').get('level') == 60:
        level_sixties += "Astrologian, "
    if classes.get('Arcanist').get('level') == 60:
        level_sixties += "Scholar, Summoner, "
    if classes.get('Thaumaturge').get('level') == 60:
        level_sixties += "Black Mage, "
    if classes.get('Lancer').get('level') == 60:
        level_sixties += "Dragoon, "
    if classes.get('Pugilist').get('level') == 60:
        level_sixties += "Monk, "
    if classes.get('Rogue').get('level') == 60:
        level_sixties += "Ninja, "
    if classes.get('Archer').get('level') == 60:
        level_sixties += "Bard, "
    if classes.get('Machinist').get('level') == 60:
        level_sixties += "Machinist, "
    if classes.get('Miner').get('level') == 60:
        level_sixties += "Miner, "
    if classes.get('Botanist').get('level') == 60:
        level_sixties += "Botanist, "
    if classes.get('Fisher').get('level') == 60:
        level_sixties += "Fisher, "
    if classes.get('Goldsmith').get('level') == 60:
        level_sixties += "Goldsmith, "
    if classes.get('Carpenter').get('level') == 60:
        level_sixties += "Carpenter, "
    if classes.get('Leatherworker').get('level') == 60:
        level_sixties += "Leatherworker, "
    if classes.get('Culinarian').get('level') == 60:
        level_sixties += "Culinarian, "
    if classes.get('Blacksmith').get('level') == 60:
        level_sixties += "Blacksmith, "
    if classes.get('Weaver').get('level') == 60:
        level_sixties += "Weaver, "
    if classes.get('Armorer').get('level') == 60:
        level_sixties += "Armorer, "

    return level_sixties[:-2] if level_sixties != "\n\nLevel 60s: " else ""
    #return level_sixties

def ffxiv_char(first_name, last_name, server):
    try:
        scraped_data = FFXIVScraper()

        data = scraped_data.validate_character(server, "%s %s" % (first_name, last_name))
        if data:
            ret = scraped_data.scrape_character(data.get('lodestone_id'))
            name = ret.get('name')
            title = ret.get('title')
            race = ret.get('race')
            clan = ret.get('clan')
            img = ret.get('portrait_url')
            jobbed = ret.get('jobbed')            
            current_class = get_job(ret.get('current_class'), jobbed)
            weapon = ret.get('weapon')
            weapon_ilvl = ret.get('weapon_ilvl')
            ilvl = ret.get('ilvl')
            fc = ret.get('free_company')
            gc = ret.get('grand_company', ["No grand company"])
            classes = ret.get('classes')

            return_string = "{}\n{}".format(img, name)
            return_string += " ({})".format(title) if title else ""
            return_string += "\n{} ({})\n".format(race, clan)            
            return_string += "{} (i{})\n".format(current_class, ilvl)
            return_string += "Weapon: {} (i{})\n\n".format(weapon, weapon_ilvl)            
            return_string += "{}\n".format(fc) if fc else "No Free Company\n"
            return_string += "{}".format(gc) if gc else "No Grand Company"
            return_string += get_level_sixties(classes)

            return return_string
        else:
            return "couldn't find character. usage: /char [first name] [last name] [server]"

    except DoesNotExist as AttributeError:
        return "couldn't find character. usage: /char [first name] [last name] [server]"
