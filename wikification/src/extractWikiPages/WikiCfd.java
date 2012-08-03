package extractWikiPages;

import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Page;

public class WikiCfd {
	
	private Map<String, Map<String, Integer>> _fd;

	public WikiCfd() {
		this._fd = new HashMap<String, Map<String,Integer>>();
	}
	
	//build the freqDist fd
	public void training(Vector<Page> articles){
		
	}
}
