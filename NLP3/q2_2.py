import nltk
import nltk.grammar as gram
from nltk.probability import DictionaryProbDist , FreqDist
from nltk.grammar import WeightedGrammar , WeightedProduction , Nonterminal
from my_simplify import *
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

# create Weighted Grammar for given productions
def createWG(productions):
    pcount = {} 
    lcount = {}
    for prod in productions:
        lcount[prod.lhs()] = lcount.get(prod.lhs(), 0) + 1
        pcount[prod] = pcount.get(prod, 0) + 1
    
    prods = [WeightedProduction(p.lhs(), p.rhs(), 
             prob=float(pcount[p]) / lcount[p.lhs()]) for 
             p in pcount]
    learned_pcfg_cnf = WeightedGrammar(Nonterminal('S'), prods)
    return learned_pcfg_cnf


# - treebank is the nltk.corpus.treebank lazy corpus reader
# - n indicates the number of trees to read
# - return an nltk.WeigthedGrammar
def pcfg_learn(treebank, n):
    productions = []
    treebank_interior_nodes = 0;
    nt = 0
    for tree in treebank.parsed_sents2()[:n]:
        tree = filter_NONE(tree)
        if tree!= None:
            treebank_interior_nodes += len(tree.productions()) + len(tree.leaves())
            productions += tree.productions()
            nt += 1
        
    learned_pcfg = createWG( productions)

#    plot_dist_productions_by_frequency(productions)
#    print 'How many productions are learned from the trees? %d ' % len(learned_pcfg.productions())
#    print 'How many interior nodes were in the treebank?    %d ' % treebank_interior_nodes
    return  learned_pcfg

#-- treebank is the nltk.corpus.treebank lazy corpus reader (simplified tags)
#-- n indicates the number of trees to read
#-- return an nltk.WeigthedGrammar in CNF
def pcfg_cnf_learn(treebank, n):
    productions = []
    treebank_interior_nodes = 0
    cnf_interior_nodes = 0
    nt = 0
    for tree in treebank.parsed_sents2()[:n]:
        tree = filter_NONE(tree)
        if tree!= None:
            treebank_interior_nodes += len(tree.productions()) + len(tree.leaves())
            tree.chomsky_normal_form(horzMarkov = 2)
            cnf_interior_nodes += len(tree.productions()) + len(tree.leaves())
            productions += tree.productions()
            nt += 1
            
    learned_pcfg_cnf = createWG(productions)
    
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

# determines whether a tree can be parsed by a grammar
# tests that a given tree can be produced by a grammar
def cover_tree(grammar, tree):
    for pt in tree.productions():
        found = False
        for pg in grammar.productions():
            if (pt.rhs()== pg.rhs()) & (pt.lhs()==pg.lhs()):
                found = True 
                break
        if not found :
            return False
    return True

# keep only the F most frequent rules out of the N rules in the PCFG
# return the number of trees "missed" by the new pcfg
def count_misses(pcfg,treebank,n):
    misses = 0
    nt = 0
    for tree in treebank.parsed_sents2()[:n]:
            tree = filter_NONE(tree)
            nt += 1
            if not cover_tree(pcfg, tree):
                misses +=1
    return misses


# Assume we "cut" the tail of the learned PCFG, that is we remove the least frequent rules,
# so that we keep only the F most frequent rules out of the N rules in the PCFG
# Draw a plot that indicates the number of trees "missed" 
# as the number of rules is reduced (sample every 10% of the size of the grammar).   
def plot_misses(pcfg,treebank,n):
    productions = []
    for tree in treebank.parsed_sents2()[:n]:
        tree = filter_NONE(tree)
        if tree!= None:
            productions += tree.productions()
    fk= FreqDist(productions).keys()
    
    x = []
    y = []
    for reduced in np.arange(10):
        F = int(len(fk)*(reduced*0.1))
        x.append(F)
        prodsTake = list(productions)
        for k in fk[len(fk)-F:]:
            prodsTake.remove(k)
        if len(prodsTake)==0:
            y.append(len(prodsTake))
            continue
        cutPcfg = createWG(prodsTake)
        y.append(count_misses(cutPcfg,treebank,n))
        
    plt.plot(x,y,lw=1.5,color= 'b')
    plt.title('cut the tail of the learned PCFG' )
    plt.xlabel('F cuted from pcfg')
    plt.ylabel('misses')
    plt.show()     
    
     
def main():    
    n = 1000
    print "--PCFG--" 
    learned_pcfg = pcfg_learn(treebank, n)
    plot_misses(learned_pcfg,treebank,n) 
    print "\n--CNF PCFG--" 
    learned_pcfg_cnf = pcfg_cnf_learn(treebank, n) 
    
if __name__ == '__main__':
    main() 