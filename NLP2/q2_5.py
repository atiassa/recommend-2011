from nltk.util import bigrams
from q2_1 import q2_1,bag_of_words
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

score = BigramAssocMeasures.chi_sq  # chi square measure of strength

def strong_bigrams(words, score_fn, n):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return [bigram for bigram in itertools.chain(words, bigrams)]

def make_bigram_extractor():
    def extractor(words):
        biWords = bigrams(words)
        return dict([(word1 + " " + word2,True) for word1,word2 in biWords])
    return extractor

def make_bigram_unigram_extractor():
    def extractor(words):
        biWords = [word1 + " " + word2 for word1,word2 in bigrams(words)]
        words = list(words) + list(biWords)
        return dict([(word,True) for word in words])
    return extractor

def make_good_bigram_unigram_extractor(n):
    def extractor(words):
        stBigrams = strong_bigrams(([word1 + " " + word2 for word1,word2 in bigrams(words)]), score , n)
        words = list(words) + list(stBigrams)
        return dict([(word,True) for word in words])
    return extractor

#when we run the same instance of evaluate_features few times, in the first time we define the train and test sets
#and in the other times we based on the same train and test set so we could be able to compare those methods    
def main():
    q21 = q2_1()
    
    print "bigram Extractor:"
    #evaluate bigram extractor
    extractor = make_bigram_extractor()
    classifier = q21.evaluate_features(extractor, 4)
    
    print "bag of words extractor:"
    #evaluate bag of words extractor
    extractor = bag_of_words
    classifier = q21.evaluate_features(extractor, 4)
    
    print "all bigram unigram extractor"
    #evaluate all bigrams and all unigrams extractor
    extractor = make_bigram_unigram_extractor()
    classifier = q21.evaluate_features(extractor, 4)
    
    print "good bigram unigram extractor:"
    #evaluate good bigrams and all unigrams extractor
    extractor = make_good_bigram_unigram_extractor(100)
    classifier = q21.evaluate_features(extractor, 4)
    
    return

if __name__ == '__main__':
    main() 