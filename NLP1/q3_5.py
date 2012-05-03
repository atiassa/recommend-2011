import  nltk
import pylab
from nltk.corpus import brown

#plot distribution of sentences by length
def getDistSentByLength():
    corpusSentences = []
    cats = brown.categories()
    for cat in cats:
        corpusSentences = corpusSentences + brown.sents(categories=cat)
    fd = nltk.FreqDist(len(sen) for sen in corpusSentences)
    
    length = sorted(fd.keys())
    noSent = [fd[n] for n in length]
    pylab.plot(length, noSent)
    pylab.title('Distribution of Sentences by Length')
    pylab.xlabel('Length')
    pylab.ylabel('Number of Sentences')
    pylab.grid(True)
    pylab.show()

def divideToLengthClasses(cat='All'):
    shortC = []
    mediumC = []
    longC = []
    taggedSentences = []
    if cat == 'All':
        taggedSentences = brown.tagged_sents()
    else:
        taggedSentences = brown.tagged_sents(categories=cat)
    for sen in taggedSentences:
        if len(sen) < 20:
            shortC.append(sen)
        else:
            if len(sen) >=20 and len(sen) <= 40:
                mediumC.append(sen)
            else:
                longC.append(sen)
    return [shortC, mediumC, longC]
    
def stratifiedSamples(classes, N):
    print "todo"

def main():
    #ploting the distribution graph
#    getDistSentByLength()
    
    #dividing entire corpus to classes according to length
    classes = divideToLengthClasses()
    
#    brown_news_tagged = brown.tagged_sents(categories='news')
#    brown_train = brown_news_tagged[100:]
#    brown_test = brown_news_tagged[:100]
#    
#    nn_tagger = nltk.DefaultTagger('NN')
#    regexp_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
#                                       (r'(The|the|A|a|An|an)$', 'AT'),   # articles
#                                       (r'.*able$', 'JJ'),                # adjectives
#                                       (r'.*ness$', 'NN'),                # nouns formed from adjectives
#                                       (r'.*ly$', 'RB'),                  # adverbs
#                                       (r'.*s$', 'NNS'),                  # plural nouns
#                                       (r'.*ing$', 'VBG'),                # gerunds
#                                       (r'.*ed$', 'VBD'),                 # past tense verbs
#                                       (r'.*', 'NN')                      # nouns (default)
#                                       ],backoff=nn_tagger)
#    at2 = nltk.AffixTagger(brown_train, backoff=regexp_tagger)
#    ut3 = nltk.UnigramTagger(brown_train, backoff=at2)
#    ct2 = nltk.NgramTagger(2, brown_train, backoff=ut3)
    
if __name__ == '__main__':
    main() 