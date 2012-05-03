import  nltk
from itertools import izip
from nltk.corpus import brown
from nltk.probability import FreqDist

# return the precentage of Unknown words - words that tag with None  
def evaluate2(self,training_corpus):
#    tag_words = sum(training_corpus,[])
#    unknow =  [w for (w ,t) in tag_words if t==None]
#    return float(len(unknow)) / len(tag_words)
    tagged_sents = self.batch_tag([nltk.untag(sent) for sent in training_corpus])
    reference = sum(training_corpus, [])
    test = sum(tagged_sents, [])
    know = 0
    unknow = 0
    for r, t in izip(reference, test):
        if t != None :
            know += 1
        else: 
            unknow += 1
    return float(know) / len(reference)


def ConfusionMatrix(self, corpus_test):
    matrix = FreqDist()
    tagged_sents = self.batch_tag([nltk.untag(sent) for sent in corpus_test])
    testTokens = sum(corpus_test,[]) # real tags from the corpus
    taggerTokens = sum(tagged_sents,[]) # tags of the tagger that in used
    for tagged, test in izip(taggerTokens, testTokens ):
        if tagged != test :
            matrix.inc((tagged[1],test[1]))
    return matrix

def crossValidate(corpus, n):
    summarize = []
    corpus_len = len(corpus)
    mean = 0
    for i in range(1,n):
        cut = int(i*0.1*corpus_len)
        train = corpus[:cut]
        test = corpus[cut:]
        
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
        at2 = nltk.AffixTagger(train, backoff=regexp_tagger)
        ut3 = nltk.UnigramTagger(train, backoff=at2)
        ct2 = nltk.NgramTagger(2, train, backoff=ut3)
        
        accu = float(ct2.evaluate(test))
        summarize.append((i,accu))
        mean += accu
    return (summarize , mean/accu)

def main():
    nltk.TaggerI.evaluate2 = evaluate2
    nltk.TaggerI.ConfusionMatrix = ConfusionMatrix
    
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[100:]
    brown_test = brown_news_tagged[:100]
    
    brown_news_taggedS = brown.tagged_sents(categories='news', simplify_tags=True)
    brown_trainS = brown_news_taggedS[100:]
    brown_testS = brown_news_taggedS[:100]
        
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
    
    ct2S = nltk.NgramTagger(2, brown_trainS, backoff=ut3) 
    
    print crossValidate(brown_news_tagged,10)
    
    print nn_tagger.ConfusionMatrix(brown_test)
    print ct2.ConfusionMatrix(brown_test)
    print ct2S.ConfusionMatrix(brown_test)
    print ""  
    
    print "evaluate2 default nn = " , nn_tagger.evaluate2(brown_test)
    print "evaluate2 regExp(default nn) = " ,regexp_tagger.evaluate2(brown_train)
    print "evaluate2 affix(regExp(default nn)) = " ,at2.evaluate2(brown_train)
    print "evaluate2 unigram(affix(regExp(default nn))) = " ,ut3.evaluate2(brown_train)
    print "evaluate2 bigram(unigram(affix(regExp(default nn)))) = " ,ct2.evaluate2(brown_train) 
    print ""  

    print "evaluate default nn = " , nn_tagger.evaluate(brown_test)
    print "evaluate regExp(default nn) = " ,regexp_tagger.evaluate(brown_test)
    print "evaluate affix(regExp(default nn)) = " ,at2.evaluate(brown_test)
    print "evaluate unigram(affix(regExp(default nn))) = " ,ut3.evaluate(brown_test)
    print "evaluate bigram(unigram(affix(regExp(default nn)))) = " ,ct2.evaluate(brown_test)
    print ""  
    
if __name__ == '__main__':
    main() 