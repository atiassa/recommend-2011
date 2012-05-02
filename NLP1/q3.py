import  nltk
from itertools import izip
from nltk.corpus import brown
from nltk.metrics import accuracy as _accuracy
from nltk.probability import FreqDist
from numpy.matrixlib.defmatrix import matrix
from operator import itemgetter
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

########################################################################
########################################################################
#defining the simplified taggers and the simplified test and train sets# 
#and returning the requested tagger and the test set                   #
########################################################################
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
##########################################################################################################################
#Check which X tags are difficult in the dataset.                                                                        #
#to check this we need to calculate precision for each tag and the tags with the lowest precision are the difficult tags.#
##########################################################################################################################
######################################################################################################################    
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
#Check which X tags are difficult in the simplified tagsSet.#                                                                        #
#############################################################
#############################################################

def checkSimplifiedDifficultTags(taggerName, x):
    tagger, testCorpus = getTaggerAndTestSetInSimplifiedMode(taggerName)
    tags = ['ADJ', 'ADV', 'CNJ', 'DET', 'EX', 'FW', 'MOD', 'N', 'NP', 'NUM', 'PRO', 'P', 'TO', 'UH', 'V', 'VD', 'VG', 'VN', 'WH']
    return getDifficultTags(tagger, testCorpus, x, tags)

#######################################################
#######################################################
#Check which X tags are difficult in the full tagsSet.#                                                                        #
#######################################################
#######################################################

def checkFullDifficultTags(tagger, testCorpus, x):
    tags = []
    return getDifficultTags(tagger, testCorpus, x, tags)

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
    nltk.DefaultTagger.MicroEvaluate = MicroEvaluate
    nltk.RegexpTagger.MicroEvaluate = MicroEvaluate
    nltk.AffixTagger.MicroEvaluate = MicroEvaluate
    nltk.UnigramTagger.MicroEvaluate = MicroEvaluate
    nltk.NgramTagger.MicroEvaluate = MicroEvaluate
    
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
    
#    print nn_tagger.ConfusionMatrix(brown_test)
#    print ct2.ConfusionMatrix(brown_test)
#    print ct2S.ConfusionMatrix(brown_test)
    
#    print "evaluate2 default nn = " , nn_tagger.evaluate2(brown_test)
#    print "evaluate2 regExp(default nn) = " ,regexp_tagger.evaluate2(brown_train)
#    print "evaluate2 affix(regExp(default nn)) = " ,at2.evaluate2(brown_train)
#    print "evaluate2 unigram(affix(regExp(default nn))) = " ,ut3.evaluate2(brown_train)
#    print "evaluate2 bigram(unigram(affix(regExp(default nn)))) = " ,ct2.evaluate2(brown_train)   
#    print "evaluate default nn = " , nn_tagger.evaluate(brown_test)
#    print "evaluate regExp(default nn) = " ,regexp_tagger.evaluate(brown_test)
#    print "evaluate affix(regExp(default nn)) = " ,at2.evaluate(brown_test)
#    print "evaluate unigram(affix(regExp(default nn))) = " ,ut3.evaluate(brown_test)
#    print "evaluate bigram(unigram(affix(regExp(default nn)))) = " ,ct2.evaluate(brown_test)
#    
#    print "micro-evaluate default nn = ", nn_tagger.MicroEvaluate(brown_test)
#    print "micro-evaluate regExp(default nn) = ", regexp_tagger.MicroEvaluate(brown_test)
#    print "micro-evaluate affix(regExp(default nn)) = ", at2.MicroEvaluate(brown_test)
#    print "micro-evaluate unigram(affix(regExp(default nn))) = ", ut3.MicroEvaluate(brown_test)
#    print "micro-evaluate bigram(unigram(affix(regExp(default nn)))) = ", ct2.MicroEvaluate(brown_test)
#    
#    print "default nn prec tag = AT => " , checkTaggerPrecForTag(nn_tagger, 'AT', brown_test)
#    print "default nn recall tag = AT => " , checkTaggerRecallForTag(nn_tagger, 'AT', brown_test)
#    
#    print "default nn prec tag = NN => " , checkTaggerPrecForTag(nn_tagger, 'NN', brown_test)
#    print "default nn recall tag = NN => " , checkTaggerRecallForTag(nn_tagger, 'NN', brown_test)

#    print "4 most difficult tags in simplified tagsSet - bigramTagger with all the backoffs:", checkSimplifiedDifficultTags("BigramTagger", 4)
#    print "4 most difficult tags in full tagsSet - bigramTagger with all the backoffs: ", checkFullDifficultTags(ct2, brown_test, 4)
    
if __name__ == '__main__':
    main() 