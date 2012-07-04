from nltk.corpus import conll2002
#from svm import *

Classes = ['B-PER', 'I-PER', 'B-LOC', 'I-LOC', 'B-ORG', 'I-ORG', 'O']

f1={} # f1 The word form (the string as it appears in the sentence)
f2={} # f2 The POS of the word
f3={} # f3 ORT - a feature that captures the orthographic (letter) structure of the word. It can have any of the following values: number, contains-digit, contains-hyphen, capitalized, all-capitals, URL, punctuation, regular.
f4={} # f4 prefix1: first letter of the word
f5={} # f5 prefix2: first two letters of the word
f6={} # f6 prefix3: first three letters of the word
f7={} # f7 suffix1: last letter of the word
f8={} # f8 suffix2: last two letters of the word
f9={} # f9 suffix3: last three letters of the word


def print_encoding():
    print "Classes"
    for i,x in enumerate(Classes): print str(i+1)+" "+x
    print "Feature WORD-FORM:" 
    for i,x in enumerate(sorted(f1, key=f1.get, reverse=False)): print str(i+1)+" "+x.encode('utf-8')
    print "Feature POS" 
    for i,x in enumerate(sorted(f2, key=f2.get, reverse=False)): print str(i+1+len(f1))+" "+x.encode('utf-8')
    print "Feature ORT" 
    for i,x in enumerate(sorted(f3, key=f3.get, reverse=False)): print str(i+1+len(f1)+len(f2))+" "+x.encode('utf-8')
    print "Feature Prefix1" 
    for i,x in enumerate(sorted(f4, key=f4.get, reverse=False)): print str(i+1+len(f1)+len(f2)+len(f3))+" "+x.encode('utf-8')
    print "Feature Prefix2" 
    for i,x in enumerate(sorted(f5, key=f5.get, reverse=False)): print str(i+1+len(f1)+len(f2)+len(f3)+len(f4))+" "+x.encode('utf-8')
    print "Feature Prefix3"
    for i,x in enumerate(sorted(f6, key=f6.get, reverse=False)): print str(i+1+len(f1)+len(f2)+len(f3)+len(f4)+len(f5))+" "+x.encode('utf-8')
    print "Feature suffix1"
    for i,x in enumerate(sorted(f7, key=f7.get, reverse=False)): print str(i+1+len(f1)+len(f2)+len(f3)+len(f4)+len(f5)+len(f6))+" "+x.encode('utf-8')
    print "Feature suffix2"
    for i,x in enumerate(sorted(f8, key=f8.get, reverse=False)): print str(i+1+len(f1)+len(f2)+len(f3)+len(f4)+len(f5)+len(f6)+len(f7))+" "+x.encode('utf-8')
    print "Feature suffix3"
    for i,x in enumerate(sorted(f9, key=f9.get, reverse=False)): print str(i+1+len(f1)+len(f2)+len(f3)+len(f4)+len(f5)+len(f6)+len(f7)+len(f8))+" "+x.encode('utf-8')

def choosing_encoding(sent):
    for tree in sent:
        for tup in tree:
            if type(tup) == tuple:
                addFeature(tup[0],tup[1],'O') 
            else:
                root = tup.node
                first = tup[0]
                addFeature(first[0],first[1],'B-'+root)
                for t in tup[1:]:
                    addFeature(t[0],t[1],'I-'+root)
                    
def addFeature(word,pos,clas):
    if (Classes.count(clas)==0): return 
    if (f1.has_key(word) == False) : f1[word] = str(len(f1)) 
    if (f2.has_key(pos) == False) : f2[pos] = str(len(f2))
    l = len(word)
    ort = getORT(word)
    if (f3.has_key(ort) == False) : f3[ort] = str(len(f3))
    if (f4.has_key(word[0]) == False) : f4[word[0]] = str(len(f4))
    if (f7.has_key(word[l-1]) == False) : f7[word[l-1]] = str(len(f7))
    if l>1: 
        if (f5.has_key(word[0:2]) == False) : f5[word[0:2]] = str(len(f5))
        if (f8.has_key(word[l-2:l]) == False) : f8[word[l-2:l]] = str(len(f8))
    if l>2:
        if (f6.has_key(word[0:3]) == False) : f6[word[0:3]] = str(len(f6)) 
        if (f9.has_key(word[l-3:l]) == False) : f9[word[l-3:l]] = str(len(f9))

def getORT(word):
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if word.isdigit() : return 'number'
    if (regex.search(word) != None) : return 'URL'
    if word.isupper() : return 'all-capitals'
    if word.istitle() : return 'capitalized'
    if ([c.isdigit() for c in word].count(True) != 0) : return 'contains-digit' 
    if (word.count('-')!=0) : return 'contains-hyphen'
    if ( sum([word.find(c) for c in [';', ':', ',', '.', '!', '?']])!=-6) :return 'punctuation' 
    return 'regular'

def extract_features(sent):
    vectors = []
    cl = []
    for tree in sent:
        for tup in tree:
            if type(tup) == tuple:
                v = generateVector(tup[0],tup[1],'O')
                if (len(v)!=0) : 
                    vectors.append(v)
                    if(cl.count(v[0])==0): cl.append(v[0]) 
            else:
                root = tup.node
                first = tup[0]
                v = generateVector(first[0],first[1],'B-'+root)
                if (len(v)!=0) : 
                    vectors.append(v)
                    if(cl.count(v[0])==0): cl.append(v[0])
                for t in tup[1:]:
                    v= generateVector(t[0],t[1],'I-'+root)
                    if (len(v)!=0) :
                        vectors.append(v)
                        if(cl.count(v[0])==0): cl.append(v[0])
    cl.sort()
    return cl , vectors

def generateVectorStrings(word,pos,clas): 
    if (Classes.count(clas)==0): return "" 
    vec = str(Classes.index(clas) + 1) + ' '   
    vec = vec + str(int(f1[word]) + 1) + ':1 ' 
    vec = vec + str(len(f1) + int(f2[pos]) + 1) + ':1 '
    vec = vec + str(len(f1) + len(f2) + int(f3[getORT(word)]) + 1) + ':1 '
    vec = vec + str(len(f1) + len(f2) + len(f3) + int(f4[word[0]]) + 1) + ':1 '
    l = len(word)
    if l>1: vec = vec + str(len(f1) + len(f2) + len(f3) + len(f4) + int(f5[word[0:2]]) + 1) + ':1 '
    if l>2: vec = vec + str(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + int(f6[word[0:3]]) + 1) + ':1 '
    vec = vec + str(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + len(f6) + int(f7[word[l-1]]) + 1) + ':1 '
    if l>1: vec = vec + str(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + len(f6) + len(f7) + int(f8[word[l-2:l]]) + 1) + ':1 '
    if l>2: vec = vec + str(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + len(f6) + len(f7) + len(f8) + int(f9[word[l-3:l]]) + 1) + ':1 '
    return vec

def generateVector(word,pos,clas):
    vec = [] 
    if (Classes.count(clas)==0): return vec 
    vec.append(Classes.index(clas) + 1)  
    vec.append(int(f1[word]) + 1)  
    vec.append(len(f1) + int(f2[pos]) + 1)
    vec.append(len(f1) + len(f2) + int(f3[getORT(word)]) + 1)
    vec.append(len(f1) + len(f2) + len(f3) + int(f4[word[0]]) + 1) 
    l = len(word)
    if l>1: vec.append(len(f1) + len(f2) + len(f3) + len(f4) + int(f5[word[0:2]]) + 1)
    if l>2: vec.append(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + int(f6[word[0:3]]) + 1) 
    vec.append(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + len(f6) + int(f7[word[l-1]]) + 1)
    if l>1: vec.append(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + len(f6) + len(f7) + int(f8[word[l-2:l]]) + 1) 
    if l>2: vec.append(len(f1) + len(f2) + len(f3) + len(f4) + len(f5) + len(f6) + len(f7) + len(f8) + int(f9[word[l-3:l]]) + 1) 
    return vec
    
def main():
#    train = conll2002.chunked_sents('esp.train')# In Spanish    
    train = conll2002.chunked_sents('esp.testa')# In Spanish
    choosing_encoding(train)
    cl , vectors = extract_features(train)
    file = open("test.txt", 'w')
    for x in vectors :
        x = x+'\n'
        file.write(x.encode('ascii'))
    file.close() 
#    conll2002.chunked_sents('esp.testa') # In Spanish
#    conll2002.chunked_sents('esp.testb') # In Spanish
#    
#    conll2002.chunked_sents('ned.train') # In Dutch
#    conll2002.chunked_sents('ned.testa') # In Dutch
#    conll2002.chunked_sents('ned.testb') # In Dutch
    
if __name__ == '__main__':
    main() 