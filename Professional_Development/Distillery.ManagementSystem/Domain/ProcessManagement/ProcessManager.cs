using Distillery.ManagementSystem.Domain.Processes;
using Distillery.ManagementSystem.Domain.ProcessManagement;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.ProcessManagement
{
    internal abstract class ProcessManager
    {
        /*This was thought to be the abstract class that both ProductionRunManager and a future SubProcessManager
         would inherit from, hence the more generic Process type in the returns of the methods.*/
        protected ProcessManager() { }
        internal abstract Process CreateNew();

        internal abstract void Update();

        internal abstract void AddToNotes();

        internal abstract (int, Process) CloseOut();
    }
}
