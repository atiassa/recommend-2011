package extractWikiPages;

import hebrewNER.NERTagger;

import java.io.ByteArrayInputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.util.List;

import vohmm.application.SimpleTagger3;
import vohmm.corpus.AffixInterface;
import vohmm.corpus.Anal;
import vohmm.corpus.AnalysisInterface;
import vohmm.corpus.BitmaskResolver;
import vohmm.corpus.Sentence;
import vohmm.corpus.Sentence.OutputData;
import vohmm.corpus.Tag;
import vohmm.corpus.Token;
import vohmm.corpus.TokenExt;
import yg.chunker.TaggerBasedHebrewChunker;
import yg.sentence.MeniTaggeedSentenceFactory;
import yg.sentence.MeniTokenExpander;

public class Tagger {
	
	private SimpleTagger3 tagger;
	private NERTagger nerTagger;
	private MeniTaggeedSentenceFactory sentenceFactory;
	private String chunkModelPrefix;
	private TaggerBasedHebrewChunker chunker;

	public Tagger(String taggeHomeDir) {
		try {
			// The follwoing object constructions are heavy - SHOULD BE APPLIED ONLY ONCE!
			// create the morphological analyzer and disambiguator 
			tagger = new SimpleTagger3(taggeHomeDir);
			// create the named-entity recognizer
			nerTagger = new NERTagger(taggeHomeDir,tagger);
			// create the noun-phrase chunker
			sentenceFactory = new MeniTaggeedSentenceFactory(null, MeniTokenExpander.expander);
	        chunkModelPrefix = taggeHomeDir + vohmm.util.Dir.CHUNK_MODEL_PREF;
			chunker = new TaggerBasedHebrewChunker(sentenceFactory, chunkModelPrefix);


		} catch (Exception e) {
			e.printStackTrace(); 
			System.exit(0);
		}
	}
	
	public String tagString(String text){
		String ans = "";
		try {
			// For string -- to String
			
			InputStream in = new ByteArrayInputStream(new String(text).getBytes("UTF-8"));
			List<Sentence> taggedSentences = tagger.getTaggedSentences(in);
			// print tagged sentence
			// by applying toString method of Senetence class with OutputData.TAGGED mode
			for (Sentence sentence : taggedSentences) 
				ans = ans + sentence.toString(OutputData.TAGGED) + "\n";
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
		return ans;
	}
	
	public void tagFile(String inputFile, String outputFile){
		
		try {	
			// The tagger gets an InputStream, i.e. both given string and text file of UTF-8 encoding is supported.
			// create input and output streams
			// Output stream
			PrintStream out = new PrintStream(new FileOutputStream(outputFile),false,"UTF-8");
			
			// Input stream			
			// For text file (UTF-8)
			InputStream in = new FileInputStream(inputFile);	
			List<Sentence> taggedSentences = tagger.getTaggedSentences(in);
		
			for (Sentence sentence : taggedSentences) {
			
				// Named-entiry recognition for the given tagged sentence
				nerTagger.addNerLabels(sentence);
		
				//Noun-phrase chunking for the given tagged sentence (will be available soon in Java)
				chunker.addBIOLabels(sentence);
			
				// print tagged sentence by using AnalysisInterface, as follows:
				for (TokenExt tokenExt : sentence.getTokens()) {
					Token token = tokenExt._token;
					out.println(token.getOrigStr());
					Anal anal =  token.getSelectedAnal();
					out.println("\tLemma: " + anal.getLemma());
		
					// NOTE: In our tagger we consider participle of a 'verb' type as a present verb.
					// In order to adapt it to MILA's schema the last parameter of BitmaskResolver constructor should be 'false' (no present verb)
					AnalysisInterface bitmaskResolver = new BitmaskResolver(anal.getTag().getBitmask(),token.getOrigStr(),false);
					out.println("\tPOS: " + bitmaskResolver.getPOS());
					out.println("\tPOS type: " + bitmaskResolver.getPOSType()); // the type of participle is "noun/adjective" or "verb"
					out.println("\tGender: " + bitmaskResolver.getGender());
					out.println("\tNumber: " + bitmaskResolver.getNumber());
					out.println("\tPerson: " + bitmaskResolver.getPerson());
					out.println("\tStatus: " + bitmaskResolver.getStatus());
					out.println("\tTense: " + bitmaskResolver.getTense());
					out.println("\tPolarity: " + bitmaskResolver.getPolarity());
					out.println("\tDefiniteness: " + bitmaskResolver.isDefinite());
					if (bitmaskResolver.hasPrefix()) {
						out.print("\tPrefixes: ");
						List<AffixInterface> prefixes = bitmaskResolver.getPrefixes();
						if (prefixes != null) {
							for (AffixInterface prefix : prefixes)
								out.print(prefix.getStr() + " " + Tag.toString(prefix.getBitmask(),true) + " ");
						}
						out.print("\n");
					} else
						out.println("\tPrefixes: None");
					if (bitmaskResolver.hasSuffix()) {
						out.println("\tSuffix Function: " + bitmaskResolver.getSuffixFunction());
						out.println("\tSuffix Gender: " + bitmaskResolver.getSuffixGender());
						out.println("\tSuffix Number: " + bitmaskResolver.getSuffixNumber());
						out.println("\tSuffix Person: " + bitmaskResolver.getSuffixPerson());
					} else 
						out.println("\tSuffix: None");		
				
				    // print token NER and Chunk properties	
					out.println("\tNER: " + tokenExt.getNER());			
					out.println("\tChunk: " + tokenExt.getChunk());			
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
	}
}
