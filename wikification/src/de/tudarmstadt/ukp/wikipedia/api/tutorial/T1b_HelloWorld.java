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
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiApiException;
import java.util.Properties;
import java.io.FileInputStream;

/**
 * Tutorial 1b
 * 
 * Get the text of a wikipedia article.
 * The text will be formatted with MediaWiki markup.
 * 
 * If you do not care about exception handling, but want to avoid crashes on every page that does not exist.
 * 
 * @author zesch
 *
 */
public class T1b_HelloWorld implements WikiConstants {

    public static void main(String[] args) throws WikiApiException {
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
        
        // Create a new wikipedia.
        Wikipedia wiki = new Wikipedia(dbConfig);

        if (wiki.existsPage(title)) {
            Page page = wiki.getPage(title);
            System.out.println(page.getText());
        }
        else {
            System.out.println("Page " + title + " does not exist");
        }
    }
}
