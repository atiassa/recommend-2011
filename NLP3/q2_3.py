import nltk
import nltk.grammar as gram
from nltk.probability import DictionaryProbDist , FreqDist
from nltk.grammar import WeightedGrammar , WeightedProduction , Nonterminal
from nltk.corpus import LazyCorpusLoader, BracketParseCorpusReader , simplify_wsj_tag
import matplotlib.pyplot as plt
import numpy as np

# filter NONE noneterminal from the tree
def filter_NONE(tree):
    if isinstance(tree, str):
        return tree
    if tree.node =='-NONE-':
        return None
    f_childrens = []
    for child in tree[0:]:
        c = filter_NONE(child)
        if c != None :
            f_childrens.append(c)
    if len(f_childrens) == 0: return None
    return nltk.Tree(tree.node,f_childrens)

def plot_histogram(hTitle,xTitle,yTitle, fd):
    y = []
    for k in fd.keys():
        y.append(fd[k])
    plt.hist(y, normed=1)
    plt.title(hTitle )
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    plt.show()

def dist_NP(above , productions):
    fd = FreqDist()
    for p in productions:
        if p.lhs() == Nonterminal('NP'):
            fd.inc(p.rhs())
    return fd

def Report_NP_statistics(treebank,n): 
    productions = []
    for item in treebank.items[:n]:
        for tree in treebank.parsed_sents(item):
            tree = filter_NONE(tree)
            print tree
            if tree!= None:
                productions += tree.productions()
    
    fd_all = dist_NP("", productions)
#    fd_S = dist_NP("S", productions)
#    fd_VP = dist_NP("VP", productions)
    plot_histogram("all","RHS non-term","distribution " , fd_all)
#    plot_histogram("S","RHS non-term","distribution " , fd_S)
#    plot_histogram("VP","RHS non-term","distribution " , fd_VP)
    
def main():    
    n = 1
    treebank = LazyCorpusLoader('treebank/combined', BracketParseCorpusReader, 
                                r'wsj_.*\.mrg', tag_mapping_function=simplify_wsj_tag)
    Report_NP_statistics(treebank, n) 
    
if __name__ == '__main__':
    main() 