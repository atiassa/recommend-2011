import nltk
import nltk.grammar as gram
from nltk.probability import DictionaryProbDist , FreqDist
from nltk.grammar import WeightedGrammar , WeightedProduction , Nonterminal
from my_simplify import *
import matplotlib.pyplot as plt
import numpy as np
import q2_2

def plot_histogram(hTitle,yTitle, fd):
    y = []
    sumall = sum(fd.values())
    for k in fd.keys()[:5]:
        y.append(float(fd[k])/sumall)
    plt.bar(np.arange(5),y)
    plt.xticks( np.arange(5) + 0.5, fd.keys()[:5])
    plt.title(hTitle )
    plt.ylabel(yTitle)
    plt.show()

def dist_NP(above , tree , p , pp):
    if isinstance(tree, str):
        if ((pp == above) | (above == "")) & (p == "NP"):
            return [tree]
        else: return []
    l = []
    if ((pp == above) | (above == "")) & (p == "NP"):
        l.append(tree.node)
    for child in tree[0:]:
        l.extend(dist_NP(above , child,tree.node,p))
        
    return l
         
def Report_NP_statistics(treebank):
    l = []
    l_S = []
    l_VP = []
    for tree in treebank.parsed_sents2():
        tree = q2_2.filter_NONE(tree)
        if tree!= None:
            l.extend(dist_NP("" , tree,"X","X"))
            l_S.extend(dist_NP("S" , tree,"X","X"))
            l_VP.extend(dist_NP("VP" , tree,"X","X"))
    fd = FreqDist(l)
    fd_S = FreqDist(l_S)
    fd_VP = FreqDist(l_VP)
    plot_histogram("All NPs","distribution " , fd)
    plot_histogram("NPs under S","distribution " , fd_S)
    plot_histogram("NPs under VP ","distribution " , fd_VP)
    
def main():   
    Report_NP_statistics(treebank)
    
if __name__ == '__main__':
    main() 