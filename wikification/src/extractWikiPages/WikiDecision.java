package extractWikiPages;

public abstract class WikiDecision {

	protected WikiCfd _wfd;
	
	public WikiDecision(WikiCfd wfd) {
		this._wfd = wfd;
	}
	
	public abstract String getLink(String term);

}
