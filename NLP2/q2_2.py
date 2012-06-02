from nltk.corpus import movie_reviews
from q2_1 import q2_1, bag_of_words
import pylab
from nltk.evaluate import accuracy as _accuracy
from itertools import izip

class q2_2(object):
    #constructing classifier for N=2 using task 1 and return the classifier and the train and test sets for this classifier
    def build_Classifier_Train_Test(self, feature_extractor):
        self.q21 = q2_1()
        classifier = self.q21.evaluate_features(feature_extractor, 2)
        train = self.q21.maintrain
        test = self.q21.maintest
        testClaassify = self.q21.testClassify
        return classifier,train,test, testClaassify
    
    #given a document name and list of words that apear in the train set 
    #return the percentage of unknown words in the given document
    def doc_unknown_words(self, docName, trainWords):
        docWords = movie_reviews.words(fileids=[docName])
        diffs = list(set(docWords) - set(trainWords))
        return float(len(diffs))/float(len(docWords))
    
    #return list of pairs (doc name, unknown words perc) for each document in test
    def test_unknown_words(self, test, train):
        ans = []
        trainWords = []
        for doc,lbl in train:    
            tmp = movie_reviews.words(fileids=[doc])
            trainWords = trainWords + list(tmp)
        for doc,lbl in test:
            perc = self.doc_unknown_words(doc, trainWords)
            p = (doc,perc)
            ans.append(p)
        return ans
    
    #divide test's documents to 5 groups according the rate of unknown words
    #0-0.2 one group, 0.2-0.4 second group,0.4-0.6 third group,0.6-0.8 forth group, 0.8-1 fifth group
    def divide_test(self,test,train):
        grp1 = []
        grp2 = []
        grp3 = []
        grp4 = []
        grp5 = []
        docsPerc = self.test_unknown_words(test, train)
        self.plot_percentage_of_unknownWords(docsPerc) 
        for doc,perc in docsPerc:
            if perc < 0.01:
                grp1.append(doc)
            else:
                if perc >= 0.01 and perc < 0.02:
                    grp2.append(doc)
                else:
                    if perc >= 0.02 and perc < 0.03:
                        grp3.append(doc)
                    else:
                        if perc >= 0.03 and perc < 0.04:
                            grp4.append(doc)
                        else:
                            grp5.append(doc)
        return [grp1,grp2,grp3,grp4,grp5]
    
    #plot size of each group
    def plotSizes(self,groups):
        x = [1,2,3,4,5]
        y = [len(n) for n in groups]
        pylab.title('Size for each Group')
        pylab.xlabel('Groups')
        pylab.ylabel('Size')
        pylab.bar(x, y, width=0.1, facecolor='blue', align='center')
        pylab.grid(False)
        pylab.show()
        return
    
    #used for identify the 5 groups of documents
    def plot_percentage_of_unknownWords(self,docsPerc):
        grps = pylab.arange(1000)
        lens = [b for a,b in docsPerc]
        pylab.plot(grps, lens)
        pylab.title('Percentage of Unknown Words')
        pylab.xlabel('Docs')
        pylab.ylabel('Percentage')
        pylab.grid(False)
        pylab.show()
        return
    
    #count no. of positive and negative docs in group
    def count_pos_neg(self,group):
        pos = 0
        for doc in group:
            if "pos/" in doc:
                pos = pos + 1
        pos = float(pos)/float(len(group))
        neg = 1.0 - pos
        return pos,neg
    
    def plot_positive_negative_relative_no(self, groups):
        x = [1,2,3,4,5]
        y_pos = []
        y_neg = []
        for g in groups:
            pos,neg = self.count_pos_neg(g)
            y_pos.append(pos)
            y_neg.append(neg)
        #positive
        pylab.title('Percentage of Positive Documents')
        pylab.xlabel('Groups')
        pylab.ylabel('Percentage - Positive')
        pylab.bar(x, y_pos, width=0.1, facecolor='blue', align='center')
        pylab.grid(False)
        pylab.show()
        #negative
        pylab.title('Percentage of Negative Documents')
        pylab.xlabel('Groups')
        pylab.ylabel('Percentage - Negative')
        pylab.bar(x, y_neg, width=0.1, facecolor='blue', align='center')
        pylab.grid(False)
        pylab.show()
        return

    # gets list of lists of file's names belonging to 5 groups, the test set and the test classify by the classifier
    # and calculate accuracy, precision, recall and f-measure for each group
    def calculateAccuracyPrecRecall(self, groups, test, testClassify):
        accuracy = []
        precPos = []
        precNeg = []
        recallPos = []
        recallNeg = []
        groupTest = []
        groupTestClassify = []
        for group in groups:
            for doc in group:
                for element1, element2 in izip(test, testClassify):
                    tdoc,tlbl = element1
                    if tdoc == doc:
                        groupTest.append(element1)
                        groupTestClassify.append(element2)
            p = self.q21.calcPrec('pos',groupTest,groupTestClassify)
            precPos.append(p)
            p = self.q21.calcPrec('neg',groupTest,groupTestClassify)
            precNeg.append(p)
            r = self.q21.calcRecall('pos', groupTest, groupTestClassify)
            recallPos.append(r)
            r = self.q21.calcRecall('neg', groupTest,groupTestClassify)
            recallNeg.append(r)
            a = _accuracy(groupTest, groupTestClassify)
            accuracy.append(a)
            groupTest = []
            groupTestClassify = []
        return precPos, precNeg, recallPos, recallNeg, accuracy
    
    #ploting the calculation graphs for each group
    def plot_calculations(self,y, ylbl, strTitle):
        x = [1,2,3,4,5]
        pylab.bar(x, y, width=0.1, facecolor='blue', align='center')
        pylab.xlabel('Groups')
        pylab.ylabel(ylbl)
        pylab.title(strTitle)
        pylab.grid(False)
        pylab.show()
        return
    
def main():
    q22 = q2_2()
    c,train,test,testClassify = q22.build_Classifier_Train_Test(bag_of_words)
    groups = q22.divide_test(test, train)
    q22.plotSizes(groups)
    q22.plot_positive_negative_relative_no(groups)
    precPos, precNeg, recallPos, recallNeg , accuracy = q22.calculateAccuracyPrecRecall(groups, test, testClassify)
    q22.plot_calculations(precPos, 'Precision', 'Positive Precision for each Group')
    q22.plot_calculations(precNeg, 'Precision', 'Negative Precision for each Group')
    q22.plot_calculations(recallPos, 'Recall', 'Positive Recall for each Group')
    q22.plot_calculations(recallNeg, 'Recall', 'Negative Recall for each Group')
    q22.plot_calculations(accuracy, 'accuracy', 'Accuracy for each Group')
    
    
if __name__ == '__main__':
    main() 