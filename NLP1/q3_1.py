import  nltk
from itertools import izip
from nltk.corpus import brown
from nltk.probability import FreqDist

# return the accuracy for Unknown words and for known words-
# words that tag with UNKNOWN are unknown words
# we take all unkown words and assums they will be taged as "NN" , and calculate the 
# number of correct "NN" from the all unkown words
# same for known words   
def evaluate2(self,gold):
    tagged_sents = self.batch_tag([[w for (w, t) in sent] for sent in gold])
    gold_tokens = sum(gold, [])
    test_tokens = sum(tagged_sents, [])
    num_unknown_correct = 0
    num_unknown = 0
    num_known_correct = 0
    num_known = 0
    for x, y in izip(gold_tokens, test_tokens):
        if y[1] == 'UNKNOWN':
            num_unknown +=1
            if x[1] == "NN":
                num_unknown_correct += 1
        else:
            num_known +=1
            if x[1] == y[1]:
                num_known_correct += 1
    if num_unknown == 0 | num_known == 0: return (1,1)
    return (float(num_unknown_correct) / num_unknown , float(num_known_correct) / num_known )


def main():
    nltk.TaggerI.evaluate2 = evaluate2
    
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[100:]
    brown_test = brown_news_tagged[:100]
    
    regexp_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
                                       (r'(The|the|A|a|An|an)$', 'AT'),   # articles
                                       (r'.*able$', 'JJ'),                # adjectives
                                       (r'.*ness$', 'NN'),                # nouns formed from adjectives
                                       (r'.*ly$', 'RB'),                  # adverbs
                                       (r'.*s$', 'NNS'),                  # plural nouns
                                       (r'.*ing$', 'VBG'),                # gerunds
                                       (r'.*ed$', 'VBD'),                 # past tense verbs
                                       (r'.*', 'UNKNOWN')                 # unkonwn (default)
                                       ],backoff=None)
    at2 = nltk.AffixTagger(brown_train, backoff=regexp_tagger)
    ut3 = nltk.UnigramTagger(brown_train, backoff=at2)
    ct2 = nltk.NgramTagger(2, brown_train, backoff=ut3)

    e = regexp_tagger.evaluate2(brown_test)
    print "evaluate2 regExp(default unknown) = accoracy unkown words: %f ,accuracy known words: " %e[0],e[1]
    e = at2.evaluate2(brown_test)
    print "evaluate2 affix(regExp(default unknown)) = accoracy unkown words: %f ,accuracy known words: " %e[0],e[1]
    e= ut3.evaluate2(brown_test)
    print "evaluate2 unigram(affix(regExp(default unknown))) = accoracy unkown words: %f ,accuracy known words: " %e[0],e[1]
    e= ct2.evaluate2(brown_test)
    print "evaluate2 bigram(unigram(affix(regExp(default unknown)))) = accoracy unkown words: %f ,accuracy known words: " %e[0],e[1]
 
if __name__ == '__main__':
    main() 