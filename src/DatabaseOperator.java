
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author alexl_000
 */
import java.nio.file.*;
import java.util.logging.Level;
import java.util.logging.Logger;
import sun.dc.pr.PRException;

public class DatabaseOperator {

    public ArrayList<String> wordArray = new ArrayList<String>();

    public DatabaseOperator(String FileLocation) throws IOException {
        //Upon creation, load up the given text file and enter in all the words to an array.

        BufferedReader fileRead = null;

        try {
            fileRead = new BufferedReader(new FileReader(FileLocation));
        } catch (FileNotFoundException ex) {
            System.err.print("FileNotFound");
        }
        //
        //While the next line being read isn't null (EoF), add it to the arrayList
        String endFileChecker;
        endFileChecker = fileRead.readLine();

        while (endFileChecker != null) {
            wordArray.add(endFileChecker);
            endFileChecker = fileRead.readLine();
        }
    }

    public void AlpabetizeList(ArrayList<String> WordList) {
        java.util.Collections.sort(WordList);
    }

    public void AddWords(ArrayList<String> wordList) {
        this.wordArray.addAll(wordList);
        AlpabetizeList(this.wordArray);
    }
}
