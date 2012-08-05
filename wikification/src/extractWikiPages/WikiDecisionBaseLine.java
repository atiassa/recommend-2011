package extractWikiPages;

public class WikiDecisionBaseLine extends WikiDecision {

	public WikiDecisionBaseLine(WikiCfd wfd) {
		super(wfd);
	}

	@Override
	public String decide(String term) {
		return _cfd.getMax(term);
	}
	

}
