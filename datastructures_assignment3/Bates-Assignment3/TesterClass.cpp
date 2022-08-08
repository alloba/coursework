//Alex Bates - Data Structures Fall 2014
//This class listens for user input and outputs strings based on returned values recieved from the morse_tree class.


#include <iostream>
#include <string>
#include <sstream>
#include "morse_tree.h"

using namespace std;


void test(morse_tree Tree)
{
	//Please forgive the horrible formatting of strings that is about to follow.
	//Hard to read, but it is correct.
	string encodeTest = Tree.encode("TEST test");
	string decodeTest = Tree.decode("- . ... - - . ... -");

	cout << "Expected encode output for 'TEST test':\n\t\t- . ... - - . ... -\n";
	cout << "Actual result:  " << encodeTest;
	if(encodeTest.compare("- . ... - - . ... -") == 0) cout << " MATCH\n";
	else cout << " NOT A MATCH\n";

	cout << "\n\n\n";

	cout << "Expected decode output for '- . ... - - . ... -:\n\t\tt e s t t e s t \n";
	cout << "Actual result:  " << decodeTest;
	if(decodeTest.compare("t e s t t e s t ") == 0) cout << " MATCH\n";
	else cout << "NOT A MATCH\n";

	cout << "\n";

	cout << "Tested\n\n";
}


int main(void)
{
	morse_tree MorseTree("morse_code.txt");
	string selection;
	int choice=0;
	string input;
	while(choice != 4)
	{
		cout << "Choose a number::\n1: Encode\n2: Decode\n3: Test\n4: Exit\n::";
		getline(cin, selection);
		istringstream ss(selection);
		ss >> choice;
		if(ss.fail()) choice = 0;
		
		if(choice == 1)
		{
			cout << "Enter string to be Encoded:\n";
			getline(cin, input);
			cout << MorseTree.encode(input) << "\n\n\n";
		}
		else if (choice == 2)
		{
			cout << "Enter string to be Decoded:\n";
			getline(cin, input);
			cout << MorseTree.decode(input)<< "\n\n\n";
		}
		else if (choice == 3) test(MorseTree);
		else if (choice == 4) break;

		else cout << "Not a Valid Selection"<< "\n\n\n";
	}
	
	
	
	system("pause");
}
