//Alex Bates - Data Structures Fall 2014

/*
This class is responsible for the creation of, and interation with, a binary tree.
The binary tree is used in the process of translating between morse code sequences and letters.

Tree Structure: Starting from the head node, going left means a '.' (dot), while going right means a '-' (dash)
				So headNode->leftNode->leftNode->rightNode is equivilent to '..-'
				Letters are stored at appropriate nodes. The node in the above example stores "u"

Public Methods:
				Constructor:
							Takes a filepath pointing to a text file that will be used for the construction of the binary tree
				Destructor:
							Runs through the tree, deleting all nodes
				encode:	
							Takes the given string and outputs a string representing the morse code for the given input.
							Unrecognized characters are ignored. (supported characters: a-z, 0-9, [.], [,], [?], [-]) 
				decode:		
							Takes a string representing a morse code sequence and returns a string representing the decoded letters
							Output will be in the form of "letter letter letter ", regardless of initial formatting of the input
							*NOTE - There will always be a trailing whitespace character in the output

*/

#pragma once
using namespace std;

class morse_tree
{
public:
	~morse_tree();
	morse_tree(string filename);

	string encode(string inputLetters);
	string decode(string inputMorseCode);
private:
	void create_tree(string filename);
	
	struct Node
	{
		string Character;
		Node* leftNode;
		Node* rightNode;
		Node(string letter, Node* lNode, Node* rNode) : Character(letter), leftNode(lNode), rightNode(rNode){}
	};
	
	void generateLeaf(Node* location, string morseCode, string letter);
	string encode(Node* pos, string input, string output);
	string decode(Node* pos, string input, string* Character);

	void deleteTree(Node* pos);

	Node* headNode;


};

