package com.alloba;

import java.io.Serializable;

class MarkovInternalEntity implements Serializable{
    String word;
    int occurances;
    double probability;

    public MarkovInternalEntity(){ }

    public MarkovInternalEntity(String word){
        this.word = word;
    }

    public boolean equals(Object o){
        if(! (o instanceof MarkovInternalEntity))
            return false;

        return this.word.equals(((MarkovInternalEntity) o).word);
    }
}