import  nltk
from nltk.corpus import brown
import pylab

def performance(cfd, wordlist):
    lt = dict((word, cfd[word].max()) for word in wordlist)
    baseline_tagger = nltk.UnigramTagger(model=lt, backoff=nltk.DefaultTagger('NN'))
    return baseline_tagger.evaluate(brown.tagged_sents(categories='news'))

def display():
    words_by_freq = list(nltk.FreqDist(brown.words(categories='news')))
    cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
    sizes = 2 ** pylab.arange(15)
    perfs = [performance(cfd, words_by_freq[:size]) for size in sizes]
    pylab.plot(sizes, perfs, '-bo')
    pylab.title('Lookup Tagger Performance with Varying Model Size')
    pylab.xlabel('Model Size')
    pylab.ylabel('Performance')
    pylab.show()
    
#Write a function that plots the number of words having a given number of tags. 
#The X-axis should show the number of tags and 
#the Y-axis the number of words having exactly this number of tags.
#corpus can be the tagged_words according to what is most convenient
def PlotNumberOfTags(corpus):
    fd1 = nltk.FreqDist(corpus)
    difCouples = fd1.keys()
    words = [w for (w,t) in difCouples]
    fd2 = nltk.FreqDist(words)
    cfd = nltk.ConditionalFreqDist((fd2[word], word) for word in fd2.keys())
    
    tags_n = pylab.arange(15)
    perfs = [cfd[n].__len__() for n in tags_n]
    pylab.plot(tags_n, perfs, '-bo')
    pylab.title('The number of words having a given number of tags')
    pylab.xlabel('Number of tags')
    pylab.ylabel('Number of words')
    pylab.show()

#def countWordsWithDiffTags():
#    tagWords = brown.tagged_words(categories='news')
#    fd1 = nltk.FreqDist(tagWords)
#    difCouples = fd1.keys()
#    words = [w for (w,t) in difCouples]
#    fd2 = nltk.FreqDist(words)
#    cfd = nltk.ConditionalFreqDist((fd2[word], word) for word in fd2.keys())
#    return cfd
         
#def countWordsWithNTags(n):
#    tagWords = brown.tagged_words(categories='news')
#    fd1 = nltk.FreqDist(tagWords)
#    difCouples = fd1.keys()
#    words = [w for (w,t) in difCouples]
#    fd2 = nltk.FreqDist(words)
#    cfd = nltk.ConditionalFreqDist((fd2[word], word) for word in fd2.keys())
#    return cfd[n].__len__()  

# function that finds words with more than N observed tags
def MostAmbiguousWords(corpus, n):
    difCouples = nltk.FreqDist(corpus).keys()
    fd2 = nltk.FreqDist([w for (w,t) in difCouples])
    cfd = nltk.ConditionalFreqDist()
    for word in fd2.keys():
        if  fd2[word] >= n : 
            cond = fd2[word] 
            cfd[cond].inc(word) 
    return cfd      

#test function that verifies that the words indeed have more than N distinct tags in the returned value.
def TestMostAmbiguousWords(cfd, N):
    for fd in cfd:
        print 1
#finds one example of usage of the word with each of the different tags in which it can occur.
def ShowExamples(word, cfd, corpus):
    difCouples = nltk.FreqDist(corpus).keys()
    for (w,t) in difCouples:
        if w == word :
            print "\'%s\'" % w +"as %s:" % t       
           
def main():
    tagWords = brown.tagged_words(categories='news')
    PlotNumberOfTags(tagWords)
    cfd = MostAmbiguousWords(tagWords, 4)
    TestMostAmbiguousWords(cfd, 4)
    ShowExamples('book', cfd, tagWords)
    
if __name__ == '__main__':
    main() 