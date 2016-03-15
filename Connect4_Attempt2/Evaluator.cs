using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect4_Attempt2
{
    class Evaluator
    {
        public static double Board_Score(BoardManager boardmanager, int[,] board, int player_piece, bool ismyturn)
        {
            double score = 0;
            for (int y = 0; y < boardmanager.height; y++)
            {
                for (int x = 0; x < boardmanager.width; x++)
                {
                    //n^2 sucks, but at least this way it doesnt do any operations if the location is empty. I cant think of a way to get out of it, anyhow
                    if (board[y, x] != 0)
                    {
                        score += Recurse_Score(y, x, -1, 0, board, player_piece); //check up
                        score += Recurse_Score(y, x, 1, 0, board, player_piece); //check down

                        score += Recurse_Score(y, x, 0, 1, board, player_piece); //right
                        score += Recurse_Score(y, x, 0, -1, board, player_piece); //left

                        score += Recurse_Score(y, x, -1, -1, board, player_piece); //up and left
                        score += Recurse_Score(y, x, -1, 1, board, player_piece); //up and right
                        score += Recurse_Score(y, x, 1, -1, board, player_piece); //down and left
                        score += Recurse_Score(y, x, 1, 1, board, player_piece); //down and right
                    }
                }
            }
            return score;
        }

        private static double Recurse_Score(int row_pos, int col_pos, int y_dir, int x_dir, int[,] board, int piece)
        {
            // checks recursively values along a certain path, starting at the given position and incrementing the given amount x and y.
            //currently the only thing it does is check the next cell on the path and increase the score by 1 if it likes what it sees.

            double score = 0;

            if (row_pos + y_dir > board.GetLength(0) - 1 || col_pos + x_dir > board.GetLength(1) - 1) return 0; //if the next thing to be checking is out of bounds, return
            if (row_pos + y_dir < 0 || col_pos + x_dir < 0) return 0; //out of bounds in the other direction.
            if (row_pos > board.GetLength(0) - 1 || col_pos > board.GetLength(1) - 1) return 0; //if the initial position is out of bounds, return

            if (board[row_pos, col_pos] != piece) return 0;

            if (board[row_pos + y_dir, col_pos + x_dir] == piece) score += 1;

            else if (board[row_pos + y_dir, col_pos + x_dir] == 0)
            {
                score += 1;
                return score;
            }

            else
            {
                score = 0;
                return score;
            }

            return Recurse_Score(row_pos + y_dir, col_pos + x_dir, y_dir, x_dir, board, piece);
        }

    }
}

