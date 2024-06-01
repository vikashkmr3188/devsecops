# Ransomware Data Processer

**Requirement & Fulfillment:**

1. Get ransomware data from given link.
     --> Downloaded from given link
3. Given this JSON as a sample, how will you write a short script/program to process this json and store into databases
     --> Script has been uploaded in repo
4. Explain selection of coding language and DB of your choice.
     --> Coding Language: Python
         Python is a versatile language with extensive support for handling JSON data and interfacing with various databases.
         It has powerful librarie for data manipulation, parsing JSON, and for database operations.

     --> Database: PostgreSQL
         PostgreSQL is an advanced, open-source relational database with a strong reputation for reliability, feature robustness, and performance.
         It supports JSON data types, which makes it ideal for storing JSON data without losing the structure.
5. Given that its large set of data, how will you ensure that no records are missed when writing into the DB
     --> Missing rows if any are identified during insert and tackled & recorded for further investigation.
6. In the case of duplicate entries, how will you handle them?
     --> Before inserting new data, compare it with existing records to avoid duplicates.

**Database ER Diagram:**

<img width="536" alt="image" src="https://github.com/vikashkmr3188/devsecops/assets/49491177/5fe19434-3a82-4706-93d0-c3b4265d5a4e">

**Detailed Steps**

Overall:
  1. Use Case understanding
  2. Tech Stack Selection
  3. Setup Enviroment - Server (EC2 instance) and Database ([Postgres](https://www.postgresql.org/download/linux/redhat/))
  4. Design Tables - ER Diagram
  5. Code flow chart
  6. Develop code
  7. Test code
  8. Document

Code Steps:
  1. Start: Begin the script execution.
  2. Load JSON Data: Load data from ransomware_overview.json.
  3. Initialize Tracking Variables: Initialize variables to track total records, inserted records, duplicate records, missed records, and missed rows.
  4. Setup Logging: Configure logging with a timestamped log file.
  5. Database Connection: Attempt to connect to the database.
  6. On success, proceed to create tables.
  7. On failure, log the error and exit.
  8. Create Tables: Execute SQL commands to create ransomware and ransomware_details tables.
  9. On success, proceed to insert data.
  10. On failure, log the error, rollback, and exit.
  11. Insert Data Function: Define the function to insert data into the database.
  12. For Each Entry in Data: Loop through each entry in the JSON data.
  13. Insert into Ransomware Table: Attempt to insert data into the ransomware table.
  14. On success, retrieve the ransomware_id.
  15. On IntegrityError, rollback the transaction, and retrieve the existing ransomware_id.
  16. Insert into Ransomware Details Table: Attempt to insert data into the ransomware_details table.
  17. On success, check the row count to determine if it was a duplicate.
  18. On IntegrityError, log the error, rollback, and add the entry to missed rows.
  19. Check Row Count: Check if the row count is zero.
  20. If zero, increment duplicate records and add to missed rows.
  21. If greater than zero, increment inserted records.
  22. Commit Transaction: Commit the transaction.
  23. All Entries Processed: After processing all entries, close the database connection.
  24. Write Missed Rows to JSON File: Write missed rows to missed_rows.json.
  25. Output Summary: Print the summary of total records, inserted records, duplicate records, and missed records.
  26. End: End the script execution.

**Screenshot:**
  1. PostgreSQL DB Creation:
     
<img width="735" alt="Screenshot 2024-06-01 at 7 50 54 PM" src="https://github.com/vikashkmr3188/devsecops/assets/49491177/81c50e9a-9746-4378-a239-c1e4da68489f">

  2. Script Execution to create table and insert data

<img width="507" alt="image" src="https://github.com/vikashkmr3188/devsecops/assets/49491177/14fb79d3-15ce-4bd9-abb8-651aa1e4bd9d">

<img width="407" alt="image" src="https://github.com/vikashkmr3188/devsecops/assets/49491177/5483e6d9-0823-46e1-afef-100db72d2cac">

<img width="360" alt="image" src="https://github.com/vikashkmr3188/devsecops/assets/49491177/d40e143a-16d8-4ebe-ba84-5847caa845a4">

<img width="1057" alt="image" src="https://github.com/vikashkmr3188/devsecops/assets/49491177/6c030cb5-1827-44bc-a2f0-c29db3820427">

Introduced deliberatly miss of row by changing data type to limited legnth varchar(2)

<img width="754" alt="image" src="https://github.com/vikashkmr3188/devsecops/assets/49491177/f4ed7c53-ab4c-455b-8e1c-46d302216aec">




  
   

