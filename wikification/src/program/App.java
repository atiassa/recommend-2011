package program;

import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Page;

import extractWikiPages.Linguistic;
import extractWikiPages.WikiCfd;
import extractWikiPages.WikiData;


public class App {

	 public static void main(String[] args){
		 WikiData wikiData = new WikiData(200, 35);
//		 WikiCfd wikiCfd = new WikiCfd();
//		 wikiCfd.training(wikiData.getArticles());
		 
		 Vector<Page> articles = wikiData.getArticles();
		 for (Page p: articles)
			 System.out.println(Linguistic.cleanText(p.getText()));
		 System.out.println();
	 }
}
