using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Connect4_Attempt2
{
    class GameManager
    {
        int width, height, win_condition, player_turn;
        Tree tree;
        BoardManager boardmanager;
        int current_turn;

        double time_to_compute;
        int borg_results;

        public int[] Get_Setup()
        {
            //all the pregame stuff. height and width of board, win conditions, what color the player wants to be
            Console.WriteLine("enter columns");
            Int32.TryParse(Console.ReadLine(), out width);

            Console.WriteLine("enter rows");
            Int32.TryParse(Console.ReadLine(), out height);

            Console.WriteLine("enter win condition");
            Int32.TryParse(Console.ReadLine(), out win_condition);

            Console.WriteLine("Are you red or blue? (Type 1/r for red, 2/b for blue)");
            string response = Console.ReadLine();
            if (response.Equals("r") || response.Equals("red") || response.Equals("1")) { player_turn = 1; }
            else player_turn = 2;

            Console.WriteLine("enter time to give the computer (in seconds)");
            Double.TryParse(Console.ReadLine(), out time_to_compute);
            time_to_compute *= 1000;

            Console.Clear();

            int[] parameters = new int[] { width, height, win_condition, player_turn }; // i kind of liked the idea of passing a single parameter instead of a bunch
            return parameters;
        }

        public void Run_Game(int[] game_parameters)
        {
            //handles the entire game. sets stuff up and then loops until its finished, then prints the end game message
            int width = game_parameters[0],
                height = game_parameters[1],
                win_condition = game_parameters[2],
                player_turn = game_parameters[3];

            

            boardmanager = new BoardManager(width, height, win_condition);
            tree = new Tree(boardmanager, new Node(boardmanager.Create_Blank_Board()));

            bool GameOn = true; 
            current_turn = 1; // the person who is currently making a move. this is used to record values on the board. 
            int most_recent_move = 1; //keeps track of the move that was played last. needed for checking if the game is over and whatever else needs it
            while (GameOn)
            {
                Console.Clear();

                Display_Board(tree.root.board);
                Console.WriteLine("Last Move Made: " + most_recent_move);
                if (player_turn == current_turn) //if its the player's turn, get the player's input
                {
                    //player code
                    //int player_move = Get_Player_Input();
                    //while (boardmanager.TestMove(player_move, tree.root.board) == false) //if the player doesnt give a valid move, keep asking.
                    //{
                    //    Console.Write("Not a Valid Move\n");
                    //    player_move = Get_Player_Input();
                    //}
                    //most_recent_move = player_move;


                    //computer v. computer code
                    Console.Write("\nBoop Beep Bop\n");

                    int seconds = DateTime.Now.Second;
                    borg_results = 1;
                    while (boardmanager.TestMove(borg_results, tree.root.board) == false) borg_results += 1;


                    bool move_made = false;



                    Thread t1 = new Thread(get_move);
                    Thread t3 = new Thread(get_move);
                    Thread t5 = new Thread(get_move);
                    Thread t7 = new Thread(get_move);
                    Thread t9 = new Thread(get_move);

                    t1.Start(2);
                    t3.Start(4);
                    t5.Start(6);
                    t7.Start(8);
                    t9.Start(10);
                    //get_move(2);
                    //tree.Generate_Branches(1,current_turn);
                    Thread.Sleep((int)time_to_compute);

                    t1.Abort();
                    t3.Abort();
                    t5.Abort();
                    t7.Abort();
                    t9.Abort();

                    if (boardmanager.TestMove(borg_results, tree.root.board) == false) borg_results = 1;
                    while (boardmanager.TestMove(borg_results, tree.root.board) == false) borg_results += 1;

                    most_recent_move = borg_results;


                }

                else // if it is the computer's turn, bust out alllllll the code. 
                {
                    //computer stuff
                    //assign the recommended move to "most_recent_move"
                    
                    Console.Write("\nBoop Beep Bop\n");

                    int seconds = DateTime.Now.Second;
                    borg_results = 1;
                    while (boardmanager.TestMove(borg_results, tree.root.board) == false) borg_results += 1;

                    bool move_made = false;
                    

                    
                    Thread t1 = new Thread(get_move);
                    Thread t3 = new Thread(get_move);
                    Thread t5 = new Thread(get_move);
                    Thread t7 = new Thread(get_move);
                    Thread t9 = new Thread(get_move);

                    t1.Start(2);
                    t3.Start(4);
                    t5.Start(6);
                    t7.Start(8);
                    t9.Start(10);
                    
                    Thread.Sleep((int)time_to_compute);
             
                    t1.Abort();
                    t3.Abort();
                    t5.Abort();
                    t7.Abort();
                    t9.Abort();
                    
                    if (boardmanager.TestMove(borg_results, tree.root.board) == false) borg_results =1;
                    while (boardmanager.TestMove(borg_results, tree.root.board) == false) borg_results += 1;

                    most_recent_move = borg_results;
                    //Thread.Sleep(8000);
                    //Create Trees
                    //Evaluate through minimax
                    //recommend a move
                }

                tree.root = new Node(boardmanager.PlayMove(most_recent_move, current_turn, tree.root.board)); //the root needs to be updated

                Console.Clear();
                Display_Board(tree.root.board);
                
                if (boardmanager.CheckWin(tree.root.board, most_recent_move))
                { //if someone wins the game
                    GameOn = false;
                    Console.Write("Player " + current_turn + " Wins.");
                }
                else if(boardmanager.CheckForPossibleMoves(tree.root.board) == false)
                { //no more moves means game over also
                    GameOn = false;
                    Console.Write("Its a tie.");
                }

                if (current_turn == 1) current_turn = 2; //swap turns
                else current_turn = 1;
            }
        }

        private int Get_Player_Input()
        {
            int player_move;
            Console.Write("Player, Enter Move: ");
            Int32.TryParse(Console.ReadLine(), out player_move);

            return player_move;
        }

        private void Display_Board(int[,] board)
        { //hopefully this gets replaced eventuall by a gui. we'll see.
            string output = " ";

            int height = board.GetLength(0);
            int width = board.GetLength(1);

            string topbit = " ";
            for (int i = 0; i < width; i++) topbit += (i + 1) + "|";
            topbit += "\n";

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
            output += " ";
            output += new string('═', width * 2) + "\n";

            output = output.Replace('1', 'R').Replace('2', 'B').Replace('0', ' ');

            

            output += "\n";

            Console.Write(topbit + output);
        }

        private void get_move(object depth)
        {
            Tree junk_tree = new Tree(boardmanager,new Node(boardmanager.Create_Blank_Board()));
            junk_tree.root.board = boardmanager.Copy_Board(tree.root.board);
            int move = 0;
            move = Evaluator.geteval(boardmanager, junk_tree, current_turn, Convert.ToInt32(depth),true);
            //move = Evaluator.MiniMax(boardmanager, junk_tree.root, current_turn, Convert.ToInt32(depth),true);
            //move = Evaluator.MiniMax(boardmanager, junk_tree, current_turn, Convert.ToInt32(depth)); //definitely dont go above 10 levels or so.
            borg_results = move;
            Console.Write("\nDid the thing:" + depth + " Move Recommended: " + move);
        }
    }
}

