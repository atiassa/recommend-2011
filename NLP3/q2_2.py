import nltk
import nltk.grammar as gram
from nltk.probability import DictionaryProbDist , FreqDist
from nltk.grammar import WeightedGrammar , WeightedProduction , Nonterminal
from nltk.corpus import LazyCorpusLoader, BracketParseCorpusReader , simplify_wsj_tag
import matplotlib.pyplot as plt
import numpy as np


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

# - treebank is the nltk.corpus.treebank lazy corpus reader
# - n indicates the number of trees to read
# - return an nltk.WeigthedGrammar
def pcfg_learn(treebank, n):
    pcount = {} 
    lcount = {}
    productions = []
    treebank_interior_nodes = 0;
    
    for item in treebank.items[:n]:
        for tree in treebank.parsed_sents(item):
            treebank_interior_nodes += len(tree.productions()) + len(tree.leaves())
            tree = filter_NONE(tree)
            if tree!= None:
                productions += tree.productions()
            
    for prod in productions:
        lcount[prod.lhs()] = lcount.get(prod.lhs(), 0) + 1 
        pcount[prod]       = pcount.get(prod,       0) + 1 

    prods = [WeightedProduction(p.lhs(), p.rhs(), 
                      prob=float(pcount[p]) / lcount[p.lhs()]) 
             for p in pcount] 
    
    learned_pcfg = WeightedGrammar(Nonterminal('S'), prods)

    plot_dist_productions_by_frequency(productions)
    print 'How many productions are learned from the trees? %d ' % len(learned_pcfg.productions())
    print 'How many interior nodes were in the treebank?    %d ' % treebank_interior_nodes
    return  learned_pcfg

#-- treebank is the nltk.corpus.treebank lazy corpus reader (simplified tags)
#-- n indicates the number of trees to read
#-- return an nltk.WeigthedGrammar in CNF
def pcfg_cnf_learn(treebank, n):
    pcount = {} 
    lcount = {}
    productions = []
    treebank_interior_nodes = 0
    cnf_interior_nodes = 0
    
    for item in treebank.items[:n]:
        for tree in treebank.parsed_sents(item):
            treebank_interior_nodes += len(tree.productions()) + len(tree.leaves())
            tree = filter_NONE(tree)
            if tree!= None:
                tree.chomsky_normal_form(horzMarkov = 2)
                cnf_interior_nodes += len(tree.productions()) + len(tree.leaves())
                productions += tree.productions()
            
    for prod in productions:
        lcount[prod.lhs()] = lcount.get(prod.lhs(), 0) + 1 
        pcount[prod]       = pcount.get(prod,       0) + 1 

    prods = [WeightedProduction(p.lhs(), p.rhs(), 
                      prob=float(pcount[p]) / lcount[p.lhs()]) 
             for p in pcount] 
  
    learned_pcfg_cnf = WeightedGrammar(Nonterminal('S'), prods)
    
    print 'How many productions are learned from the CNF trees?   %d ' % len(learned_pcfg_cnf.productions())
    print 'How many interior nodes were in the original treebank? %d ' %  treebank_interior_nodes
    print 'How many interior nodes were in the CNF treebank?      %d ' % cnf_interior_nodes
    return learned_pcfg_cnf 

def plot_dist_productions_by_frequency(productions):
    f= FreqDist(productions)
    fdd = FreqDist(f.values())
    x = []
    y = []
    for k in fdd.keys():
        x.append(k)
        y.append(fdd[k])
    plt.plot(x,y,lw=2,color= 'b')
    plt.title('Productions by frequency' )
    plt.xlabel('frequency')
    plt.ylabel('number of rules with frequency')
    plt.show()

def main():    
    n = 20
    treebank = LazyCorpusLoader('treebank/combined', BracketParseCorpusReader, 
                                r'wsj_.*\.mrg', tag_mapping_function=simplify_wsj_tag)
    print "\n--PCFG--" 
    learned_pcfg = pcfg_learn(treebank, n) 
    print "\n--CNF PCFG--" 
    learned_pcfg_cnf = pcfg_cnf_learn(treebank, n) 
    
if __name__ == '__main__':
    main() 