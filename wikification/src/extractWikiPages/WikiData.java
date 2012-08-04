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
	
	private final int ARTICLES_NUM = 10;
	private Vector<Page> _articles;
	
	public WikiData(int N_words , int M_outgoing_links){
		_articles = new Vector<Page>();
		try {
			extractPages(N_words ,M_outgoing_links);
		} catch (WikiApiException e) {
			// TODO Auto-generated catch block
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
		Wikipedia wiki = createWiki();
		Page page;
		Category cat =  wiki.getCategory("יונקים");
		Vector<Page> openlist = new Vector<Page>();
		
		openlist.addAll(cat.getArticles());
		while(!openlist.isEmpty() & _articles.size() < ARTICLES_NUM){
			page = openlist.remove(0);
			
			if(openlist.size()<1000)
					openlist.addAll(page.getOutlinks());
			
			//System.out.println(page.getTitle()+" : links "+page.getNumberOfOutlinks() +" : words "+page.getText().split("\\s+").length);
			if(page.getNumberOfOutlinks() <= m_outgoing_links & page.getText().split("\\s+").length >= n_words){
				_articles.add(page);
				//System.out.println(_articles.size() + " ======== "+ page.getTitle());
				//System.out.println( page.getText());
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

	
}
