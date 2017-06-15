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

def ffxiv_char(first_name, last_name, server):
    try:
        scraped_data = FFXIVScraper()

        data = scraped_data.validate_character(server, "{} {}".format(first_name, last_name))

        if data:
            if str(type(data)) == "<type 'str'>":
                return data
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
            gender = ret.get('gender')
            nameday = ret.get('nameday')
            guardian = ret.get('guardian')
            citystate = ret.get('citystate')
            achievement_count = ret.get('achievement_count')
            achieve_names = ret.get('achieve_names')
            achieve_descs = ret.get('achieve_descs')
            achievements_enabled = ret.get('achievements_enabled')

            character_info = "{}\n{}".format(img, name)
            character_info += " ({})".format(title) if title else ""
            character_info += "\n{} ({}), {}\n".format(race, clan, gender)
            character_info += "{} (i{})\n".format(current_class, ilvl)
            character_info += "Weapon: {} (i{})\n\n".format(weapon, weapon_ilvl) 
            character_info += "Nameday: {}\n".format(nameday)
            character_info += "Guardian: {}\n".format(guardian)
            character_info += "City-state: {}\n".format(citystate)         
            character_info += "Free Company: {}\n".format(fc) if fc else "No Free Company\n"
            character_info += "Grand Company: {}".format(gc) if gc else "No Grand Company"
            character_info += get_level_seventies(classes)

            if achievements_enabled:
                character_info += "\n\nAchievements: {}\n".format(achievement_count)
                character_info += "Latest Achievements:\n"
                for i, achievement in enumerate(achieve_names):
                    character_info += "- {} ({})\n".format(achievement, achieve_descs[i])
            else:
                character_info += "\n\nAchievements page disabled. You can enable permissions here: " + \
                "http://na.finalfantasyxiv.com/lodestone/my/setting/account/"

            return character_info
        else:
            return "couldn't find character. usage: /char [first name] [last name] [server]"

    except DoesNotExist as AttributeError:
        return "couldn't find character. usage: /char [first name] [last name] [server]"


def ffxiv_achievements(first_name, last_name, server, count):
    try:
        scraped_data = FFXIVScraper()
        data = scraped_data.validate_character(server, "{} {}".format(first_name, last_name))

        if data:
            if str(type(data)) == "<type 'str'>":
                return data
            ret = scraped_data.scrape_achievements(data.get('lodestone_id'), count)

            name = "{} {}".format(first_name, last_name)
            achievement_count = ret.get('achievement_count')
            achieve_names = ret.get('achieve_names')
            achieve_descs = ret.get('achieve_descs')
            achievement_status = ret.get('achievement_status')

            achievement_info = "{}'s Achievements\n".format(name.title())
            if "okay" in achievement_status:
                achievement_info += "Achievements Earned: {}\n\n".format(achievement_count)
                achievement_info += "Latest {} Achievements:\n".format(count)
                for i, achievement in enumerate(achieve_names):
                    achievement_info += "-- {}\n{}\n".format(achievement, achieve_descs[i])
            else:
                achievement_info += achievement_status

            return achievement_info

    except DoesNotExist as AttributeError:
        return "couldn't find character. usage: /char [first name] [last name] [server]"


def ffxiv_item(item_name):
    try:
        scraped_data = FFXIVScraper()
        data = scraped_data.scrape_item(item_name)
        if str(type(data)) == "<type 'str'>":
            return data

        name = data.get('name')
        item_type = data.get('type')
        subtype = data.get('subtype')
        description = data.get('description')
        ilevel = data.get('ilevel')
        ilevel_req = data.get('ilevel_req')
        item_classes = data.get('item_classes')
        stat_1_name = data.get('stat_1_name')
        stat_2_name = data.get('stat_2_name')
        stat_3_name = data.get('stat_3_name')
        stat_1_num = data.get('stat_1_num')
        stat_2_num = data.get('stat_2_num')
        stat_3_num = data.get('stat_3_num')
        nq_effect = data.get('nq_effect')
        hq_effect = data.get('hq_effect')
        bonuses = data.get('bonuses')
        icon = data.get('icon')
        photo = data.get('photo')

        if item_type == "Arms" or item_type == "Tools":

            item_text = "{}\n{}\n".format(name, subtype)

            if description != "":
                item_text += "{}\n\n".format(description)

            item_text += "{}\n{}\n\n".format(ilevel, ilevel_req)
            item_text += "{}: {}\n".format(stat_1_name, stat_1_num)
            item_text += "{}: {}\n".format(stat_2_name, stat_2_num)
            item_text += "{}: {}\n\n".format(stat_3_name, stat_3_num)
            if len(bonuses) > 0:
                item_text += "Bonuses:\n"
                for bonus in bonuses:
                    item_text += "{}\n".format(bonus)

        elif item_type == "Armor" or item_type == "Accessories":

            item_text = "{}\n{}\n".format(name, subtype)
            if description != "":
                item_text += "{}\n\n".format(description)

            item_text += "{}\n{}\n\n".format(ilevel, ilevel_req)

            if item_type == "Armor":
                item_text += "{}: {}\n{}: {}\n\n".format(stat_1_name, stat_1_num, stat_2_name, stat_2_num)
            if len(bonuses) > 0:
                item_text += "Bonuses:\n"
                for bonus in bonuses:
                    item_text += "{}\n".format(bonus)

        elif "Medicines" in item_type:
            item_text = "{}\n{}\n".format(name, subtype)            
            if subtype == "Medicine":
                item_text += "Effect: {}\n\n".format(nq_effect)
                item_text += "{}: {}\n".format(stat_1_name, stat_1_num)
                item_text += "{}\n".format(description)
            else:
                item_text += "Effect (NQ):\n{}\n\n".format(nq_effect)
                item_text += "Effect (HQ):\n{}\n\n".format(hq_effect)
                item_text += "{}\n".format(description)

        item_text += icon

        item_all = [item_text, photo]
        return item_all

    except DoesNotExist as AttributeError:
        return "couldn't find item."

