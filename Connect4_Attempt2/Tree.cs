using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect4_Attempt2
{
    class Tree
    {
        public Node root;
        BoardManager boardmanager;

        public Tree(BoardManager manager, Node new_root)
        {
            root = new_root;
            boardmanager = manager;
        }

        public void Set_Root(Node n)
        {
            root = n;
        }

        public void Generate_Branches(int max_depth, int player_move)
        {
            Generate_Branches_Recurse(root, player_move, max_depth, 0);
        }

        void Generate_Branches_Recurse(Node n, int player_move, int max_depth, int current_depth)
        {
            if (current_depth > max_depth) { return; }

            for (int i = 1; i <= boardmanager.width; i++)
            {
                if (boardmanager.TestMove(i, n.board))
                {
                    n.Add_Child(new Node(boardmanager.PlayMove(i, player_move, n.board), i));
                }
            }
            if (player_move == 2) player_move = 1;
            else player_move = 2;
            foreach (Node child in n.children) Generate_Branches_Recurse(child, player_move, max_depth, current_depth + 1);
        }
    }


}
