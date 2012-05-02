import  nltk
from itertools import izip
from nltk.corpus import brown
from nltk.metrics import accuracy as _accuracy
from operator import itemgetter
    
def evaluate2(self,training_corpus):
    tagged_sents = self.batch_tag([nltk.untag(sent) for sent in training_corpus]) 
    gold_tokens = sum(training_corpus, []) 
    test_tokens = sum(tagged_sents, []) 
    return _accuracy(gold_tokens, test_tokens)

def MicroEvaluate(self,corpus_test):
    tagged_sents = self.batch_tag([nltk.untag(sent) for sent in corpus_test])#tagger tagged
    testTokens = sum(corpus_test,[]) # real tags from the corpus
    taggerTokens = sum(tagged_sents,[]) # tags of the tagger that in used
    tags = [] #all possible tags------------------TODO
    for x in testTokens:
        w,t = x
        if not tags.__contains__(t):
            tags.append(t)
    fmeasure = 0
    for tag in tags:
        fmeasure += calcFMeasur(tag, testTokens, taggerTokens)
    if len(tags) == 0:
        return 0
    return fmeasure / len(tags)

#tag both in the test and by the tagger
def calcTP(tag, CorpusTags, TaggerTags):
    tp = 0
    for x, y in izip(CorpusTags, TaggerTags):
        w,t = x
        if x == y and t == tag :
            tp += 1
    return tp

#non-tag both in the test and by the tagger    
def calcTN(tag, CorpusTags, TaggerTags):
    tn = 0
    for x, y in izip(CorpusTags, TaggerTags):
        testw,testTag = x
        taggerw,taggerTag = y
        if testw == taggerw and testTag != tag and taggerTag != tag :
            tn += 1
    return tn
    
#non-tag by the test and tag by the tagger
def calcFP(tag, CorpusTags, TaggerTags):
    fp = 0
    for x, y in izip(CorpusTags, TaggerTags):
        testw,testTag = x
        taggerw,taggerTag = y
        if testw == taggerw and testTag != tag and taggerTag == tag :
            fp += 1
    return fp

#tag by the test and non tag by the tagger
def calcFN(tag, CorpusTags, TaggerTags):
    fn = 0
    for x, y in izip(CorpusTags, TaggerTags):
        testw,testTag = x
        taggerw,taggerTag = y
        if testw == taggerw and testTag == tag and taggerTag != tag :
            fn += 1
    return fn
    
#Precision(T) = TP / TP + FP
def calcPrec(tag, CorpusTags, TaggerTags):
    tp = calcTP(tag, CorpusTags, TaggerTags)
    fp = calcFP(tag, CorpusTags, TaggerTags)
    if tp+fp == 0:
        prec = 0
    else:
        prec = float(float(tp)/(tp+fp))
    return prec

#Recall(T) = TP / TP + FN    
def calcRecall(tag, CorpusTags, TaggerTags):
    tp = calcTP(tag, CorpusTags, TaggerTags)
    fn = calcFN(tag, CorpusTags, TaggerTags)
    if tp + fn == 0:
        recall = 0
    else:
        recall = float(float(tp)/(tp+fn))
    return recall
    
#F-Measure(T) = 2 x Precision x Recall / (Recall + Precision)  
def calcFMeasur(tag, CorpusTags, TaggerTags):
    prec = calcPrec(tag, CorpusTags, TaggerTags)
    recall = calcRecall(tag, CorpusTags, TaggerTags)
    if recall + prec == 0:
        fMeasure = 0
    else:
        fMeasure = float((2 * prec * recall)/(recall + prec))
    return fMeasure     

######################################################################################################
######################################################################################################
#To test the precision and recall functions we will calculate the precision and recall               #
#for the default_tagger: expected precision(for the default tag) = same value as evaluate func       #
#                                   because TP = no. of words that the tagger took right decision    #
#                                           FP = no. of words that in the test tagged as non tag     #
#                                                and the tagger tagged them as tag                   #
#                                            => TP + FP = no. of words in the test                   #
#                              expected recall(for the default tag) = 1                              #
#                                    because FN = 0 for the default tag                              #
#                                                   cause the tagger give each word the default tag  #
#                              for any other tag the values should be 0 becasue TP = 0 for each tag  #
######################################################################################################
######################################################################################################
def checkTaggerPrecForTag(tagger, tag, testCorpus):
    tagged_sents = tagger.batch_tag([nltk.untag(sent) for sent in testCorpus])#tagger tagged
    testTokens = sum(testCorpus,[]) # real tags from the corpus
    taggerTokens = sum(tagged_sents,[]) # tags of the tagger that in used
    return calcPrec(tag, testTokens, taggerTokens)

def checkTaggerRecallForTag(tagger, tag, testCorpus):
    tagged_sents = tagger.batch_tag([nltk.untag(sent) for sent in testCorpus])#tagger tagged
    testTokens = sum(testCorpus,[]) # real tags from the corpus
    taggerTokens = sum(tagged_sents,[]) # tags of the tagger that in used
    return calcRecall(tag, testTokens, taggerTokens)

##########################################################################################################################
##########################################################################################################################
#Check which X tags are difficult in the dataset.                                                               #
#to check this we need to calculate precision for each tag and the tags with the lowest precision are the difficult tags.#
##########################################################################################################################
##########################################################################################################################
def checkDifficultTags(tagger, testCorpus, isSimplified, x):
    difficultTags = []
    corpusTokens = sum(testCorpus, [])
    simplifiedTags = ['ADJ', 'ADV', 'CNJ', 'DET', 'EX', 'FW', 'MOD', 'NN', 'NP', 'NUM', 'PRO', 'P', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'WH']
    fullTags = []###-------> TODO
    precs = []
    tags = []
    #defining which tags are we checking full or simplified tags
    if isSimplified:
        tags = simplifiedTags
    else:
        tags = fullTags
    #calculating precision for each tag
    tagger_tags = tagger.batch_tag([nltk.untag(sent) for sent in testCorpus])
    taggedTokens = sum(tagger_tags, [])
    for t in tags:
        p = calcPrec(t, corpusTokens, taggedTokens)
        precs.append((t,p))
    #insert x lowest tags to difficultTags
    precs = sorted(precs, key=itemgetter(1))
    for w,p in precs:
        if len(difficultTags) < x:
            difficultTags.append(w)     
    return difficultTags
    
def main():
    
    nltk.DefaultTagger.MicroEvaluate = MicroEvaluate
    nltk.RegexpTagger.MicroEvaluate = MicroEvaluate
    nltk.AffixTagger.MicroEvaluate = MicroEvaluate
    nltk.UnigramTagger.MicroEvaluate = MicroEvaluate
    nltk.NgramTagger.MicroEvaluate = MicroEvaluate
    
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
        
    print "evaluate default nn = " , nn_tagger.evaluate(brown_test)
    print "evaluate regExp(default nn) = " ,regexp_tagger.evaluate(brown_test)
    print "evaluate affix(regExp(default nn)) = " ,at2.evaluate(brown_test)
    print "evaluate unigram(affix(regExp(default nn))) = " ,ut3.evaluate(brown_test)
    print "evaluate bigram(unigram(affix(regExp(default nn)))) = " ,ct2.evaluate(brown_test)
    
    print "micro-evaluate default nn = ", nn_tagger.MicroEvaluate(brown_test)
    print "micro-evaluate regExp(default nn) = ", regexp_tagger.MicroEvaluate(brown_test)
    print "micro-evaluate affix(regExp(default nn)) = ", at2.MicroEvaluate(brown_test)
    print "micro-evaluate unigram(affix(regExp(default nn))) = ", ut3.MicroEvaluate(brown_test)
    print "micro-evaluate bigram(unigram(affix(regExp(default nn)))) = ", ct2.MicroEvaluate(brown_test)
    
    print "default nn prec tag = AT => " , checkTaggerPrecForTag(nn_tagger, 'AT', brown_test)
    print "default nn recall tag = AT => " , checkTaggerRecallForTag(nn_tagger, 'AT', brown_test)
    
    print "default nn prec tag = NN => " , checkTaggerPrecForTag(nn_tagger, 'NN', brown_test)
    print "default nn recall tag = NN => " , checkTaggerRecallForTag(nn_tagger, 'NN', brown_test)
    
    print "difficult tags in simplified dataset : ", checkDifficultTags(ct2, brown_test, True, 4)
if __name__ == '__main__':
    main() 