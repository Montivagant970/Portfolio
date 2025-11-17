using Distillery.ManagementSystem.Domain.Processes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Distillery.ManagementSystem.Domain.Persons;
using System.Data.Common;
using System.Reflection.Metadata.Ecma335;

namespace Distillery.ManagementSystem.Domain.Sales
{
    internal class InvoiceManager
    {
        internal InvoiceManager() { }

        internal Invoice CreateNew() //(Invoice, Dictionary<int, InvoiceLine>) the information to create invoicelines are likewise created in this method. One would only need to return it.
        {
            int conditionNewCustomer = 0;
            string? userInput;
            int customerId;
            string billingAddress = "";
            int spiritId = -1;
            int quantity = -1;
            Dictionary<int, int> productIdAndQuantity = new();

            Prompter prompter = new();
            PersonManager personManager = new();

            // query the database for Spirit Names paired with Spirit IDs and Inventory Prices paired with Product IDs
            var sql_DB = SQL_DB.Instance;
            Dictionary<int, string> spiritNamesAndIds = sql_DB.GetSpiritIds();
            Dictionary<int, decimal> inventoryPrices = sql_DB.GetPrices();

            // determine new or existing customer - first input name of customer
            Console.Clear();
            Console.WriteLine("Please enter the customer's first and last name.");
            string[] customerFullName = prompter.GetValidString().Split(' ');
            Console.Clear();

            // do-while to check if the person is a preexisting customer or not. To the contrary, prompts the user to 
            do
            {
                Console.WriteLine("CURRENT CUSTOMERS\nCustomer ID:\tName:\t\t\tPhone Number:\tAddress:");

                foreach (var customer in sql_DB.TableCustomers)
                {
                    if (customer.Value.FirstName == customerFullName[0] && customer.Value.LastName == customerFullName[1])
                    {
                        Console.WriteLine(customer.Value.DisplayDetails(customer.Key));
                        conditionNewCustomer = 1;
                    }
                }

                if (conditionNewCustomer == 0)
                {

                    Console.WriteLine("*** no matches found ***");
                    Console.WriteLine("\nCreate new customer profile? (Yes/No)");
                    userInput = prompter.GetYesNo();

                    switch (userInput)
                    {
                        case "yes":
                            personManager.AddNewCustomer(customerFullName[0], customerFullName[1]);
                            break;
                        case "no":
                            Utilities.ManageInvoices();
                            break;
                    }
                }

            } while (conditionNewCustomer == 0);

            // select the customer in the database for which the invoice is for
            do
            {
                Console.WriteLine("\nPlease enter the customer ID to start creating the invoice.");
                customerId = prompter.GetValidNumber();
            } while (customerId == -1);
            Console.Clear();

            // set the invoice date
            DateTime invoiceDate = DateTime.Now;

            // get billing address
            do
            {
                Console.WriteLine("Is the billing address the same as the residential address? (Yes/No)");
                userInput = prompter.GetYesNo();
            } while (userInput != "yes" &&  userInput != "no");

            switch (userInput)
            {
                case "yes":
                    var customerInQuestion = sql_DB.TableCustomers[customerId];
                    billingAddress = customerInQuestion.Address;
                    break;
                case "no":
                    Console.WriteLine();
                    billingAddress = prompter.GetValidString("Please enter the billing address. (e.g. 123 Street Name, Fort Collins, CO, USA. 80526.)");
                    break;
            }
            Console.Clear();

            // retrieve the orders on the invoice
            conditionNewCustomer = 0;
            do
            {
                // retrieve a valid Spirit ID
                do
                {
                    Console.WriteLine("Spirit:\t\tID:");
                    foreach (var product in spiritNamesAndIds)
                    {
                        Console.WriteLine($"{product.Value}\t\t{product.Key}");
                    }

                    spiritId = prompter.GetValidId(spiritNamesAndIds);
                } while (spiritId == -1);

                // retrieve a valid number of bottles
                do
                {
                    Console.Clear();
                    Console.WriteLine("Please enter the quantity of bottles purchased.");
                    quantity = prompter.GetValidNumber();
                } while (quantity == -1);

                // associate Spirit IDs with their Quantities purchased
                productIdAndQuantity[spiritId] = quantity;

                // prompt for additional purchases
                Console.Clear();
                userInput = prompter.GetYesNo("Are there other products on the invoice? (Yes/No)");

                // break loop when no more orders are desired
                if (userInput == "no")
                    conditionNewCustomer = 1;
                Console.Clear();

            } while (conditionNewCustomer == 0);


            // calculate invoice total (could be method of separate class)
            List<decimal> orderTotals = [];

            foreach (var pair in productIdAndQuantity) // Dictionary<int productId, int quantityOfBottles> for reference
            {
                if (inventoryPrices.ContainsKey(pair.Key))
                {
                    decimal subtotal = inventoryPrices[pair.Key] * pair.Value;
                    orderTotals.Add(subtotal);
                }
            }

            decimal invoiceTotal = orderTotals.Sum();

            // subtract purchase from product stock
            foreach (var pair in productIdAndQuantity)
            {
                sql_DB.TableProductStock[pair.Key].Quantity = sql_DB.TableProductStock[pair.Key].Quantity - (pair.Value * .75);
                /*Another good addition for further iterations of this project would be a check to ensure that the ordered bottles do
                 not subtract the stock below zero. The .75 above converts the amount to be subtracted from the product stock, as the
                inventory is in liters and standard bottles contain 750ml of product.*/
            }

            return new Invoice(customerId, invoiceDate, billingAddress, invoiceTotal);
        }

        internal Dictionary<int, InvoiceLine> CreateInvoiceLine(Invoice invoice)
        {
            return new Dictionary<int, InvoiceLine>();
        }
    }
}
