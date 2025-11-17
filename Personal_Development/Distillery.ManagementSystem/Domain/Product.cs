using Distillery.ManagementSystem.Domain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain
{
    internal class Product : IPrintable
    {
        internal string Name { get; }
        internal double Quantity { get; set; }
        internal bool IsSpirit { get; }
        internal double? UnitPrice { get; set; }

        internal Product(string name, double quantity, bool isSpirit, double? unitPrice)
        {
            Name = name;
            Quantity = quantity;
            IsSpirit = isSpirit;
            UnitPrice = unitPrice;
        }

        public string DisplayDetails(int db_Id)
        {
            return $"Product: {db_Id} {Name}\nQuantity in Stock: {Quantity}\nSpirit? {(IsSpirit ? "Yes" : "No")}";
        }
    }
}
