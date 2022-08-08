using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect4_Attempt2
{
    class Program
    {
        static void Main(string[] args)
        {
            GameManager manager = new GameManager();
            manager.Run_Game(manager.Get_Setup());
            //Run_Game(Get_Setup());
            Console.WriteLine("Press Any Key to Exit");
            Console.ReadKey();
        }
    }
}
