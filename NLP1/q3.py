import  nltk
from nltk.corpus import brown
import itertools as iter
    
class TaggerI(object): 
    def tag(self, tokens): 
        raise NotImplementedError() 
    
    def batch_tag(self, sentences): 
        return [self.tag(sent) for sent in sentences] 

    def evaluate(self, gold): 
        tagged_sents = self.batch_tag([nltk.untag(sent) for sent in gold]) 
        gold_tokens = sum(gold, []) 
        test_tokens = sum(tagged_sents, []) 
        return accuracy(gold_tokens, test_tokens)  

    def evaluate2(self, training_corpus):
        tagged_sents = self.batch_tag([nltk.untag(sent) for sent in training_corpus]) 
        gold_tokens = sum(training_corpus, []) 
        test_tokens = sum(tagged_sents, []) 
        return accuracy(gold_tokens, test_tokens)

def accuracy(reference, test): 
    if len(reference) != len(test): 
        raise ValueError("Lists must have the same length.") 
    num_correct = 0 
    for x, y in iter.izip(reference, test): 
        if x == y: 
            num_correct += 1 
    return float(num_correct) / len(reference)

def main():
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[100:]
    brown_test = brown_news_tagged[:100]
        
    nn_tagger = nltk.DefaultTagger('NN')
    print nn_tagger.evaluate(brown_test)
    regexp_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
                                       (r'(The|the|A|a|An|an)$', 'AT'),   # articles
                                       (r'.*able$', 'JJ'),                # adjectives
                                       (r'.*ness$', 'NN'),                # nouns formed from adjectives
                                       (r'.*ly$', 'RB'),                  # adverbs
                                       (r'.*s$', 'NNS'),                  # plural nouns
                                       (r'.*ing$', 'VBG'),                # gerunds
                                       (r'.*ed$', 'VBD'),                 # past tense verbs
                                       (r'.*', 'NN')                      # nouns (default)
                                       ],backoff=nn_tagger)
    print regexp_tagger.evaluate(brown_test)
    at2 = nltk.AffixTagger(brown_train, backoff=regexp_tagger)
    print at2.evaluate(brown_test)
    ut3 = nltk.UnigramTagger(brown_train, backoff=at2)
    print ut3.evaluate(brown_test)
    ct2 = nltk.NgramTagger(2, brown_train, backoff=ut3)     
    print ct2.evaluate(brown_test) 
        
if __name__ == '__main__':
    main() 