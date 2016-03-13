using System.Collections.Generic;

namespace Connect4_Attempt2
{
    internal class Node
    {
        public int[,] board;
        public List<Node> children;

        public Node(int[,] given_board)
        {
            board = given_board;
            children = new List<Node>();
        }

        public void Add_Child(Node child)
        {
            children.Add(child);
        }
    }
}