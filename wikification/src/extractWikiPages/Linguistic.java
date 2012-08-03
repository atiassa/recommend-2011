package extractWikiPages;

public class Linguistic {
	
	public static String cleanText(String text){
		String noRef = Linguistic.removeRef(text);
		String noPar = Linguistic.removeParentheses(noRef);
		String noLinks = Linguistic.removeLinks(noPar);
		return noLinks;
	}
	
	private static String removeRef(String text){
		if (!text.contains("<ref>"))
			return text;
		while (text.contains("<ref>")){
			int ind1 = text.indexOf("<ref>");
			int ind2 = text.indexOf("</ref>");
			String start = text.substring(0, ind1);
			String rest = text.substring(ind2+6);
			text = start + rest;
		}
		return text;
	}
	
	private static String removeParentheses(String text){
		if (!text.contains("{{"))
			return text;
		while (text.contains("{{")){
			int ind1 = text.indexOf("{{");
			int ind2 = text.indexOf("}}");
			String start = text.substring(0, ind1);
			String rest = text.substring(ind2+2);
			text = start + rest;
		}
		return text;
	}
	
	private static String removeLinks(String text){
		if (!text.contains("[["))
			return text;
		while (text.contains("[[")){
			int ind1 = text.indexOf("[[");
			int ind2 = text.indexOf("]]");
			String start = text.substring(0, ind1);
			String anchor = text.substring(ind1+2, ind2);
			String rest = text.substring(ind2+2);
			String[] termLink = anchor.split("\\|");
			if (termLink.length > 2)
				text = start + rest;
			else
				if(termLink.length == 1)
					text = start + anchor + rest;
				else
					text = start + termLink[0] + rest;
		}
		return text;
	}

}
