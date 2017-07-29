import urllib2
import urllib
from HTMLParser import HTMLParser
import string
import time

extension = '.mp4'

valid_file_chars = '-_(). %s%s' % (string.ascii_letters, string.digits)

link = 'https://www.reddit.com/r/GlobalOffensive/'

o = urllib2.build_opener()

#put your username at 'put your username here' and change the user agent if you want

o.addheaders = [('User-Agent', 'Twitch link grabing bot by /u/put your username here')]

twitch_clips = set()

class getClips(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for a in attrs:
            if a[0] == 'href':
                if 'https://clips.twitch.tv/' in a[1]:
                    twitch_clips.add(a[1])

class getVideo(HTMLParser):
    def __init__(self, title):
        HTMLParser.__init__(self)
        self.title = title
    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            
            for a in attrs:
                if a[0] == 'content':
                    if 'https://clips-media-assets.twitch.tv' in a[1]:
                        url = a[1]
                        while not url[-1] in string.digits:
                            url = url[:-1]
                        url += extension
                        print 'The source url we found is: ',url
                        urllib.urlretrieve(url, 'clips/'+title + extension)
                        print 'asldkfjsdlf',title
                        return

class getTitle(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = ''
        self.found = False
    def handle_starttag(self, tag, a):
        if tag == 'title':
            self.found = True

    def handle_data(self, data):
        if self.found == True:
            self.title = data
            self.found = False

def main():
    
    connection = o.open(link)
    html = connection.read().decode('UTF-8')

    parser = getClips()
    parser.feed(html)

    for clip in twitch_clips:
        print clip
        
        connection = urllib2.urlopen(clip)
     
        c_page = connection.read().decode('UTF-8')
        
        t_parser = getTitle()
        t_parser.feed(c_page)
        title = t_parser.title.encode('ascii')
        
        print 'The video title is:',title
        title = ''.join(ch for ch in title if ch in valid_file_chars)
        v_parser = getVideo(title)
       
        v_parser.feed(c_page)

    
