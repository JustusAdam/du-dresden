# Original version written by Henning Thielemann http://www.henning-thielemann.dex

import re
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

translations = [
    ('computer', 'gombjudor'),
    ('windows', 'windoof'),
    ('microsoft', 'mükroschrodd'),
    ('gates', 'gejts'),
    ('pentium', 'penndsium'),
    ('system', 'süsdem'),
    ('feature', 'mergmal'),
    ('features', 'mergmale'),
    ('software', 'sofdwehr'),
    ('hardware', 'hardwehr'),
    ('instruction', 'insdrakdschn'),
    ('extension', 'ixtenschn'),
    ('expansion', 'ixpanschn'),
    ('download', 'daunlohd'),
    ('download_', 'runnerladen'),
    ('downloaden_', 'runnerladen'),
    ('homepage', 'hohmbejdsch'),
    ('byte', 'beit'),
    ('update', 'abdejt'),
    ('team_', 'diehm'),
    ('crew_', 'kruh'),
    ('chat_', 'schedd'),
    ('cool', 'guhl'),
    ('cookies', 'gegse'),
    ('netiquette', 'neddigedde'),
    ('power', 'bauer'),
    ('backup', 'bäggab'),
    ('myspace', 'maischbäß'),
    ('space', 'schbäß'),
    ('provider', 'verneddsor'),  # 'broweidor',
    # 'halsabschneidor',
    ('free', 'frieh'),
    ('screenshot', 'bildschirmfoddo'),
    ('compiler', 'übersedsor'),
    ('compilieren', 'übersedsn'),
    ('quellcode', 'quälkod'),
    ('sourcecode', 'quälkod'),
    ('meeting', 'dreffn'),  # 'dsusammengunfd',
    ('developer', 'endwigglor'),
    ('release', 'rielies'),
    ('_user', 'benuddsor'),
    ('_link_', 'vorweis'),
    ('hyperlink', 'nedsvorweis'),
    ('_fan_', 'fenn'),
    ('office', 'büro'),
    ('chip', 'schipp'),
    ('feedback', 'fiedbegg'),
    ('recyceln', 'widderverwerdn'),
    ('recyclen', 'widderverwerdn'),
    ('recycling', 'widderverwerdung'),
    ('style', 'sdil'),
    ('luther', 'ludder'),
    ('saison', 'sesong'),
    # 'garage': 'garahsche',
    ('garage', 'karahsche'),
    ('manege', 'manehsche'),
    ('passagier', 'bassaschier'),
    ('vietnamese', 'fidschi'),
    ('vietnamesen', 'fidschis'),
    ('google', 'guhgel'),
    ('pool', 'buhl'),
    ('service', 'sörwis'),
    ('haskell', 'hässgl'),
    ('news', 'njuhs'),
    ('_new_', 'njuh'),
    ('_york_', 'jorg'),
    ('layout', 'lejaud'),
    # 'mund_': 'gusche',
    ('mund_', 'nischl'),
    ('schnitte_', 'bemme'),
    ('arbeit_', 'orbeit'),
    ('_arbeiten_', 'klechen'),
    ('_arbeite_', 'kleche'),
    ('_arbeitet_', 'klecht'),
    ('_arbeitest_', 'klechst'),
    ('_mutter_', 'olle'),
    ('_vater_', 'vadda'),
    ('digital', 'diggedal'),
    ('medien', 'medchen'),
    ('fernseher_', 'glotze'),
    ('_taxi_', 'taxe'),
    ('fünfzig', 'fuffzich'),
    ('spam', 'sbämm'),
    ('slogan', 'slogän'),
    ('honecker', 'honi'),
    ('trabant', 'trabbi'),
    ('germany', 'dschörmeni'),
    ('community', 'gemeenschofd'),
    ('chemnitz', 'Gorl-Morgs-Stodd'),
    # Karl-Marx-Denkmal -> Nischl
    # ein - 'n
    # eine - 'ne
    # nicht wahr - nuwor
    # kannst du - kannste
    ('_nun_', 'nu'),
    ('_aber_', 'awor'),
    ('_nein_', 'nee'),
    ('_auch_', 'och'),
    ('_gleich_', 'glei'),
    ('ex', 'eggs'),  # Experte
    ('ax', 'aggs'),  # Praxis
    ('ox', 'oggs'),  # paradox
    ('echse', 'eggse'),  # wechseln
    ('achse', 'aggse'),  # wachsen
    ('sp', 'schb'),
    ('st', 'schd'),
    # St am Anfang fast immer Scht, Ausnahme: Stil, St., Story
    # 'sp': 'sb',
    ('st_', 'sd'),   # Analyst, Gerüst, Ast, fast
    ('ste_', 'sde'),
    ('stel_', 'sdl'),
    ('stem_', 'sdm'),
    ('sten_', 'sdn'),
    ('ster_', 'sder'),
    ('stes_', 'sdes'),
    ('stet_', 'sded'),
    ('spe_', 'sbe'),
    ('spen_', 'sbn'),
    ('ck', 'gg'),
    ('k', 'g'),
    ('th', 'd'),
    ('t', 'd'),
    ('ph', 'ph'),
    ('p', 'b'),
    ('ie', 'ie'),  # prevent the 'e' from being treated as the only vowel in its environment, as in 'Beispiel'
    ('y', 'ü'),
    ('ayer', 'aier'),  # Bayern
    ('eyer', 'eier'),  # Meyer
    ('ich', 'isch'),
    ('ech', 'esch'),
    ('äch', 'äsch'),
    ('üch', 'üsch'),
    ('lch', 'lsch'),
    ('agt', 'acht'),  # gefragt
    ('ägt', 'ächt'),  # überträgt
    ('egt', 'echt'),  # überlegt
    ('agen', 'ahchn'),  # tragen
    ('ägen', 'ähchn'),  # Mägen
    ('egen', 'ehchn'),  # legen
    ('_chemn', 'gemn'),
    ('_che', 'sche'),
    ('_den_', 'den'),  # prevent from being shrinked to 'dn'
    ('_die_', 'de'),
    ('der_', 'dor'),
    ('ter_', 'dor'),
    ('ein', 'een'),
    ('nen_', 'n\''),
    ('en_', 'n'),
    ('el_', 'l'),
    ('nd_', 'nn'),
    ('tion', 'dsion'),
    ('tionen', 'dsion\''),
    ('ig_', 'ich'),
    ('igen_', 'chen'),  # mäßigen
    ('pzig', 'pzisch'),  # Leipzig
    ('mpf_', 'mff'),
    ('pf_', 'bb'),

    ('eipzig', 'eibzsch'),
    ('der', 'dor'),
    ('auch', 'och'),
    ('schläge', 'schlähche')
]

translations.sort(key=lambda a: len(a[0]), reverse=True)


def compile_if_regex(regex):
    if regex.startswith('_'):

        if regex.endswith('_'):
            return re.compile(r'(\b)%s(\b)' % source[1:-1])
        else:
            return re.compile(r'(\b)%s' % source[1:])

    elif regex.endswith('_'):
        return re.compile(r'%s(\b)' % source[:-1])

    else:
        return word


# compile all underscore pseude regexes in the translations
translations = [
    (compile_if_regex(source), translation)
    for source, translation in translations
]


def handle_one(word):
    if engine == 'twitter':
        if re.match('@.*?', word):
            # don't translate twitter account mentions
            return word

        if re.match('https?://.*', word):
            # don't translate URLs
            return word

    if method == 'saxophone':
        s_word = send_saxophone_request(word)
    else:
        s_word = apply_substitutions(word)

    # restore capitalization
    if word.isupper():
        s_word = s_word.upper()
    elif word[0].isupper():
        s_word = s_word[:1].upper() + s_word[1:]

    return s_word


def translate(phrase, engine='none', method='local'):
    """Translate a phrase by applying a local dictionary."""

    return ' '.join(map(handle_one, phrase.split()))


def apply_one_substitution(source, translation, word):
    """apply one substitution to one word"""

    if isinstance(source, str):
        logging.debug('replacing[syllable] {} with {} to {}'.format(source, translation, word))
        return word.replace(source, translation)

    else:
        # source is a compiled regex
        logging.debug('replacing[regex] {} with {} to {}'.format(source, translation, word))
        return re.sub(regex, translation, word)


def apply_substitutions(word):
    """Apply all local translations to a given word."""

    word = word.lower()

    for source, translation in translations:

        word = apply_one_substitution(source, translation, word)

    return word


def send_saxophone_request(word):
    """Send a single word to the original Saxophone for translation."""
    r = requests.get(url='http://parallelnetz.de/Saxophone',
                     params={
                         'phrase': word.lower().encode('cp1252')
                     })
    if r.status_code == 200:
        soup = BeautifulSoup(r.content.decode('cp1252'))
        return soup.find_all('td')[-1].string
