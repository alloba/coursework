package com.alloba;

import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;

import static org.junit.Assert.*;

public class MarkovTest {
    @Test
    public void generate() throws Exception {
        ArrayList<String> words = new ArrayList<>();
        words.addAll(Arrays.asList("this is quite the sentence the here that i the am typing and the making long for no reason".split(" ")));

        Markov m = new Markov();
        m.generate(words);
        System.out.println(m);
    }

    @Test
    public void addToMarkov() throws Exception {
        MarkovInternalEntity e1 = new MarkovInternalEntity("testWord");
        Markov m = new Markov();
        m.addToMarkov("test1", "test2");
        m.addToMarkov("test1", "test2");
        m.addToMarkov("test1", "test2");


        m.addToMarkov("test1", "test3");


        m.addToMarkov("test2", "test2");
        m.addToMarkov("test2", "test2");
        m.addToMarkov("test2", "test6");
        System.out.println(m.markovChain);
    }

    @Test
    public void rebalanceMarkovInternalEntityList() throws Exception {
        MarkovInternalEntity e1 = new MarkovInternalEntity("testWord");
        Markov m = new Markov();

    }

    @Test
    public void pullSingleWord() throws Exception {
    }

}