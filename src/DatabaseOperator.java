
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
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

public class DatabaseOperator {

    public ArrayList<String> wordArray = new ArrayList<>();
    String fileLocation;

    public DatabaseOperator(String FileLocation) throws IOException {
        //Upon creation, load up the given text file and enter in all the words to an array.

        this.fileLocation = FileLocation;

        File file = new File(this.fileLocation);
        if (!file.exists()) {
            file.createNewFile();
        }

        //
        BufferedReader fileRead = new BufferedReader(new FileReader(file));

        //While the next line being read isn't null (EoF), add it to the arrayList
        String endFileChecker;
        endFileChecker = fileRead.readLine();

        while (endFileChecker != null) {
            wordArray.add(endFileChecker);
            endFileChecker = fileRead.readLine();
        }
        fileRead.close();
    }

    public void Save() throws IOException {
        //save the arrayList to the file specified at class instantiation
        File file = new File(this.fileLocation);

        FileWriter fw = new FileWriter(file.getAbsoluteFile());

        try (BufferedWriter bw = new BufferedWriter(fw)) {
            for (String x : this.wordArray) {
                bw.write(x);
            }
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

    public String SelectWord(String weekDay) {
        //Take the first letter of the given string, and create a sublist of words starting with that letter.

        String workingLetter = weekDay.substring(0, 0).toLowerCase();
        ArrayList<String> workingList = new ArrayList<>();

        workingList.addAll(this.wordArray);

        for (String x : workingList) {
            //check each item in word list. if it isnt starting with the right letter, junk it.
            if (!x.toLowerCase().startsWith(workingLetter)) {
                workingList.remove(x);
            }
        }

        int endIndex = workingList.size() - 1;
        //randomly get one of the elements in the list and return it for use.
        Random r;
        r = new Random();
        return workingList.get(r.nextInt(endIndex));
    }
}
