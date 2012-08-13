package extractWikiPages;

import hebrewNER.NERTagger;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import vohmm.application.SimpleTagger3;
import vohmm.corpus.PatternKey;
import vohmm.corpus.Sentence;
import vohmm.corpus.Sentence.OutputData;
import vohmm.corpus.Sentence.OutputSentenceFormat;
import vohmm.corpus.Tag;
import vohmm.lexicon.BGULexicon;
import vohmm.prob.CandidatesFilter;
import vohmm.prob.DelcozCandidatesFilter;
import vohmm.util.Bitmask;
import vohmm.util.Morph;
import vohmm.util.Pair;
import vohmm.util.Pair2;
import yg.chunker.TaggerBasedHebrewChunker;
import yg.sentence.MeniTaggeedSentenceFactory;
import yg.sentence.MeniTokenExpander;

class UnsupportedFeatureIdException extends Exception {
	protected int _featureId;

	UnsupportedFeatureIdException(int featureId) {
		_featureId = featureId;
	}

	public String toString() {
		return String.format("Unsupported feature ID: %d",_featureId);
	}
}

public class Tagger {

	static String in_linebyline_encoding = "UTF-8"; 
	static String outencoding = "UTF-8"; //"CP1255";
	static final boolean bAllFiles = true;
	
	static final boolean bKBest=false;

	static Map<Integer,Long> mFeaturesMask = new HashMap<Integer,Long>();

	//static yg.tagger.SequentialTagger k;
	
	static SimpleTagger3 tagger = null;

	static long mask = Bitmask.ALL_MASK;
	static boolean bLemma = false;
	static boolean bLog = false;
	static boolean linebyline = false;
	static boolean bLemmaPrefix = false;	
	static OutputSentenceFormat format;
	static OutputData outputData=OutputData.TAGGED;
    static boolean bHasPN, bPN,bExt;
	static boolean bWST;
	static TaggerBasedHebrewChunker chunker = null;
	static NERTagger nerTagger=null;
	static int iSent=0,iTok=0;
	
	public Tagger() {

		String[] args = {"tagger/","out1.txt","out2.txt"};
		try {
			
			Set<String> features = new TreeSet<String>();
			if (args.length > 3) {
				for (int i=3; i < args.length; i++)
					features.add(args[i]);
			}
			
			
			System.out.println(features);
			
			mask = getMask(features);
			bLog = features.contains("-log");
			bLemma = (features.contains("-lemma") || features.contains("-lemma-prefix"));
			bLemmaPrefix = features.contains("-lemma-prefix");
			format = (features.contains("-sentenceperline") ? OutputSentenceFormat.SENTENCEPERLINE : OutputSentenceFormat.WORDPERLINE);
			if (features.contains("-conll"))
				outputData = OutputData.CONLL;
			if (features.contains("-tokenfeat"))
				outputData = OutputData.TOKENFEAT;
			if (features.contains("-noam"))
				outputData = OutputData.NOAM;			
			if (features.contains("-koppel"))
				outputData = OutputData.KOPPEL;
			if (features.contains("-rafi"))
				outputData = OutputData.RAFI;
			if (features.contains("-dudi"))
				outputData = OutputData.DUDI;
			if (features.contains("-lemmatized"))
				outputData = OutputData.LEMMATIZED;			
			if (features.contains("-tokenized"))
				outputData = OutputData.TOKENIZED;
			
			System.out.println(outputData);
			
            bExt = features.contains("-bExt");
            bHasPN = features.contains("-bHasPN");
            bPN = features.contains("-bPN");
            bWST = features.contains("-bWST");
            linebyline = features.contains("-bLinebyline");
            if (features.contains("-hazal"))
            	BGULexicon._bHazal = true;
            
            if (features.contains("-chunk")) {
            	MeniTaggeedSentenceFactory sentenceFactory = new MeniTaggeedSentenceFactory(null, MeniTokenExpander.expander);
            	String chunkModelPrefix = args[0] + vohmm.util.Dir.CHUNK_MODEL_PREF;
            	chunker = new TaggerBasedHebrewChunker(sentenceFactory, chunkModelPrefix);
            }             
            
            if (features.contains("-NER")) 
            	nerTagger = new NERTagger(args[0],tagger);
            
            String extLexicon=null;
            for (String str : features) {
            	if (str.startsWith("lexicon="))
            		extLexicon = str.substring(str.indexOf("=")+1);
            }
			tagger = new SimpleTagger3(args[0],bLog,bWST,!features.contains("-bNoUKPrefDist"),features.contains("-bComp"),extLexicon);			
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void tagFile(){
		try {
			tag("out1.txt","out2.txt");
			System.out.println(iTok + " tokens, " + iSent + " sentences");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	protected static long getMask(Set<String> features) throws NumberFormatException, UnsupportedFeatureIdException {
		long mask = 0;
		for (String feature : features) {
			try {
				int featureindex = Integer.parseInt(feature);
				try {
					mask |= getMask(featureindex);
				} catch (UnsupportedFeatureIdException usf) {
					System.err.println("WARNNING: feature index " + featureindex + ", is not supported");
				}
			} catch (NumberFormatException nf) {
			}
		}

		if (mask == 0)
			mask = Bitmask.ALL_MASK;

		return mask;
	}

	protected static long getMask(int id) throws UnsupportedFeatureIdException {
		Long mask = mFeaturesMask.get(id);
		if (mask == null)
			throw new UnsupportedFeatureIdException(id);
		return mask;
	}

	protected static void tag(String indir,String outdir) throws Exception {
		File in = new File(indir);
		File out = new File(outdir);
		if (!out.exists() || out.isFile()) {				
			PrintStream outstream = new PrintStream(new FileOutputStream(out),false,outencoding);
			printFeatureTitles(outstream);
			tag(in,outstream);
			outstream.close();
		} else
			tag(in,outdir,(in.isDirectory() ? in.getAbsolutePath().length() : in.getParent().length()));
	}

	protected static void tag(File infile,PrintStream out) throws Exception {
		if (infile.isDirectory()) {
			File[] files = infile.listFiles();
			Arrays.sort(files);
			for (int i=0;i<files.length;i++)
				tag(files[i],out);
		} else { // file to be taggged
			if (bAllFiles || infile.getName().endsWith(".txt")) {
				//debug
				System.out.println(infile.getAbsolutePath());				
				InputStream in = new FileInputStream(infile); 
				if (linebyline) {
					BufferedReader reader = new BufferedReader(new InputStreamReader(in,in_linebyline_encoding));
					String line=null;
					while ((line = reader.readLine()) != null) {
						line = line.trim();						
						if (!line.equals("")  && line.length() >1) 
							tag(new ByteArrayInputStream(line.getBytes("UTF-8")),out);
					}
				} else 				
					tag(in,out);
				in.close();
			}
		}
	}

	protected static void tag(File infile,String outdir,final int pos) throws Exception {
		if (infile.isDirectory()) {
			// create correspond directory for xml
			String out = outdir + infile.getAbsolutePath().substring(pos);
			System.out.println(out);
            if (!(new File(out)).exists()) {
            	if ((new File(out)).mkdir())
            		System.out.println("Success creating directory: " + out);
            	else
            		System.out.println("Error in creation of directory: " + out);
            }
            // call for analysis of each file/dir under the currect directory
			File[] files = infile.listFiles();
			Arrays.sort(files);
			for (int i=0;i<files.length;i++)
				tag(files[i],outdir,pos);

		} else { // file to be taggged
			if (bAllFiles || infile.getName().endsWith(".txt")) {
				//debug
				System.out.println(infile.getAbsolutePath());
				InputStream in = new FileInputStream(infile);	
				if (linebyline) {
					PrintStream outstream = new PrintStream(new FileOutputStream(outdir + infile.getAbsolutePath().substring(pos)),false,outencoding);
					printFeatureTitles(outstream);
					BufferedReader reader = new BufferedReader(new InputStreamReader(in,in_linebyline_encoding));
					String line=null;
					while ((line = reader.readLine()) != null) {
						line = line.trim();
						if (!line.equals(""))
							tag(new ByteArrayInputStream(line.getBytes("UTF-8")),outstream);
					}
					outstream.close();
				}
				else {
					String outfile = outdir + infile.getAbsolutePath().substring(pos);
					//outfile = outfile.substring(0,outfile.length()-3) + "txt";
					PrintStream outstream = new PrintStream(new FileOutputStream(outfile),false,outencoding);
					printFeatureTitles(outstream);					
					tag(in,outstream);
					outstream.close();
				}
				in.close();
			}
		}
	}

	protected static void tag(InputStream in,PrintStream out) throws Exception {

		if (bKBest)
			kbesttag(in,out);		
		else {

			/*BufferedReader reader = new BufferedReader(new InputStreamReader(in,"UTF-8"));
			String s;
			while ((s = reader.readLine()) != null)
				vohmm.util.Logger.logln(s);*/
			
			List<Sentence> taggedSentences = null;
			try {
				taggedSentences = tagger.getTaggedSentences(in);
			} catch (Exception e) {
				e.printStackTrace();
				return;
			}
	
			if (taggedSentences.size() == 0) {
				System.out.println("no sentence was identified!");
			}
					
			
			//tmp for rav-kook
			int tmpSent=0;
			for (Sentence sentence : taggedSentences) {
				
				//System.out.println(sentence);

				//tmp for rav-kook			
				//if (sentence !=null && sentence.size() > 0 && !(tmpSent == 0 && sentence.size()==2 && sentence.getToken(1).getOrigStr().equals("."))) {
				if (sentence !=null && sentence.size() > 0) {
					
					if (nerTagger!=null) 
						nerTagger.addNerLabels(sentence);

					if (chunker!=null) 
						chunker.addBIOLabels(sentence);
								
					iTok+=sentence.size();
					if (outputData != Sentence.OutputData.NOAM)
						out.println(sentence.toString(outputData,bLemma,bPN,bExt,bHasPN,nerTagger!=null,chunker!=null,bLemmaPrefix));
					else {
						out.println("<s>");
						out.print(sentence.toString(outputData,bLemma,bPN,bExt,bHasPN,nerTagger!=null,chunker!=null));
						out.println("</s>");
					}
				}
				//tmp for rav-kook
				tmpSent++;
				iSent++;
			}
		}
	}
	
	protected static void kbesttag(InputStream in,PrintStream out) throws Exception {
		CandidatesFilter filterer = new DelcozCandidatesFilter();
		for (List<Pair2<String,List<Pair<PatternKey,Double>>>> sentence : tagger.getKBestTaggedSentences(in)) {
			iSent++;
			for (Pair2<String,List<Pair<PatternKey,Double>>> token : sentence) {
				iTok++;
				
				//debug
				vohmm.util.Logger.logln(token.getFirst());
				vohmm.util.Logger.logln("Before filter:");
				for (Pair<PatternKey,Double> p : token.getSecond())
					vohmm.util.Logger.logln("\t" + p.getFirst() + " " + Math.exp(p.getSecond()));
				
				filterer.filter(token.getSecond(),token.getFirst());
				
				//debug
				vohmm.util.Logger.logln("After filter:");
				for (Pair<PatternKey,Double> p : token.getSecond())
					vohmm.util.Logger.logln("\t" + p.getFirst() + " " + Math.exp(p.getSecond()));

				
				out.print(token.getFirst());
				out.print(" ");				
				for (Pair<PatternKey,Double> anal : token.getSecond()) { 
					out.print(anal.getFirst());				
					out.print(" ");
					//tmp
					//break;
				}
				out.println();
			}			
			out.println();
		}
	}
	
	public static String getFeatureString(long bitmask) {
		StringBuilder ret = new StringBuilder();
		addFeature(bitmask & Bitmask.BASEFORM_POS,ret);
		addFeature(bitmask & Bitmask.BASEFORM_GENDER,ret);
		addFeature(bitmask & Bitmask.BASEFORM_NUMBER ,ret);
		addFeature(bitmask & Bitmask.BASEFORM_PERSON,ret);
		addFeature(bitmask & Bitmask.BASEFORM_STATUS,ret);
		addFeature(bitmask & Bitmask.BASEFORM_TENSE,ret);
		addFeature(bitmask & Bitmask.BASEFORM_POLARITY,ret);
		addFeature(bitmask & Bitmask.PREFIX_FUNCTION_CONJUNCTION,ret);
		addFeature(bitmask & Bitmask.PREFIX_FUNCTION_DEFINITEARTICLE,ret);
		addFeature(bitmask & Bitmask.PREFIX_FUNCTION_PREPOSITION,ret);
		addFeature(bitmask & Bitmask.PREFIX_FUNCTION_RELATIVIZER_SUBORDINATINGCONJUNCTION,ret);
		addFeature(bitmask & Bitmask.PREFIX_FUNCTION_TEMPORALSUBCONJ,ret);
		addFeature(bitmask & Bitmask.PREFIX_FUNCTION_ADVERB,ret);
		addFeature(bitmask & Bitmask.SUFFIX_FUNCTION,ret);
		addFeature(bitmask & Bitmask.SUFFIX_GENDER,ret);
		addFeature(bitmask & Bitmask.SUFFIX_NUMBER,ret);
		addFeature(bitmask & Bitmask.SUFFIX_PERSON,ret);
		return ret.toString().trim();
	}

	private static void addFeature(long bitmask,StringBuilder sb) {
		if (bitmask==0)
			sb.append("NULL ");
		else {
			sb.append(Tag.toString(bitmask,true).trim().replaceAll(" ","-"));
			sb.append(" ");
		}
	}
	
	static private void printFeatureTitles(PrintStream out) {
		if (outputData == OutputData.TOKENFEAT)
			out.println(Morph.INDEX_FILE_HEADER);
	}

	static {
		mFeaturesMask.put(1,Bitmask.BASEFORM_POS);
		mFeaturesMask.put(2,Bitmask.BASEFORM_GENDER);
		mFeaturesMask.put(3,Bitmask.BASEFORM_NUMBER);
		mFeaturesMask.put(4,Bitmask.BASEFORM_PERSON);
		mFeaturesMask.put(5,Bitmask.BASEFORM_STATUS);
		mFeaturesMask.put(6,Bitmask.BASEFORM_TENSE);
		mFeaturesMask.put(7,Bitmask.BASEFORM_POLARITY);
		mFeaturesMask.put(8,Bitmask.SUFFIX_FUNCTION);
		mFeaturesMask.put(9,Bitmask.SUFFIX_GENDER);
		mFeaturesMask.put(10,Bitmask.SUFFIX_NUMBER);
		mFeaturesMask.put(11,Bitmask.SUFFIX_PERSON);
		mFeaturesMask.put(12,Bitmask.PREFIX_MASK | Bitmask.PREFIX_FUNCTION_DEFINITEARTICLE);
		mFeaturesMask.put(13,Bitmask.PREFIX_FUNCTION_DEFINITEARTICLE);
		mFeaturesMask.put(14,Bitmask.PREFIX_FUNCTION_CONJUNCTION);
		mFeaturesMask.put(15,Bitmask.PREFIX_FUNCTION_INTERROGATIVE);
		mFeaturesMask.put(16,Bitmask.PREFIX_FUNCTION_PREPOSITION);
		mFeaturesMask.put(17,Bitmask.PREFIX_FUNCTION_RELATIVIZER_SUBORDINATINGCONJUNCTION);
		mFeaturesMask.put(18,Bitmask.PREFIX_FUNCTION_TEMPORALSUBCONJ);
		mFeaturesMask.put(19,Bitmask.PREFIX_FUNCTION_ADVERB);
	}
}
