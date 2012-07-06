import nltk
from nltk import Tree
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader.bracket_parse import BracketParseCorpusReader

"""
    retruns a simplyfied wsj version of @param tag
    @param tag: a string tag
    @return: retruns a simplyfied wsj version of @param tag
"""
def simplify_my_tag(tag):
    if tag and tag[0] == '^':
        tag = tag[1:]
    try:
        tag = wsj_mapping2[tag.lower()]
    except KeyError:
        pass
    return tag.upper() 


wsj_mapping2 = { 
       '-lrb-': '(',   '-rrb-': ')',    '-lsb-': '(', 
       '-rsb-': ')',   '-lcb-': '(',    '-rcb-': ')', 
       '-none-': '-NONE-',   'cc': 'CNJ',     'cd': 'NUM', 
       'dt': 'DET',    'ex': 'EX',      'fw': 'FW', # existential "there", foreign word 
       'in': 'P',      'jj': 'ADJ',     'jjr': 'ADJ', 
       'jjs': 'ADJ',   'ls': 'L',       'md': 'MOD',  # list item marker 
       'nn': 'N',      'nnp': 'NP',     'nnps': 'NP', 
       'nns': 'N',     'pdt': 'DET',    'pos': '', 
       'prp': 'PRO',   'prp$': 'PRO',   'rb': 'ADV', 
       'rbr': 'ADV',   'rbs': 'ADV',    'rp': 'PRO', 
       'sym': 'S',     'to': 'TO',      'uh': 'UH', 
       'vb': 'V',      'vbd': 'VD',     'vbg': 'VG', 
       'vbn': 'VN',    'vbp': 'V',      'vbz': 'V', 
       'wdt': 'WH',    'wp': 'WH',      'wp$': 'WH', 
       'wrb': 'WH', 
       'bes': 'V',     'hvs': 'V',     'prp^vbp': 'PRO'   # additions for NPS Chat corpus 
        }

"""
    returns a list of trees in @param self with simplyfied tags
    @param self: a treebank loader
    @return: returns a list of trees with simplyfied tags
"""
def parsed_sents2(self):
    return [simplify_tree(tree) for tree in self.parsed_sents()]


"""
    returns a tree with simplyfied tags
    @param tree: a tree
    @return: returns a list of trees with simplyfied tags
"""
def simplify_tree(tree):
    if isinstance(tree, Tree):
        return Tree(simplify_tag(tree.node),[simplify_tree(tree[i]) for i in range(0, len(tree))])
    else:
        return tree    


"""
    retruns a simplyfied wsj version of @param tag
    @param tag: a string tag
    @return: retruns a simplyfied wsj version of @param tag
"""
def simplify_tag(tag):
    if tag.lower() in wsj_mapping2:
        return simplify_my_tag(tag)
    tag = simplify_my_tag(tag)
    if '-' not in tag:
        return tag
    else:
        return tag.split('-')[0]

nltk.corpus.BracketParseCorpusReader.simplify_tag = simplify_tag
nltk.corpus.BracketParseCorpusReader.simplify_tree = simplify_tree
nltk.tag.simplify.simplify_tag = simplify_tag
nltk.tag.simplify.wsj_mapping2 = wsj_mapping2
nltk.corpus.BracketParseCorpusReader.parsed_sents2 = parsed_sents2
treebank = LazyCorpusLoader('treebank/combined', BracketParseCorpusReader, r'wsj_.*\.mrg', tag_mapping_function=simplify_my_tag)

