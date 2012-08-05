package extractWikiPages;

import java.util.HashMap;
import java.util.Set;
import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.parser.Link;
import de.tudarmstadt.ukp.wikipedia.parser.ParsedPage;
import de.tudarmstadt.ukp.wikipedia.parser.Section;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.FlushTemplates;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParser;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParserFactory;

public class WikiCfd {
	
	private HashMap<String, HashMap<String, Integer>> _fd;

	public WikiCfd() {
		this._fd = new HashMap<String, HashMap<String,Integer>>();
	}
	
	/*
	 * build the freqDist fd where key is term and values are links
	 */
	public void training(Vector<Page> articles){
		for(Page p : articles){
			String text = p.getText();
			
			// get a ParsedPage object
			MediaWikiParserFactory pf = new MediaWikiParserFactory();
			pf.setTemplateParserClass( FlushTemplates.class );

			MediaWikiParser parser = pf.createParser();
			ParsedPage pp = parser.parse(text);
						    
			//get the internal links of each section
			for (Section section : pp.getSections()){
			    for (Link link : section.getLinks(Link.type.INTERNAL)) {
			    	String t = link.getTarget();
			    	t= t.replace("_", " ");
			    	addToMap(link.getText(),t);
			        //System.out.println("[" + link.getText()+" |"+t+"]");
			    }
			}
		}
	}

	/*
	 * add increase link value in tne term key by 1
	 * create new one if it not exists in hash
	 */
	private void addToMap(String term, String link) {
		if(_fd.containsKey(term)){
			if(_fd.get(term).containsKey(link))
				_fd.get(term).put(link, _fd.get(term).get(link).intValue() + 1);
			else
				_fd.get(term).put(link, 1);
		}
		else{
			HashMap<String, Integer> h =  new HashMap<String, Integer>();
			h.put(link, 1);
			_fd.put(term,h);
		}
	}


	/*
	 * return the link with the max value from the values related to the key "term"
	 */
	public String getMax(String term) {
		if(_fd.containsKey(term)){
			HashMap<String, Integer> h = _fd.get(term);
			Integer maxv = Integer.MIN_VALUE;
			String maxl = "";
			for (String link : h.keySet()){
				Integer v = h.get(link);
				if(v.compareTo(maxv) > 0){
					maxv = v;
					maxl = link;
				}
			}
			return maxl;
		}
		return null;
	}

	public HashMap<String, HashMap<String, Integer>> getCfd() {
		return _fd;
	}
	
	public Set<String> getAllTerms(){
		return _fd.keySet();
	}

}
