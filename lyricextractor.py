
from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
import string

from pattern.en.wordlist import ACADEMIC
from pattern.en.wordlist import PROFANITY
from pattern.en import tag
from denver import *
import re

def lyrics_extractor(link1, link2):
    html = requests.get(link1, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})
    soup = BeautifulSoup(html.text, "lxml")
    headers = ''.join(soup.find('h1').text.strip())
    song =  headers.split('Lyrics')[0].strip()
    artist = ''.join(headers.split('Lyrics')[1:]).strip()
    lyrics = unicode(soup.find('div', {'class':'lyrics'}).text)
    lyrics = [x for x in lyrics.splitlines() if x]
    lyrics = [x.encode('utf-8') for x in lyrics if x[0] not in ['[']]

    exclude = set(string.punctuation)
    additional_bad_words = ['hella', 'motherfuckers', 'motherfuckin', 'booty', 'niggas', 'bitches', 'death', 'grave', 'gun', 'kill', 'rage', 'war']

    wordlist = []
    for line in lyrics:
        wordlist.extend([''.join(ch.lower() for ch in s if ch not in exclude) for s in line.split()])

    count = 0
    for each in wordlist:
        if each in PROFANITY or each in additional_bad_words:
            count += 1

    denver_nouns = random_denver_song(link2)
    new_lyrics = []
    for line in lyrics:
        line2 = []
        for word in line.split():
            word = "".join(l for l in word if l not in string.punctuation)
            if word.lower() in PROFANITY or word.lower() in additional_bad_words:
                line2.append(random.choice(denver_nouns)[0][0])
            else:
                line2.append(word)
        new_lyrics.append(' '.join(line2))

    return new_lyrics, count