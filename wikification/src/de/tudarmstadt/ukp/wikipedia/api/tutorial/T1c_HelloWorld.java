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

import de.tudarmstadt.ukp.wikipedia.api.*;
import de.tudarmstadt.ukp.wikipedia.api.exception.*;
import java.util.Properties;
import java.io.FileInputStream;

/**
 * Tutorial 1c
 * 
 * Get the text of a wikipedia article.
 * The text will be formatted with MediaWiki markup.
 * 
 * Handle exceptions.
 * 
 * @author zesch
 *
 */
public class T1c_HelloWorld implements WikiConstants {

    public static void main(String[] args) {
		String host = "localhost";
		String db = "hewiki";
		String user = "root";
		String pwd = "password";
		String title = "מחשב";
		Properties prop = new Properties();
		FileInputStream fis;
		try {
			// We use XML properties to have default UTF-8 encoding (properties files are in ASCII)
			fis = new FileInputStream("jwpl.xml");
			prop.loadFromXML(fis);
			host = prop.getProperty("host", "localhost");
			db = prop.getProperty("db", "hewiki");
			user = prop.getProperty("user", "root");
			pwd = prop.getProperty("pwd", "password");
			title = prop.getProperty("title", "צורה");
			fis.close();
		} catch (java.io.FileNotFoundException e) {
			System.out.println("jwpl.properties not found - using default");
		} catch (java.io.IOException e) {
			System.out.println("Bad format in jwpl.xml");
		}
		System.out.println("host = " + host + " db = " + db + " user = " + user + " pwd = " + pwd + " title = " + title);
        // configure the database connection parameters
        DatabaseConfiguration dbConfig = new DatabaseConfiguration();
        dbConfig.setHost(host);
        dbConfig.setDatabase(db);
        dbConfig.setUser(user);
        dbConfig.setPassword(pwd);
        dbConfig.setLanguage(Language.hebrew);
        
        // Create a new wikipedia.
        Wikipedia wiki = null;
        try {
            wiki = new Wikipedia(dbConfig);
        } catch (WikiInitializationException e1) {
            System.out.println("Could not initialize Wikipedia.");
            e1.printStackTrace();
            System.exit(1);
        }
        
        // Get the page with title 
        try {
            Page page = wiki.getPage(title);
            System.out.println(page.getText());
			System.out.println("=============================Parsed Page=======================");
			System.out.println(page.getParsedPage().getText());
        } catch (WikiApiException e) {
            System.out.println("Page " + title + " does not exist");
            e.printStackTrace();
            System.exit(1);
        }
    }
}
