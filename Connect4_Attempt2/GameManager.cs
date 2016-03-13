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

            int[] parameters = new int[] { width, height, win_condition, player_turn };
            return parameters;
        }

        public void Run_Game(int[] game_parameters)
        {
            int width = game_parameters[0],
                height = game_parameters[1],
                win_condition = game_parameters[2],
                player_turn = game_parameters[3];

            BoardManager boardmanager = new BoardManager(width, height, win_condition);
            tree = new Tree(boardmanager, new Node(boardmanager.Create_Blank_Board()));

            bool GameOn = true;
            int current_turn = 1;
            int most_recent_move = 1;
            while (GameOn)
            {
                Display_Board(tree.root.board);
                if (player_turn == current_turn)
                {
                    int player_move = Get_Player_Input();
                    while (boardmanager.TestMove(player_move, tree.root.board) == false)
                    {
                        Console.WriteLine("Not a Valid Move");
                        player_move = Get_Player_Input();
                    }
                    most_recent_move = player_move;
                }
                else
                {
                    //computer stuff
                    //assign the recommended move to "most_recent_move"
                    //until this happens, its just going to submit whatever the player did last, since the most_recent_move isn't updated.
                    Console.WriteLine("Boop Beep Bop");
                    
                    //Create Trees
                    //Evaluate through minimax
                    //recommend a move
                }

                tree.root.board = boardmanager.PlayMove(most_recent_move, current_turn, tree.root.board);
                
                if (boardmanager.CheckWin(tree.root.board, most_recent_move))
                {
                    GameOn = false;
                    Console.WriteLine("Player " + current_turn + " Wins.");
                }
                if(boardmanager.CheckForPossibleMoves(tree.root.board) == false)
                {
                    GameOn = false;
                    Console.WriteLine("Its a tie.");
                }

                if (current_turn == 1) current_turn = 2;
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
        {
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

