from werkzeug.urls import url_quote_plus
import bs4
import re
import requests


class DoesNotExist(Exception):
    pass


class Scraper(object):

    def __init__(self):
        self.s = requests.Session()

    def update_headers(self, headers):
        self.s.headers.update(headers)

    def make_request(self, url=None):
        return self.s.get(url)


class FFXIVScraper(Scraper):

    def __init__(self):
        super(FFXIVScraper, self).__init__()
        headers = {
            'Accept-Language': 'en-us,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) Chrome/27.0.1453.116 Safari/537.36',
        }
        self.update_headers(headers)
        self.lodestone_url = 'http://eu.finalfantasyxiv.com/lodestone'

    def validate_character(self, server_name, character_name):
        # Search for character
        url = self.lodestone_url + '/character/?q={}&worldname={}'.format(
                                   url_quote_plus(character_name), server_name)

        r = self.make_request(url=url)

        if not r:
            return None

        soup = bs4.BeautifulSoup(r.content, "html5lib")
        
        for tag in soup.select('.entry'):
            char_name = str(tag.p.contents[0])
            if str(tag.p.contents[0]).lower() == character_name.lower():
                return {
                    'lodestone_id': re.findall(r'(\d+)', str(tag.a['href']))[0],
                    'name': char_name,
                }

        return None

    def scrape_achievements(self, lodestone_id, count):
        achievement_url = self.lodestone_url + '/character/{}/achievement/'.format(lodestone_id)
        r = self.make_request(url=achievement_url)
        achievement_soup = bs4.BeautifulSoup(r.content, "html5lib")

        achieve_names = []
        achieve_descs = []
        achievement_count = ""

        if "You do not have permission" not in str(achievement_soup):
            achievement_status = "okay"

            # Total number of achievements
            achievement_count = achievement_soup.select('.parts__total')[0].contents[0]
            achievement_count = achievement_count[:achievement_count.index(' ')]

            achieve_ids = []
            achieve_urls = []
            achieve_name = ""


            for i in range(0,int(count)+1):
                achieve_ids.append(achievement_soup.select('.entry__achievement')[i]['href'])
                achieve_urls.append("http://eu.finalfantasyxiv.com{}".format(achieve_ids[i]))

                achieve_name = achievement_soup.select('.entry__activity__txt')[i].contents[0]
                achieve_names.append(achieve_name[achieve_name.index('"')+1:achieve_name.rfind('"')])

            achievement_soup.decompose()

            # Achievement descriptions
            for i in range(0,int(count)+1):
                r = self.make_request(url=achieve_urls[i])
                achieve_desc_soup = bs4.BeautifulSoup(r.content, "html5lib")
                achieve_descs.append(achieve_desc_soup.select('.achievement__base--text')[0].contents[0])
                achieve_desc_soup.decompose()

        else:
            achievement_status = "Achievements page disabled. You can enable permissions here: http://na.finalfantasyxiv.com/lodestone/my/setting/account/"

        data = {
            'achievement_status': achievement_status,
            'achievement_count': achievement_count,
            'achieve_names': achieve_names,
            'achieve_descs': achieve_descs
        }

        return data

    def scrape_item(self, item_name):
        item_url = "http://eu.finalfantasyxiv.com/lodestone/playguide/db/item/?patch=&db_search_category=item&category2=&q="
        item_name = '+'.join(item_name.split(' '))

        item_url += item_name
        r = self.make_request(url=item_url)
        item_soup = bs4.BeautifulSoup(r.content, "html5lib")

        if "The search did not return any results" in str(item_soup):
            return "can't find that item."

        item_name = item_soup.select('.db-table__txt--detail_link')[0].text
        item_id = str(item_soup.select('.db-table__txt--detail_link')[0])
        item_id = item_id[82:item_id.rfind('?')-1]
        item_soup.decompose()

        item_url = "http://eu.finalfantasyxiv.com/lodestone/playguide/db/item/{}/".format(item_id)
        r = self.make_request(url=item_url)
        item_soup = bs4.BeautifulSoup(r.content, "html5lib")
        '''with open("data/foodsoup.txt", "a") as soup_file:
            soup_file.write(str(item_soup))
        soup_file.close()'''
        #item_pic = str(item_soup.select('.sys_nq_element')[0])
        item_pic = item_soup.find("img", {"class":"db-view__item__icon__item_image sys_nq_element"})['src']

        has_photo = str(item_soup.find("a", {"href":"#tab2"}))
        has_photo = has_photo[24:has_photo.rfind(')')]
        has_photo = True if int(has_photo) > 0 else False
        item_photo = ""
        if has_photo:
            item_photo = str(item_soup.find("a", {"class":"fancybox_element"})['href'])

        if item_soup.select('.db-view__help_text'):
            description = item_soup.select('.db-view__help_text')[0].text
            description = description.strip()
        elif item_soup.select('.db-view__info_text'):
            description = item_soup.select('.db-view__info_text')[0].text
            description = description.strip()
        else:
            description = ""

        item_type = item_soup.select('.breadcrumb__link')[3].text
        item_subtype = item_soup.select('.breadcrumb__link')[4].text
        item_pic = item_soup.find("img", {"class":"db-view__item__icon__item_image sys_nq_element"})['src']

        if item_type == "Arms" or item_type == "Tools":
            item_level = item_soup.select('.db-view__item_level')[0].text
            item_classes = item_soup.select('.db-view__item_equipment__class')[0].text
            item_level_req = item_soup.select('.db-view__item_equipment__level')[0].text
            physical_dmg = item_soup.select('.db-view__item_spec__value')[0].text
            auto_attack = item_soup.select('.db-view__item_spec__value')[1].text
            delay = item_soup.select('.db-view__item_spec__value')[2].text

            bonuses = []
            if item_soup.select('.db-view__basic_bonus'):
                bonuses_raw = str(item_soup.select('.db-view__basic_bonus')[0].text)
                for line in bonuses_raw.split('\n'):
                    line = line.strip()
                    if line != "":
                        bonuses.append(line.strip())

            data = {
                'name': item_name,
                'type': item_type,
                'subtype': item_subtype,
                'description': description,
                'ilevel': item_level,
                'ilevel_req': item_level_req,
                'physical_dmg': physical_dmg,
                'auto_attack': auto_attack,
                'delay': delay,
                'bonuses': bonuses,
                'icon': item_pic,
                'photo': item_photo
            }

            return data
        elif item_type == "Armor":
            item_level = item_soup.select('.db-view__item_level')[0].text
            item_classes = item_soup.select('.db-view__item_equipment__class')[0].text
            item_level_req = item_soup.select('.db-view__item_equipment__level')[0].text

            if item_subtype == "Shield":
                stat_1 = "Block Strength"
                stat_2 = "Block Rate"
            else:
                stat_1 = "Defence"
                stat_2 = "Magic Defence"

            stat_1_num = item_soup.select('.db-view__item_spec__value')[0].text
            stat_2_num = item_soup.select('.db-view__item_spec__value')[1].text

            bonuses = []
            if item_soup.select('.db-view__basic_bonus'):
                bonuses_raw = str(item_soup.select('.db-view__basic_bonus')[0].text)
                for line in bonuses_raw.split('\n'):
                    line = line.strip()
                    if line != "":
                        bonuses.append(line.strip())

            data = {
                'name': item_name,
                'type': item_type,
                'subtype': item_subtype,
                'description': description,
                'ilevel': item_level,
                'ilevel_req': item_level_req,
                'stat_1': stat_1,
                'stat_2': stat_2,
                'stat_1_num': stat_1_num,
                'stat_2_num': stat_2_num,
                'bonuses': bonuses,
                'icon': item_pic,
                'photo': item_photo
            }

            return data
        elif item_type == "Accessories":            
            item_level = item_soup.select('.db-view__item_level')[0].text
            item_classes = item_soup.select('.db-view__item_equipment__class')[0].text
            item_level_req = item_soup.select('.db-view__item_equipment__level')[0].text
                
            bonuses = []
            if item_soup.select('.db-view__basic_bonus'):
                bonuses_raw = str(item_soup.select('.db-view__basic_bonus')[0].text)
                for line in bonuses_raw.split('\n'):
                    line = line.strip()
                    if line != "":
                        bonuses.append(line.strip())

            data = {
                'name': item_name,
                'type': item_type,
                'subtype': item_subtype,
                'description': description,
                'ilevel': item_level,
                'ilevel_req': item_level_req,
                'bonuses': bonuses,
                'icon': item_pic,
                'photo': item_photo
            }

            return data
        elif "Medicines" in item_type:

            if item_subtype == "Medicine":
                recast_time = str(item_soup.find("div", {"class":"db-view__item_spec__value"}).text).strip()
                nq_effect = str(item_soup.find("ul", {"class":"sys_nq_element"}).text).strip()
                nq_effect = nq_effect.replace('\t','').replace('\n','')
                hq_effect = ""
                description = description.replace('.Restores', '. Restores')
            else:
                nq_effect = str(item_soup.find("ul", {"class":"sys_nq_element"}).text).strip()
                nq_effect = nq_effect.replace('\t','').replace('\n','')
                nq_effect = nq_effect.replace(')',')\n')[:-1]
                hq_effect = str(item_soup.find("ul", {"class":"sys_nq_element"}).text).strip()
                hq_effect = hq_effect.replace('\t','').replace('\n','')
                hq_effect = hq_effect.replace(')',')\n')[:-1]
                recast_time = ""
                description = str(item_soup.select('.db-view__info_text')[1].text).strip()
                description = description.replace('EXP','\nEXP').replace(' Duration','\nDuration').replace('(Duration',' (Duration')

                for links in item_soup.select('.db-table__txt--detail_link'):
                    links = str(links)
                    if "recipe" in links:
                        recipe_url = 'http://eu.finalfantasyxiv.com/lodestone/playguide/db/'
                        recipe_url = recipe_url + links[links.find('recipe/'):]
                        recipe_url = recipe_url[:recipe_url.rfind('/">')]
                        print(recipe_url)

                '''for tag in item_soup.select('.db-view__data__reward__item__name__wrapper'):
                    print(str(tag))'''
                #print(str(item_soup.select('.db-view__data__reward__item__name__wrapper')))


            data = {
                'name': item_name,
                'type': item_type,
                'subtype': item_subtype,
                'nq_effect': nq_effect,
                'hq_effect': hq_effect,
                'description': description,
                'recast_time': recast_time,
                'icon': item_pic,
                'photo': item_photo
            }
            return data
        elif item_type == "Materials":
            return "WIP"
        elif item_type == "Other":
            return "WIP"

    def scrape_character(self, lodestone_id):
        character_url = self.lodestone_url + '/character/{}/'.format(lodestone_id)
        r = self.make_request(url=character_url)
        soup = bs4.BeautifulSoup(r.content, "html5lib")

        if not r:
            raise DoesNotExist()

        soup = bs4.BeautifulSoup(r.content, "html5lib")
        character_link = '/lodestone/character/{}/'.format(lodestone_id)

        # For debugging/lodestone updates: write entire soup data to file
        '''with open("data/soup.txt", "a") as soup_file:
            soup_file.write(str(soup))
        soup_file.close()'''

        for tag in soup.select('.frame__chara__link'):
            if character_link not in tag['href']:
                raise DoesNotExist()

        # Picture
        portrait_url = soup.select('.character__detail__image')[0].a['href']
        #portrait_url = portrait_url[:portrait_url.index('?')]

        # Name, Server, Title
        name = soup.select('.frame__chara__name')[0].text
        server = soup.select('.frame__chara__world')[0].text

        try:
            title = soup.select('.frame__chara__title')[0].text.strip()
        except (AttributeError, IndexError):
            title = None

        # Race, Clan, Gender
        race = soup.select('.character-block__name')[0].contents[0]
        clan, gender = soup.select('.character-block__name')[0].contents[2].split(' / ')
        if gender.strip('\n\t')[-1] == u'\u2642':
            gender = u'\u2642'.encode('utf-8')
        else:
            gender = u'\u2640'.encode('utf-8')
        #gender = 'Male' if gender.strip('\n\t')[-1] == u'\u2642' else 'Female'

        # Grand Company
        try:
            grand_company = soup.select('.character-block__name')[3].contents[0]
        except (AttributeError, IndexError):
            grand_company = None

        # Free Company
        try:
            free_company = soup.select('.character__freecompany__name')[0].h4.a.contents[0]
        except (AttributeError, IndexError):
            free_company = None

        # Classes
        classes = {}
        for job_nm in range(0,23):
            ffxiv_class = soup.select('.character__job__name')[job_nm].contents[0]
            level = soup.select('.character__job__level')[job_nm].contents[0]

            if not ffxiv_class:
                continue

            level = 0 if level == '-' else int(level)
            classes[ffxiv_class] = dict(level=level)

        # Current class
        weapon_html = soup.select('.db-tooltip__item__category')[0]
        current_class = weapon_html.string.strip()
        current_class = current_class.replace('Two-handed ', '').replace('One-handed ', '').replace("'s Arm", '')
        current_class = current_class.replace("'s Primary Tool", '').replace("'s Grimoire", '')

        # Weapon name
        equipped_gear = []
        for i, tag in enumerate(soup.select('.db-tooltip__item__name')):
            equipped_gear.append(tag.text)
        
        # Job crystal status
        if "Soul of the Summoner" in '\t'.join(equipped_gear):
            jobbed = "SMN"
        elif "Soul of" in '\t'.join(equipped_gear):
            jobbed = "Yes"
        else:
            jobbed = "No"

        # Item Level
        total_ilvl = 0.0
        ilvl_list = []
        for tag in soup.select('.db-tooltip__item__level'):
            ilvl_list.append(tag.text.strip()[11:])

        # Lodestone HTML contains all equipment twice, so half list size.
        ilvl_list = ilvl_list[0:(len(ilvl_list)/2)]

        # Removes job crystal from ilvl calculation
        if jobbed != "No":
            del ilvl_list[-1]

        for gear_ilvl in ilvl_list:
            total_ilvl += float(gear_ilvl)

        ilvl = str(int(round(total_ilvl / len(ilvl_list))))

        nameday = soup.select('.character-block__birth')[0].contents[0]
        guardian = soup.select('.character-block__name')[1].contents[0]
        citystate = soup.select('.character-block__name')[2].contents[0]

        achievement_url = self.lodestone_url + '/character/{}/achievement/'.format(lodestone_id)
        r = self.make_request(url=achievement_url)
        achievement_soup = bs4.BeautifulSoup(r.content, "html5lib")

        # For debugging/lodestone updates: write entire soup data to file
        '''with open("data/ach_soup.txt", "a") as soup_file:
            soup_file.write(str(achievement_soup))
        soup_file.close()'''

        achieve_names = []
        achieve_descs = []
        achievement_count = ""

        if "You do not have permission" not in str(achievement_soup):
            achievements_enabled = True

            # Total number of achievements
            achievement_count = achievement_soup.select('.parts__total')[0].contents[0]
            achievement_count = achievement_count[:achievement_count.index(' ')]

            achieve_ids = []
            achieve_urls = []
            achieve_name = ""


            for i in range(0,3):
                achieve_ids.append(achievement_soup.select('.entry__achievement')[i]['href'])
                achieve_urls.append("http://eu.finalfantasyxiv.com{}".format(achieve_ids[i]))

                achieve_name = achievement_soup.select('.entry__activity__txt')[i].contents[0]
                achieve_names.append(achieve_name[achieve_name.index('"')+1:achieve_name.rfind('"')])

            achievement_soup.decompose()

            # Achievement descriptions
            for i in range(0,3):
                r = self.make_request(url=achieve_urls[i])
                achieve_desc_soup = bs4.BeautifulSoup(r.content, "html5lib")
                achieve_descs.append(achieve_desc_soup.select('.achievement__base--text')[0].contents[0])
                achieve_desc_soup.decompose()

        else:
            achievements_enabled = False

        data = {
            'name': name,
            'server': server,
            'title': title,
            'race': race,
            'clan': clan,
            'portrait_url': portrait_url,
            'grand_company': grand_company,
            'free_company': free_company,
            'classes': classes,
            'current_class': current_class,
            'weapon': equipped_gear[0],
            'weapon_ilvl': ilvl_list[0],
            'ilvl': ilvl,
            'jobbed': jobbed,
            'gender': gender,
            'nameday': nameday,
            'guardian': guardian,
            'citystate': citystate,
            'achievements_enabled': achievements_enabled,
            'achievement_count': achievement_count,
            'achieve_names': achieve_names,
            'achieve_descs': achieve_descs
        }

        return data
