using Distillery.ManagementSystem;
using Distillery.ManagementSystem.Domain;
using Distillery.ManagementSystem.Domain.Processes;
using System.Net.Http.Headers;

static void PrintWelcome()
{
    Console.WriteLine("\n************************************************************");
    Console.WriteLine("*** COPPERMUSE DISTILLERY'S PRODUCTION MANAGEMENT SYSTEM ***");
    Console.WriteLine("************************************************************");

    Console.WriteLine("\nPress enter to log in.");

    Console.ReadLine();
}

PrintWelcome();

Utilities.ShowMainMenu();
