import  nltk
from itertools import izip
from nltk.corpus import brown
from operator import itemgetter

#computes for the tagger Avg of F-measure.
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

#calc TP (tag both in the test and by the tagger)
def calcTP(tag, CorpusTags, TaggerTags):
    tp = 0
    for x, y in izip(CorpusTags, TaggerTags):
        w,t = x
        if x == y and t == tag :
            tp += 1
    return tp

#calc TN (non-tag both in the test and by the tagger)    
def calcTN(tag, CorpusTags, TaggerTags):
    tn = 0
    for x, y in izip(CorpusTags, TaggerTags):
        testw,testTag = x
        taggerw,taggerTag = y
        if testw == taggerw and testTag != tag and taggerTag != tag :
            tn += 1
    return tn
    
#calc FP (non-tag by the test and tag by the tagger)
def calcFP(tag, CorpusTags, TaggerTags):
    fp = 0
    for x, y in izip(CorpusTags, TaggerTags):
        testw,testTag = x
        taggerw,taggerTag = y
        if testw == taggerw and testTag != tag and taggerTag == tag :
            fp += 1
    return fp

#calc FN (tag by the test and non tag by the tagger)
def calcFN(tag, CorpusTags, TaggerTags):
    fn = 0
    for x, y in izip(CorpusTags, TaggerTags):
        testw,testTag = x
        taggerw,taggerTag = y
        if testw == taggerw and testTag == tag and taggerTag != tag :
            fn += 1
    return fn
    
#calc Precision(T) = TP / TP + FP
def calcPrec(tag, CorpusTags, TaggerTags):
    tp = calcTP(tag, CorpusTags, TaggerTags)
    fp = calcFP(tag, CorpusTags, TaggerTags)
    if tp+fp == 0:
        prec = 0
    else:
        prec = float(float(tp)/(tp+fp))
    return prec

#calc Recall(T) = TP / TP + FN    
def calcRecall(tag, CorpusTags, TaggerTags):
    tp = calcTP(tag, CorpusTags, TaggerTags)
    fn = calcFN(tag, CorpusTags, TaggerTags)
    if tp + fn == 0:
        recall = 0
    else:
        recall = float(float(tp)/(tp+fn))
    return recall
    
#calc F-Measure(T) = 2 x Precision x Recall / (Recall + Precision)  
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

########################################################################
#defining the simplified taggers and the simplified test and train sets# 
#and returning the requested tagger and the test set                   #
########################################################################
def getTaggerAndTestSetInSimplifiedMode(taggerName):
    brown_news_taggedS = brown.tagged_sents(categories='news', simplify_tags=True)
    brown_trainS = brown_news_taggedS[100:]
    brown_testS = brown_news_taggedS[:100]
    
    nn_taggerS = nltk.DefaultTagger('NN')
    regexp_taggerS = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
                                       (r'(The|the|A|a|An|an)$', 'AT'),   # articles
                                       (r'.*able$', 'JJ'),                # adjectives
                                       (r'.*ness$', 'NN'),                # nouns formed from adjectives
                                       (r'.*ly$', 'RB'),                  # adverbs
                                       (r'.*s$', 'NNS'),                  # plural nouns
                                       (r'.*ing$', 'VBG'),                # gerunds
                                       (r'.*ed$', 'VBD'),                 # past tense verbs
                                       (r'.*', 'NN')                      # nouns (default)
                                       ],backoff=nn_taggerS)
    at2S = nltk.AffixTagger(brown_trainS, backoff=regexp_taggerS)
    ut3S = nltk.UnigramTagger(brown_trainS, backoff=at2S)
    ct2S = nltk.NgramTagger(2, brown_trainS, backoff=ut3S)
    if taggerName == "DefaultTagger":
        return nn_taggerS,brown_testS
    else:
        if taggerName == "RegExpTagger":
            return regexp_taggerS, brown_testS
        else:
            if taggerName == "AffixTagger":
                return at2S,brown_testS
            else:
                if taggerName == "UnigramTagger":
                    return ut3S,brown_testS
                else:
                    if taggerName == "BigramTagger":
                        return ct2S,brown_testS

##########################################################################################################################
#Check which X tags are difficult in the dataset.                                                                        #
#to check this we need to calculate precision for each tag and the tags with the lowest precision are the difficult tags.#
##########################################################################################################################
def getDifficultTags(tagger, testCorpus, x, tagsSet):
    difficultTags = []
    precs = []
    #defining which tags are we checking full or simplified tags if simplified -> getting the tagger and the testCorpus according to simplified tags set    
    corpusTokens = sum(testCorpus, [])
    #calculating precision for each tag
    tagger_tags = tagger.batch_tag([nltk.untag(sent) for sent in testCorpus])
    taggedTokens = sum(tagger_tags, [])
    for t in tagsSet:
        p = calcPrec(t, corpusTokens, taggedTokens)
        precs.append((t,p))
    #insert x lowest tags to difficultTags
    precs = sorted(precs, key=itemgetter(1))
    for w,p in precs:
        if len(difficultTags) < x:
            difficultTags.append(w)     
    return difficultTags


#############################################################
#############################################################
#Check which X tags are difficult in the simplified tagsSet.#
#############################################################
#############################################################
def checkSimplifiedDifficultTags(taggerName, x):
    tagger, testCorpus = getTaggerAndTestSetInSimplifiedMode(taggerName)
    tags = ['ADJ', 'ADV', 'CNJ', 'DET', 'EX', 'FW', 'MOD', 'N', 'NP', 'NUM', 'PRO', 'P', 'TO', 'UH', 'V', 'VD', 'VG', 'VN', 'WH']
    return getDifficultTags(tagger, testCorpus, x, tags)

###################
#get full tagsSet.#
###################
def getFullTagsList():
    ans = []
    brown_news_tagged = brown.tagged_sents()
    for sen in brown_news_tagged:
        for w,t in sen:
            if not ans.__contains__(t):
                ans.append(t)
    return ans
    
#######################################################
#Check which X tags are difficult in the full tagsSet.#
#######################################################
def checkFullDifficultTags(tagger, testCorpus, x):
    tags = getFullTagsList()
    return getDifficultTags(tagger, testCorpus, x, tags)

def main():
    nltk.TaggerI.MicroEvaluate = MicroEvaluate 
    
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
    print ""  
    
    print "micro-evaluate default nn = ", nn_tagger.MicroEvaluate(brown_test)
    print "micro-evaluate regExp(default nn) = ", regexp_tagger.MicroEvaluate(brown_test)
    print "micro-evaluate affix(regExp(default nn)) = ", at2.MicroEvaluate(brown_test)
    print "micro-evaluate unigram(affix(regExp(default nn))) = ", ut3.MicroEvaluate(brown_test)
    print "micro-evaluate bigram(unigram(affix(regExp(default nn)))) = ", ct2.MicroEvaluate(brown_test)
    print ""  
    
    print "default nn prec tag = AT => " , checkTaggerPrecForTag(nn_tagger, 'AT', brown_test)
    print "default nn recall tag = AT => " , checkTaggerRecallForTag(nn_tagger, 'AT', brown_test)
    print "" 
    
    print "default nn prec tag = NN => " , checkTaggerPrecForTag(nn_tagger, 'NN', brown_test)
    print "default nn recall tag = NN => " , checkTaggerRecallForTag(nn_tagger, 'NN', brown_test)
    print "" 

    print "4 most difficult tags in simplified tagsSet - bigramTagger with all the backoffs:", checkSimplifiedDifficultTags("BigramTagger", 4)
    print "4 most difficult tags in full tagsSet - bigramTagger with all the backoffs: ", checkFullDifficultTags(ct2, brown_test, 4)
    print "" 

if __name__ == '__main__':
    main() 