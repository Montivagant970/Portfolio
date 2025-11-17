using Distillery.ManagementSystem.Domain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.Processes
{
    internal abstract class Process : IPrintable
    {
        /*ProcessType should never be changed, while the other properties could imaginably be updated*/
        internal ProcessType ProcessType { get; }
        internal DateTime StartDate { get; set; }
        internal DateTime? EndDate { get; set; }
        internal string? Notes { get; set; }

        protected Process() { }
        protected Process(ProcessType processType, DateTime startDate, DateTime? endDate, string? notes) 
        {
            ProcessType = processType;
            StartDate = startDate;
            EndDate = endDate;
            Notes = notes;
        }

        public abstract string DisplayDetails(int db_Id);
    }
}
