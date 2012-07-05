import nltk
import nltk.grammar as gram
from nltk.probability import ConditionalFreqDist , FreqDist , DictionaryProbDist ,ProbDistI,  MLEProbDist, LidstoneProbDist
from nltk.grammar import WeightedGrammar , WeightedProduction , Nonterminal
from nltk.corpus import LazyCorpusLoader, BracketParseCorpusReader , simplify_wsj_tag
import matplotlib.pyplot as plt
import numpy as np
from nltk.model import NgramModel

# return the number of trees in the whole treebank
def treebank_tree_num(treebank):
    count = 0
    for item in treebank.items:
        count += len( treebank.parsed_sents(item))
    return count

# return list of the remain words from treebank after n trees counted  
def get_treebank_test_sent(treebank, n):
    nt = 0
    test = []
    for item in treebank.items:
        for tree in treebank.parsed_sents(item):
            if nt >= n:
                test.extend(['START']+tree.leaves())
            nt += 1
    return test

# generate n sentences from bigram , each sent have 30 words
def generate_sent(bigram , n):
    s = []
    for i in range(0,n):
        s.append(bigram.generate(30))
    return s

#-- return a bigram model acquired from the corpus
#-- n is the number of trees from the corpus to use for training
#-- estimator is a function that takes a ConditionalFreqDist and returns a ConditionalProbDist.  
#-- By default, use None - meaning, use the MLEProbDist estimator.
#-- return a bigram model 
def bigram_learn(treebank, n, estimator=None):
    if estimator is None:
        def e(fdist, bins):
            MLEProbDist(fdist)
        estimator = e
    nt = 0
    train = []
    for item in treebank.items:
        if nt > n: break
        for tree in treebank.parsed_sents(item):
            if nt > n: break
            train.extend(['START']+tree.leaves())
            nt += 1
    
    return NgramModel(2, train, estimator)

def main():
    treebank = LazyCorpusLoader('treebank/combined', BracketParseCorpusReader, 
                                r'wsj_.*\.mrg', tag_mapping_function=simplify_wsj_tag)
    treeNum = treebank_tree_num(treebank)
    
    LIDestimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    
    MLEbigram = bigram_learn(treebank, treeNum*0.8) #  MLEestimator estimator
    LIDbigram = bigram_learn(treebank, treeNum*0.8 , LIDestimator)
    
    test = get_treebank_test_sent(treebank, treeNum*0.8)
    MLEentropy = MLEbigram.entropy(test)
    LIDentropy = LIDbigram.entropy(test)
    
    if MLEentropy < LIDentropy:
        sents = generate_sent(MLEbigram , 50)
    else : 
        sents = generate_sent(LIDbigram , 50)
    print sents
    
if __name__ == '__main__':
    main() 