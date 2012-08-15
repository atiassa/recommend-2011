package extractWikiPages;
import java.io.BufferedReader;

import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.List;
import java.util.Vector;

import com.sun.msv.datatype.xsd.LengthFacet;

import pyclass.BitMask;
import pyclass.HebTokenizer;
import pyclass.Tagger;

import vohmm.application.BasicTagger;
import vohmm.corpus.Sentence;

import de.tudarmstadt.ukp.wikipedia.parser.ParsedPage;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.FlushTemplates;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParser;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParserFactory;

public class Linguistic {
	
	private static Tagger tagger = null;
	private static BitMask bitResolver ;
	
	public Linguistic(){
		
	}
	
	public static String cleanText(String text){
		if (tagger==null){
			tagger = new Tagger();
			bitResolver = new BitMask(tagger.getTagger());
		}
		return segmentationAndStemming(text);
	}
	
	private static  String segmentationAndStemming(String text){
		//first we need to use the package to split the prefixes and suffixes.
		text  = segmentation(text);
		
		//remove all the stop words from the text - after the split.
		text = removeStopWords(text);
		return text;
	}
	
	private static  String removeStopWords(String text){
		Vector<String> stopWords = readStopWords();
		String[] textWords = text.split("\t");
		String res = "";
		for (int i=0; i<textWords.length; i++){
			if (!stopWords.contains(textWords[i])){
				res = res + textWords[i];
				if (i < textWords.length - 1)
					res = res + " ";
			}
		}
		return res;
	}

	private static  Vector<String> readStopWords() {
		Vector<String> stopWords = new Vector<String>();
		try {
			FileReader fr = new FileReader("he-stopwords.txt");
			BufferedReader br = new BufferedReader(fr);
			String s = br.readLine();
			while (s != null){
				stopWords.add(s);
				s = br.readLine();
			}
		} catch (FileNotFoundException e) {
			System.out.println("stop words file not found");
			e.printStackTrace();
		} catch (IOException e) {
			System.out.println("can't read line from stop words file");
			e.printStackTrace();
		}
		return stopWords;
	}
	
	//getting a fileName of the full article, the filename for the tokenized text,
	//the filename of the segmented text and the file name of the analyzed (the output)
	//and writing to the last file the analyzed text 
	private static String segmentation(String text){
		String res = "";
		try {
			Writer in1 = new BufferedWriter(new OutputStreamWriter(
				    new FileOutputStream("in1.txt"), "UTF-8"));
			in1.write(text);
			in1.close();
		
			//first phase - running the hebtokenizer.py - writing the result to the tokenize fileName
			HebTokenizer tokenizer = new HebTokenizer();
			tokenizer.tokenize();
			
			//second phase - running the tagger - writing the tagged text to the pos fileName
			tagger.tagFile();
			List<Sentence> sentences = tagger.getSentences();
			
			//third phase - running the bitmasks_to_tags.py - writing the result to the Analyzed fileName
			res  = bitResolver.bitRelosve(sentences);
		
			// return clean text after segmentation
		} catch (Exception e) {
			e.printStackTrace();
		}
		return res;
	}
	
	
}
