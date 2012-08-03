package program;

import extractWikiPages.Linguistic;
import extractWikiPages.WikiCfd;
import extractWikiPages.WikiData;


public class App {

	 public static void main(String[] args){
		 WikiData wikiData = new WikiData(200, 35);
		 WikiCfd wikiCfd = new WikiCfd();
		 wikiCfd.training(wikiData.getArticles());
		 
	 }
}
