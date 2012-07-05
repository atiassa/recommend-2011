import nltk
import nltk.grammar as gram
from nltk.probability import DictionaryProbDist , FreqDist
from nltk.grammar import WeightedGrammar , WeightedProduction , Nonterminal
from nltk.corpus import LazyCorpusLoader, BracketParseCorpusReader , simplify_wsj_tag
import matplotlib.pyplot as plt
import numpy as np
import q2_2

def plot_histogram(hTitle,xTitle,yTitle, fd):
    y = []
    for k in fd.keys():
        y.append(fd[k])
    plt.hist(y )
    plt.title(hTitle )
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    plt.show()

def dist_NP(above , tree , p):
    if isinstance(tree, str):
        return []
    l = []
    for child in tree[0:]:
        if p :
            if tree.node =='NP':
                l.append(child.node)
        if (tree.node == above) | (above =="") :
            l.extend(dist_NP(above , child,True))
        else: l.extend(dist_NP(above , child,False))
    return l
         
def Report_NP_statistics(treebank):
    l = []
    l_S = []
    l_VP = []
    for item in treebank.items[2:]:
        for tree in treebank.parsed_sents(item):
            tree = q2_2.filter_NONE(tree)
            if tree!= None:
                l.extend(dist_NP("" , tree,True))
                l_S.extend(dist_NP("S" , tree,False))
                l_VP.extend(dist_NP("VP" , tree,False))
                
    fd = FreqDist(l)
    fd_S = FreqDist(l_S)
    fd_VP = FreqDist(l_VP)
    plot_histogram("All NPs","RHS non-term","distribution " , fd)
#    plot_histogram("NPs under S","RHS non-term","distribution " , fd_S)
#    plot_histogram("NPs under VP ","RHS non-term","distribution " , fd_VP)
    
def main():   
    treebank = LazyCorpusLoader('treebank/combined', BracketParseCorpusReader, 
                                r'wsj_.*\.mrg', tag_mapping_function=simplify_wsj_tag)
    Report_NP_statistics(treebank)
    
if __name__ == '__main__':
    main() 