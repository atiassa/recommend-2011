import  nltk
from nltk.evaluate import accuracy
from nltk.corpus import brown
from q2_1 import q2_1
import pylab

#getting tagger trained by the brown corpus
def getTrainedTagger():
    train = brown.tagged_sents(simplify_tags=True)
    newTrain = []
    for sen in train:
        newSen = []
        for word,tag in sen:
            newSen.append((word.lower(),tag))
        newTrain.append(newSen)
    nn_tagger = nltk.DefaultTagger('NN')
    regexp_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
                                       (r'(The|the|A|a|An|an)$', 'AT'),   # articles
                                       (r'.*able$', 'JJ'),                # adjectives
                                       (r'.*ness$', 'NN'),                # nouns formed from adjectives
                                       (r'.*ly$', 'RB'),                  # adverbs
                                       (r'.*s$', 'NNS'),                  # plural nouns
                                       (r'.*ing$', 'VBG'),                # gerunds
                                       (r'.*ed$', 'VBD'),                 # past tense verbs
                                       (r'.*', 'NN')                      # nouns (default)
                                       ],backoff=nn_tagger)
    at2 = nltk.AffixTagger(newTrain, backoff=regexp_tagger)
    ut3 = nltk.UnigramTagger(newTrain, backoff=at2)
    ct2 = nltk.NgramTagger(2, newTrain, backoff=ut3)
    return ct2

def make_pos_extractor(pos):
    tagger = getTrainedTagger()
    def extractor(words):
        taggedWords = tagger.tag(words)
        return dict([(word, True) for word,tag in taggedWords if tag in pos])
    return extractor
#['ADJ', 'ADV', 'CNJ', 'DET', 'EX', 'FW', 'MOD', 'N', 'NP', 'NUM', 'PRO', 'P', 'TO', 'UH', 
#'V', 'VD', 'VG', 'VN', 'WH']
def main():
    q21 = q2_1()
    x = []
    y = []
    pos = ['N', 'VG', 'ADJ', 'ADV']
    print pos
    extractor = make_pos_extractor(pos)
    classifier = q21.evaluate_features(extractor, 10)
    x.append(1)
    acc = accuracy(q21.maintest, q21.testClassify)
    y.append(acc)
    
    pos = ['N', 'V', 'VG', 'VN', 'VN', 'ADJ', 'ADV']
    print pos
    extractor = make_pos_extractor(pos)
    classifier = q21.evaluate_features(extractor, 10)
    x.append(2)
    acc = accuracy(q21.maintest, q21.testClassify)
    y.append(acc)
    
    pos = ['V', 'ADJ', 'ADV']
    print pos
    extractor = make_pos_extractor(pos)
    classifier = q21.evaluate_features(extractor, 10)
    x.append(3)
    acc = accuracy(q21.maintest, q21.testClassify)
    y.append(acc)
    
    pos = ['ADJ', 'ADV']
    print pos
    extractor = make_pos_extractor(pos)
    classifier = q21.evaluate_features(extractor, 10)
    x.append(4)
    acc = accuracy(q21.maintest, q21.testClassify)
    y.append(acc)
    
    pos = ['N', 'ADJ', 'ADV']
    print pos
    extractor = make_pos_extractor(pos)
    classifier = q21.evaluate_features(extractor, 10)
    x.append(5)
    acc = accuracy(q21.maintest, q21.testClassify)
    y.append(acc)
    
    pylab.bar(x, y, width=0.02, facecolor='blue', align='center')
    pylab.xlabel('POS')
    pylab.ylabel("Accuracy")
    pylab.title("Accuracy for each pos set")
    pylab.grid(False)
    pylab.show()
    return
    
if __name__ == '__main__':
    main() 