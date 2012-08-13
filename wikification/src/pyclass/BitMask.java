package pyclass;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.List;

import vohmm.corpus.AffixInterface;
import vohmm.corpus.AnalysisInterface;
import vohmm.corpus.BitmaskResolver;
import vohmm.corpus.Tag;

public class BitMask {
    
	public BitMask() {
    }

	
	public void bitRelosve() throws Exception{
		String         line;
		BufferedReader br = new BufferedReader(  new InputStreamReader(new FileInputStream(new File("out2.txt")), "UTF8"));
		
		while ((line = br.readLine()) != null) {
				String[] l = line.split("\t");
				if(l.length!=2)
					continue;
				Long bits = new Long(l[1]);
				String word = l[0];
				System.out.println(word);
				
				// NOTE: In our tagger we consider participle of a 'verb' type as a present verb.
				// In order to adapt it to MILA's schema the last parameter of BitmaskResolver constructor should be 'false' (no present verb)
				AnalysisInterface bitmaskResolver = new BitmaskResolver(bits,word,false);
				System.out.println("\tPOS: " + bitmaskResolver.getPOS());
				System.out.println("\tPOS type: " + bitmaskResolver.getPOSType()); // the type of participle is "noun/adjective" or "verb"
				System.out.println("\tGender: " + bitmaskResolver.getGender());
				System.out.println("\tNumber: " + bitmaskResolver.getNumber());
				System.out.println("\tPerson: " + bitmaskResolver.getPerson());
				System.out.println("\tStatus: " + bitmaskResolver.getStatus());
				System.out.println("\tTense: " + bitmaskResolver.getTense());
				System.out.println("\tPolarity: " + bitmaskResolver.getPolarity());
				System.out.println("\tDefiniteness: " + bitmaskResolver.isDefinite());
				if (bitmaskResolver.hasPrefix()) {
					System.out.print("\tPrefixes: ");
					List<AffixInterface> prefixes = bitmaskResolver.getPrefixes();
					if (prefixes != null) {
						for (AffixInterface prefix : prefixes)
							System.out.print(prefix.getStr() + " " + Tag.toString(prefix.getBitmask(),true) + " ");
					}
					System.out.print("\n");
				} else
					System.out.println("\tPrefixes: None");
				if (bitmaskResolver.hasSuffix()) {
					System.out.println("\tSuffix Function: " + bitmaskResolver.getSuffixFunction());
					System.out.println("\tSuffix Gender: " + bitmaskResolver.getSuffixGender());
					System.out.println("\tSuffix Number: " + bitmaskResolver.getSuffixNumber());
					System.out.println("\tSuffix Person: " + bitmaskResolver.getSuffixPerson());
				} else 
					System.out.println("\tSuffix: None");		
			}
		br.close();
	}
	
}
