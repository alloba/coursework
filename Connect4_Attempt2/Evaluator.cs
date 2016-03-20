using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect4_Attempt2
{
    class Evaluator
    {
        public static int Board_Score(BoardManager boardmanager, int[,] board, int player_piece)
        {
            int score = 0;

            for (int i = 0; i < boardmanager.width; i++)
            {
                int row_pos = 0;

                int board_height = board.GetLength(0);
                int board_width = board.GetLength(1);

                //find the first non-empty space in the column
                while (board[row_pos, i] == 0 && row_pos < board_height-1) row_pos += 1;
                //if the entire thing is empty, score for that row is 0
                if (board[row_pos, i] == 0) return 0;

                //otherwise, actually calculate the score
                else
                {
                    score += Recurse_Score(row_pos, i, -1, 0, board, player_piece, boardmanager.win_condition); //down
                    score += Recurse_Score(row_pos, i, 1, 0, board, player_piece, boardmanager.win_condition); //down
                    score += Recurse_Score(row_pos, i, 0, -1, board, player_piece, boardmanager.win_condition); //left
                    score += Recurse_Score(row_pos, i, 0, 1, board, player_piece, boardmanager.win_condition); //right
                    score += Recurse_Score(row_pos, i, -1, -1, board, player_piece, boardmanager.win_condition); //up and left
                    score += Recurse_Score(row_pos, i, -1, 1, board, player_piece, boardmanager.win_condition); //up and right
                    score += Recurse_Score(row_pos, i, 1, -1, board, player_piece, boardmanager.win_condition); //down and left
                    score += Recurse_Score(row_pos, i, 1, 1, board, player_piece, boardmanager.win_condition); //down and right
                }
            }
            return score;
        }

        //this name makes no sense, i just havent changed it over from a previous version yet.
        private static int Recurse_Score(int row_pos, int col_pos, int y_dir, int x_dir, int[,] board, int desired_piece, int winning_score)
        {
            int score = 0;
            int board_height = board.GetLength(0);
            int board_width = board.GetLength(1);

            int piece = board[row_pos, col_pos];
            //if the top piece isnt the desired piece, then you are done. return 0.
            if (board[row_pos, col_pos] != piece) return score;

            //while its still a connected line of pieces
            while(board[row_pos, col_pos] == piece)
            {
                //if increasing the value won't push things out of bounds. (checks is greater than board size and if less than 0
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

            //if a wall or enemy piece was hit in the previous loop, the current location val will not be 0. if that is the case, then check if there are enough pieces(score) to call it a win
            if(board[row_pos, col_pos] != 0)
            {
                if (score >= winning_score)
                {
                    if (piece != desired_piece) { if (Math.Abs(score - winning_score) < 2) return score + 4; } //meaning the other side is about to win, so really do this move.
                    else return score + 2;
                }
                //this is a very good thing, so add more score than usual i guess. dunno how much yet. 2 for now.

                else return 0; //if there arent enough pieces, then its a worthless configuration, so return 0 as score.
            }

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
            if (blank_spaces + score >= winning_score) return score;
            else return 0;


            //and now for copious testing.
        }

        public static int MiniMax(BoardManager boardmanager, Tree t, int player, int max_depth)
        {
            t.Generate_Branches(max_depth, player);

            Node n = t.root;
            Node max_node = n.children[0];

            foreach (Node child in n.children)
            {
                if (Maximum_Value(boardmanager, child, player, max_depth, 1) > Board_Score(boardmanager, max_node.board, player))
                {
                    max_node = child;
                }
            }
            
            return max_node.move_made;
            

        }

        private static int Min_Value(BoardManager boardmanager, Node node, int player, int max_depth, int current_depth)
        {
            if (node.children.Count() == 0) return Board_Score(boardmanager, node.board, player);
            if (current_depth >= max_depth) return Board_Score(boardmanager, node.board, player);

            int value = 10000;
            foreach(Node child in node.children)
            {
                int min_val = Maximum_Value(boardmanager, child, player, max_depth, current_depth + 1);
                if (min_val < value) value = min_val;
            }
            return value;
        }

        private static int Maximum_Value(BoardManager boardmanager, Node node, int player, int max_depth, int current_depth)
        {
            if (node.children.Count() == 0) return Board_Score(boardmanager, node.board, player);
            if (current_depth >= max_depth) return Board_Score(boardmanager, node.board, player);

            int value = -1000;
            foreach(Node child in node.children)
            {
                int max_val = Min_Value(boardmanager, child, player, max_depth, current_depth + 1);
                if (max_val > value) value = max_val;
            }
            return value;
        }
    }
}

