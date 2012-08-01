'''
- Articles
- Each article links to other articles (outgoing links)
- Categories (in hebrew, these are called "קטגוריה")
- Redirect (in hebrew, "הפניה")
- Disambiguation links (in hebrew, "פירושונים")
- A template of the article (in hebrew, "תבנית")
'''

class Article(object):

    def __init__(self):
        self.links = []
        self.Categories = []
        self.Redirect = []
        self.Disambiguation_links  = []
        self.template = []
