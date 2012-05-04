import  nltk
import pylab
from nltk.corpus import brown
import random

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

def getAllTaggedCorpus():
    taggedSens = []
    cats = brown.categories()
    for cat in cats:
        for sen in brown.tagged_sents(categories=cat):
            taggedSens.append(sen)
    return taggedSens
        
def divideToLengthClasses(cat='All'):
    shortC = []
    mediumC = []
    longC = []
    taggedSentences = []
    if cat == 'All':
        taggedSentences = getAllTaggedCorpus()
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
    testSet = []
    trainSet = []
    for cl in classes:
        noSenTest = int((float(N)/100)*len(cl))
        while noSenTest > 0:
            r = int(random.uniform(1,len(cl)-1))
            testSet.append(cl.pop(r))
            noSenTest -= 1
        trainSet = trainSet + cl
    return trainSet, testSet
        
def divideToGenereClasses():
    classes = []
    taggedSentences = []
    cats = brown.categories()
    for cat in cats:
        for sen in brown.tagged_sents(categories=cat):
            taggedSentences.append(sen)
        classes.append(taggedSentences)
    return classes
    
def main():
    #ploting the distribution graph
#    getDistSentByLength()
    #############################################################
    #cycle of training-testing First case - Random split 90%-10%#
    #############################################################
    train, test = stratifiedSamples([getAllTaggedCorpus()], 10)

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
    print "evaluate bigram(unigram(affix(regExp(default nn)))) Random Split= " ,ct2.evaluate(test)
    
    ###############################################################################################
    #cycle of training-testing second case - Stratified split 90%-10% according to sentence length#
    ###############################################################################################
    classes = divideToLengthClasses()
    train, test = stratifiedSamples(classes, 10)

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
    print "evaluate bigram(unigram(affix(regExp(default nn)))) Length split = " ,ct2.evaluate(test)
    
    #################################################################################################
    #cycle of training-testing Third case - Stratified split 90%-10% according to the sentence genre#
    #################################################################################################
    classes = divideToGenereClasses()
    train, test = stratifiedSamples(classes, 10)

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
    print "evaluate bigram(unigram(affix(regExp(default nn)))) Genere split = " ,ct2.evaluate(test)
    
if __name__ == '__main__':
    main() 