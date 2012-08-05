package extractWikiPages;

import java.util.Map;
import java.util.Vector;

public abstract class WikiDecision {

	protected WikiCfd _cfd;
	
	public WikiDecision(WikiCfd wfd) {
		this._cfd = wfd;
	}
	
	// Decide to which link we will link the term
	public abstract String decide(String term);
	
	//TODO return Set of all terms that we can link
	public Vector<String> findTerms(String cleanText){
		//for each term in the cfd
			//if exist in the text add getlink to the result
		return null;
	}
	
	//TODO 
	public Map<String, String> buildDecisionsMap(Vector<String> terms){
		//for each term perform decide
		return null;
	}

}
