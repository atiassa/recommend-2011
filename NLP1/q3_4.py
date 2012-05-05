import  nltk
from nltk.corpus import brown

# cross-validation process consists of splitting the data in 10 subsets of 10% each. 
# iterate the process of training/testing 10 times,
# each time withholding one subset of 10% for testing and training on the other 9 subsets.
# return the results of the accuracy as a table with rows: i (iteration number), accuracy(i) 
# and accuracy averaged over the ten experiments as tuple 
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
    brown_news_tagged = brown.tagged_sents(categories='news')
    p = crossValidate(brown_news_tagged,10)
    print "accuracy table:"
    print p[0]
    print "accuracy mean: %f" %p[1] 

if __name__ == '__main__':
    main() 