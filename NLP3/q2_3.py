from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from q2_1 import q2_1, bag_of_words
from itertools import izip
from nltk.evaluate import accuracy
import pylab

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
    while len(words)  < K:
        try:
            word = fd.next()    
            words.append(word)
        except StopIteration:
            break  
    #words contains k most frequent words
    def extractor(document): 
        ans = []     
        for word in document:
            if word in words:
                ans.append(word)
        #removing stop words and return the filtered features  
        return stopword_remover(ans)
    return extractor


#define 5 steps for K or less, xE(1..5), if K*x > no. of features in the train or x>=5
#                                           return no. of features in the train. 
def kVal(q21,x,K):
    if x*K > q21.W:
        return q21.W
    if x >=5:
        return q21.W
    return K*x

#crating graph of accuracy vs. K/W
def plotGraph(q21, K):
    x = []
    y = []
    for i in range(1,6):
        newK = kVal(q21, i, K)
        extractor = make_topK_non_stopword_extractor(newK, stopset)
        print "top K without stops words, K = ", newK, ":"
        classifier = q21.evaluate_features(extractor, 10)
        x.append(float(newK)/float(q21.W))
        acc = accuracy(q21.maintest, q21.testClassify)
        y.append(acc)
    pylab.bar(x, y, width=0.02, facecolor='blue', align='center')
    pylab.xlabel('K/W')
    pylab.ylabel("Accuracy")
    pylab.title("Accuracy for each K/W value")
    pylab.grid(False)
    pylab.show()
    return

# counting the no. of pos tags to documents that the classifier changed his decision after changing the feature extractor method     
def newTaggs(oldClassiffy, newClassify):
    noPos = 0
    noNeg = 0
    for x,y in izip(oldClassiffy,newClassify):
        if x[0] == y[0] and x[1] != y[1]:
            if y[1] == 'neg':
                noNeg = noNeg + 1
            else:
                noPos = noPos + 1 
    return noPos, noNeg

def main():
    q21 = q2_1()
    print "bag of words extractor:"
    firstClassifier = q21.evaluate_features(bag_of_words, 10)
    oldClassify = q21.testClassify
    print "top k frequent words without stop words extractor:"
    extractor = make_topK_non_stopword_extractor(10000, stopset)
    secondClassifier = q21.evaluate_features(extractor, 10)
    newClassify = q21.testClassify
    #identifying documents that classified differently and report new positive, new negative
    noPos, noNeg = newTaggs(oldClassify, newClassify)
    print "No of documents that the classifier classify them as pos in bag of words extractor and neg in top k extractor is:", noNeg
    print "No of documents that the classifier classify them as neg in bag of words extractor and pos in top k extractor is:", noPos
    #drawing plot of accuract vs. K/W
    plotGraph(q21, 5000)
    return

if __name__ == '__main__':
    main() 