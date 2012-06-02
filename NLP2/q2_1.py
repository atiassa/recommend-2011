import  nltk
import nltk.evaluate 
from nltk.corpus import movie_reviews
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import random
from itertools import izip
from nltk.probability import FreqDist

from nltk.classify import NaiveBayesClassifier as classifier
from nltk.evaluate import accuracy, precision, recall, f_measure
#from nltk.classify.util import accuracy
#from nltk.metrics import precision, recall


class q2_1(object):
        
    #split to train and test one list of documents names
    def randomChoosDocs(self,documents, numDocs, label):
        train = []
        test = []
        tmpNum = 0
        while tmpNum < numDocs:
            r = int(random.uniform(1,len(documents)-1))
            train.append((documents.pop(r),label))
            tmpNum = tmpNum + 1
        for doc in documents:
            x = (doc,label)
            test.append(x)
        return train,test
    
    #performing the stratified split (training, test) dataset of (positive, negative) documents
    def stratifiedSplit(self,negative, positive, N):
        testSet = []
        trainSet = []
        percTrain = float(N-1)/float(N) # percent of how many documents should be in train set from each docs list
        noTrainNeg = math.ceil(percTrain*len(negative))# round up
        noTrainPos = math.ceil(percTrain*len(positive))# round up
        #insert train and test random docs from negative list
        tmptrain, tmptest = self.randomChoosDocs(negative, noTrainNeg,'neg')
        trainSet = trainSet + tmptrain
        testSet = testSet + tmptest
        #insert train and test random docs from positive list
        tmptrain, tmptest = self.randomChoosDocs(positive, noTrainPos,'pos')
        trainSet = trainSet + tmptrain
        testSet = testSet + tmptest
        return trainSet, testSet
    
    #return the test docs with the lables the classifier gives after training
    def classifyTest(self,test, classifier, feature_extractor):
        testClassifies = []
        for doc,lbl in test:
            tmpLbl = classifier.classify(feature_extractor(movie_reviews.words(fileids=[doc])))
            x = (doc,tmpLbl)
            testClassifies.append(x)
        return testClassifies
    
    #calc TP (label both in the test and by the classifier)
    def calcTP(self,label, testSet, classifierTest):
        tp = 0
        for x, y in izip(testSet, classifierTest):
            doc,lbl = x
            if x == y and lbl == label :
                tp += 1
        return tp
    
    #calc TN (non-label both in the test and by the classifier)    
    def calcTN(self,label, testSet, classifierTest):
        tn = 0
        for x, y in izip(testSet, classifierTest):
            testDoc,testLbl = x
            classifierDoc,classifierLbl = y
            if testDoc == classifierDoc and testLbl != label and classifierLbl != label :
                tn += 1
        return tn
        
    #calc FP (non-label by the test and label by the classifier)
    def calcFP(self,label, testSet, classifierTest):
        fp = 0
        for x, y in izip(testSet, classifierTest):
            testDoc,testLbl= x
            classifierDoc,classifierLbl = y
            if testDoc == classifierDoc and testLbl != label and classifierLbl == label :
                fp += 1
        return fp
    
    #calc FN (label by the test and non label by the classifier)
    def calcFN(self,label, TestSet, classifierTest):
        fn = 0
        for x, y in izip(TestSet, classifierTest):
            testDoc,testLbl = x
            classifierDoc,classifierLbl = y
            if testDoc == classifierDoc and testLbl == label and classifierLbl != label :
                fn += 1
        return fn
        
    #calc Precision(T) = TP / TP + FP
    def calcPrec(self,label, testSet, classifierTest):
        tp = self.calcTP(label, testSet, classifierTest)
        fp = self.calcFP(label, testSet, classifierTest)
        if tp+fp == 0:
            prec = 0
        else:
            prec = float(float(tp)/(tp+fp))
        return prec
    
    #calc Recall(T) = TP / TP + FN    
    def calcRecall(self,label, testSet, classifierTest):
        tp = self.calcTP(label, testSet, classifierTest)
        fn = self.calcFN(label, testSet, classifierTest)
        if tp + fn == 0:
            recall = 0
        else:
            recall = float(float(tp)/(tp+fn))
        return recall
        
    #calc F-Measure(T) = 2 x Precision x Recall / (Recall + Precision)  
    def calcFMeasur(self,label, testSet, classifierTest):
        prec = self.calcPrec(label, testSet, classifierTest)
        recall = self.calcRecall(label, testSet, classifierTest)
        if recall + prec == 0:
            fMeasure = 0
        else:
            fMeasure = float((2 * prec * recall)/(recall + prec))
        return fMeasure
            
    def evaluate_features(self,feature_extractor, N):
        self.negative = movie_reviews.fileids('neg') #list of all names of the documents under neg folder
        self.positive = movie_reviews.fileids('pos') #list of all names of the documents under pos folder
        self.maintrain, self.maintest = self.stratifiedSplit(self.negative, self.positive, N)
        lst = []
        for doc,lbl in self.maintrain:
            x = (feature_extractor(movie_reviews.words(fileids=[doc])),lbl)
            lst.append(x)
        nb = classifier.train(lst)
        self.testClassify = self.classifyTest(self.maintest, nb, feature_extractor)
        print "accuracy = ", accuracy(self.maintest, self.testClassify)
        print "Negative:"
        print "    precision = ", self.calcPrec('neg', self.maintest, self.testClassify)
        print "    recall = ", self.calcRecall('neg', self.maintest, self.testClassify)
        print "    f measure = ", self.calcFMeasur('neg', self.maintest, self.testClassify)
        print "Positive:"
        print "    precision = ", self.calcPrec('pos', self.maintest, self.testClassify)
        print "    recall = ", self.calcRecall('pos', self.maintest, self.testClassify)
        print "    f measure = ", self.calcFMeasur('pos', self.maintest, self.testClassify)
        nb.show_most_informative_features()
        return nb
    
    #return a list of document's names that the classifier predicted wrong label
    def error_prediction_docs(self, testSet, testClassify):
        ans = []
        for real,predict in izip(testSet, testClassify):
            if real != predict:
                realDoc, realLbl = real
                predDoc, predLbl = predict
                if predDoc == realDoc and realLbl != predLbl:
                    ans.append(realDoc)
        return ans
          
    #return k worst errors made by the classifier by returning the features that involved in many wrong decisions 
    #using the mainTest and testClassify parameters
    def worst_errors_many_wrong_decisions(self, k, feature_extractor):
        worst_errors = []
        features = []
        wrongDocs = self.error_prediction_docs(self.maintest, self.testClassify)
        for doc in wrongDocs:
            feature_dic = feature_extractor(movie_reviews.words(fileids=[doc]))
            features = features + feature_dic.keys()
        fd = FreqDist(feature.lower() for feature in features)
        for i in range(1, k+1):
            x = fd.max()
            fd.pop(x)
            worst_errors.append(x)
        return worst_errors
    
# return a dictionary with all different words that apear in the document with the value True for each word  
def bag_of_words(document):
    return dict([(word, True) for word in document])
        
def main():
    s = q2_1()
    nbClassifier = s.evaluate_features(bag_of_words,2.0)
    #k features that involved in many wrong decisions
    errors = s.worst_errors_many_wrong_decisions(10, bag_of_words)
    print "10 features that involved in many wrong decisions: ", errors
    
if __name__ == '__main__':
    main() 