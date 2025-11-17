using Distillery.ManagementSystem.Domain;
using Distillery.ManagementSystem.Domain.Persons;
using Distillery.ManagementSystem.Domain.Sales;
using Distillery.ManagementSystem.Domain.Processes;
using Distillery.ManagementSystem.Domain.ProcessManagement;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem
{
    internal class SQL_DB
    {
        //*****SINGLETON*****
        private static SQL_DB _instance;
        private static readonly object _lock = new object();

        public Dictionary<int, ProductionRun> TableProductionRuns { get; private set; }
        public Dictionary<int, Product> TableProductStock { get; private set; }
        public Dictionary<int, Customer> TableCustomers { get; private set; }
        public Dictionary<int, Invoice> TableInvoices { get; private set; }

        // private constructor
        private SQL_DB()
        {
            TableProductionRuns = new Dictionary<int, ProductionRun>();
            TableProductStock = new Dictionary<int, Product>();
            TableCustomers = new Dictionary<int, Customer>();
            TableInvoices = new Dictionary<int, Invoice>();

            InitializeDB();
        }

        // public accessor
        internal static SQL_DB Instance
        {
            get
            {
                if (_instance == null)
                {
                    lock (_lock)
                    {
                        if (_instance == null)
                        {
                            _instance = new SQL_DB();
                        }
                    }
                }
                return _instance;
            }
        }

        private void InitializeDB()
        {
            TableProductionRuns.Add(1, new ProductionRun(ProcessType.ProductionRun, new DateTime(2016, 04, 20, 14, 30, 0), new DateTime(2016, 05, 12, 15, 30, 0), "Shiver me timbers! This here rum got me about to walk the plank.", 190, 56));
            TableProductionRuns.Add(2, new ProductionRun(ProcessType.ProductionRun, new DateTime(2016, 05, 12, 16, 30, 0), new DateTime(2016, 05, 24, 8, 30, 0), "Y this tequila come out stinky tho?", 957, 34));
            TableProductionRuns.Add(3, new ProductionRun(ProcessType.ProductionRun, new DateTime(2016, 05, 24, 09, 30, 0), new DateTime(2016, 06, 13, 11, 45, 0), "This whisky tastes like cowboy boots.", 54, 69));
            TableProductionRuns.Add(4, new ProductionRun(ProcessType.ProductionRun, new DateTime(2016, 05, 24, 09, 30, 0), null, null, 2, null));
            TableProductStock.Add(54, new Product("Whiskey", 236, true, 48.99));
            TableProductStock.Add(43, new Product("Corn", 367, false, null));
            TableProductStock.Add(76, new Product("Molasses", 926, false, null));
            TableProductStock.Add(190, new Product("Rum", 32, true, 31.99));
            TableProductStock.Add(957, new Product("Tequila", 2346, true, 39.99));
            TableProductStock.Add(5, new Product("Sugar", 500, false, null));
            TableProductStock.Add(2, new Product("Gin", 22, true, 33.99));
            TableCustomers.Add(1, new Customer("Charlie", "Bucket", "23 Middle Street, Denver, CO, USA. 80014.", "303-123-5421", "chocolatelover@hotmail.com"));
            TableCustomers.Add(2, new Customer("Mike", "Teavee", "363 Pearl Street, Boulder, CO, USA. 80301.", "303-630-5159", "boomboomkaboom@gmail.com"));
            TableCustomers.Add(3, new Customer("Agustus", "Gloop", "8993 Turtle Nest Avenue, Fort Collins, CO, USA. 80526.", "970-023-1047", "greedynincompoop@yahoo.com"));
            TableCustomers.Add(4, new Customer("Veruca", "Salt", "24 Willow Way, Greeley, CO, USA. 80543.", "970-197-9835", "iwantapony@elitemail.com"));
            TableCustomers.Add(5, new Customer("Violet", "Beuaregarde", "2099 Goldrush Road, Golden, CO, USA. 80401.", "303-182-7881", "alltimegumchamp@aol.com"));
            TableInvoices.Add(1, new Invoice(3, new DateTime(2016, 05, 24, 09, 30, 0), "8993 Turtle Nest Avenue, Fort Collins, CO, USA. 80526.", 98.43m));
        }
        //*****SINGLETON*****

        internal void AddEntry<T>(T dataEntry)
        {
            int newRowId;

            if (dataEntry is ProductionRun productionRunEntry)
            {
                newRowId = TableProductionRuns.Any() ? TableProductionRuns.Keys.Max() + 1 : 1;
                TableProductionRuns.Add(newRowId, productionRunEntry);
            }
            else if (dataEntry is Product productEntry)
            {
                newRowId = TableProductStock.Any() ? TableProductStock.Keys.Max() + 1 : 1;
                TableProductStock.Add(newRowId, productEntry);
            }
            else if (dataEntry is Customer customerEntry)
            {
                newRowId = TableCustomers.Any() ? TableCustomers.Keys.Max() + 1 : 1;
                TableCustomers.Add(newRowId, customerEntry);
            }
            else if (dataEntry is Invoice invoiceEntry)
            {
                newRowId = TableInvoices.Any() ? TableInvoices.Keys.Max() + 1 : 1;
                TableInvoices.Add(newRowId, invoiceEntry);
            }
            else
            {
                throw new InvalidOperationException($"Unsupported type: {typeof(T).Name}");
            }
        }

        internal void UpdateEntry<T>(int id, T dataEntry)
        {
            if (dataEntry is ProductionRun productionRunEntry)
            {
                foreach (var row in TableProductionRuns)
                {
                    if (id == row.Key)
                    {
                        row.Value.EndDate = productionRunEntry.EndDate;
                        row.Value.QuantityProduced = productionRunEntry.QuantityProduced;
                        row.Value.Notes = productionRunEntry.Notes;
                    }
                }
            }
        }

        internal Dictionary<int, string> GetSpiritIds() 
        {
            Dictionary<int, string> spiritIds = new();

            foreach (var stockItem in TableProductStock) 
            {
                if (stockItem.Value.IsSpirit)
                {
                    spiritIds[stockItem.Key] = stockItem.Value.Name;
                }

            }
            return spiritIds;
        }

        internal List<int> GetOpenProductionRuns() 
        {
            List<int> openProductionRuns = new();

            foreach (var run in TableProductionRuns) 
            {
                if (run.Value.EndDate == null)
                {
                    openProductionRuns.Add(run.Key);
                }
            }
            return openProductionRuns;
        }

        internal Dictionary<int, decimal> GetPrices()
        {
            Dictionary<int, decimal> itemPrices = new();

            foreach (var stockItem in TableProductStock)
            {
                if (stockItem.Value.IsSpirit)
                {
                    itemPrices[stockItem.Key] = (decimal)stockItem.Value.UnitPrice;
                }
            }
            return itemPrices;
        }
    }
}
