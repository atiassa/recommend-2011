import nltk
import nltk.grammar as gram
from nltk.probability import ConditionalFreqDist , FreqDist , ConditionalProbDist,  MLEProbDist, LidstoneProbDist
from  my_simplify import *
import numpy as np
import math
import random
from q2_2 import *

class BigramModel():
    def __init__(self, corpus, n, estimator=None): 
        if estimator is None: 
            estimator = lambda fdist, bins: MLEProbDist(fdist)
        bi = []
        self._l = []
        for tree in corpus[:n]:
            ts =  tree.leaves()
            sent = ['START'] + ts
            bi += nltk.bigrams(sent)
            self._l.append(len(sent))
            
        cfd = ConditionalFreqDist(bi)
        self._model = ConditionalProbDist(cfd, estimator, len(cfd))

    def prob(self, word, context):
        contpd = self._model[context]
        if word in contpd.samples():
            if contpd.prob(word) == 0:
                return 1
            return  contpd.prob(word)
        else:
            return 1

    def logprob(self, word, context):
        return -math.log(self.prob(word, context), 2) 

    def generate(self, context="START"):
        wordsNum = random.choice(self._l) 
        text = [context]
        for i in range(wordsNum):
            text.append(self._generate_one(text[-1]))
        return text


    def _generate_one(self, context):
        if context == '.':
            context = 'START'
        if context in self._model.conditions():
            return self._model[context].generate()

    def entropy(self, text):
        e = 0.0
        for i in range(1, len(text)):
            context = text[-1] 
            token = text[i]
            e += self.logprob(token, context)
        return e

#-- return a bigram model acquired from the corpus
#-- n is the number of trees from the corpus to use for training
#-- estimator is a function that takes a ConditionalFreqDist and returns a ConditionalProbDist.  
#-- By default, use None - meaning, use the MLEProbDist estimator.
#-- return a bigram model 
def bigram_learn(corpus, n, estimator=None):
    return BigramModel(corpus, n, estimator)

def calc_entropy(corpus, train_size, bigram):
    sigma = 0
    length = 0
    for sent in corpus[train_size:]:
        sigma += bigram.entropy(" ".join(sent.leaves()))
        length += 1
    return float(sigma) / length

def main():
    corpus = []
    for tree in treebank.parsed_sents2():
        tree = filter_NONE(tree)
        if tree!= None:
            corpus.append(tree)
    treeNum = len(corpus)
                  
    LIDestimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2,bins)
    
    train_size = int(treeNum*0.8)
    MLEbigram = bigram_learn(corpus, train_size) #  MLEestimator estimator
    LIDbigram = bigram_learn(corpus, train_size , LIDestimator)
    
    MLEentropy = calc_entropy(corpus, train_size, MLEbigram)
    LIDentropy = calc_entropy(corpus, train_size, LIDbigram)
    print "MLE entropy = %f" %MLEentropy 
    print "LID entropy = %f" %LIDentropy
    
    for i in range(50):
        print str(i+1) +" " + " ".join(MLEbigram.generate()[1:]) 
    
if __name__ == '__main__':
    main() 