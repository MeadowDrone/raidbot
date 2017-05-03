from werkzeug.urls import url_quote_plus
from gevent.pool import Pool
import bs4
import re
import requests
import math
import io


def strip_tags(html, invalid_tags):
    soup = bs4.BeautifulSoup(html, "html5lib")

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, bs4.NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)

    return soup


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
        self.lodestone_domain = 'na.finalfantasyxiv.com'
        self.lodestone_url = 'http://%s/lodestone' % self.lodestone_domain

    def validate_character(self, server_name, character_name):

        # Search for character
        url = self.lodestone_url + '/character/?q=%s&worldname=%s' \
                                   % (url_quote_plus(character_name), server_name)

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

    def scrape_character(self, lodestone_id):
        character_url = self.lodestone_url + '/character/%s/' % lodestone_id

        r = self.make_request(url=character_url)

        if not r:
            raise DoesNotExist()

        soup = bs4.BeautifulSoup(r.content, "html5lib")
        '''with open("data/soup.txt", "a") as soup_file:
            soup_file.write(str(soup))
        soup_file.close()'''
        character_link = '/lodestone/character/%s/' % lodestone_id

        for tag in soup.select('.frame__chara__link'):

            if character_link not in tag['href']:
                raise DoesNotExist()

        # Name, Server, Title
        name = soup.select('.frame__chara__name')[0].text
        server = soup.select('.frame__chara__world')[0].text

        try:
            title = soup.select('.frame__chara__title')[0].text.strip()
        except (AttributeError, IndexError):
            title = None

        # Race, Tribe, Gender
        race = soup.select('.character-block__name')[0].contents[0]
        clan, gender = soup.select('.character-block__name')[0].contents[2].split(' / ')
        gender = 'male' if gender.strip('\n\t')[-1] == u'\u2642' else 'female'

        # Nameday & Guardian
        '''nameday_text = soup.find(
            text='Nameday').parent.parent.select('dd')[1].text
        nameday = re.findall('(\d+)', nameday_text)
        nameday = {
            'sun': int(nameday[0]),
            'moon': (int(nameday[1]) * 2) - (0 if 'Umbral' in nameday_text else 1),
        }'''
        nameday = soup.select('.character-block__birth')[0].contents[0]
        guardian = soup.select('.character-block__name')[1].contents[0]

        # City-state
        citystate = soup.select('.character-block__name')[2].contents[0]

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
        #for tag in soup.select('.character__level__list'):
            #print(str(tag.li.span.img['data-tooltip']))

        for job_nm in range(0,23):
            class_ = soup.select('.character__job__name')[job_nm].contents[0]
            level = soup.select('.character__job__level')[job_nm].contents[0]

            if not class_:
                continue

            if level == '-':
                level = 0
            else:
                level = int(level)

            classes[class_] = dict(level=level)

        '''for tag in soup.select('.class_list .ic_class_wh24_box'):
            class_ = tag.text

            if not class_:
                continue

            level = tag.next_sibling.next_sibling.text

            if level == '-':
                level = 0
                exp = 0
                exp_next = 0
            else:
                level = int(level)
                exp = int(
                    tag.next_sibling.next_sibling.next_sibling.next_sibling.text.split(' / ')[0])
                exp_next = int(
                    tag.next_sibling.next_sibling.next_sibling.next_sibling.text.split(' / ')[1])

            classes[class_] = dict(level=level, exp=exp, exp_next=exp_next)'''

        # Stats
        '''stats = {}
        images = soup.select("img")

        for img in images:
            m = re.search(
                '/images/character/attribute_([a-z]{3})',
                img.get('src'))
            if m and m.group(1) and m.group(1) in (
                    'str', 'dex', 'vit', 'int', 'mnd', 'pie'):
                stats[m.group(1)] = img.parent.select("span")[0].text'''

        # Equipment
        current_class = None
        parsed_equipment = []
        total_ilevel = 0.0
        jobbed = "No"
        two_handed = False
        item_count = 0
        crystal_posns = []

        for i, tag in enumerate(soup.select('.popup_w412_body_gold')):
            weapon_tags = tag.select('.db-tooltip__item__category')
            item_tags = tag.select('.db-tooltip__item__name')

            # Current class
            if weapon_tags:
                if i == 0:
                    slot_name = weapon_tags[0].string.strip()
                    if 'Two-handed' in slot_name or '\'s Arm' in slot_name or'\'s Grimoire' in slot_name:
                        two_handed = True
                    if 'One-handed' in slot_name or 'Primary Tool' in slot_name or 'Gladiator' in slot_name:
                        two_handed = False
                    slot_name = slot_name.replace('Two-handed ', '')
                    slot_name = slot_name.replace('One-handed ', '')
                    slot_name = slot_name.replace("'s Arm", '')
                    slot_name = slot_name.replace("'s Primary Tool", '')
                    slot_name = slot_name.replace("'s Grimoire", '')
                    current_class = slot_name

            # Weapon name
            if item_tags:
                if i == 0:
                    weapon_details = item_tags[0]
                    weapon_name = str(weapon_details)
                    weapon_name = weapon_name[weapon_name.index(">") + 1:]
                    weapon_name = weapon_name[:weapon_name.index("<")]
                elif item_tags[0] == weapon_details:
                    break  # Character data contains duplicate items, so stop looking once the first dupe is found

                if "Soul of the Summoner" in str(item_tags):
                    jobbed = "SMN"
                    crystal_posns.append(i)
                elif "Soul of" in str(item_tags):
                    jobbed = "Yes"
                    crystal_posns.append(i)


        # Item Levels (weapon and character average)
        # crystal_posns is the slot number of the job crystal, which has dupes,
        # so use the position of the first instance to calculate number of
        # items equipped
        for i, tag in enumerate(soup.select('.db-tooltip__item__level')):
            if i < crystal_posns[0]:
                ilvl_string = str(tag)
                ilvl_string = ilvl_string[
                    ilvl_string.index("Item Level ") + 11:]
                ilvl_string = ilvl_string[:ilvl_string.index("<")]

                if i == 0:
                    weapon_ilvl = int(ilvl_string)

                total_ilevel += float(ilvl_string)

        if two_handed:
            total_ilevel += float(weapon_ilvl)

        ilevel = str(int(total_ilevel / 13))

        data = {
            'name': name,
            'server': server,
            'title': title,
            'race': race,
            'clan': clan,
            'gender': gender,
            'portrait_url': soup.select('.character__detail__image')[0].a['href'],
            'grand_company': grand_company,
            'free_company': free_company,
            'classes': classes,
            'current_class': current_class,
            'weapon': weapon_name,
            'weapon_ilvl': weapon_ilvl,
            'ilevel': ilevel,
            'jobbed': jobbed,
            #'legacy': len(soup.select('.bt_legacy_history')) > 0,
            #'avatar_url': soup.select('.player_name_txt .player_name_thumb img')[0]['src'],
            #'nameday': nameday,
            #'guardian': guardian,
            #'citystate': citystate,
        }

        return data
