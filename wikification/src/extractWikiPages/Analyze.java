package extractWikiPages;

import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.parser.Link;
import de.tudarmstadt.ukp.wikipedia.parser.ParsedPage;
import de.tudarmstadt.ukp.wikipedia.parser.Section;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.FlushTemplates;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParser;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParserFactory;

public class Analyze {

	private WikiDecision _dec;
	
	public Analyze(WikiDecision dec){
		this._dec = dec;
	}
	
	//TODO
	public Vector<Page> generateTestDataSet(){
		
		return null;
	}
	
	//TODO
	public double getAccuracy(Vector<Page> test){
		// go over each page in test
			// clean the text
			// find all terms
			// build the hash with our decisions
			// build hash with real decision
			// sum = sum + compare the two hash
			//sum the "mechane"
		// calc accuracy for all
		return 0;
	}
	
	//return the real map of <term ,link> from the Page
	private Map<String, String> buildRealMap(Page p){
		HashMap<String , String> h = new HashMap<String, String>();
		MediaWikiParserFactory pf = new MediaWikiParserFactory();
		pf.setTemplateParserClass( FlushTemplates.class );
		MediaWikiParser parser = pf.createParser();
		ParsedPage pp = parser.parse(p.getText());
					    
		//get the internal links of each section
		for (Section section : pp.getSections()){
		    for (Link link : section.getLinks(Link.type.INTERNAL)) {
		    	String t = link.getTarget();
		    	t= t.replace("_", " ");
		    	h.put(link.getText(),t);
		    }
		}
		return null;
	}
	
	//TODO return num of hits
	private int compareTwoMaps(Map<String, String> real, Map<String, String> our){
		
		return 0;
	}
}
