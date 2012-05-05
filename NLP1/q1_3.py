import  nltk
from nltk.corpus import brown
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# a function that will draw a 3D plot with axes for:
# Word length (in characters)
# Word frequency
# Word ambiguity
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
    ax.plot( word_frequency ,word_ambiguity ,word_length)
    ax.set_title('Correlation between word size or frequency and ambiguity level')
    ax.set_xlabel('Word frequency')
    ax.set_ylabel('Word ambiguity')
    ax.set_zlabel('Word length')
    plt.show()
           
def main():
    tagWords =  brown.tagged_words(categories='news')
    Plot3DCorrelation(tagWords)
    
if __name__ == '__main__':
    main() 