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
    
#Write a function that plots the number of words having a given number of tags. 
#The X-axis should show the number of tags and 
#the Y-axis the number of words having exactly this number of tags.
def displayPlot1():
    import pylab
    sizes = 2 ** pylab.arange(15)
    perfs = []
    pylab.plot(sizes, perfs, '-bo')
    pylab.title('Lookup Tagger Performance with Varying Model Size')
    pylab.xlabel('Model Size')
    pylab.ylabel('Performance')
    pylab.show()

#def countWordsWithDiffTags():
#    tagWords = brown.tagged_words(categories='news')
#    fd1 = nltk.FreqDist(tagWords)
#    difCouples = fd1.keys()
#    words = [w for (w,t) in difCouples]
#    fd2 = nltk.FreqDist(words)
#    cfd = nltk.ConditionalFreqDist((fd2[word], word) for word in fd2.keys())
#    return cfd
         
def countWordsWithNTags(n):
    tagWords = brown.tagged_words(categories='news')
    fd1 = nltk.FreqDist(tagWords)
    difCouples = fd1.keys()
    words = [w for (w,t) in difCouples]
    fd2 = nltk.FreqDist(words)
    cfd = nltk.ConditionalFreqDist((fd2[word], word) for word in fd2.keys())
    return cfd[n]  

# function that finds words with more than N observed tags
def countWordsWithMoreNTags(n):
    difCouples = nltk.FreqDist(brown.tagged_words(categories='news')).keys()
    fd2 = nltk.FreqDist([w for (w,t) in difCouples])
    cfd = nltk.ConditionalFreqDist()
    for word in fd2.keys():
        if  fd2[word] >= n : 
            cond = fd2[word] 
            cfd[cond].inc(word) 
    return cfd        
       
def main():
    display()
#    displayPlot1(2);
#    s = countWordsWithNTags(2);
#    x = countWordsWithNTags(3);
#    print x
    
if __name__ == '__main__':
    main() 