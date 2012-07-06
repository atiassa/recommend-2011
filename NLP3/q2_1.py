from nltk.grammar import Nonterminal ,toy_pcfg2
from nltk.probability import ConditionalFreqDist , FreqDist , DictionaryProbDist ,ProbDistI,  MLEProbDist
from nltk.tree import Tree
import numpy as np
import math



def makeLhrProbDict(grammar):
    LhsProbDist = {}
    for nonTr in grammar.productions():
        nonTr_productions = grammar.productions(nonTr.lhs())
        dict = {}
        for pr in nonTr_productions:
            dict[pr.rhs()] = pr.prob()
        probDist = DictionaryProbDist(dict)
        LhsProbDist[nonTr.lhs()] = probDist
    return LhsProbDist

# return a tree sampled from the language described by the grammar
def pcfg_generate(grammar):
    start = grammar.start()
    pd = makeLhrProbDict(grammar)
    t = generate_one(grammar, [start],pd)
    return t

def generate_one(grammar, items ,pd ):
    if len(items) == 1 :
        if isinstance(items[0], Nonterminal):
            rhs = pd[items[0]].generate()
            return Tree(str(items[0]), generate_one(grammar, rhs,pd))
        else:
            return items
    else:
        l = [] 
        for r in items:
            l.append(generate_one(grammar, [r],pd))
        return l

# - Generate 1,000 random sentences using nltk.grammar.toy_pcfg2
# - Compute the frequency distribution of each non-terminal and pre-terminal in the generated corpus.
# - For each distribution, compute the KL-divergence between the MLE estimation of the probability
#      distribution constructed on your test corpus and toy_pcfg2.  
def validate_pcfg_generate(grammar):
    pd = makeLhrProbDict(grammar)
    productions = []
    cfd = ConditionalFreqDist()
    
    for i in np.arange(1000):
        tree = pcfg_generate(grammar)
        productions += tree.productions()    

    for p in productions:
        cfd[p.lhs()].inc(p.rhs())
        
    for c in cfd.conditions():
        p = MLEProbDist(cfd[c])
        q = pd[c]
        div = KL_Divergence(p,q)
        print "KL_Divergence for %s = %f" %(c , div)
    
# calc KL div between p ang q safely
def KL_Divergence(p,q):
    eps = 0.0001
    SP = set(p.samples()) 
    SQ = set(q.samples())
    if (len(SP) == 0) | (len(SQ) == 0):
        return -1
    SU = SP | SQ
    pc = eps*len(SU - SP)/len(SP) 
    qc = eps*len(SU - SQ)/len(SQ)
    Ptag = []
    Qtag = []
    for x in SU:
        if x in SP:
            Ptag.append(p.prob(x)-pc)
        else: Ptag.append(eps)
        if x in SQ:
            Qtag.append(q.prob(x)-qc)
        else: Qtag.append(eps)
    div = 0
    for pi , qi in zip(Ptag,Qtag):
        d = pi / qi
        if (d > 0):
            div += pi * math.log(d) 
    return div  

def main():
    grammar = toy_pcfg2
    validate_pcfg_generate(grammar)
    
if __name__ == '__main__':
    main() 