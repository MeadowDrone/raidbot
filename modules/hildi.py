import random

def hildi():
    hildi = ['Hildibrand: We are as siblings now, my constant comrade, for I have shared with you the secrets of House Manderville. Now you must use that knowledge. Go to the fallen chimera and dance like only a Manderville can!']
    hildi.extend(['???: ([Singing]) Fancy yourself a Manderville man? You would do what only a Manderville can? Then lift up your legs, and put up your hands, be a Mander-Mander-Manderville, man!'])
    hildi.extend(['Godbert: But you were not drawn here by some coincidence, were you? No, you came in search of me, Godbert! Why else would you gyrate your hips in such a gentlemanly fashion, if not that?'])
    hildi.extend(['Godbert: HILDIBRAND HELIDOR MAXIMILLIAN MANDERVILLE!!!'])
    hildi.extend(['Godbert: ([Singing]) Godbert the Goldsmith\'s a Manderville man, Smithing as only a Manderville can, Oil him up and give him a tan, Fit for a Mander-Manderville man!'])
    hildi.extend(['Godbert: Hah! Do not worry, little one-- I deal with worse cases before my morning bowel movement!'])
    hildi.extend(['Hildibrand: Hah hah hah! A man so garishly dressed should be easy to find in snowy Coerthas!'])
    hildi.extend(['Hildibrand: A ridiculous outfit!'])
    hildi.extend(['Hildibrand: Hah hah, what reasons indeed? It is enough to make a gentleman laugh!'])
    hildi.extend(['Hildibrand: My redoubtable confederate!'])
    hildi.extend(['Hildibrand: Hail to thee, fellow servant of justice! '])
    hildi.extend(['Hildibrand: We have scoured every ilm of this area to no avail. I can only conclude that, having learned that his opponent was to be the legendary Inspector Hildibrand, the duelist renounced his criminal ways and retreated into hiding.'])
    hildi.extend(['Hildibrand: Though I will still endeavor to avoid fisticuffs, I will be duly armed should worse come to worst.'])
    hildi.extend(['Hildibrand: ...Wherefore art though, my nefarious nemesis?'])
    hildi.extend(['Gilgamesh: For Gilgamesh... It is embiggening time!'])
    hildi.extend(['Hildibrand: I believe this is addressed to me, condescending Inspector Briardien.\nBriardien: Piss off.'])
    hildi.extend(['Hildibrand: Very well! I-- and I alone-- Hildibrand, agent of enquiry, inspector extraordinaire, once more accept your challenge!'])

    hildi_imgs = ["img/hildi.png", "img/hildi2.png", 
                    "img/hildi3.jpg", "img/hildi4.gif", 
                    "img/hildi5.gif", "img/hildi6.gif", 
                    "img/hildi7.jpg", "img/hildi8.gif",
                    "img/hildi9.png", "img/hildi10.jpg",
                    "img/hildi11.png", "img/hildi12.png"]

    return(random.choice(hildi_imgs), random.choice(hildi))