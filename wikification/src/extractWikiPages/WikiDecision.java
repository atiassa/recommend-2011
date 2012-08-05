package extractWikiPages;

import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

public abstract class WikiDecision {

	protected WikiCfd _cfd;
	
	public WikiDecision(WikiCfd wfd) {
		this._cfd = wfd;
	}
	
	// Decide to which link we will link the term
	public abstract String decide(String term);
	
	// return Set of all terms that we can link
	public Vector<String> findTerms(String cleanText){
		Vector<String> ans = new Vector<String>();
		for(String term : _cfd.getAllTerms()){
			if(cleanText.contains(term))
				ans.add(term);
		}
		return ans;
	}
	
	// for each term perform decide
	public Map<String, String> buildDecisionsMap(Vector<String> terms){
		
		HashMap<String , String> h = new HashMap<String, String>();
		for(String term : terms){
			h.put(term, _cfd.getMax(term));
		}
		return h;
	}

	public WikiCfd getWikiCfd() {
		return _cfd;
	}

}
