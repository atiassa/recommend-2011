package extractWikiPages;

import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Category;
import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiApiException;
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
		try {
			generateTestDataSet();
		} catch (WikiApiException e) {
			e.printStackTrace();
		}
	}
	
	private void generateTestDataSet() throws WikiApiException{
		System.out.println("--------Start generating Test DataSet---------");
		WikiData wikiData = _dec.getWikiCfd().getWikiData();
		Page page;
		Category cat =  wikiData.getWikipedia().getCategory("יונקים");
		Vector<Integer> trainIDs  = wikiData.getArticlesIDs();

		Vector<Page> openlist = new Vector<Page>();
		openlist.addAll(cat.getArticles());
		while(_test.size() < TEST_PAGES_NUM){
			page = openlist.remove(0);
			
			if(openlist.size()<1000)
					openlist.addAll(page.getOutlinks());
			
			if(!trainIDs.contains(page.getPageId()))
				_test.add(page);
		}
		System.out.println("--------Done generating Test DataSet---------");

	}
	
	public double getAccuracy(){
		System.out.println("--------Start Decision process & Accuracy calculation---------");
		int hits = 0;
		int total = 0;
		// get a ParsedPage object
		MediaWikiParserFactory pf = new MediaWikiParserFactory();
		pf.setTemplateParserClass( FlushTemplates.class );
		MediaWikiParser parser = pf.createParser();
		for(Page p: _test){
			ParsedPage pp = parser.parse(p.getText());
			String cleanText = Linguistic.cleanText(pp.getText());
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
		    	h.put(Linguistic.cleanText(link.getText()),t);
		    }
		}
		return h;
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
