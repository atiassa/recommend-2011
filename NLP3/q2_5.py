import nltk
import nltk.grammar as gram
from nltk.probability import ConditionalFreqDist , FreqDist , DictionaryProbDist ,ProbDistI,  MLEProbDist, LidstoneProbDist
from nltk.grammar import WeightedGrammar , WeightedProduction , Nonterminal
import my_simplify
import matplotlib.pyplot as plt
import numpy as np
from nltk.model import NgramModel
import q2_2
import q2_1
import q2_4

def bigram_learn(train, estimator=None):
    if estimator is None:
        estimator = lambda fdist, bins: MLEProbDist(fdist)

    return NgramModel(2, train, estimator)

def likelihood(treebank, model):
    sigma = 0
    for tree in treebank:
        sigma += model.entropy(tree.leaves())

    avrg = sigma / len(treebank)
    return avrg

def main():
    n= 2000
    learned_pcfg = q2_2.pcfg_learn(my_simplify.treebank, n)
    sents = []
    for i in range(0,1000):
        sents.append(['START']+q2_1.pcfg_generate(learned_pcfg).leaves())

    LIDestimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    MLEbigram = bigram_learn(sents)
    LIDbigram = bigram_learn(sents, LIDestimator)
    
    MLEentropy = MLEbigram.entropy(test)
    LIDentropy = LIDbigram.entropy(test)
    
    if MLEentropy < LIDentropy:
        sents = generate_sent(MLEbigram , 50)
    else : 
        sents = generate_sent(LIDbigram , 50)
    print sents
     
if __name__ == '__main__':
    main() 