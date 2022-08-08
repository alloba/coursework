//Alex Bates - Data Structures Fall 2014
//Refer to "morse_tree.h" for a summary of this class

#include <string>
#include "morse_tree.h"
#include <fstream>
#include <iostream>
#include <algorithm>

using namespace std;


//Constructor that takes the filepath to the text file that stores the morse code information
morse_tree::morse_tree(string filename)
{
	headNode = nullptr;
	create_tree(filename);
}

//Takes characters and converts them to their morse code representation
string morse_tree::encode(string inputLetters)
{

	//Forces input to be lowercase letters. All functions assume lower case letters to work with.
	//The only reason i included <algorithm>
	transform(inputLetters.begin(), inputLetters.end(), inputLetters.begin(), tolower);

	string encodedString = "" ;

	//Loop through until the input letter are exhausted. Special attention is given to avoiding putting in more than a single space between anything
	while(inputLetters.compare("") != 0) 
	{
		if(inputLetters.at(0) == ' ') inputLetters = inputLetters.substr(1);
		encodedString += encode(headNode, inputLetters.substr(0,1), "");
		encodedString += " ";
		inputLetters = inputLetters.substr(1);
	}
	return encodedString.substr(0,encodedString.length()-1);
}

//Recurse though the tree. 
//The entire tree is searched for a matching character. If found, the series of dits and dahs taken to get there are stored in 'output'. else "" is returned.
string morse_tree::encode(Node* pos, string input, string output)
{
	if(pos == nullptr) {return "";}
	if(input.compare(pos->Character)==0) {return output;}
	
	return encode(pos->leftNode,input, output+".") + encode(pos->rightNode,input, output+"-");
}

//Follow the dits and dahs down the tree until you run out of them.
//If a code is entered that is invalid, the output says so.
string morse_tree::decode(string inputMorseCode)
{
	
	string workingInput = inputMorseCode;
	string storedVal = "";	//the final output
	string decodedVal ="" ; //a partial result. single letter
	string* holder = new string;

	while(workingInput.compare("") != 0)
	{
		//make sure decode returns a valid result before adding it to the output. (invalid results marked by a return of "")
		decodedVal = decode(headNode, workingInput.substr(0, workingInput.find(" ")), holder);
		if(decodedVal.compare("") ==0) {storedVal = "[[Not A Valid Sequence]] "; break;}
		else 
		{
			storedVal += decodedVal;
			storedVal += " ";
		}
		if(workingInput.find(" ") != string::npos) workingInput = workingInput.substr(workingInput.find(" ")+1);
		else workingInput = "";
	}
	
	delete holder;
	return storedVal;
}

//Go down the tree following dits and dahs until an end is hit or you run out of dits and dahs. 
//I had some trouble thinking of a better way to do this, so currently all instances of this function access the same pointer to update it
//The value in this pointer is then returned as a result. 
string morse_tree::decode(Node* pos, string input, string* Character)
{
	if(pos == nullptr) {return *Character = ""; return *Character;}
	if(input.compare("") == 0) {*Character = pos->Character; return *Character;}
	
	if(input.at(0) == '.') decode(pos->leftNode,input.substr(1), Character);
	else if(input.at(0) == '-') decode(pos->rightNode,input.substr(1), Character);
	return *Character;
}

//Read from a text file and create a tree based off the values within.
//Format of text file is assumed "lowercaseLetter[SPACE]morseCodeSequence[NEWLINE]"
void morse_tree::create_tree(string filename)
{
	headNode = new Node("", nullptr, nullptr);
	
	string line;
	ifstream myfile(filename);
	
	if(myfile.is_open())
	{
		string morseSubstring = "";
		while(getline(myfile, line))
		{
			morseSubstring = line.substr(2);
			generateLeaf(headNode, morseSubstring, line.substr(0,1));
		}
		myfile.close();
	}
	//invalid path 
	else cout << "File Not Found" << "\n";

}

void morse_tree::generateLeaf(Node* location, string morseCode, string letter)
{
	//what happens when spaghetti code recurses? These are the questions that keep me up at night.
					//i like to imagine maybe a hollow earth concept, but with pasta. makes no sense, buts what a lovely visual
	
	//This method worms its way down the given morseCode string, adding connections in the binary tree as it goes. 
	//Base case is that the morseCode string is empty. at that point the letter that sequence corresponds to is stored.

	if(location == nullptr) location = new Node("",nullptr,nullptr);
	if(location->leftNode == nullptr) location->leftNode = new Node("",nullptr,nullptr);
	if(location->rightNode == nullptr) location->rightNode = new Node("",nullptr,nullptr);

	if(morseCode.compare("")==0)
	{
		location->Character = letter;
		return;
	}

	if(morseCode.substr(0,1).compare("-")==0)  generateLeaf(location->rightNode,morseCode.substr(1),letter);
	if(morseCode.substr(0,1).compare(".")==0)  generateLeaf(location->leftNode,morseCode.substr(1),letter);
	return;
}

morse_tree::~morse_tree(void)
{
	deleteTree(headNode);
}

//Hopefully this goes through and deletes every single Node
void morse_tree::deleteTree(Node* pos)
{
	if(pos->leftNode != nullptr) deleteTree(pos->leftNode);
	if(pos->rightNode!= nullptr) deleteTree(pos->rightNode);
	pos = nullptr;
	delete pos;
}
