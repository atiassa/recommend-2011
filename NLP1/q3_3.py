import  nltk
from itertools import izip
from nltk.corpus import brown
from nltk.probability import FreqDist

# return confusion matrix tabulates all the mistakes committed by a tagger in the form of 
# a matrix C[ti, tj]. C[ti, tj] counts the number of times the tagger predicted ti instead of tj
def ConfusionMatrix(self, corpus_test):
    matrix = FreqDist()
    tagged_sents = self.batch_tag([nltk.untag(sent) for sent in corpus_test])
    testTokens = sum(corpus_test,[]) # real tags from the corpus
    taggerTokens = sum(tagged_sents,[]) # tags of the tagger that in used
    for tagged, test in izip(taggerTokens, testTokens ):
        if tagged != test :
            matrix.inc((tagged[1],test[1]))
    return matrix

def main():
    nltk.TaggerI.ConfusionMatrix = ConfusionMatrix
    
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
    
    print ct2.ConfusionMatrix(brown_test)
        
if __name__ == '__main__':
    main() 