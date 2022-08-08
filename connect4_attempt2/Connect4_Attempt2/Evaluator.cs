using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Connect4_Attempt2
{
    class Evaluator
    {
        public static int Board_Score(BoardManager boardmanager, int[,] board, int player_piece)
        {
            int score = 0;


            //if putting a piece anywhere on the board would cause the other side to win, block it.
            int other_player;
            if (player_piece == 1) other_player = 2;
            else other_player = 1;

            //for (int i = 1; i <= boardmanager.width; i++)
            //{
            //    int[,] future_board = boardmanager.PlayMove(i, other_player, board);
            //    bool result = boardmanager.CheckWin(future_board, i);
            //    if (result)
            //    {
            //        return 5000;
            //    }

            //}

            //!!!these values should be 0 to < width. but in testing i got more interesting moves with this.
            for (int i = 1; i < boardmanager.width-1; i++)
            {
                int row_pos = 0;

                int board_height = board.GetLength(0);
                int board_width = board.GetLength(1);

                //find the first non-empty space in the column
                while (board[row_pos, i] == 0 && row_pos < board_height-1) row_pos += 1;

                score += Recurse_Score(row_pos, i, -1, 0, board, player_piece, boardmanager.win_condition); //up
                score += Recurse_Score(row_pos, i, 1, 0, board, player_piece, boardmanager.win_condition); //down
                score += Recurse_Score(row_pos, i, 0, -1, board, player_piece, boardmanager.win_condition); //left
                score += Recurse_Score(row_pos, i, 0, 1, board, player_piece, boardmanager.win_condition); //right
                score += Recurse_Score(row_pos, i, -1, -1, board, player_piece, boardmanager.win_condition); //up and left
                score += Recurse_Score(row_pos, i, -1, 1, board, player_piece, boardmanager.win_condition); //up and right
                score += Recurse_Score(row_pos, i, 1, -1, board, player_piece, boardmanager.win_condition); //down and left
                score += Recurse_Score(row_pos, i, 1, 1, board, player_piece, boardmanager.win_condition); //down and right
            }
            //Console.WriteLine(score);
            return score;
        }

        //this name makes no sense, i just havent changed it over from a previous version yet.
        private static int Recurse_Score(int row_pos, int col_pos, int y_dir, int x_dir, int[,] board, int desired_piece, int winning_score)
        {
            int score = 0;
            int board_height = board.GetLength(0);
            int board_width = board.GetLength(1);

            int piece = board[row_pos, col_pos];




            //while its still a connected line of pieces
            while(board[row_pos, col_pos] == piece)
            {
                //if increasing the value won't push things out of bounds. (checks if greater than board size and if less than 0
                if (row_pos + y_dir < board_height && col_pos + x_dir < board_width && col_pos + x_dir >=0 && row_pos + y_dir >=0)
                {
                    row_pos += y_dir;
                    col_pos += x_dir;
                }
                //if its hitting a wall, then force stop the loop
                else break;
            }

            //so now the row_pos and col_pos are all the way along the direction that is supposed to be being checked at the moment. 
            //from this point, go all the way back in the other direction, counting how many pieces you hit along the way until either a wall or a blank space is hit.

            while(board[row_pos,col_pos] == piece)
            {
                score += 1;
                //check if decreasing the value would put things out of bounds.
                if (row_pos - y_dir >= 0 && col_pos - x_dir >= 0  && row_pos - y_dir <board_height && (col_pos - x_dir < board_width))
                {
                    row_pos -= y_dir;
                    col_pos -= x_dir;
                }
                //if things get out of bounds, force stop the loop
                else break;
            }

            //if a wall or different piece was hit in the previous loop, the current location val will not be 0. if that is the case, then check if there are enough pieces(score) to call it a win
//
           

            if (board[row_pos, col_pos] != 0)
            {
                if (piece != desired_piece && Math.Abs(score - winning_score) < 2)
                {
                    return score + 20; 
                }

                if (score >= winning_score && piece == desired_piece)
                {
                    return score *0; //this is a very good thing, so add more score than usual i guess. dunno how much yet. 
                }
               

                else return 0; //if there arent enough pieces, then its a worthless configuration, so return 0 as score.
            }

            
            //!!--checking for if there are more related pieces on the other side of the blank space
          
            
            

            //at this point you need to be counting the amount of blank spaces that remain avaliable in whatever direction.
            int blank_spaces = 0;

            while (board[row_pos, col_pos] == 0)
            {
                blank_spaces += 1;
                //go backwards along the line as long as it isnt out of bounds
                if (row_pos - y_dir >= 0 && col_pos - x_dir >= 0   && row_pos - y_dir < board_height && col_pos - x_dir < board_width)
                {
                    row_pos -= y_dir;
                    col_pos -= x_dir;
                }
                else break;
            }

            //now the number of blank spaces can be combined with the number of pieces found in the line.
            //if there are enough for a win to be possible, return score. else return 0;
            if (blank_spaces + score >= winning_score) return score-5;
            else return 0;


            //and now for copious testing (pls).
        }


        public static int Score(BoardManager boardmanager, int[,] board, int player_piece)
        {
            int score = 0;
            int width = boardmanager.width;
            int height = boardmanager.height;

            int current_row = height-1;
            int current_column = 0;

            bool inBounds = true;

            while(inBounds)
            {
                if (current_row > height-1 || current_column > width-1) { inBounds = false; break; }

                if (board[current_row, current_column] == 0) current_row += 1;
                else
                {
                    score += CheckConnections(current_row, current_column, board, player_piece, boardmanager.win_condition);
                    if (current_row + 1 < height-1) current_row += 1;
                    else
                    {
                        if (current_column + 1 < width)
                        {
                            current_column += 1;
                            current_row = 0;
                        }
                        else inBounds = false;
                    }
                }
                if (current_row > height || current_column > width) { inBounds = false; break; }
            }

            return score;
        }

        public static int CheckConnections(int row_pos, int col_pos, int[,] board, int player, int win_condition)
        {
            int score = 0;


            int up = CheckDirection(row_pos, col_pos,-1, 0, board);
            if (up == -1) { }
            else if (up >= win_condition-1 && board[row_pos, col_pos] == player) score += 100;
            else if (up >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            int down = CheckDirection(row_pos, col_pos, 1, 0, board);
            if (down == -1) { }
            else if (down >= win_condition-1 && board[row_pos, col_pos] == player) score += 100;
            else if (down >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            int left = CheckDirection(row_pos, col_pos, 0, -1, board);
            if (left == -1) { }
            else if (left >= win_condition - 1 && board[row_pos, col_pos] == player) score += 100;
            else if (left >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            int right = CheckDirection(row_pos, col_pos, 0, 1, board);
            if (right == -1) { }
            else if (right >= win_condition - 1 && board[row_pos, col_pos] == player) score += 100;
            else if (right >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            int upleft = CheckDirection(row_pos, col_pos, -1, -1, board);
            if (upleft == -1) { }
            else if (upleft >= win_condition - 1 && board[row_pos, col_pos] == player) score += 100;
            else if (upleft >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            int upright = CheckDirection(row_pos, col_pos, -1, 1, board);
            if (upright == -1) { }
            else if (upright >= win_condition - 1 && board[row_pos, col_pos] == player) score += 100;
            else if (upright >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            int downleft = CheckDirection(row_pos, col_pos, 1, -1, board);
            if (downleft == -1) { }
            else if (downleft >= win_condition - 1 && board[row_pos, col_pos] == player) score += 100;
            else if (downleft >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            int downright = CheckDirection(row_pos, col_pos, 1, 1, board);
            if (downright == -1) { }
            else if (downright >= win_condition - 1 && board[row_pos, col_pos] == player) score += 100;
            else if (downright >= win_condition - 1 && board[row_pos, col_pos] != player) score += 200;
            else score -= 100;

            return score;
        }

        public static int CheckDirection(int row_pos, int col_pos, int y, int x, int[,] board)
        {
            int pieces = 0;
            int height = board.GetLength(0);
            int width = board.GetLength(1);

            int initial_piece = board[row_pos, col_pos];

            while(row_pos < height && row_pos >= 0 && col_pos < width && col_pos >= 0)
            {
                if (board[row_pos, col_pos] == initial_piece)
                {
                    pieces += 1;
                    row_pos += y; col_pos += x;
                }
                else if (board[row_pos, col_pos] == 0) return pieces;
                else return -1;
            }
            return -1;
        }

        public static int geteval(BoardManager boardmanager, Tree t, int player, int depth, bool maximizing_player)
        {

            //bool isempty = true;
            //for (int i = 0; i < boardmanager.height; i++)
            //{
            //    for (int j = 0; j < boardmanager.width; j++)
            //    {
            //        if (t.root.board[i, j] != 0) { isempty = false; break; }
            //    }
            //}
            //if (isempty) return 1;


            int notplayer;
            if (player == 1) notplayer = 2;
            else notplayer = 1;
            for(int i = 0; i < boardmanager.width; i ++)
            {
                int[,] testboard = boardmanager.PlayMove(i + 1, notplayer, t.root.board);

                bool empty = true;
                int row = 0;
                while (testboard[row, i] == 0)
                {   if (row + 1 < boardmanager.height) row += 1;
                    else break;
                }
                if (testboard[row, i] != 0) empty = false;


                if (!empty && boardmanager.CheckWin(testboard, i + 1) && boardmanager.TestMove(i + 1, t.root.board)) return i + 1;
                else { }
                
                    
            }
            


            t.Generate_Branches(depth,player);
            Node n = t.root;
            int bestscore = n.children[0].score;
            Node bestnode = n.children[0];

            foreach(Node child in n.children)
            {
                int val = MiniMax(boardmanager, child, player, depth, true);
               
                if (val >= bestscore) bestnode = child;
            }


            if (bestnode.move_made == boardmanager.width || bestnode.move_made == 1)
            {
                Random r = new Random();
                return r.Next(1, boardmanager.width + 1);
            }
            else
            {
                return bestnode.move_made;
            }
        }

        public static int MiniMax(BoardManager boardmanager, Node n, int player, int depth, bool maximizing_player)
        {
            if (depth == 0 || n.children.Count() == 0) {return Board_Score(boardmanager, n.board, player); }

            if (maximizing_player)
            {
                n.score = -10000;
                foreach (Node child in n.children)
                {
                    int val = MiniMax(boardmanager, child, player, depth - 1, false);
                    if (val > n.score) n.score = val;
                }
                return n.score;
            }
            else
            {
                n.score = 100000;
                foreach (Node child in n.children)
                {
                    int val = MiniMax(boardmanager, child, player, depth - 1, true);
                    if (val < n.score) n.score = val;
                }
                return n.score;
            }
        }

        //public static int MiniMax(BoardManager boardmanager, Tree t, int player, int max_depth)
        //{
        //    t.Generate_Branches(max_depth, player);

        //    Node n = t.root;
        //    Node max_node = n.children[0];

        //    foreach (Node child in n.children)
        //    {
        //        int val = Maximum_Value(boardmanager, child, player, max_depth, 0);
        //        if (val > max_node.score) max_node = child;
        //        Console.WriteLine(child.score);
        //    }
            
        //    return max_node.move_made;
            

        //}

        //private static int Min_Value(BoardManager boardmanager, Node node, int player, int max_depth, int current_depth)
        //{
        //    //if (node.children.Count() == 0) { return node.score; }

        //    if (current_depth == max_depth) { return node.score; }

        //    //int value = 100000;
        //    node.score = -100000;
        //    foreach(Node child in node.children)
        //    {
        //        int min_val = Maximum_Value(boardmanager, child, player, max_depth, current_depth + 1);
        //        Console.WriteLine("::" + min_val);
        //        if (min_val > child.score) node.score = min_val;
        //    }
        //    return node.score;
        //}

        //private static int Maximum_Value(BoardManager boardmanager, Node node, int player, int max_depth, int current_depth)
        //{
        //    //if (node.children.Count() == 0) { node.score = Board_Score(boardmanager, node.board, player); return node.score; }
        //    if (current_depth == max_depth) {return node.score; }

        //    node.score = -100000;
        //    foreach(Node child in node.children)
        //    {
        //        int max_val = Min_Value(boardmanager, child, player, max_depth, current_depth + 1);
        //        Console.WriteLine("::" + max_val);
        //        if (max_val < child.score) node.score = max_val;
        //    }
        //    return node.score;
        //}
    }
}

