import page_parser
 
    
def processPage(page):
    print page 
 
class DataGathering(object):
    
    def __init__(self,N = 200, M = 2):
        self.articals = []
        self.data_gathering()     
     
    def data_gathering(self): 
        page_parser.parseWithCallback("hewikisource-20120628-pages-articles.xml", processPage)

    def _getArticals(self):
        return self.articals

page_parser.parseWithCallback("hewikisource-20120628-pages-articles.xml", processPage)