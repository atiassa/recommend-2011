package extractWikiPages;

import java.io.FileInputStream;
import java.util.Properties;
import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.DatabaseConfiguration;
import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.api.WikiConstants.Language;
import de.tudarmstadt.ukp.wikipedia.api.Wikipedia;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiApiException;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiInitializationException;

public class WikiData {
	
	private final int ARTICLES_NUM = 5000;
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
	public Vector<Page> getPages(){
		return _articles;
	}
	
	/*
	 * fill Vector with Pages ,filter out "small articles" -- those that have
	 * less than N words and those that have less than M outgoing links.
	 */
	private void extractPages(int n_words, int m_outgoing_links) throws WikiApiException {
		String title = "מחשב";
		Wikipedia wiki = createWiki(title);
		Vector<Page> _child = new Vector<Page>();
		while(_articles.size() < ARTICLES_NUM){
			Page page = wiki.getPage(title);
			if(page.getNumberOfOutlinks() <= m_outgoing_links & page.getText().split("\\s+").length >= n_words)
				_articles.add(page);
		}
		
	}

	/*
	 * read from jwmp.xml and create Wikipedia to the given title
	 */
	private Wikipedia createWiki(String title) throws WikiInitializationException{
		String host = "localhost";
		String db = "hewiki";
		String user = "root";
		String pwd = "123456";
		Properties prop = new Properties();
		FileInputStream fis;
		try {
			// We use XML properties to have default UTF-8 encoding (properties files are in ASCII)
			fis = new FileInputStream("jwpl.xml");
			prop.loadFromXML(fis);
			host = prop.getProperty("host", "localhost");
			db = prop.getProperty("db", "hewiki");
			user = prop.getProperty("user", "root");
			pwd = prop.getProperty("pwd", "123456");
			title = prop.getProperty("title", "צורה");
			fis.close();
		} catch (java.io.FileNotFoundException e) {
			System.out.println("jwpl.properties not found - using default");
		} catch (java.io.IOException e) {
			System.out.println("Bad format in jwpl.properties");
		}
		System.out.println("host = " + host + " db = " + db + " user = " + user + " pwd = " + pwd + " title = " + title);
        // configure the database connection parameters
        DatabaseConfiguration dbConfig = new DatabaseConfiguration();
        dbConfig.setHost(host);
        dbConfig.setDatabase(db);
        dbConfig.setUser(user);
        dbConfig.setPassword(pwd);
        dbConfig.setLanguage(Language.hebrew);
        
        // Create a new Hebrew wikipedia.
        Wikipedia wiki = new Wikipedia(dbConfig);
		return wiki;
	}

	
}
