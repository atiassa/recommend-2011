package program;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyInteger;
import org.python.util.PythonInterpreter;

import pyclass.HebTokenizer;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;

import extractWikiPages.Analyze;
import extractWikiPages.WikiCfd;
import extractWikiPages.WikiData;
import extractWikiPages.WikiDecisionBaseLine;


public class App {

	 public static void main(String[] args){
//		 int train = 1000;
//		 int test = (int)(0.2*train);
//		 WikiData wikiData = new WikiData(200, 35,train);
//		 WikiCfd wikiCfd = new WikiCfd(wikiData);
//		 wikiCfd.training();
//		 WikiDecisionBaseLine wikidecision = new WikiDecisionBaseLine(wikiCfd); 
//		 Analyze analyze = new Analyze(wikidecision, test);
//		 
//		 System.out.println("Accuracy = "+analyze.getAccuracy());
		 
		 HebTokenizer tok = new HebTokenizer();
		 try {
			System.out.println(tok.tokenize("[[שימי[[\n[[שימי[["));
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	 }
}
