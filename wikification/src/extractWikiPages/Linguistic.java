package extractWikiPages;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;

import vohmm.application.BasicTagger;

import de.tudarmstadt.ukp.wikipedia.parser.ParsedPage;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.FlushTemplates;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParser;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParserFactory;

public class Linguistic {
	
	public static String cleanText(String text){
		// get a ParsedPage object
		MediaWikiParserFactory pf = new MediaWikiParserFactory();
		pf.setTemplateParserClass( FlushTemplates.class );

		MediaWikiParser parser = pf.createParser();
		ParsedPage pp = parser.parse(text);
		return pp.getText();
	}
	
	public static String segmentationAndStemming(String text){
		//first we need to use the package to split the prefixes and suffixes.
		//TODO
		
		//remove all the stop words from the text - after the split.
		text = Linguistic.removeStopWords(text);
		return text;
	}
	
	private static String removeStopWords(String text){
		Vector<String> stopWords = readStopWords();
		String[] textWords = text.split(" ");
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

	private static Vector<String> readStopWords() {
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
		private static void segmentation(String fileName, String tokenizedFileName, String posFileName, String analyzeFileName){
			//first phase - running the hebtokenizer.py - writing the result to the tokenize fileName
			
			//just for checking the jar
			tokenizedFileName = "ben-gurion-tokenized.txt";
			posFileName = "ben-gurion.pos";
			
			//second phase - running the tagger - writing the tagged text to the pos fileName
			String[] args = {tokenizedFileName, posFileName, "-bWST"};
			BasicTagger.main(args);
			
			//third phase - running the bitmasks_to_tags.py - writing the result to the Analyzed fileName
			
		}
}
