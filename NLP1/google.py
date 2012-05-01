import urllib2
import re
from xgoogle.BeautifulSoup import BeautifulSoup


def google(search,tokenizer):
    search = search.replace(" ","%20")
    url = 'http://www.google.com/search?q='+search
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent' : user_agent}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html)
    html =  soup.prettify().split("\n")
    html = html[167 :]
    html = "\n".join(html)
    links =re.findall(r"url\?q=(.+)&amp;s",html)
    return links
