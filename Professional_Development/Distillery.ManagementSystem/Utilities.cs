using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using Distillery.ManagementSystem.Domain;
using Distillery.ManagementSystem.Domain.Processes;
using Distillery.ManagementSystem.Domain.ProcessManagement;
using Distillery.ManagementSystem.Domain.Sales;

namespace Distillery.ManagementSystem
{
    internal class Utilities
    {
        private static void ListRuns()
        {
            var sql_DB = SQL_DB.Instance;

            foreach (var run in sql_DB.TableProductionRuns) 
            {
                Console.WriteLine();
                Console.WriteLine(run.Value.DisplayDetails(run.Key));
            }
        }

        private static void ListProducts()
        {
            var sql_DB = SQL_DB.Instance;

            foreach (var product in sql_DB.TableProductStock)
            {
                Console.WriteLine();
                Console.WriteLine(product.Value.DisplayDetails(product.Key));
            }
        }

        private static void ListInvoices()
        {
            var sql_DB = SQL_DB.Instance;

            foreach (var invoice in sql_DB.TableInvoices)
            {
                Console.WriteLine();
                Console.WriteLine(invoice.Value.DisplayDetails(invoice.Key));
            }
        }

        private static void CreateNewProductionRun()
        {
            ProductionRunManager productionRunManager = new();
            var sql_DB = SQL_DB.Instance;

            ProductionRun output = productionRunManager.CreateNew();
            sql_DB.AddEntry(output);

            ManageProductionRuns();
        }

        private static void CloseOutProductionRun()
        {
            ProductionRunManager productionRunManager = new();
            var sql_DB = SQL_DB.Instance;

            var output = productionRunManager.CloseOut();
            sql_DB.UpdateEntry(output.Item1, output.Item2);

            ManageProductionRuns();
        }

        private static void CreateNewInvoice() 
        {
            InvoiceManager invoiceManager = new();
            var sql_DB = SQL_DB.Instance;

            Invoice output = invoiceManager.CreateNew();
            sql_DB.AddEntry(output);

            ManageInvoices();
        }

        internal static void ShowMainMenu()
        {
            Console.Clear();
            Console.WriteLine("********************");
            Console.WriteLine("* Select an option *");
            Console.WriteLine("********************");

            Console.WriteLine("1: View Product Inventory");
            Console.WriteLine("2: Manage Production Runs");
            Console.WriteLine("3: **Manage Subprocess**");
            Console.WriteLine("4: Manage Invoices");
            Console.WriteLine("0: Close application");

            Console.Write("Your selection: ");

            string? userSelection = Console.ReadLine();
            switch (userSelection)
            {
                case "1":
                    // gives the current products in stock
                    ListProducts();

                    Console.WriteLine("\nPress any key to return to the Main Menu.");
                    Console.ReadKey();
                    Console.Clear();
                    ShowMainMenu();
                    break;
                case "2":
                    // brings the user to the Production Run Management menu
                    ManageProductionRuns();
                    break;
                case "3":
                    Console.WriteLine("\nUNDER CONSTRUCTION: Come back later! Press any key to return to the Main Menu.");
                    Console.ReadKey();
                    Console.Clear();
                    ShowMainMenu();
                    break;
                case "4":
                    // brings the user to the Invoice Management menu
                    ManageInvoices();
                    break;
                case "0":
                    break;
                default:
                    Console.WriteLine("\nInvalid input. Press any key to return to try again.");
                    Console.ReadKey();
                    Console.Clear();
                    ShowMainMenu();
                    break;
            }
        }

        internal static void ManageProductionRuns()
        {
            string? userSelection;

            Console.Clear();
            Console.WriteLine("*****************************");
            Console.WriteLine("* Production Run Management *");
            Console.WriteLine("*****************************");

            Console.WriteLine("1: List Production Runs");
            Console.WriteLine("2: Create New");
            Console.WriteLine("3: Close Out");
            Console.WriteLine("4: **Edit Existing**");
            Console.WriteLine("5: **Add Notes**");
            Console.WriteLine("0: Back to Main Menu");

            Console.Write("Your selection: ");

            userSelection = Console.ReadLine();
            switch (userSelection)
            {
                case "1":
                    // lists all Production Runs, both open and closed
                    ListRuns();

                    Console.WriteLine("\nPress any key to return to the Production Run Management.");
                    Console.ReadKey();
                    Console.Clear();
                    ManageProductionRuns();
                    break;
                case "2":
                    /*allows the user to start a new Production Run (PR). 
                    Steps:
                    1. enter the ID of the spirit to be produced
                    2. enter the date or choose to start the PR now
                    3. the PR should now be visible from the List Production Runs option*/
                    Console.Clear();
                    CreateNewProductionRun();
                    break;
                case "3":
                    /*allows the user to close out a Production Run (PR). 
                    Steps:
                    1. choose an the correct ID from the open PR's
                    2. enter the date or choose to end the PR now
                    3. enter the quantity of product produced
                    4. record any notes to be included with the PR
                    5. the PR should now be updated in the List Production Runs option and the stock should be correctly 
                    incremented (visible from Main Menu) to reflect the new product in stock. */
                    Console.Clear();
                    CloseOutProductionRun();
                    break;
                case "4":
                    Console.WriteLine("\nUNDER CONSTRUCTION: Come back later! Press any key to return to the Production Run Management.");
                    Console.ReadKey();
                    Console.Clear();
                    ManageProductionRuns();
                    break;
                case "5":
                    Console.WriteLine("\nUNDER CONSTRUCTION: Come back later! Press any key to return to the Production Run Management.");
                    Console.ReadKey();
                    Console.Clear();
                    ManageProductionRuns();
                    break;
                case "0":
                    ShowMainMenu();
                    break;
                default:
                    Console.WriteLine("\nInvalid input. Press any key to return to try again.");
                    Console.ReadKey();
                    Console.Clear();
                    ShowMainMenu();
                    break;
            }
        }

        internal static void ManageInvoices()
        {
            string? userSelection;

            Console.Clear();
            Console.WriteLine("**********************");
            Console.WriteLine("* Invoice Management *");
            Console.WriteLine("**********************");

            Console.WriteLine("1: List Invoices");
            Console.WriteLine("2: Create New Invoice");
            Console.WriteLine("3: **Print Invoice**");
            Console.WriteLine("4: **List Invoice Lines**"); 
            Console.WriteLine("0: Back to Main Menu");

            Console.Write("Your selection: ");

            userSelection = Console.ReadLine();
            switch (userSelection)
            {
                case "1":
                    // lists all Invoices
                    ListInvoices();

                    Console.WriteLine("\nPress any key to return to the Invoice Management.");
                    Console.ReadKey();
                    Console.Clear();
                    ManageInvoices();
                    break;
                case "2":
                    /*allows the user to create a new invoice
                    Steps:
                    1. to get started, enter the first and last name of the person purchasing product
                    2.a. if the person is already in the database, it will display all matches and you can subsequently
                    choose the right one (in the hypothetical that there are people of the same name in the DB)
                    2.b. if the person is not in the DB, user will be promted to create a new profile. From there, address,
                    phone number, and email must be provided. The record is subsequently added to the customer table of the DB.
                    From there, the process follows step 2.a.
                    3. choose whether the billing address is the same as the residental address, if not, enter differing address
                    4. select spirit to be purchased via its ID
                    5. enter the quantity of bottles purchased
                    6. repeat steps 4-5 for all bottle orders, when finished, enter that there are no more products on the invoice
                    7. the invoice should now be updated in the List Invoices option and the stock should be correctly 
                    decremented (visible from Main Menu) to reflect the product taken from stock. */
                    Console.Clear();
                    CreateNewInvoice();

                    break;
                case "3":
                    Console.WriteLine("\nUNDER CONSTRUCTION: Come back later! Press any key to return to the Invoice Management.");
                    Console.ReadKey();
                    Console.Clear();
                    ManageInvoices();
                    break;
                case "4":
                    Console.WriteLine("\nUNDER CONSTRUCTION: Come back later! Press any key to return to the Invoice Management.");
                    Console.ReadKey();
                    Console.Clear();
                    ManageInvoices();
                    break;
                case "0":
                    ShowMainMenu();
                    break;
                default:
                    Console.WriteLine("\nInvalid input. Press any key to return to try again.");
                    Console.ReadKey();
                    Console.Clear();
                    ShowMainMenu();
                    break;
            }
        }
    }
}
