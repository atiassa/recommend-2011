import sys
import nltk 
from urllib import urlopen
import urllib2
from urlparse import urlparse
#from xgoogle.search import GoogleSearch, SearchError
import google
import justext
from nltk.corpus import brown
      
def main():
    s = q1_1()
    sentences = s.getTextFromWeb()
    text = ""
    for sen in sentences:
        text = text + sen + "\n"
    clean_file = open('cleanText.txt', 'w')
    clean_file.write(text)
    clean_file.close()
    s.createCorpusFile(s.tagText(sentences))
    print "end"
           
class q1_1(object):
    
    def getTagger(self):
        brown_news_tagged = brown.tagged_sents(categories='news')
#        brown_train = brown_news_tagged[100:]
#        brown_test = brown_news_tagged[:100]
        nn_tagger = nltk.DefaultTagger('NN')
        regexp_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
                                           (r'(The|the|A|a|An|an)$', 'AT'),   # articles
                                           (r'.*able$', 'JJ'),                # adjectives
                                           (r'.*ness$', 'NN'),                # nouns formed from adjectives
                                           (r'.*ly$', 'RB'),                  # adverbs
                                           (r'.*s$', 'NNS'),                  # plural nouns
                                           (r'.*ing$', 'VBG'),                # gerunds
                                           (r'.*ed$', 'VBD'),                 # past tense verbs
                                           (r'.*', 'NN')                      # nouns (default)
                                           ],backoff=nn_tagger)
        
        affix_tagger = nltk.AffixTagger(brown_news_tagged, backoff=regexp_tagger)
        ut3 = nltk.UnigramTagger(brown_news_tagged, backoff=affix_tagger)
        ct2 = nltk.NgramTagger(2, brown_news_tagged, backoff=ut3)
        return ct2
    
    def segment_sentences(self,words):
        start = 0
        sents = []
        words = words.lower()
        for i, word in enumerate(words):
            if word in '.?!': #and classifier.classify(punct_features(words, i)) == True:
                sents.append(words[start:i+1])
                start = i+1
        if start < len(words):
            sents.append(words[start:])
        return sents
    
    def getTextFromWeb(self):
        num_results = 10
        search_list = ["nbc", "bbc"]
        sites = [] 
        text = []
        results = []
        while len(search_list)!=0 and len(results) < num_results:
            search = search_list.pop()
            results = results + google.google(search,nltk.word_tokenize)

        for d in results:
            sites.append(d)
            if len(sites) == num_results:
                break
  
        for url in sites:
            print url
            try:
                page = urllib2.urlopen(url).read()
            except urllib2.HTTPError, e:
                print "Search failed: %s" % e 
                continue
            paragraphs = justext.justext(page, justext.get_stoplist('English'))
            if len(text) < 50:
                for paragraph in paragraphs:
                    if paragraph['class'] == 'good' and len(text) < 50:
                        text = text + self.segment_sentences(paragraph['text'].encode('utf8'))
        return text

    def tagText(self,text):
        taggedSentences =[]
        for sentence in text:
            x = self.getTagger().tag(sentence.split())
            taggedSentences = taggedSentences + x  
        return taggedSentences
    
    def createCorpusFile(self,tag_text):      
        tag_file = open('tagText', 'w')
        for w,t in tag_text:
            tag_file.write(w+"/"+t+" " )
        tag_file.close()
        
    

if __name__ == '__main__':
    main()     

