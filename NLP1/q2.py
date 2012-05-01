import  nltk
from nltk.corpus import brown
    
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
                if self._get_backoff() is not None: return self._get_backoff().tag_one(tokens, index, history)
        return tag 
 
    def choose_tag(self, tokens, index, history):
        w = tokens[index]
        cf =  self._cfd[w]
        return cf.max()
    
def main():
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[100:]
    brown_test = brown_news_tagged[:100]

# Train the unigram model
    nn_tagger = nltk.DefaultTagger('NN')
    ut2 = nltk.UnigramTagger(brown_train, backoff=nn_tagger)
    simpleUnigramTagger = SimpleUnigramTagger(brown_train)
    print simpleUnigramTagger.tag(nltk.tag.untag(brown_test[0]))
    print 'Unigram tagger accuracy: %4.1f%%' % ( 100.0 * simpleUnigramTagger.evaluate(brown_test))
    print 'Unigram tagger with backoff accuracy: %4.1f%%' % ( 100.0 * ut2.evaluate(brown_test))
        
if __name__ == '__main__':
    main() 