import bs4
import re
import requests


def wiki(term):
    main_page = 'http://en.wikipedia.org/wiki/Main_Page'
    articles = ['a', 'an', 'of', 'the', 'is']
    wlink = title_except(term, articles)

    if 1 == len(wlink):
        response = main_page
    else:
        search_term = wlink[1].lstrip().replace(' ', '_')
        search_term = wlink.replace(' ', '_')

        response = main_page if len(
            search_term) < 1 else "http://en.wikipedia.org/wiki/" + search_term

    response = response + '\n' + get_para(response)

    return response.encode('utf-8')


def title_except(s, exceptions):
    word_list = re.split(' ', s)  # re.split behaves as expected
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word in exceptions and word or word.capitalize())
    return " ".join(final)


def get_para(wlink):
    # Gets the first paragraph from a wiki link

    msg = ""
    try:
        page_request = requests.get(wlink)
        page = requests.post(page_request)
    except IOError:
        print("can't find that on wikipedia??? ? ? ?? i thought wikipedia had EVERYTHING????")
    else:
        soup = bs4.BeautifulSoup(page, "html5lib")
        msg = "".join(
            soup.find(
                'div', {
                    'id': 'bodyContent'}).p.findAll(
                text=True))

        while 460 < len(msg):
            pos = msg.rfind('.')
            msg = msg[:pos]

    return msg


def get_wiki(text):
    search_term = text.replace("/wiki ", "")
    if len(search_term) < 1:
        return "usage: /wiki toilet"
    else:
        reply = wiki(search_term)
        if ("link's broken :argh:" in reply):
            return "can't find %s on wikipedia" % (search_term)
        else:
            return reply

if __name__ == "__main__":
    wiki(search_term)
