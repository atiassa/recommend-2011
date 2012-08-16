package extractWikiPages;

import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Category;
import de.tudarmstadt.ukp.wikipedia.api.DatabaseConfiguration;
import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.api.WikiConstants.Language;
import de.tudarmstadt.ukp.wikipedia.api.Wikipedia;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiApiException;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiInitializationException;

public class WikiData {
	
	private final int ARTICLES_NUM ;
	private Vector<Page> _articles;
	private Wikipedia _wikipedia;
	
	public WikiData(int N_words , int M_outgoing_links, int train_pages_num){
		_articles = new Vector<Page>();
		ARTICLES_NUM = train_pages_num;

		try {
			_wikipedia = createWiki();
			extractPages(N_words ,M_outgoing_links);
		} catch (WikiApiException e) {
			e.printStackTrace();
		}
	
	}
	
	/*
	 *  obtain information for ARTICLES_NUM articles in the categories you select
	 */
	public Vector<Page> getArticles(){
		return _articles;
	}
	
	/*
	 * fill Vector with Pages ,filter out "small articles" -- those that have
	 * less than N words and those that have less than M outgoing links.
	 */
	private void extractPages(int n_words, int m_outgoing_links) throws WikiApiException {
		System.out.println("Bulding wikipedia Train DataSet with "+ARTICLES_NUM+" articles.");
		Page page;
		Category cat =  _wikipedia.getCategory("יונקים");
		Vector<Page> openlist = new Vector<Page>();
		
		openlist.addAll(cat.getArticles());
		while(!openlist.isEmpty() & _articles.size() < ARTICLES_NUM){
			page = openlist.remove(0);
			
			if(openlist.size()<1000)
					openlist.addAll(page.getOutlinks());
			
			if(page.getNumberOfOutlinks() <= m_outgoing_links & page.getText().split("\\s+").length >= n_words){
				_articles.add(page);
				if(_articles.size()%10 ==0)
					System.out.println("  get so far : "+_articles.size());
			}
				
		}
	}

	/*
	 * read from jwmp.xml and create Wikipedia
	 */
	private Wikipedia createWiki() throws WikiInitializationException{
        // configure the database connection parameters
        DatabaseConfiguration dbConfig = new DatabaseConfiguration();
        dbConfig.setHost("localhost");
        dbConfig.setDatabase("hewiki");
        dbConfig.setUser("root");
        dbConfig.setPassword("123456");
        dbConfig.setLanguage(Language.hebrew);
        
        // Create a new Hebrew wikipedia.
        Wikipedia wiki = new Wikipedia(dbConfig);
		return wiki;
	}
	
	public Vector<Integer> getArticlesIDs(){
		Vector<Integer>	v = new Vector<Integer>();
		for(Page p : _articles){
			p.getPageId();
		}
		return v;
	}

	public Wikipedia getWikipedia() {
		return _wikipedia;
	}

	
}
