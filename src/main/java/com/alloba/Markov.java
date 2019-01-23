package com.alloba;

import java.io.Serializable;
import java.util.*;
public class Markov implements Serializable {

    HashMap<String, List<MarkovInternalEntity>> markovChain = new HashMap<>();

    public void generate(List<String> wordlist) {
        System.out.println("Beginning Markov Chain Generation");
        System.out.println("Total Lines: " + wordlist.size());
        for(int i = 0; i < wordlist.size() - 1; i++){
            if(i%1000 == 0){
                System.out.println("Currently Processed [" + i + "] Words out of [" + wordlist.size() + "]");
            }
            addToMarkov(wordlist.get(i), wordlist.get(i+1));
        }
    }

    void addToMarkov(String word1, String word2){
        List<MarkovInternalEntity> workingMarkofEntityList = new ArrayList<>();
        if(markovChain.containsKey(word1))
            workingMarkofEntityList = markovChain.get(word1);

        if(workingMarkofEntityList.contains(new MarkovInternalEntity(word2))){
            workingMarkofEntityList.get(workingMarkofEntityList.indexOf(new MarkovInternalEntity(word2))).occurances += 1;
        }
        else{
            MarkovInternalEntity e = new MarkovInternalEntity(word2);
            e.occurances = 1;
            workingMarkofEntityList.add(e);
            markovChain.put(word1, workingMarkofEntityList);
        }

        rebalanceMarkovInternalEntityList(workingMarkofEntityList);
    }

    void rebalanceMarkovInternalEntityList(List<MarkovInternalEntity> workingMarkovEntityList){
        final int totalContainedOccurances = workingMarkovEntityList.stream().mapToInt(e -> e.occurances).sum();
        workingMarkovEntityList.forEach(e -> e.probability = ((double)e.occurances) / totalContainedOccurances);
    }

    public String pullSingleWord(String startingWord) {
        if(! markovChain.keySet().contains(startingWord)){
            throw new RuntimeException("That word does not exist in this markov chain");
        }

        List<MarkovInternalEntity> workingSet = markovChain.get(startingWord);
        int currentItem = 0;
        while(true){
            if(currentItem >= workingSet.size())
                currentItem = 0;

            if(Math.random() <= workingSet.get(currentItem).probability)
                return workingSet.get(currentItem).word;

            currentItem ++;
        }
    }

    public String pullSingleWord() {
        //only get something with a capital letter at the start.
        Object[] keySet = markovChain.keySet().toArray();
        Object[] properKeySet = Arrays.stream(keySet)
                .filter(item -> !item.equals(""))
                .filter(word -> Character.isUpperCase(((String)word).charAt(0)))
                .toArray();
        int randKey = new Random().nextInt(properKeySet.length);
        return (String) properKeySet[randKey];
    }



}
