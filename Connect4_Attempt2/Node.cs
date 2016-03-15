using System.Collections.Generic;

namespace Connect4_Attempt2
{
    internal class Node
    {
        public int[,] board;
        public int move_made;
        public List<Node> children;

        public Node(int[,] given_board, int move=-1)
        {
            board = given_board;
            children = new List<Node>();
            move_made = move;
        }

        public void Add_Child(Node child)
        {
            children.Add(child);
        }
    }
}