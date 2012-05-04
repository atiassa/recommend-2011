import nltk 
import urllib2
import google
import justext
from nltk.corpus import brown
      
def main():
    s = q1_1()
#####################################################################################################
#First Part getting about 50 sentences using google search and tagged them with an automatic tagger #
#write the text without the tags to cleanText.txt file and the tagged text to tagText file          #
#####################################################################################################
#    sentences = s.getTextFromWeb()
#    text = ""
#    for sen in sentences:
#        text = text + sen + "\n"
#    clean_file = open('cleanText.txt', 'w')
#    clean_file.write(text)
#    clean_file.close()
#    s.tagTextAndWriteToFile(sentences)

#########################################################
# Second Part after inserting tagged files to the Corpus#
#########################################################
    #ca45 => first human tagged file
    #ca46 => second human tagged file
    #ca47 => automatic tagger tagged file
#    dif1 = s.Compare_files('ca45', 'ca46') #compare 2 human taggs
#    dif2 = s.Compare_files('ca47', 'ca45') #compare first human taggs to auto tagger
#    dif3 = s.Compare_files('ca47', 'ca46') #compare second human taggs to auto tagger
#    s.write_differences_to_dif_file(dif1, 'Dif2Human.txt')
#    s.write_differences_to_dif_file(dif2, 'DifFirstHumanToAuto.txt')
#    s.write_differences_to_dif_file(dif3, 'DifSecondtHumanToAuto.txt')
    
    print "end"
           
class q1_1(object):
    
    # getting Bigram->Unigram->affix->regexp->DefaultNN tagger
    def getTagger(self):
        brown_news_tagged = brown.tagged_sents(categories='news')
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
        affix_tagger = nltk.AffixTagger(brown_news_tagged, backoff=regexp_tagger)
        ut3 = nltk.UnigramTagger(brown_news_tagged, backoff=affix_tagger)
        ct2 = nltk.NgramTagger(2, brown_news_tagged, backoff=ut3)
        return ct2
    
    #split the whole text to sentences using . or ? or ! as delimeters
    def segment_sentences(self,words):
        start = 0
        sents = []
        for i, word in enumerate(words):
            if word in '.?!': #and classifier.classify(punct_features(words, i)) == True:
                sents.append(words[start:i+1])
                start = i+1
        if start < len(words):
            sents.append(words[start:])
        return sents
    
    #getting text from web using google search 
    #(google.py -> we edited this file we got from our course web to adjust to our code)
    def getTextFromWeb(self):
        num_results = 10
        search_list = ["bbc", "Little Red Riding Hood"]
        sites = [] 
        text = []
        results = []
        while len(search_list)!=0 and len(results) < num_results:
            search = search_list.pop()
            results = results + google.google(search,nltk.word_tokenize)

        for d in results:
            sites.append(d)
            if len(sites) == num_results:
                break
  
        for url in sites:
            print url
            try:
                page = urllib2.urlopen(url).read()
            except urllib2.HTTPError, e:
                print "Search failed: %s" % e 
                continue
            paragraphs = justext.justext(page, justext.get_stoplist('English'))
            if len(text) < 50:
                for paragraph in paragraphs:
                    if paragraph['class'] == 'good' and len(text) < 50:
                        sentences = self.segment_sentences(paragraph['text'].encode('utf8'))
                        for s in sentences:
                            if not text.__contains__(s):
                                text.append(s)
        return text

    #tagging the text we got from the web using the tagger we defined above and write it to tagText file
    def tagTextAndWriteToFile(self,sentences):
        tag_file = open('tagText', 'w')
        tagger = self.getTagger()
        for sentence in sentences:
            tagged_sen = tagger.tag(sentence.split())
            for w,t in tagged_sen:
                tag_file.write(w + "/" + t + " ")
            tag_file.write("\n")
        tag_file.close()
    

    #comparing 2 files in the brown corpus and returning a list with all the words that are different
    #we assume we are talking on the same file and the only thing that can be different is the tag for each word
    def Compare_files(self, firstName, secondName):
        differences = []
        if firstName == 'ca47':#the tagger tag file is tagged in full mode
            file1Sentences = brown.tagged_sents(fileids=[firstName], simplify_tags=True)
        else:#our files were tagged in simplify mode
            file1Sentences = brown.tagged_sents(fileids=[firstName])
        file2Sentences = brown.tagged_sents(fileids=[secondName])
        i = 0
        while len(file1Sentences) != i:
            sen1 = file1Sentences[i]
            sen2 = file2Sentences[i]
            i = i + 1
            while len(sen1) != 0:
                tw1 = sen1.pop()
                tw2 = sen2.pop()
                w1, t1 = tw1
                w2, t2 = tw2
                if w1 == w2 and t1 != t2:
                    differences.append(w1)
        return differences
    
    #getting a list of words and file name and write the content of the list to the file
    def write_differences_to_dif_file(self, dif, difFileName):
        dif_file = open(difFileName, 'w')
        for w in dif:
            dif_file.write(w + " / ")
        dif_file.close()
                

if __name__ == '__main__':
    main()     

