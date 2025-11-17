using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.Interfaces
{
    internal interface IPrintable
    {
        public string DisplayDetails(int db_Id);
    }
}
