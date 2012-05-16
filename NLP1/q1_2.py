import  nltk
from nltk.corpus import brown
import pylab
    
#function that plots the number of words having a given number of tags. 
#The X-axis should show the number of tags and 
#the Y-axis the number of words having exactly this number of tags.
#corpus - tagged_words
def PlotNumberOfTags(corpus):
    fd1 = nltk.FreqDist(corpus)
    difCouples = fd1.keys()
    words = [w for (w,t) in difCouples]
    fd2 = nltk.FreqDist(words)
    cfd = nltk.ConditionalFreqDist((fd2[word], word) for word in fd2.keys())
    
    tags_n = pylab.arange(1,19)
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
    tagWords = brown.tagged_words(categories='news')
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
    for w in cfd.conditions():
        if w == word :
            for t in cfd[w]:
                for s in tag_sents:
                    if s.count((w,t))!= 0:
                        sent = ' '.join(b for (b,f) in s)
                        print "\'%s\'" % w +"as %s: " % t + sent 
                        break 
           
def main():
    tagWords =  brown.tagged_words(categories='news')
    PlotNumberOfTags(tagWords)
    cfd = MostAmbiguousWords(tagWords, 3)
    TestMostAmbiguousWords(cfd, 3)
    ShowExamples('the', cfd, tagWords)
    
if __name__ == '__main__':
    main() 