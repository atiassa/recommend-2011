# -*- coding: utf-8 -*-
import page_parser
import re

# Media and categories; the codes for these differ per language.
# We have of the popular ones (>900.000 articles as of July 2012) here,
# as well as Latin, which is useful for testing.
# Add other languages as required.
#_MEDIA_CAT = """
#  [Ii]mage|[Cc]ategory      # English
# |[Aa]rchivo                # Spanish
# |[Ff]ile                   # English, Italian
# |[CcKk]at[?e]gor[?i][ea]   # Dutch, German, French, Italian, Spanish, Polish, Latin
# |[Bb]estand                # Dutch
# |[Bb]ild                   # German
# |[Ff]icher                 # French
# |[Pp]lik                   # Polish
# |[Ff]asciculus             # Latin
#"""
#
#_UNWANTED = re.compile(r"""
#  (:?
#    \{\{ .*? \}\}                           # templates
#  | \| .*? \n                               # left behind from templates
#  | \}\}                                    # left behind from templates
#  | <!-- .*? -->
#  | <div .*?> .*? </div>
#  | <math> .*? </math>
#  | <nowiki> .*? </nowiki>
#  | <ref .*?> .*? </ref>
#  | <ref .*?/>
#  | <span .*?> .*? </span>
#  | \[\[ (:?%s): (\[\[.*?\]\]|.)*? \]\]
#  | \[\[ [a-z]{2,}:.*? \]\]                 # interwiki links
#  | =+                                      # headers
#  | \{\| .*? \|\}
#  | \[\[ (:? [^]]+ \|)?
#  | \]\]
#  | '{2,}
#  )
#""" % _MEDIA_CAT,
#re.DOTALL | re.MULTILINE | re.VERBOSE)
#
#def text_only(text):
#    return _UNWANTED.sub("", text)
#
#def category_links(text):
#    if re.match(r"INSERT INTO `categorylinks` VALUES", text):
#        return re.findall(r"\((\d+),'([^']+)'(?:,'[^']*'){5}\)", text)


    
def processPage(page):
    if page.title.find('קטגוריה') != 0: 
        print "----- "+page.title+" ----"
        print page.text
#    if page.title.find('תבנית') ==0: 
#        print "----- "+page.title+" ----"
#        print page.text
#    print category_links(page.text)
#    print "-------------------------------------------------------------------------"
 
class DataGathering(object):
    
    def __init__(self,N = 200, M = 2):
        self.articals = []
        self.data_gathering()     
     
    def data_gathering(self): 
        page_parser.parseWithCallback("hewikisource-20120628-pages-articles.xml", processPage)

    def _getArticals(self):
        return self.articals

page_parser.parseWithCallback("hewikisource-20120628-pages-articles.xml", processPage)

