package com.alloba;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

/**
 * Hello world!
 */
public class App {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        System.out.println("Hello World!");

        String inputPath = "C:\\Projects\\MarkovProject\\src\\main\\resources\\2000Leagues.txt";
        String outputPath = "C:\\Projects\\MarkovProject\\src\\main\\resources\\dumpOut.ser";


        generateMarkov(inputPath, outputPath);


        Markov m = loadMarkov("C:\\Projects\\MarkovProject\\src\\main\\resources\\dumpOut.ser");
        String currentWord = m.pullSingleWord();
        for (int i = 0; i < 300; i++) {
            currentWord = m.pullSingleWord(currentWord);
            System.out.print(currentWord + " ");

            if(currentWord.contains(".") || currentWord.contains("!")|| currentWord.contains("?")) {
//                System.out.println("AAAAAAAAAAAAAAAAAAAAAAAAA: " + currentWord + ":::::::::::");
                System.out.print("\n");
            }
        }
    }

    public static void generateMarkov(String filenameInputPath, String filenameOutputPath) throws IOException {
        Markov m = new Markov();
        String inputText = new String(Files.readAllBytes(Paths.get(filenameInputPath)));
        String filteredInputText = inputText.replaceAll("\n", " ");
        List<String> filteredList = Arrays.asList(filteredInputText.split(" "));
        filteredList.replaceAll(x -> {
            if(x.equals(" "))
                return "";
            else
                return x;
        });

        m.generate(filteredList);


        ObjectOutputStream writer = new ObjectOutputStream(new FileOutputStream(filenameOutputPath));
        writer.writeObject(m);
        writer.close();
    }

    public static Markov loadMarkov(String inputPath) throws IOException, ClassNotFoundException {
        Markov m = (Markov) new ObjectInputStream(new FileInputStream(inputPath)).readObject();
        return m;
    }
}
