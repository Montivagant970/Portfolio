using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.Persons
{
    internal class PersonManager
    {
        internal PersonManager() { }

        internal void AddNewCustomer(string inputFirstName, string inputLastName)
        {
            Prompter prompter = new();
            var sql_DB = SQL_DB.Instance;

            string address;
            string phoneNumber;
            string email;

            Console.Clear();
            address = prompter.GetValidString("Please enter a residential address. (e.g. 123 Street Name, Fort Collins, CO, USA. 80526.)");
            Console.Clear();

            phoneNumber = prompter.GetValidString("Please enter a phone number: (e.g. 970-123-4567)");
            Console.Clear();

            email = prompter.GetValidString("Please enter an email address: (e.g. address@email.com)");
            Console.Clear();

            sql_DB.AddEntry(new Customer(inputFirstName, inputLastName, address, phoneNumber, email));
        }
    }
}
