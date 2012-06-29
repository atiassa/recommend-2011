from nltk.grammar import Nonterminal ,toy_pcfg2
from nltk.probability import DictionaryProbDist 
from nltk.tree import Tree

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
    LhsProbDist = makeLhrProbDict(grammar)
    start = grammar.start()
    return generate_one(grammar, [start] ,LhsProbDist)

def generate_one(grammar, items,LhsProbDist):
    if len(items) == 1 :
        if isinstance(items[0], Nonterminal):
            rhs = LhsProbDist[items[0]].generate()
            return Tree(items[0], generate_one(grammar, rhs,LhsProbDist))
        else:
            return items
    else:
        l = [] 
        for r in items:
            l.append(generate_one(grammar, [r] ,LhsProbDist))
        return l
                
def main():
#    t= Tree("1",["a"])
#
#    t.draw()

    grammar = toy_pcfg2
    s = pcfg_generate(grammar)
    s.draw()
    np_productions = toy_pcfg2.productions(Nonterminal('NP'))
    dict = {}
    for pr in np_productions: dict[pr.rhs()] = pr.prob()
    np_probDist = DictionaryProbDist(dict)
    
    # Generate a random RHS from np_probDist
    print np_probDist.generate()
    
    # Each time you call, you get a random sample
    print np_probDist.generate()
    print np_probDist.generate()
    print np_probDist.generate()
    print np_probDist.generate()
    print np_probDist.generate()
    print np_probDist.generate()

    
if __name__ == '__main__':
    main() 