using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect4_Attempt2
{
    class GameManager
    {
        int width, height, win_condition, player_turn;
        Tree tree;

        public int[] Get_Setup()
        {
            //all the pregame stuff. height and width of board, win conditions, what color the player wants to be
            Console.WriteLine("enter columns");
            Int32.TryParse(Console.ReadLine(), out width);

            Console.WriteLine("enter rows");
            Int32.TryParse(Console.ReadLine(), out height);

            Console.WriteLine("enter win condition");
            Int32.TryParse(Console.ReadLine(), out win_condition);

            Console.WriteLine("Which color would you like to be? red or blue (r/b)? Red Goes first, blue goes second.");
            string response = Console.ReadLine();
            if (response.Equals("r") || response.Equals("red") || response.Equals("1")) { player_turn = 1; }
            else player_turn = 2;

            int[] parameters = new int[] { width, height, win_condition, player_turn }; // i kind of liked the idea of passing a single parameter instead of a bunch
            return parameters;
        }

        public void Run_Game(int[] game_parameters)
        {
            //handles the entire game. sets stuff up and then loops until its finished, then prints the end game message.
            int width = game_parameters[0],
                height = game_parameters[1],
                win_condition = game_parameters[2],
                player_turn = game_parameters[3];

            BoardManager boardmanager = new BoardManager(width, height, win_condition);
            tree = new Tree(boardmanager, new Node(boardmanager.Create_Blank_Board()));

            bool GameOn = true; 
            int current_turn = 1; // the person who is currently making a move. this is used to record values on the board. 
            int most_recent_move = 1; //keeps track of the move that was played last. needed for checking if the game is over and whatever else needs it
            while (GameOn)
            {
                Display_Board(tree.root.board);
                if (player_turn == current_turn) //if its the player's turn, get the player's input
                {
                    int player_move = Get_Player_Input();
                    while (boardmanager.TestMove(player_move, tree.root.board) == false) //if the player doesnt give a valid move, keep asking.
                    {
                        Console.WriteLine("Not a Valid Move");
                        player_move = Get_Player_Input();
                    }
                    most_recent_move = player_move;
                }
                else // if it is the computer's turn, bust out alllllll the code. 
                {
                    //computer stuff
                    //assign the recommended move to "most_recent_move"
                    //until this happens, its just going to submit whatever the player did last, since the most_recent_move isn't updated.
                    Console.WriteLine("Boop Beep Bop");

                    //tree.Generate_Branches(2, current_turn);
                    //Display_Board(tree.root.board);
                    Console.WriteLine(Evaluator.Board_Score(boardmanager, tree.root.board, current_turn, true));

                    //Create Trees
                    //Evaluate through minimax
                    //recommend a move
                }

                tree.root = new Node(boardmanager.PlayMove(most_recent_move, current_turn, tree.root.board)); //the root is no longer needed, reassign to the new board.
                Display_Board(tree.root.board);
                
                if (boardmanager.CheckWin(tree.root.board, most_recent_move))
                { //if someone wins the game
                    GameOn = false;
                    Console.WriteLine("Player " + current_turn + " Wins.");
                }
                else if(boardmanager.CheckForPossibleMoves(tree.root.board) == false)
                { //no more moves means game over also
                    GameOn = false;
                    Console.WriteLine("Its a tie.");
                }

                if (current_turn == 1) current_turn = 2; //swap turns
                else current_turn = 1;
            }
        }

        private int Get_Player_Input()
        {
            int player_move;
            Console.WriteLine("Enter Move");
            Int32.TryParse(Console.ReadLine(), out player_move);

            return player_move;
        }

        private void Display_Board(int[,] board)
        { //hopefully this gets replaced eventuall by a gui. we'll see.
            string output = "";

            int height = board.GetLength(0);
            int width = board.GetLength(1);

            output += new string('═', width * 2) + "\n";

            for (int row = 0; row < height; row++)
            {
                output += "|";
                for (int col = 0; col < width; col++)
                {
                    output += board[row, col].ToString() + " ";
                }
                output += "|\n";
            }
            output += new string('═', width * 2) + "\n";

            output = output.Replace('1', 'r').Replace('2', 'b');

            Console.WriteLine(output);
        }
    }
}

