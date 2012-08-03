package extractWikiPages;

import java.util.HashMap;
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
	
	//build the freqDist fd
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
			        System.out.println("[" + link.getText()+" |"+t+"]");
			    }
			}
			System.out.println("");
		}
	}

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


}
