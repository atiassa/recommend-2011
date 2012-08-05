package program;

import java.util.Vector;

import de.tudarmstadt.ukp.wikipedia.api.Page;

import extractWikiPages.Analyze;
import extractWikiPages.Linguistic;
import extractWikiPages.WikiCfd;
import extractWikiPages.WikiData;
import extractWikiPages.WikiDecisionBaseLine;


public class App {

	 public static void main(String[] args){
		 int train = 500;
		 int test = (int)(0.2*train);
		 WikiData wikiData = new WikiData(200, 35,train);
		 WikiCfd wikiCfd = new WikiCfd(wikiData);
		 wikiCfd.training();
		 WikiDecisionBaseLine wikidecision = new WikiDecisionBaseLine(wikiCfd); 
		 Analyze analyze = new Analyze(wikidecision, test);
		 
		 System.out.println("Accuracy = "+analyze.getAccuracy());
	 }
}
