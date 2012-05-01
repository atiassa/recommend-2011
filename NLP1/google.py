import urllib2
import nltk
import re
from xgoogle.BeautifulSoup import BeautifulSoup
import os

def cleanSparse(raw, cutOff):
    raw = re.sub("[\t, ]+"," ",raw)
    raw = raw.split("\n")
    raw = filter(lambda t: len(t) > cutOff,raw)
    return "\n".join(raw)

def google(search,tokenizer):
    search = search.replace(" ","%20")
    search = search.replace("(","%28")
    search = search.replace(")","%29")
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

#    URLtoHTMLtoTEXT = {}
    return links
#    for url in links:
#        try:
#            html = urllib2.urlopen(url).read()
#        except:
#            continue
#        HTMLTokens = tokenizer(html)
#        #raw = justext.justext(url, justext.get_stoplist('English'))
#        raw = nltk.clean_html(html)
#        lessraw = cleanSparse(raw,50)
#        rawTextTokens = tokenizer(lessraw)
#        URLtoHTMLtoTEXT[url] = ((html,HTMLTokens),(lessraw,rawTextTokens,raw))
#
#    return URLtoHTMLtoTEXT

def PrintFile(text, fileName):
    print os.path
    f = open(os.path.join("cText.txt"), "w")
    f.write(text)
    f.write("\n")
    f.close()


def AnalyzeResults(results):
    for (index, key) in enumerate(results.keys()):
        value = results[key]
        (text, tokens,moreraw) = value[1]
        tokensText = reduce(lambda x,y: x + "\n" + y, tokens)
        PrintFile(tokensText, "Tokens-%s.txt" % (index))
        PrintFile(text, "Raw-%s.txt" % (index))
