using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.Processes
{
    internal class SubProcess : Process
    {
        /*The subprocesses, i.e. brewing, fermenting, and distilling, were intentionally not implemented in this 
        proof of concept, as the structure, user input, and querying would largely be the same as for production
        runs. The only additions would be the use of ProcessType (see class enum), the linking of a vessel ID, and
        the association of one or many employees. Otherwise on an application level, the functionality would be largely 
        the same, i.e. create new, close out, update, and write notes. Further implementations of this project would
        see its implementation.*/

        internal SubProcess() { }

        public override string DisplayDetails(int db_Id)
        {
            return "";
        }

    }
}
