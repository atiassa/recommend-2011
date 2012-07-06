import nltk
from my_simplify import *
from  q2_2 import *
from  q2_1 import *
from  q2_4 import *

def main():
    corpus = []
    for tree in treebank.parsed_sents2():
        tree = filter_NONE(tree)
        if tree!= None:
            corpus.append(tree)
    treeNum = len(corpus)
    
    train_size = int(treeNum*0.8)
    MLEbigram = bigram_learn(corpus, train_size) #  MLEestimator estimator
    
    learned_pcfg = pcfg_learn(treebank, 1000)
    trees = []
    for i in np.arange(1000):
        trees.append(pcfg_generate(learned_pcfg))
    
    MLEentropy = calc_entropy(corpus, train_size, MLEbigram)
    print "MLE bigram entropy = %f" %MLEentropy
    
    PCFGentropy = calc_entropy(trees, 0, MLEbigram)
    print "learned PCFG entropy = %f" %PCFGentropy
     
if __name__ == '__main__':
    main() 