using Distillery.ManagementSystem.Domain.Interfaces;
using Distillery.ManagementSystem.Domain.Persons;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.Sales
{
    internal class Invoice : IPrintable
    {
        internal int CustomerId { get; }
        internal DateTime InvoiceDate { get; }
        internal string BillingAddress { get; }
        internal decimal InvoiceTotal { get; }

        internal Invoice(int customerId, DateTime invoiceDate, string billingAddress, decimal invoiceTotal)
        {
            CustomerId = customerId;
            InvoiceDate = invoiceDate;
            BillingAddress = billingAddress;
            InvoiceTotal = invoiceTotal;
        }

        public string DisplayDetails(int db_Id)
        {
            var sql_DB = SQL_DB.Instance;
            int customerId = sql_DB.TableInvoices[db_Id].CustomerId;

            return $"Invoice ID: {db_Id}\nCustomer: {sql_DB.TableCustomers[customerId].FirstName} {sql_DB.TableCustomers[customerId].LastName}\nInvoice Total: {InvoiceTotal}\nInvoice Date:\t{InvoiceDate}\nBilling Address: {BillingAddress}";
        }
    }
}
