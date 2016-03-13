using System;

namespace Connect4_Attempt2
{
    internal class BoardManager
    {
        private int height;
        private int width;
        private int win_condition;

        public BoardManager(int width, int height, int win_condition)
        {
            this.width = width;
            this.height = height;
            this.win_condition = win_condition;
        }

        internal int[,] Create_Blank_Board()
        {
            int[,] new_board = new int[height, width];
            for (int i = 0; i < height; i++)
            {
                for (int j = 0; j < width; j++)
                {
                    new_board[i, j] = 0;
                }
            }
            return new_board;
        }

        internal bool TestMove(int player_move, int[,] board)
        {
            if (player_move > width || player_move < 1) return false;
            if (board[0, player_move - 1] == 0) return true;
            else return false;
        }

        internal int[,] PlayMove(int move, int player, int[,] board)
        {
            move = move - 1;
            if (board[0, move] != 0)
            {
                return board; //edge case where column full
            }

            for (int i = 1; i < height; i++)
            {
                if (board[i, move] != 0)
                {
                    board[i - 1, move] = player;
                    return board;
                }
            }
            board[height - 1, move] = player; // if no pieces are in the column
            return board;
        }

        internal bool CheckWin(int[,] board, int most_recent_move)
        {
            int column = most_recent_move - 1;
            int row = 0;
            while (board[row, column] == 0) row += 1; //scrolls down until it finds where the most recently placed piece actually winded up
            int piece = board[row, column]; //assumes that whatever was found there is what we are checking for (no reason it shouldnt be)

            int consecutive_pieces = 0;
            //check horizontal

            for (int c = column - win_condition; c < column + win_condition; c++)
            {
                try
                {
                    if (board[row, c] == piece) consecutive_pieces += 1;
                    else consecutive_pieces = 0;
                    if (consecutive_pieces == win_condition) return true;
                }
                catch (Exception)
                { consecutive_pieces = 0; }
            }

            //check vertical
            consecutive_pieces = 0;

            for (int r = row - win_condition; r < row + win_condition; r++)
            {
                try
                {
                    if (board[r, column] == piece) consecutive_pieces += 1;
                    else consecutive_pieces = 0;
                    if (consecutive_pieces == win_condition) return true;
                }
                catch (Exception)
                { consecutive_pieces = 0; }
            }

            //check diagonal. top left to down right first, top right to down left second
            int consecutive_right = 0;
            int consecutive_left = 0;
            for (int i = -win_condition; i < win_condition; i++)
            {
                try
                {
                    if (board[row + i, column + i] == piece) consecutive_left += 1;
                    else consecutive_left = 0;
                    if (consecutive_left == win_condition) return true;
                }
                catch (Exception)
                { consecutive_left = 0; }

                try
                {
                    if (board[row + i, column - i] == piece) consecutive_right += 1;
                    else consecutive_right = 0;
                    if (consecutive_right == win_condition) return true;
                }
                catch (Exception)
                { consecutive_right = 0; }
            }

            return false; //no winning configurations found around the given coordinates for this piece
        }

        internal bool CheckForPossibleMoves(int[,] board)
        {
            for(int i = 0; i < width; i ++)
            {
                if (board[0, i] == 0)  return true;
            }
            return false;
        }
    }
}