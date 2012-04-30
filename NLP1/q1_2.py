import  nltk
from nltk.corpus import brown
import pylab
import matplotlib.pyplot as plt
    
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
    pylab.plot(tags_n, perfs)
    pylab.title('The number of words having a given number of tags')
    pylab.xlabel('Number of tags')
    pylab.ylabel('Number of words')
    pylab.grid(True)
    pylab.show()

# function that finds words with more than N observed tags
def MostAmbiguousWords(corpus, n):
    difCouples = nltk.FreqDist(corpus).keys()
    word_by_num_of_tags = nltk.FreqDist([w for (w,t) in difCouples])
    cfd = nltk.ConditionalFreqDist()
    for (w,t) in difCouples:
        if  word_by_num_of_tags[w] >= n : 
            cfd[w].inc(t) 
    return cfd      

#test function that verifies that the words indeed have more than N distinct tags in the returned value.
def TestMostAmbiguousWords(cfd, N):
    word_with_more_then_n = cfd.conditions() 
    
    ccfd = nltk.ConditionalFreqDist()
    tagWords = [(w.lower(),t) for (w,t) in brown.tagged_words(categories='news')]
    for (x,y) in tagWords:
        if word_with_more_then_n.count(x)!= 0 :
            ccfd[x].inc(y)
    for w in ccfd.conditions():
        if len(ccfd[w])<N:
            print "Not all words occur with more than %d tags." %N
            return
    print "All words occur with more than %d tags." %N
        
#finds one example of usage of the word with each of the different tags in which it can occur.
def ShowExamples(word, cfd, corpus):
    tag_sents = brown.tagged_sents(categories='news')
    difCouples = nltk.FreqDist(corpus).keys()
    for (w,t) in difCouples:
        if w == word :
            for s in tag_sents:
                if [(a.lower(),b) for (a,b) in s].count((w,t))!= 0:
                    sent = ' '.join(b for (b,f) in s)
                    print "\'%s\'" % w +"as %s: " % t + sent 
                    break 

def Plot3DCorrelation(tagWords):
    word_length = []
    word_frequency = []
    word_ambiguity = []
    
    words_by_freq = nltk.FreqDist([w for (w,t) in tagWords])
    difCouples = nltk.FreqDist(tagWords).keys()
    word_by_ambiguity = nltk.FreqDist([w for (w,t) in difCouples])
    
    for w in words_by_freq.keys():
        word_frequency.append(words_by_freq[w])
        word_length.append(len(w)) 
        word_ambiguity.append(word_by_ambiguity[w]) 

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(word_length , word_frequency ,word_ambiguity )
    ax.set_title('Correlation between word size or frequency and ambiguity level')
    ax.set_xlabel('Word length')
    ax.set_ylabel('Word frequency')
    ax.set_zlabel('Word ambiguity')
    plt.show()
           
def main():
    tagWords = [(w.lower(),t) for (w,t) in brown.tagged_words(categories='news')]
#    PlotNumberOfTags(tagWords)
    Plot3DCorrelation(tagWords)
    cfd = MostAmbiguousWords(tagWords, 4)
#    TestMostAmbiguousWords(cfd, 4)
    ShowExamples('book', cfd, tagWords)
    
if __name__ == '__main__':
    main() 