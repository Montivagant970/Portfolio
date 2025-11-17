using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.Sales
{
    internal class InvoiceLine
    {
        internal int InvoiceID { get; }
        internal int ProductID { get; }
        internal double UnitPrice { get; }
        internal int Quantity { get; }
        internal double InvoiceLineTotal { get; }

        internal InvoiceLine(int invoiceID, int productID, double unitPrice, int quantity, double invoiceLineTotal)
        {
            InvoiceID = invoiceID;
            ProductID = productID;
            UnitPrice = unitPrice;
            Quantity = quantity;
            InvoiceLineTotal = invoiceLineTotal;
        }
    }
}
