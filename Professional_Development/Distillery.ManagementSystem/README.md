*  **Program.cs** : entry point to the Distillery Management System.
*  **SQL_DB.cs** : a mock SQL database, structured as a singleton to ensure only a single instance of the database when running the application.
*  **Utilities.cs** : class to manage the various menus of the application.
*  **EntityRelationshipDiagram_Distillery.PDF** : diagram of the fictitious relational database that the SQL_DB.cs class attempts to imitate. The diagram was a means to practice designing a database, its structure and key relationships.
*  *Domain:*
  *  **Product.cs** : class modelling the products of the distillery, instantiable as both raw ingredients or spirits.
  *  **Prompter.cs** : class to handle input prompts by the user with each method generalized in such a way to ensure that it can be used in a variety of different data input scenarios within the app.
  *  *Interfaces:*
     *  **IPrintable.cs** : basic interface that requires the classes that implement it to include a print method to display its details.
  *  *Persons:*
     *  **Customer.cs** : class modelling the customers to the distillery.
     *  **PersonManager.cs** : class tasked with the management of customers within the system - here with method AddNewCustomer().
  *  *ProcessManagement:*
     *  **ProcessManager.cs** : abstract class to serve as the parent to the ProductionRunManager.cs and a future, currently unimplemented SubProcessManager.cs.
     *  **ProductionRunManager.cs** : class tasked with the management of production runs within the system - here with methods CreateNew() and CloseOut().
  *  *Processes:*
     *  **Process.cs** : abstract class modelling child of types ProductionRun and SubProcess.
     *  **ProcessType.cs** : enum to denote which type of process an instantiated child process belongs to.
     *  **ProductionRun.cs** : child class modelling production runs of the distillery.
     *  **SubProcess.cs** : currently unimplemented child class modelling sub-processes of the distillery.
  *  *Sales:*
     *  **Invoice.cs** : class modelling invoices of the distillery.
     *  **InvoiceLine.cs** : class modelling invoice lines to the invoices of the distillery.
     *  **InvoiceManager.cs** : class tasked with the management of invoices within the system - here with method CreateNew().

The current version does not have implementations for sub-process management, invoice lines, the editing or note adding of production runs, or the printing of invoices.
