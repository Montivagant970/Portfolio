using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Distillery.ManagementSystem.Domain.Interfaces;

namespace Distillery.ManagementSystem.Domain.Processes
{
    internal class ProductionRun : Process
    {
        /*Spirit ID should never be updated. The spirit cannot magically change after initialization.
         QuantityProduced must be settable to be updated as the production run closes out*/
        internal int SpiritId { get; }
        internal int? QuantityProduced { get; set; }

        internal ProductionRun(DateTime endDate, string notes, int quantityProduced) : base(ProcessType.ProductionRun, DateTime.Now, endDate, notes) // closeout specific constructor
        {
            QuantityProduced = quantityProduced;
            EndDate = endDate;
            Notes = notes;
        }

        internal ProductionRun(ProcessType processType, DateTime startDate, DateTime? endDate, string? notes, int spiritId, int? quantityProduced) : base(processType, startDate, endDate, notes)
        {
            SpiritId = spiritId;
            QuantityProduced = quantityProduced;
        }

        public override string DisplayDetails(int db_Id)
        {
            // query DB for Spirit Names and IDs
            var sql_DB = SQL_DB.Instance;
            Dictionary<int, string> spiritNamesAndIds = sql_DB.GetSpiritIds();

            return $"Production Run ID: {db_Id}\nSpirit ID: {SpiritId} {spiritNamesAndIds[SpiritId]}\nStart Date:\t{StartDate}\nEnd Date:\t{EndDate}\nQuantity produced: {QuantityProduced} liters\nDistiller Notes: {Notes}";
        }
    }
}
