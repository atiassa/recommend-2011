import  nltk
from itertools import izip
from nltk.corpus import brown
from nltk.probability import FreqDist

# return the precentage of Unknown words - words that tag with None  
def evaluate2(self,training_corpus):
    tag_words = sum(training_corpus,[])
    unknow =  [w for (w ,t) in tag_words if t==None]
    return float(len(unknow)) / len(tag_words)

def main():
    nltk.TaggerI.evaluate2 = evaluate2
    
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[100:]
    brown_test = brown_news_tagged[:100]
    
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
    at2 = nltk.AffixTagger(brown_train, backoff=regexp_tagger)
    ut3 = nltk.UnigramTagger(brown_train, backoff=at2)
    ct2 = nltk.NgramTagger(2, brown_train, backoff=ut3)

    print "evaluate2 default nn = " , nn_tagger.evaluate2(brown_test)
    print "evaluate2 regExp(default nn) = " ,regexp_tagger.evaluate2(brown_train)
    print "evaluate2 affix(regExp(default nn)) = " ,at2.evaluate2(brown_train)
    print "evaluate2 unigram(affix(regExp(default nn))) = " ,ut3.evaluate2(brown_train)
    print "evaluate2 bigram(unigram(affix(regExp(default nn)))) = " ,ct2.evaluate2(brown_train)
 
if __name__ == '__main__':
    main() 