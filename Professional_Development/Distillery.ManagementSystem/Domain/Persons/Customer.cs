using Distillery.ManagementSystem.Domain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.Persons
{
    internal class Customer : IPrintable
    {
        /*The get and set methods for the following properties has not been implemented in this version of the application.
         Immaginably, there could be a features that allows for the updating of customer information.*/
        internal string FirstName { get; set; }
        internal string LastName { get; set; }
        internal string Address { get; set; }
        internal string PhoneNumber { get; set; }
        internal string Email { get; set; }

        internal Customer(string firstName, string lastName, string address, string phoneNumber, string email)
        {
            FirstName = firstName;
            LastName = lastName;
            Address = address;
            PhoneNumber = phoneNumber;
            Email = email;
        }

        public string DisplayDetails(int db_Id)
        {
            if (LastName.Length < 7)
                return $"{db_Id}\t\t{FirstName} {LastName}\t\t{PhoneNumber}\t{Address}";
            else
                return $"{db_Id}\t\t{FirstName} {LastName}\t{PhoneNumber}\t{Address}";
        }
    }
}
