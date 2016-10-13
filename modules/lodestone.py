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

    def scrape_topics(self):
        url = self.lodestone_url + '/topics/'
        r = self.make_request(url)

        news = []
        soup = bs4.BeautifulSoup(r.content, "html5lib")
        for tag in soup.select('.topics_list li'):
            entry = {}
            title_tag = tag.select('.topics_list_inner a')[0]
            script = str(tag.select('script')[0])
            entry['timestamp'] = int(re.findall(r"1[0-9]{9},", script)[0].rstrip(','))
            entry['link'] = '//' + self.lodestone_domain + title_tag['href']
            entry['id'] = entry['link'].split('/')[-1]
            entry['title'] = title_tag.string.encode('utf-8').strip()
            body = tag.select('.area_inner_cont')[0]
            for a in body.findAll('a'):
                if a['href'].startswith('/'):
                    a['href'] = '//' + self.lodestone_domain + a['href']
            entry['body'] = body.encode('utf-8').strip()
            entry['lang'] = 'en'
            news.append(entry)
        return news

    def validate_character(self, server_name, character_name):

        # Search for character
        url = self.lodestone_url + '/character/?q=%s&worldname=%s' \
                                   % (url_quote_plus(character_name), server_name)

        r = self.make_request(url=url)

        if not r:
            return None

        soup = bs4.BeautifulSoup(r.content, "html5lib")

        for tag in soup.select('.player_name_area .player_name_gold a'):
            if tag.string.lower() == character_name.lower():
                return {
                    'lodestone_id': re.findall(r'(\d+)', tag['href'])[0],
                    'name': str(tag.string),
                    }

        return None

    def verify_character(self, server_name, character_name, verification_code, lodestone_id=None):
        if not lodestone_id:
            char = self.validate_character(server_name, character_name)
            if not char:
                raise DoesNotExist()
            lodestone_id = char['lodestone_id']

        url = self.lodestone_url + '/character/%s/' % lodestone_id

        r = self.make_request(url=url)

        if not r:
            return False

        soup = bs4.BeautifulSoup(r.content, "html5lib")

        page_name = soup.select('.player_name_txt h2 a')[0].text
        page_server = soup.select('.player_name_txt h2 span')[0].text
        page_name = page_name.strip()
        page_server = page_server.strip()[1:-1]

        if page_name != character_name or page_server != server_name:
            print "%s %s" % (page_name, page_server)
            print "Name mismatch"
            return False

        return lodestone_id if soup.select('.txt_selfintroduction')[0].text.strip() == verification_code else False

    def scrape_character(self, lodestone_id):
        character_url = self.lodestone_url + '/character/%s/' % lodestone_id

        r = self.make_request(url=character_url)

        if not r:
            raise DoesNotExist()

        soup = bs4.BeautifulSoup(r.content, "html5lib")
        
        character_link = '/lodestone/character/%s/' % lodestone_id
        if character_link not in soup.select('.player_name_thumb a')[0]['href']:
            raise DoesNotExist()

        # Name, Server, Title
        name = soup.select('.player_name_txt h2 a')[0].text.strip()
        server = soup.select('.player_name_txt h2 span')[0].text.strip()[1:-1]

        try:
            title = soup.select('.chara_title')[0].text.strip()
        except (AttributeError, IndexError):
            title = None

        # Race, Tribe, Gender
        race, clan, gender = soup.select('.chara_profile_title')[0].text.split(' / ')
        gender = 'male' if gender.strip('\n\t')[-1] == u'\u2642' else 'female'

        # Nameday & Guardian
        nameday_text = soup.find(text='Nameday').parent.parent.select('dd')[1].text
        nameday = re.findall('(\d+)', nameday_text)
        nameday = {
            'sun': int(nameday[0]),
            'moon': (int(nameday[1]) * 2) - (0 if 'Umbral' in nameday_text else 1),
            }
        guardian = soup.find(text='Guardian').parent.parent.select('dd')[3].text

        # City-state
        citystate = soup.find(text=re.compile('City-state')).parent.parent.select('dd.txt_name')[0].text

        # Grand Company
        try:
            grand_company = soup.find(text=re.compile('Grand Company')).parent.parent.select('.txt_name')[0].text.split('/')
        except (AttributeError, IndexError):
            grand_company = None

        # Free Company
        try:
            free_company = None
            for elem in soup.select('.chara_profile_box_info'):
                if 'Free Company' in elem.text:
                    fc = elem.select('a.txt_yellow')[0]
                    free_company = {
                        'id': re.findall('(\d+)', fc['href'])[0],
                        'name': fc.text,
                        'crest': [x['src'] for x in elem.find('div', attrs={'class': 'ic_crest_32'}).findChildren('img')]
                    }
                    break
        except (AttributeError, IndexError):
            free_company = None

        # Classes
        classes = {}
        for tag in soup.select('.class_list .ic_class_wh24_box'):
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
                exp = int(tag.next_sibling.next_sibling.next_sibling.next_sibling.text.split(' / ')[0])
                exp_next = int(tag.next_sibling.next_sibling.next_sibling.next_sibling.text.split(' / ')[1])

            classes[class_] = dict(level=level, exp=exp, exp_next=exp_next)

        # Stats
        stats = {}

        images = soup.select("img")

        for img in images:
            m = re.search('/images/character/attribute_([a-z]{3})', img.get('src'))
            if m and m.group(1) and m.group(1) in ('str', 'dex', 'vit', 'int', 'mnd', 'pie'):
                stats[m.group(1)] = img.parent.select("span")[0].text

        # Equipment
        current_class = None
        parsed_equipment = []
        total_ilevel = 0.0
        jobbed = "No"
        item_count = 0
        crystal_posns = []
        
        for i, tag in enumerate(soup.select('.popup_w412_body_gold')):
            item_tags = tag.select('.db-tooltip__item__category')

            if item_tags:
                if i == 0:
                    slot_name = item_tags[0].string.strip()
                    slot_name = slot_name.replace('Two-handed ', '')
                    slot_name = slot_name.replace('One-handed ', '')
                    slot_name = slot_name.replace("'s Arm", '')
                    slot_name = slot_name.replace("'s Primary Tool", '')
                    slot_name = slot_name.replace("'s Grimoire", '')
                    current_class = slot_name
                
        for i, tag in enumerate(soup.select('.popup_w412_body_gold')):
            item_tags = tag.select('.db-tooltip__item__name')
            if item_tags:
                if i == 0:
                    weapon_details = item_tags[0]
                    weapon_name = str(weapon_details)
                    weapon_name = weapon_name[weapon_name.index(">")+1:]
                    weapon_name = weapon_name[:weapon_name.index("<")]
                elif item_tags[0] == weapon_details:
                    break
                    
                if "Soul of the Summoner" in str(item_tags):
                    jobbed = "SMN"
                elif "Soul of" in str(item_tags):
                    jobbed = "Yes"
                    crystal_posns.append(i)
                    
        for i, tag in enumerate(soup.select('.db-tooltip__item__level')):
            if i < crystal_posns[0]:
                ilvl_string = str(tag)
                ilvl_string = ilvl_string[ilvl_string.index("Item Level ")+11:]
                ilvl_string = ilvl_string[:ilvl_string.index("<")]
                
                if i == 0:
                    weapon_ilvl = str(int(ilvl_string))
                    
                total_ilevel += float(ilvl_string)
                
        ilevel = str(int(total_ilevel/(crystal_posns[0])))

        data = {
            'name': name,
            'server': server,
            'title': title,
            'race': race,
            'clan': clan,
            'gender': gender,
            'portrait_url': soup.select('.bg_chara_264 img')[0]['src'],            
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


    def scrape_free_company(self, lodestone_id):
        url = self.lodestone_url + '/freecompany/%s/' % lodestone_id
        html = self.make_request(url).content

        if 'The page you are searching for has either been removed,' in html:
            raise DoesNotExist()

        soup = bs4.BeautifulSoup(html, "html5lib")

        fc_tag = strip_tags(soup.select('.vm')[0].contents[-1].encode('utf-8'), ['br']).text
        fc_tag = fc_tag[1:-1] if fc_tag else ''
        formed = soup.select('.table_style2 td script')[0].text

        crest = [x['src'] for x in soup.find('div', attrs={'class': 'ic_crest_64'}).findChildren('img')]

        if formed:
            m = re.search(r'ldst_strftime\(([0-9]+),', formed)
            if m.group(1):
                formed = m.group(1)
        else:
            formed = None

        slogan = soup.find(text='Company Slogan').parent.parent.select('td')[0].contents
        slogan = ''.join(x.encode('utf-8').strip().replace('<br/>', '\n') for x in slogan) if slogan else ""

        active = soup.find(text='Active').parent.parent.select('td')[0].text.strip()
        recruitment = soup.find(text='Recruitment').parent.parent.select('td')[0].text.strip()
        active_members = soup.find(text='Active Members').parent.parent.select('td')[0].text.strip()
        rank = soup.find(text='Rank').parent.parent.select('td')[0].text.strip()

        focus = []
        for f in soup.select('.focus_icon li img'):
            on = not (f.parent.get('class') and 'icon_off' in f.parent.get('class'))
            focus.append(dict(on=on,
                              name=f.get('title'),
                              icon=f.get('src')))

        seeking = []
        for f in soup.select('.roles_icon li img'):
            on = not (f.parent.get('class') and 'icon_off' in f.parent.get('class'))
            seeking.append(dict(on=on,
                                name=f.get('title'),
                                icon=f.get('src')))

        estate_block = soup.find(text='Estate Profile').parent.parent
        if estate_block.select('td')[0].text.strip() != 'No Estate or Plot':
            estate = dict()
            estate['name'] = estate_block.select('.txt_yellow')[0].text
            estate['address'] = estate_block.select('p.mb10')[0].text

            greeting = estate_block.select('p.mb10')[1].contents
            estate['greeting'] = ''.join(x.encode('utf-8').strip().replace('<br/>', '\n') for x in greeting) if greeting else ""
        else:
            estate = None

        url = self.lodestone_url + '/freecompany/%s/member' % lodestone_id

        html = self.make_request(url).content

        if 'The page you are searching for has either been removed,' in html:
            raise DoesNotExist()

        soup = bs4.BeautifulSoup(html, "html5lib")

        try:
            name = soup.select('.ic_freecompany_box .pt4')[0].text
            server = soup.select('.ic_freecompany_box .crest_id span')[-1].text[1:-1]
            grand_company = soup.select('.crest_id')[0].contents[0].strip()
            friendship = soup.select('.friendship_color')[0].text[1:-1]
        except IndexError:
            raise DoesNotExist()

        roster = []

        def populate_roster(page=1, soup=None):
            if not soup:
                r = self.make_request(url + '?page=%s' % page)
                soup = bs4.BeautifulSoup(r.content, "html5lib")

            for tag in soup.select('.player_name_area'):
                if not tag.find('img'):
                    continue

                name_anchor = tag.select('.player_name_gold')[0].find('a')

                member = {
                    'name': name_anchor.text,
                    'lodestone_id': re.findall('(\d+)', name_anchor['href'])[0],
                    'rank': {
                        'id': int(re.findall('class/(\d+?)\.png', tag.find('img')['src'])[0]),
                        'name': tag.select('.fc_member_status')[0].text.strip(),
                        },
                    }

                if member['rank']['id'] == 0:
                    member['leader'] = True

                roster.append(member)

        populate_roster(soup=soup)

        try:
            pages = int(soup.find(attrs={'rel': 'last'})['href'].rsplit('=', 1)[-1])
        except TypeError:
            pages = 1

        if pages > 1:
            pool = Pool(5)
            for page in xrange(2, pages + 1):
                pool.spawn(populate_roster, page)
            pool.join()

        return {
            'name': name,
            'server': server.lower(),
            'grand_company': grand_company,
            'friendship': friendship,
            'roster': roster,
            'slogan': slogan,
            'tag': fc_tag,
            'formed': formed,
            'crest': crest,
            'active': active,
            'recruitment': recruitment,
            'active_members': active_members,
            'rank': rank,
            'focus': focus,
            'seeking': seeking,
            'estate': estate
}