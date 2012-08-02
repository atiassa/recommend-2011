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

import java.util.Set;
import java.util.TreeSet;

import de.tudarmstadt.ukp.wikipedia.api.Category;
import de.tudarmstadt.ukp.wikipedia.api.DatabaseConfiguration;
import de.tudarmstadt.ukp.wikipedia.api.Page;
import de.tudarmstadt.ukp.wikipedia.api.WikiConstants;
import de.tudarmstadt.ukp.wikipedia.api.Wikipedia;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiApiException;
import de.tudarmstadt.ukp.wikipedia.api.exception.WikiPageNotFoundException;
import java.util.Properties;
import java.io.FileInputStream;


/**
 * Tutorial 5
 * 
 * Wikipedia categories are used as a kind of semantic tag for pages.
 * They are organized in a thesaurus like structure.
 * 
 * If we get all pages assigned to categories in the sub-tree under a category 
 * 
 * @author zesch
 *
 */
public class T5_PageList implements WikiConstants {

    public static void main(String[] args) throws WikiApiException {
		String host = "localhost";
		String db = "hewiki";
		String user = "root";
		String pwd = "password";
		String category = "יונקים";
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
			category = prop.getProperty("category", "יונקים");
			fis.close();
		} catch (java.io.FileNotFoundException e) {
			System.out.println("jwpl.properties not found - using default");
		} catch (java.io.IOException e) {
			System.out.println("Bad format in jwpl.xml");
		}
		System.out.println("host = " + host + " db = " + db + " user = " + user + " pwd = " + pwd + " category = " + category);
        // configure the database connection parameters
        DatabaseConfiguration dbConfig = new DatabaseConfiguration();
        dbConfig.setHost(host);
        dbConfig.setDatabase(db);
        dbConfig.setUser(user);
        dbConfig.setPassword(pwd);
        dbConfig.setLanguage(Language.hebrew);

        // Create a new wikipedia.
        Wikipedia wiki = new Wikipedia(dbConfig);

        // Get the category
        Category topCat;
        try {
            topCat = wiki.getCategory(category);
        } catch (WikiPageNotFoundException e) {
            throw new WikiApiException("Category " + category + " does not exist");
        }

        // Add the pages categorized under the category
        Set<String> pages = new TreeSet<String>();
        for (Page p : topCat.getArticles()) {
            pages.add(p.getTitle().getPlainTitle());
        }
        
        // Get the pages categorized under each subcategory of C
        for (Category childCategory : topCat.getDescendants()) {
            for (Page p : childCategory.getArticles()) {
                pages.add(p.getTitle().getPlainTitle());
            }
            System.out.println("Number of pages: " + pages.size());
        }
        
        // Output the pages
        for (String page : pages) {
            System.out.println(page);
        }

    }
}
