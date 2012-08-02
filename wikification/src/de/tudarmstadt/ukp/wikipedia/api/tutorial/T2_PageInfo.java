/*******************************************************************************
 * Copyright (c) 2010 Torsten Zesch.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the GNU Lesser Public License v3
 * which accompanies this distribution, and is available at
 * http://www.gnu.org/licenses/lgpl.html
 * 
 * Contributors:
 *     Torsten Zesch - initial API and implementation
 ******************************************************************************/
package de.tudarmstadt.ukp.wikipedia.api.tutorial;

import de.tudarmstadt.ukp.wikipedia.api.DatabaseConfiguration;
import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.api.WikiConstants;
import de.tudarmstadt.ukp.wikipedia.api.Wikipedia;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiApiException;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiPageNotFoundException;
import java.util.Properties;
import java.io.FileInputStream;

/**
 * Tutorial 2
 * 
 * A page provides a number of informative methods.
 * 
 * @author zesch
 *
 */
public class T2_PageInfo implements WikiConstants {

    public static void main(String[] args) throws WikiApiException {
		String host = "localhost";
		String db = "hewiki";
		String user = "root";
		String pwd = "123456";
		String title = "מחשב";
        // String title = "הנדסת_תוכנה";
		// String title = "צורה";
		// String title = "בן-גוריון";
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

        // Create a new wikipedia
        Wikipedia wiki = new Wikipedia(dbConfig);
        
        Page page;
        try {
            page = wiki.getPage(title);
        } catch (WikiPageNotFoundException e) {
            throw new WikiApiException("Page " + title + " does not exist");
        }
        
        // the title of the page
        System.out.println("Queried string       : " + title);
        System.out.println("Title                : " + page.getTitle());

        // whether the page is a disambiguation page
        System.out.println("IsDisambiguationPage : " + page.isDisambiguation());
        
        // whether the page is a redirect
        // If a page is a redirect, we can use it like a normal page.
        // The other infos in this example are transparently served by the page that the redirect points to. 
        System.out.println("redirect page query  : " + page.isRedirect());
        
        // the number of links pointing to this page
        System.out.println("# of ingoing links   : " + page.getNumberOfInlinks());
        
        // the number of links in this page pointing to other pages
        System.out.println("# of outgoing links  : " + page.getNumberOfOutlinks());
        
        // the number of categories that are assigned to this page
        System.out.println("# of categories      : " + page.getNumberOfCategories());
    }
}
