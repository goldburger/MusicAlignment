from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import time

mididatabase = 'http://www.markheadrick.com/'

req = urllib.request.urlopen(mididatabase + 'midi.php')
soup = BeautifulSoup(req, 'html.parser', parseOnlyThese=SoupStrainer('a'))

for link in soup:
    if link.has_attr('href') and link['href'][-4:] == '.mid':
        time.sleep(0.1)

        midi_req = urllib.request.urlopen(mididatabase + link['href'])
        filename = link['href'].split('/')[-1]

        with open('data/midi/{0}'.format(filename), 'wb') as f:
            f.write(midi_req.read())
