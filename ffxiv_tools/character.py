#!/usr/bin/env python

from lodestone import FFXIVScraper, DoesNotExist
import json
import io


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
            classes = ret.get('classes')
            current_class = ret.get('current_class')
            weapon = ret.get('weapon')
            weapon_ilvl = ret.get('weapon_ilvl')
            ilevel = ret.get('ilevel')
            jobbed = ret.get('jobbed')
            fc = ret.get('free_company')
            gc = ret.get('grand_company', ["No grand company"])

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

            level_sixties = level_sixties[:-2] if level_sixties != "\n\nLevel 60s: " else ""

            if title:
                return_string = "%s\n%s (%s)\n%s (i%s)\nWeapon: %s (i%s)\n\n%s (%s)\n%s\n%s%s" % (
                    img,
                    name, title,
                    current_class, ilevel,
                    weapon, weapon_ilvl,
                    race, clan,
                    fc, gc,
                    level_sixties)
            else:
                return_string = "%s\n%s\n%s (i%s)\nWeapon: %s (i%s)\n\n%s (%s)\n%s\n%s%s" % (
                    img,
                    name,
                    current_class, ilevel,
                    weapon, weapon_ilvl,
                    race, clan,
                    fc, gc,
                    level_sixties)

            return return_string
        else:
            return "couldn't find character. usage: /char [first name] [last name] [server]"

    except DoesNotExist as AttributeError:
        return "couldn't find character. usage: /char [first name] [last name] [server]"
