package pyclass;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.Writer;
import java.util.List;

import vohmm.application.SimpleTagger3;
import vohmm.corpus.AffixInterface;
import vohmm.corpus.Anal;
import vohmm.corpus.AnalysisInterface;
import vohmm.corpus.BitmaskResolver;
import vohmm.corpus.Lemma;
import vohmm.corpus.Sentence;
import vohmm.corpus.Tag;
import vohmm.corpus.Token;
import vohmm.corpus.TokenExt;

public class BitMask {
    
	SimpleTagger3 tagger;
	
	public BitMask(SimpleTagger3 ta) {
		tagger = ta;
    }

	
	public String bitRelosve(List<Sentence> taggedSentences) throws Exception{
		String text = "";
		//PrintStream out = new PrintStream(new FileOutputStream("out2.txt"),true,"UTF-8");
		for (Sentence sentence : taggedSentences) {
			
			// print tagged sentence by using AnalysisInterface, as follows:
			for (TokenExt tokenExt : sentence.getTokens()) {
				Token token = tokenExt._token;
				Anal anal =  token.getSelectedAnal();
				Lemma lemma = anal.getLemma();

				// NOTE: In our tagger we consider participle of a 'verb' type as a present verb.
				// In order to adapt it to MILA's schema the last parameter of BitmaskResolver constructor should be 'false' (no present verb)
				//AnalysisInterface bitmaskResolver = new BitmaskResolver(anal.getTag().getBitmask(),token.getOrigStr(),false);
				
				text = text + lemma.getStr().replace("^"," ") +" ";
			}
		}
		return text;
		
	}
	
}
