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
        else:
            return ffxiv_class
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

def get_level_seventies(classes):
    level_seventies = "\n\nLevel 70s: "

    if classes.get('Gladiator').get('level') == 70:
        level_seventies += "Paladin, "
    if classes.get('Dark Knight').get('level') == 70:
        level_seventies += "Dark Knight, "
    if classes.get('Marauder').get('level') == 70:
        level_seventies += "Warrior, "
    if classes.get('Conjurer').get('level') == 70:
        level_seventies += "White Mage, "
    if classes.get('Astrologian').get('level') == 70:
        level_seventies += "Astrologian, "
    if classes.get('Arcanist').get('level') == 70:
        level_seventies += "Scholar, Summoner, "
    if classes.get('Thaumaturge').get('level') == 70:
        level_seventies += "Black Mage, "
    if classes.get('Lancer').get('level') == 70:
        level_seventies += "Dragoon, "
    if classes.get('Pugilist').get('level') == 70:
        level_seventies += "Monk, "
    if classes.get('Rogue').get('level') == 70:
        level_seventies += "Ninja, "
    if classes.get('Archer').get('level') == 70:
        level_seventies += "Bard, "
    if classes.get('Machinist').get('level') == 70:
        level_seventies += "Machinist, "
    if classes.get('Red Mage').get('level') == 70:
        level_seventies += "Red Mage, "
    if classes.get('Samurai').get('level') == 70:
        level_seventies += "Samurai, "
    if classes.get('Miner').get('level') == 70:
        level_seventies += "Miner, "
    if classes.get('Botanist').get('level') == 70:
        level_seventies += "Botanist, "
    if classes.get('Fisher').get('level') == 70:
        level_seventies += "Fisher, "
    if classes.get('Goldsmith').get('level') == 70:
        level_seventies += "Goldsmith, "
    if classes.get('Carpenter').get('level') == 70:
        level_seventies += "Carpenter, "
    if classes.get('Leatherworker').get('level') == 70:
        level_seventies += "Leatherworker, "
    if classes.get('Culinarian').get('level') == 70:
        level_seventies += "Culinarian, "
    if classes.get('Blacksmith').get('level') == 70:
        level_seventies += "Blacksmith, "
    if classes.get('Weaver').get('level') == 70:
        level_seventies += "Weaver, "
    if classes.get('Armorer').get('level') == 70:
        level_seventies += "Armorer, "

    return level_seventies[:-2] if level_seventies != "\n\nLevel 70s: " else ""


def ffxiv_char(first_name, last_name, server, full):
    try:
        scraped_data = FFXIVScraper()

        data = scraped_data.validate_character(server, "{} {}".format(first_name, last_name))
        if data:
            ret = scraped_data.scrape_character(data.get('lodestone_id'), full)
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


            if full:
                gender = ret.get('gender')
                nameday = ret.get('nameday')
                guardian = ret.get('guardian')
                citystate = ret.get('citystate')
                achievement_count = ret.get('achievement_count')
                achieve_one = ret.get('achieve_one')
                achieve_two = ret.get('achieve_two')
                achieve_three = ret.get('achieve_three')
                achievement_status = ret.get('achievement_status')

            character_info = "{}\n{}".format(img, name)
            character_info += " ({})".format(title) if title else ""

            if full:
                character_info += "\n{} ({}), {}\n".format(race, clan, gender)
                character_info += "{} (i{})\n".format(current_class, ilvl)
                character_info += "Weapon: {} (i{})\n\n".format(weapon, weapon_ilvl) 
                character_info += "Nameday: {}\n".format(nameday)
                character_info += "Guardian: {}\n".format(guardian)
                character_info += "City-state: {}\n".format(citystate)
            else:
                character_info += "\n{} ({})\n".format(race, clan)
                character_info += "{} (i{})\n".format(current_class, ilvl)
                character_info += "Weapon: {} (i{})\n\n".format(weapon, weapon_ilvl) 
            

         
            character_info += "Free Company: {}\n".format(fc) if fc else "No Free Company\n"

            if full:
                character_info += "Grand Company: {}".format(gc) if gc else "No Grand Company"
                character_info += get_level_sixties(classes)
                #character_info += get_level_seventies(classes)

                if "okay" in achievement_status:
                    character_info += "\n\nAchievements: {}\n".format(achievement_count)
                    character_info += "Latest Achievements:\n- {}\n- {}\n- {}".format(achieve_one, achieve_two, achieve_three)
                else:
                    character_info += "\n\n{}".format(achievement_status)

            else:
                character_info += "Grand Company: {}".format(gc.split('/')[0]) if gc else "No Grand Company"

            return character_info
        else:
            return "couldn't find character. usage: /char [first name] [last name] [server]"

    except DoesNotExist as AttributeError:
        return "couldn't find character. usage: /char [first name] [last name] [server]"
