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

        # Equipment
        current_class = None
        parsed_equipment = []
        total_ilevel = 0.0
        jobbed = "No"
        two_handed = False
        item_count = 0
        len_gear = 0

        # Current class
        for i, tag in enumerate(soup.select('.db-tooltip__item__category')):
            if i > 0:
                break
            current_class = tag.string.strip()
            current_class = current_class.replace('Two-handed ', '').replace('One-handed ', '').replace("'s Arm", '')
            current_class = current_class.replace("'s Primary Tool", '').replace("'s Grimoire", '')
            print(current_class)

        # Weapon name and job status
        item_tags = []
        for i, tag in enumerate(soup.select('.db-tooltip__item__name')):
            if str(tag.string) != "None":
                item_tags.append(str(tag.string))

        weapon_name = item_tags[0]
        
        if "Soul of the Summoner" in item_tags:
            jobbed = "SMN"
        elif "Soul of" in item_tags:
            jobbed = "Yes"

        # Item Levels (weapon and character average)
        ilevel_tags = []
        for tag in soup.select('.db-tooltip__item__level'):
            ilevel_tags.append(str(tag))

        ilevel_list = ilevel_tags[0:(len(ilevel_tags)/2)-1]
        num_items = len(ilevel_list)

        for i, ilvl in enumerate(ilevel_list):
            
            ilvl = ilvl[ilvl.index("Item Level ") + 11:]
            ilvl = ilvl[:ilvl.index("<")]
            if i == 0:
                weapon_ilvl = int(ilvl)

            total_ilevel += float(ilvl)

        ave = int(round(total_ilevel / num_items))
        ilevel = str(ave)

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
