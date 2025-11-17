using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Distillery.ManagementSystem.Domain
{
    internal class Prompter
    {
        internal Prompter() { }

        internal int GetValidId(List<int> nameIdPair)
        {
            string? inputId;
            int intInputId;

            // do-while forces the user to enter a valid ID
            do
            {
                // do-while forces the user to not enter a non-null or non-white space value
                do
                {
                    Console.WriteLine("\nPlease enter an ID:");
                    Console.Write("Your input: ");

                    inputId = Console.ReadLine();

                    if (string.IsNullOrEmpty(inputId))
                    {
                        Console.WriteLine("\nThe ID field is mandatory. Please enter a valid ID.");
                        Console.WriteLine("Press any key to try again.");
                        Console.ReadKey();
                        Console.Clear();
                        return intInputId = -1;
                    }

                } while (string.IsNullOrEmpty(inputId));

                // VISUAL END OF INNER NESTED DO-WHILE //

                bool isValidNumber = int.TryParse(inputId, out intInputId);

                if (!isValidNumber || !nameIdPair.Contains(intInputId))
                {
                    Console.WriteLine("\nInvalid ID.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                    return intInputId = -1;
                }

            } while (!nameIdPair.Contains(intInputId));

            return intInputId;
        }

        internal int GetValidId(Dictionary<int, string> stockDB)
        {
            string? inputId;
            int intInputId;
            // do-while forces the user to enter a valid ID
            do
            {
                // do-while forces the user to not enter a non-null or non-white space value
                do
                {
                    Console.WriteLine();
                    Console.WriteLine("Please enter an ID:");
                    Console.Write("Your input: ");

                    inputId = Console.ReadLine();

                    if (string.IsNullOrEmpty(inputId))
                    {
                        Console.WriteLine("\nThe ID field is mandatory. Please enter a valid ID.");
                        Console.WriteLine("Press any key to try again.");
                        Console.ReadKey();
                        Console.Clear();
                        return intInputId = -1;
                    }

                } while (string.IsNullOrEmpty(inputId));

                // VISUAL END OF INNER NESTED DO-WHILE //

                bool isValidNumber = int.TryParse(inputId, out intInputId);

                if (!isValidNumber || !stockDB.ContainsKey(intInputId))
                {
                    Console.WriteLine("\nInvalid ID.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                    return intInputId = -1;
                }

            } while (!stockDB.ContainsKey(intInputId));

            return intInputId;
        }

        internal int GetValidNumber()
        {
            string? inputNumber;
            int outputNumber;

            // do-while forces the user to not enter a non-null or non-white space value
            do
            {
                Console.Write("Your input: ");

                inputNumber = Console.ReadLine();

                bool isValidNumber = int.TryParse(inputNumber, out outputNumber);

                if (string.IsNullOrEmpty(inputNumber) || !isValidNumber)
                {
                    Console.WriteLine("\nA numeric value is mandatory. Please enter a valid number.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                    return outputNumber = -1;
                }

            } while (!string.IsNullOrEmpty(inputNumber) && !(outputNumber is int));

            return outputNumber;
        }

        internal DateTime GetDateTime()
        {
            string? inputDateTime;
            DateTime outputDateTime;

            do
            {
                Console.Clear();
                Console.WriteLine("Please enter the date and time (e.g. 10/10/2025 13:42):");
                inputDateTime = Console.ReadLine();

                if (!DateTime.TryParse(inputDateTime, out outputDateTime))
                {
                    Console.WriteLine("\nInvalid format. Please try again.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
            } while (!DateTime.TryParse(inputDateTime, out outputDateTime));

            return outputDateTime;
        }

        internal string GetValidString()
        {
            string? inputString;
            int intString;
            bool isValidNumber;

            do
            {
                Console.WriteLine("Your input: ");
                inputString = Console.ReadLine();

                isValidNumber = int.TryParse(inputString, out intString);

                if (string.IsNullOrEmpty(inputString))
                {
                    Console.WriteLine("\nThe field is mandatory. Please provide an input.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
                else if (isValidNumber)
                {
                    Console.WriteLine("\nThe field cannot be a number.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
            } while (string.IsNullOrEmpty(inputString) || isValidNumber);

            return inputString;
        }

        /*I noticed that a lot of the do-while loops in the various managers can be avoided if there were an
         overloaded method that passes a message to be printed at the top of each new attempt. The reason for
        the do-while loops in the managers is to ensure that the person receives the field prompt after each
        failed attempt. In further iterations, I would like to correct this also for the other Get...() methods,
        especially where it would lead to greater simplicity in the code. Look at InvoiceManager for the
        implementation of this specific overloaded method.*/
        internal string GetValidString(string message)
        {
            string? inputString;
            int intString;
            bool isValidNumber;

            do
            {
                Console.WriteLine(message);
                Console.WriteLine("Your input: ");
                inputString = Console.ReadLine();

                isValidNumber = int.TryParse(inputString, out intString);

                if (string.IsNullOrEmpty(inputString))
                {
                    Console.WriteLine("\nThe field is mandatory. Please provide an input.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
                else if (isValidNumber)
                {
                    Console.WriteLine("\nThe field cannot be a number.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
            } while (string.IsNullOrEmpty(inputString) || isValidNumber);

            return inputString;
        }

        internal string GetYesNo()
        {
            string? inputString;
            int intString;
            bool isValidNumber;

            Console.WriteLine("Your input: ");
            inputString = Console.ReadLine().ToLower();

            isValidNumber = int.TryParse(inputString, out intString);

            if (string.IsNullOrEmpty(inputString))
            {
                Console.WriteLine("\nThe field is mandatory. Please provide an input.");
                Console.WriteLine("Press any key to try again.");
                Console.ReadKey();
                Console.Clear();
            }
            else if (isValidNumber)
            {
                Console.WriteLine("\nThe input cannot be a number.");
                Console.WriteLine("Press any key to try again.");
                Console.ReadKey();
                Console.Clear();
            }
            else if (inputString != "yes" && inputString != "no")
            {
                Console.WriteLine("\nThe input must be either 'Yes' or 'No'.");
                Console.WriteLine("Press any key to try again.");
                Console.ReadKey();
                Console.Clear();
            }

            return inputString;
        }

        internal string GetYesNo(string message)
        {
            string? inputString;
            int intString;
            bool isValidNumber;

            do
            {
                Console.WriteLine(message);
                Console.WriteLine("Your input: ");
                inputString = Console.ReadLine().ToLower();

                isValidNumber = int.TryParse(inputString, out intString);

                if (string.IsNullOrEmpty(inputString))
                {
                    Console.WriteLine("\nThe field is mandatory. Please provide an input.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
                else if (isValidNumber)
                {
                    Console.WriteLine("\nThe input cannot be a number.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
                else if (inputString != "yes" && inputString != "no")
                {
                    Console.WriteLine("\nThe input must be either 'Yes' or 'No'.");
                    Console.WriteLine("Press any key to try again.");
                    Console.ReadKey();
                    Console.Clear();
                }
            } while (inputString != "yes" && inputString != "no");

            return inputString;
        }
    }
}
