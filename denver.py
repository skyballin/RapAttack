from urllib2 import urlopen
from bs4 import BeautifulSoup
from pattern.en import tag
import string
import random

def random_denver_song(link):

    html = urlopen(link).read()
    soup = BeautifulSoup(html)
    albums = soup.find('div',{'id':'listAlbum'}).findAll('a')
    links = [s['href'] for s in albums if s.has_attr('href')]
    links = [s for s in links if s[14]!= 'z']
    song_choice = random.choice(links)
    return denver_lyrics(song_choice)

def denver_lyrics(link):
    link = link.replace('..', 'http://www.azlyrics.com/')
    html = urlopen(link).read()
    soup = BeautifulSoup(html)
    lyrics = str(''.join(''.join([s.text for s in soup.findAll('div')]).split('lyrics')[1:]).split('\n\n\n\n\r\nif')[0].strip()).replace('LYRICS', "").replace('JOHN DENVER', '')
    lyrics = [x for x in lyrics.splitlines() if x]
    lyrics = ' '.join([str(x) for x in lyrics if x[0] not in ['[', ' ']])
    exclude = set(string.punctuation)
    lyrics = ''.join(ch.lower() for ch in lyrics if ch not in exclude)
    lyrics = lyrics.split()
    nounlist = []
    for word in lyrics:
        if tag(word)[0][1] in ['NN', 'NNP'] and len(word)>2 and tag(word) not in nounlist:
            nounlist.append(tag(word))
    return nounlist


#http://www.azlyrics.com/n/neildiamond.html
#http://www.azlyrics.com/j/johndenver.html