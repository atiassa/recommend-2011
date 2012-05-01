import nltk 
import urllib2
#from xgoogle.search import GoogleSearch, SearchError
import google
import justext
from nltk.corpus import brown
      
def main():
    s = q1_1()
#    sentences = s.getTextFromWeb()
#    text = ""
#    for sen in sentences:
#        text = text + sen + "\n"
#    clean_file = open('cleanText.txt', 'w')
#    clean_file.write(text)
#    clean_file.close()
#    s.tagTextAndWriteToFile(sentences)

    dif = s.Compare_files()
    s.write_differences(dif)
    
    print "end"
           
class q1_1(object):
    
    def getTagger(self):
        brown_news_tagged = brown.tagged_sents(categories='news')
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
        search_list = ["Netali", "bbc"]
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

    def tagTextAndWriteToFile(self,sentences):
        tag_file = open('tagText', 'w')
        tagger = self.getTagger()
        for sentence in sentences:
            tagged_sen = tagger.tag(sentence.split())
            for w,t in tagged_sen:
                tag_file.write(w + "/" + t + " ")
            tag_file.write("\n")
        tag_file.close()
    

    def Compare_files(self):
        differences = []
        file1Sentences = brown.tagged_sents(fileids=['ca45']) #first human tagged file
        file2Sentences = brown.tagged_sents(fileids=['ca46']) #second human tagged file
        i = 0
        while len(file1Sentences) != i:
            sen1 = file1Sentences[i]
            sen2 = file2Sentences[i]
            i = i + 1
            while len(sen1) != 0:
                tw1 = sen1.pop()
                tw2 = sen2.pop()
                w1, t1 = tw1
                w2, t2 = tw2
                if w1 == w2 and t1 != t2:
                    differences.append(w1)
        return differences
    
    def write_differences(self, dif):
        dif_file = open('DifFile.txt', 'w')
        for w in dif:
            dif_file.write(w + "\n")
        dif_file.close()
                

if __name__ == '__main__':
    main()     

