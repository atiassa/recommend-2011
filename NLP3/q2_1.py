from nltk.grammar import Nonterminal ,toy_pcfg2
from nltk.probability import DictionaryProbDist , FreqDist
from nltk.tree import Tree
import numpy as np

LhsProbDist = {}

def makeLhrProbDict(grammar):
    for nonTr in grammar.productions():
        nonTr_productions = grammar.productions(nonTr.lhs())
        dict = {}
        for pr in nonTr_productions:
            dict[pr.rhs()] = pr.prob()
        
        probDist = DictionaryProbDist(dict)
        LhsProbDist[nonTr.lhs()] = probDist

# return a tree sampled from the language described by the grammar
def pcfg_generate(grammar):
    start = grammar.start()
    return generate_one(grammar, [start])

def generate_one(grammar, items):
    if len(items) == 1 :
        if isinstance(items[0], Nonterminal):
            rhs = LhsProbDist[items[0]].generate()
            return Tree(items[0], generate_one(grammar, rhs))
        else:
            return items
    else:
        l = [] 
        for r in items:
            l.append(generate_one(grammar, [r]))
        return l
    
def validate_pcfg_generate(grammar):
    pcount = {} # Production count: the number of times a given production occurs 
    lcount = {} # LHS-count: counts the number of times a given lhs occurs
    for i in np.arange(0,1000):
        sentence = pcfg_generate(grammar)
        
#        
#    
#  
#    for prod in productions: 
#        lcount[prod.lhs()] = lcount.get(prod.lhs(), 0) + 1 
#        pcount[prod]       = pcount.get(prod,       0) + 1 
#
#    prods = [WeightedProduction(p.lhs(), p.rhs(), 
#                                 prob=float(pcount[p]) / lcount[p.lhs()]) 
#             for p in pcount] 
#    return WeightedGrammar(start, prods) 
   
    
def main():
    grammar = toy_pcfg2
    LhsProbDist = makeLhrProbDict(grammar)
    validate_pcfg_generate(grammar)
    
if __name__ == '__main__':
    main() 