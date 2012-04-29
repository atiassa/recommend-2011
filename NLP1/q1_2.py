import  nltk
from nltk.corpus import brown

def performance(cfd, wordlist):
    lt = dict((word, cfd[word].max()) for word in wordlist)
    baseline_tagger = nltk.UnigramTagger(model=lt, backoff=nltk.DefaultTagger('NN'))
    return baseline_tagger.evaluate(brown.tagged_sents(categories='news'))

def display():
    import pylab
    words_by_freq = list(nltk.FreqDist(brown.words(categories='news')))
    cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
    sizes = 2 ** pylab.arange(15)
    perfs = [performance(cfd, words_by_freq[:size]) for size in sizes]
    pylab.plot(sizes, perfs, '-bo')
    pylab.title('Lookup Tagger Performance with Varying Model Size')
    pylab.xlabel('Model Size')
    pylab.ylabel('Performance')
    pylab.show()

def displayPlot1():
    import pylab
    sizes = 2 ** pylab.arange(15)
    perfs = []
    pylab.plot(sizes, perfs, '-bo')
    pylab.title('Lookup Tagger Performance with Varying Model Size')
    pylab.xlabel('Model Size')
    pylab.ylabel('Performance')
    pylab.show()

#Write a function that plots the number of words having a given number of tags. 
#The X-axis should show the number of tags and 
#the Y-axis the number of words having exactly this number of tags.  
def countWordsWithDiffTags():
    tagWords = brown.tagged_words(categories='news')
    fd1 = nltk.FreqDist(tagWords)
    difCouples = fd1.keys()
    words = [w for (w,t) in difCouples]
    fd2 = nltk.FreqDist(words)
    cfd = nltk.ConditionalFreqDist((fd2[word], word) for word in fd2.keys())
    return cfd
    
    
def countWordsWithNTags(n):
    cfd = countWordsWithDiffTags()
    return cfd[n]  
    
    
    
def main():
#    display()
#    displayPlot1(2);
    x = countWordsWithNTags(6);
    print x
if __name__ == '__main__':
    main() 