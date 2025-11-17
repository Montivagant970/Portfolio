using Distillery.ManagementSystem.Domain.Processes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain.ProcessManagement
{
    internal class ProductionRunManager : ProcessManager
    {
        internal ProductionRunManager() { }

        internal override ProductionRun CreateNew()
        {
            Dictionary<int, string> spiritNamesAndIds = new();
            Prompter prompter = new();

            int spiritId;
            string? inputStartDate;
            DateTime outputStartDate;

            // query the database for spirit IDs and their corresponding names, imitates a two column SQL query
            var sql_DB = SQL_DB.Instance;
            spiritNamesAndIds = sql_DB.GetSpiritIds(); 

            // retrieve the Spirit ID
            do
            {
                Console.WriteLine("Spirit:\t\tID:");
                foreach (var product in spiritNamesAndIds)
                {
                    Console.WriteLine($"{product.Value}\t\t{product.Key}");
                }

                spiritId = prompter.GetValidId(spiritNamesAndIds);
            } while (spiritId == -1);

            // retrieve a start date from the user, assigning the current time if production is immediate, otherwise triggers input fields
            do
            {
                Console.Clear();
                Console.WriteLine("Is the production run beginning immediately? (Yes/No)");

                inputStartDate = prompter.GetYesNo();
            } while (inputStartDate != "yes" && inputStartDate != "no");

            if (inputStartDate.ToLower() == "yes")
                outputStartDate = DateTime.Now;
            else
                outputStartDate = prompter.GetDateTime();

            return new ProductionRun(ProcessType.ProductionRun, outputStartDate, null, null, spiritId, null);
        }

        internal override (int, Process) CloseOut()
        {
            Dictionary<int, string> spiritNamesAndIds = new();
            List<int> openProductionRuns = new();
            Prompter prompter = new Prompter();

            string? userInput;
            int productionRunId = -1;
            DateTime outputEndDate;
            int quantitySpiritProduced;
            string? distillerNotes;

            // query the database for spirit IDs and their corresponding names, imitates a two column SQL query. Retrieve open production runs
            var sql_DB = SQL_DB.Instance;
            spiritNamesAndIds = sql_DB.GetSpiritIds();
            openProductionRuns = sql_DB.GetOpenProductionRuns();

            // retrieve the Production Run ID to be changed in the system
            do
            {
                Console.WriteLine("OPEN PRODUCTION RUNS\nProduction ID:\tSpirit ID:\tSpirit:\t\tStart Date:");

                foreach (var run in sql_DB.TableProductionRuns)
                {
                    string productName = "";

                    if (run.Value.EndDate == null)
                    {
                        foreach (var product in spiritNamesAndIds)
                        {
                            if (product.Key == run.Value.SpiritId)
                            {
                                productName = product.Value;
                            }
                        }
                        Console.WriteLine($"{run.Key}\t\t{run.Value.SpiritId}\t\t{productName}\t\t{run.Value.StartDate}");
                    }
                }

                productionRunId = prompter.GetValidId(openProductionRuns);
            } while (productionRunId == -1);

            // retrieve the End Date of the production run
            do
            {
                Console.Clear();
                Console.WriteLine("Did the production run just finish? (Yes/No)");
                Console.Write("Your selection: ");

                userInput = prompter.GetYesNo();
            } while(userInput != "yes" && userInput != "no");

            if (userInput.ToLower() == "yes")
                outputEndDate = DateTime.Now;
            else
                outputEndDate = prompter.GetDateTime();

            // retrieve how much product was produced
            do
            {
                Console.Clear();
                Console.WriteLine("How much product was produced? (in liters)");

                quantitySpiritProduced = prompter.GetValidNumber();
            } while (quantitySpiritProduced == -1);

            do
            {
                Console.Clear();
                Console.WriteLine("Please record the production run notes.");

                distillerNotes = Console.ReadLine();
            } while (distillerNotes == null);

            // add produced spirit to stock
            sql_DB.TableProductStock[sql_DB.TableProductionRuns[productionRunId].SpiritId].Quantity = sql_DB.TableProductStock[sql_DB.TableProductionRuns[productionRunId].SpiritId].Quantity + quantitySpiritProduced;

            return (productionRunId, new ProductionRun(outputEndDate, distillerNotes, quantitySpiritProduced));
        }

        internal override void Update()
        {
            throw new NotImplementedException();
        }
        internal override void AddToNotes()
        {
            throw new NotImplementedException();
        }
    }
}
