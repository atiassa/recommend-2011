from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from q2_1 import q2_1, bag_of_words

stopset = set(stopwords.words('english'))

def stopword_remover(words): 
    return dict([(word, True) for word in words if word not in stopset])

def make_topK_non_stopword_extractor(K, stopwords):
    #count for each word in the Data set how many times the word apears
    words = movie_reviews.words()
    fd = FreqDist(word.lower() for word in words)
    words = []
    #taking k most frequent words
    fd = fd.__iter__()
    while len(words) < K:
        try:
            word = fd.next()
            words.append(word)
        except StopIteration:
            break  
    #words contains k most frequent words
    #removing stop words and return the filtered features  
    return stopword_remover(words)

def new_extractor(words):
    return stopword_remover
def main():
    q21 = q2_1()
#    print "bag of words extractor:"
#    firstClassifier = q21.evaluate_features(bag_of_words, 10)
#    print "top k frequent words without stop words extractor:"
    extractor = make_topK_non_stopword_extractor(10000, stopset)
    secondClassifier = q21.evaluate_features(extractor, 10)
    
    return
if __name__ == '__main__':
    main() 