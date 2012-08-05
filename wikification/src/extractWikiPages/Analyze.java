package extractWikiPages;

import java.util.Map;
import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Page;

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
	
	//TODO map<Term,Link>
	private Map<String, String> buildRealMap(Page p){
		
		return null;
	}
	
	//TODO return num of hits
	private int compareTwoMaps(Map<String, String> real, Map<String, String> our){
		
		return 0;
	}
}
