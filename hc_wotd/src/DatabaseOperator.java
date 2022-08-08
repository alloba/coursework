
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
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
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

public class DatabaseOperator {

    public ArrayList<String> wordArray = new ArrayList<>();
    String fileLocation;

    File pathFile;

    public DatabaseOperator(String FileLocation) throws IOException {
        //Upon creation, load up the given text file and enter in all the words to an array.

        this.fileLocation = FileLocation;

        System.out.println(new File(DatabaseOperator.class.getProtectionDomain().getCodeSource().getLocation().getPath() + FileLocation));
        File file = new File(DatabaseOperator.class.getProtectionDomain().getCodeSource().getLocation().getPath() + FileLocation);
        this.pathFile = file;

        if (!file.exists()) {
            file.createNewFile();
        }

        //
        BufferedReader fileRead = new BufferedReader(new FileReader(file));

        //While the next line being read isn't null (EoF), add it to the arrayList
        String endFileChecker;
        endFileChecker = fileRead.readLine();

        while (endFileChecker != null) {
            this.wordArray.add(endFileChecker);
            endFileChecker = fileRead.readLine();
        }
        fileRead.close();
    }

    public void Save() {
        //save the arrayList to the file specified at class instantiation

        FileWriter fw = null;
        try {
            fw = new FileWriter(this.pathFile);
        } catch (IOException ex) {
            Logger.getLogger(DatabaseOperator.class.getName()).log(Level.SEVERE, null, ex);
        }

        try (BufferedWriter bw = new BufferedWriter(fw)) {
            for (String x : this.wordArray) {
                bw.write(x);
                bw.write("\r");
            }
        } catch (IOException ex) {
            Logger.getLogger(DatabaseOperator.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public void AlpabetizeList(ArrayList<String> WordList) {
        java.util.Collections.sort(WordList);
    }

    public void AddWords(ArrayList<String> wordList) {
        //add words from the list, if they do not already exist in the list
        //then sort the list.

        for (String x : wordList) {
            if (!this.wordArray.contains(x)) {
                this.wordArray.add(x);
            }
        }
        AlpabetizeList(this.wordArray);
    }

    public String SelectWord(String startingLetters) {
        //Take the first letter of the given string, and create a sublist of words starting with that letter.

        // String workingLetter = startingLetters.substring(0, 1).toLowerCase();
        ArrayList<String> workingList = new ArrayList<>();

        for (String x : this.wordArray) {
            // check every word. if it starts with the right letter, add it to the list.
            if (x.startsWith(startingLetters)) {
                workingList.add(x);
            }
        }

        //randomly get one of the elements in the list and return it for use.
        Random r = new Random();
        int endIndex = workingList.size();

        if (workingList.size() > 0) {
            return workingList.get(r.nextInt(endIndex));
        } else {
            return "No Word Found";
        }
    }
}
