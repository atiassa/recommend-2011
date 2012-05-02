import  nltk
from nltk.corpus import brown
import numpy as np
import re, yaml 
from nltk.probability import FreqDist, ConditionalFreqDist 
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.tag.sequential import  SequentialBackoffTagger
from nltk.featstruct import FeatDict
    
class SimpleUnigramTagger (nltk.TaggerI): 
    
    def __init__(self, train,backoff=None):
        self._dictionary = []
        for w in train:
            self._dictionary.extend(w)
        self._cfd = nltk.ConditionalFreqDist(self._dictionary) 
        if backoff is None: 
            self._taggers = [self] 
        else: 
            self._taggers = [self] + backoff._taggers 
 
    def _get_backoff(self): 
        if len(self._taggers) < 2: return None 
        else: return self._taggers[1] 
 
    backoff = property(_get_backoff, doc='''The backoff tagger for this tagger.''') 
 
    def tag(self, tokens): 
    # docs inherited from TaggerI 
        tags = [] 
        for i in range(len(tokens)): 
            tags.append(self.tag_one(tokens, i, tags)) 
        return zip(tokens, tags) 
 
    def tag_one(self, tokens, index, history): 
        tag = None 
        for tagger in self._taggers: 
            tag = tagger.choose_tag(tokens, index, history) 
            if tag is not None:  break 
            else: 
                if self._get_backoff() is not None: 
                    return self._get_backoff().tag_one(tokens, index, history)
        return tag 
 
    def choose_tag(self, tokens, index, history):
        w = tokens[index]
        cf =  self._cfd[w]
        return cf.max()

def optimize_parameter():
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[:int(0.8*len(brown_news_tagged))]
    rest = brown_news_tagged[int(0.8*len(brown_news_tagged)):]
    brown_development = rest[:int(0.5*len(rest))]
    brown_test = rest[int(0.5*len(rest)):]
    opt_cut_of = 0
    best_accu = 0
    
    for cut_off in range(0,19):
        affix_tagger = nltk.AffixTagger(brown_train ,backoff=None , cutoff=cut_off)
        accu = 100.0 * affix_tagger.evaluate(brown_development)
        print accu
        if  accu > best_accu :
            best_accu = accu
            opt_cut_of = cut_off
    print opt_cut_of
    return opt_cut_of

def _H(self, tl, tag_probs):
    ans = 0
    for t in tl:
        i =  [x[0] for x in tag_probs].index(t)
        p = tag_probs[i][1]
        ans += p*np.log2(p) 
    return -ans

def _train(self, tagged_corpus, cutoff=0, verbose=False): 
    token_count = hit_count = 0 
    useful_contexts = set() 
    fd = ConditionalFreqDist() 
    tag_prob = FreqDist()
    for sentence in tagged_corpus: 
        tokens, tags = zip(*sentence) 
        for index, (token, tag) in enumerate(sentence): 
            # Record the event. 
            token_count += 1 
            tag_prob.inc(tag)
            context = self.context(tokens, index, tags[:index])
            if context is None: continue 
            fd[context].inc(tag) 
            # If the backoff got it wrong, this context is useful: 
            if (self.backoff is None or 
                tag != self.backoff.tag_one(tokens, index, tags[:index])): 
                useful_contexts.add(context) 
    # Build the context_to_tag table -- for each context,  
    # calculate the entropy.  Only include contexts that 
    # lower then `cutoff` .
    total_tags = float(sum(tag_prob.values()))
    tags_probs = [(t,tag_prob[t]/total_tags) for t in tag_prob.keys()]
    useful_contexts_after_filter = useful_contexts.copy()
    for context in useful_contexts:
        dd = fd[context]
#        total_tags = float(sum(dd.values()))
#        tags_probs = [(t,dd[t]/total_tags) for t in dd.keys()]
        h = self.H(dd.keys(),tags_probs)
        if h > cutoff:
            useful_contexts_after_filter.remove(context)
    
    # Build the context_to_tag table -- for each context, figure
    # out what the most likely tag is.  
    for context in useful_contexts_after_filter:
        best_tag = fd[context].max()
        hits = fd[context][best_tag]
        self._context_to_tag[context] = best_tag
        hit_count += hits
    # Display some stats, if requested. 
    if verbose: 
        size = len(self._context_to_tag) 
        backoff = 100 - (hit_count * 100.0)/ token_count 
        pruning = 100 - (size * 100.0) / len(fd.conditions()) 
        print "[Trained Unigram tagger:", 
        print "size=%d, backoff=%.2f%%, pruning=%.2f%%]" % (size, backoff, pruning)
        

def main():
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[:int(0.8*len(brown_news_tagged))]
    rest = brown_news_tagged[int(0.8*len(brown_news_tagged)):]
    brown_development = rest[:int(0.5*len(rest))]
    brown_test = rest[int(0.5*len(rest)):]
    
    affix_tagger = nltk.AffixTagger(brown_train, backoff= nltk.DefaultTagger('NN') , cutoff=2)
    nltk.AffixTagger._train = _train
    nltk.AffixTagger.H = _H
    affix_tagger2 = nltk.AffixTagger(brown_train, backoff= nltk.DefaultTagger('NN') , cutoff=2)
#    optimize_parameter()
#    nn_tagger = nltk.DefaultTagger('NN')
#    ut2 = nltk.UnigramTagger(brown_train, backoff=nn_tagger)
##    simpleUnigramTagger = SimpleUnigramTagger(brown_train)
##    print simpleUnigramTagger.tag(nltk.tag.untag(brown_test[0]))
    print 'Unigram tagger accuracy: %4.1f%%' % ( 100.0 * affix_tagger.evaluate(brown_test))
    print 'Unigram tagger with backoff accuracy: %4.1f%%' % ( 100.0 * affix_tagger2.evaluate(brown_test))
        
if __name__ == '__main__':
    main() 