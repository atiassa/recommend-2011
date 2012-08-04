package extractWikiPages;
import de.tudarmstadt.ukp.wikipedia.parser.ParsedPage;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.FlushTemplates;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParser;
import de.tudarmstadt.ukp.wikipedia.parser.mediawiki.MediaWikiParserFactory;

public class Linguistic {
	
	public static String cleanText(String text){
		// get a ParsedPage object
		MediaWikiParserFactory pf = new MediaWikiParserFactory();
		pf.setTemplateParserClass( FlushTemplates.class );

		MediaWikiParser parser = pf.createParser();
		ParsedPage pp = parser.parse(text);
		return pp.getText();
	}
	
	public static String segmentationAndStemming(String text){
		
		return null;
	}
}
