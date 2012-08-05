package extractWikiPages;

import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Category;
import de.tudarmstadt.ukp.wikipedia.api.DatabaseConfiguration;
import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.api.Wikipedia;
import de.tudarmstadt.ukp.wikipedia.api.WikiConstants.Language;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiApiException;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiInitializationException;
import de.tudarmstadt.ukp.wikipedia.parser.Link;
import de.tudarmstadt.ukp.wikipedia.parser.ParsedPage;
import de.tudarmstadt.ukp.wikipedia.parser.Section;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.FlushTemplates;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParser;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParserFactory;

public class Analyze {

	private WikiDecision _dec;
	private final int TEST_PAGES_NUM;
	private Vector<Page> _test;
	
	public Analyze(WikiDecision dec, int test_pages_num){
		this._dec = dec;
		TEST_PAGES_NUM = test_pages_num;
		_test = new Vector<Page>();
		generateTestDataSet();
	}
	
	//TODO
	private void generateTestDataSet(){
		WikiData wikiData = _dec.getWikiCfd().getWikiData();
		Page page;
		try {
			Category cat =  wikiData.getWikipedia().getCategory("יונקים");
		} catch (WikiApiException e) {
			e.printStackTrace();
		}
		Vector<Integer> trainIDs  = wikiData.getArticlesIDs();

		Vector<Page> openlist = new Vector<Page>();
		while(_test.size() < TEST_PAGES_NUM){
			page = openlist.remove(0);
			
			if(openlist.size()<1000)
					openlist.addAll(page.getOutlinks());
			
			if(!trainIDs.contains(page.getPageId()))
				_test.add(page);
		}

	}
	
	public double getAccuracy(){
		int hits = 0;
		int total = 0;
		for(Page p: _test){
			String cleanText = Linguistic.cleanText(p.getText());
			Vector<String> ourTerms = this._dec.findTerms(cleanText);
			Map<String, String> realMap = buildRealMap(p);
			Map<String, String> ourMap = this._dec.buildDecisionsMap(ourTerms);
			hits = hits + this.compareTwoMaps(realMap, ourMap);
			total = total + realMap.size();
		}
		return (double)hits/(double)total;
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
	
	//return num of hits
	private int compareTwoMaps(Map<String, String> real, Map<String, String> our){
		int hits = 0;
		for(String term: our.keySet()){
			String ourLink = our.get(term);
			String realLink = real.get(term);
			if(realLink != null && realLink.equals(ourLink))
				hits++;
		}
		return hits;
	}
	
}
