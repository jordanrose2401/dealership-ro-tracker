I am trying to create a sample-data generator for a project I am working on. The project is a repair order tracker for a car dealership. Read INTAKE.md and DATA\_DESIGN.md before anything else, and if there are contradictions defer to the prompt but inform me of the contradiction.

The sample data should include the following columns with the listed column header names: order\_no (Order numbers are 5-digit integers from 10000 to 99999, unique within each file, except for the deliberate duplicate in bad\_orders.csv), date\_opened (the date the order was opened relative to the current day, dates are in ISO format YYYY-MM-DD. Read today's date from the system clock each time the script runs. Never type in a date, 'N days ago' means today minus N calendar days), date\_completed (the date the order was completed also relative to today same format as date\_opened), make\_model (the make and model of the car, should be one column for example an entry would look like Ford F-150), vin (invented, not real vehicles, modeled after the rules of actual VINs: 17 characters long, never includes the letters I, O, or Q, check digit does not need to be valid for our purposes. These should be uppercase, unique and one per order), reason (this is the reason the car repair is delayed, I want them to come from a pre selected list to aid with data validation, these options should come from the following list: Parts, Customer Approval, Technician, Warranty, set them in one place in the script described below. Open orders should have a reason from the list, and completed orders must have a blank reason).

For our purposes we will count all calendar days including holidays. I want a fixed random seed. Ages stay tied to today, but the choice of makes, models, and VINs should stay the same to make testing less confusing. As a rule date\_completed can't be before data opened or in the future, but this rule only applies to good\_orders.csv.


Create a csv named "good\_orders.csv" stored in data\\ at the projects root with exactly 12 rows. This csv will contain valid orders. Populate the columns with the following test cases: An order opened 6 days ago. An order opened 7 days ago. An order opened today. An order opened 8 days ago. A completed order with a completion date and a blank reason. Orders with each of the pre-selected reasons. I want you to also show which rows cover each of these test cases, and one row can cover multiple test cases. You may include other order with different ages to fill out the 12 rows, and include at least two completed orders.


Also create a csv with invalid orders called "bad\_orders.csv" stored in the same data\\ folder described above. These cases should include: An order with a reason that isn't valid. An order missing a opening date. An open order with a blank reason. An order with a completion date earlier than the opening date. Two orders with the same order number. Each row in bad\_orders.csv must break exactly one rule and otherwise be valid. The bad file should have exactly 6 rows with the duplicate case taking two.


The good and bad files should use the same headers and formats described above, with one row per case, two rows for the duplicate case check.
Black cells are truly empty, not the text "None" or "Null".


This should be coded using python, standard library only. Name the script data\_gen.py stored in scripts\\ at the projects root and build output paths relative to the script's own location. The script should also print a short summary, covering both files, when it runs that lists each row and which case(s) it covers. Do not include a "covers" column in either csv. This script should create data\\ if it's missing and overwrite the CSVs each run. Use the csv module from the standard library for writing. The script is done when running the script twice on the same day produces identical files.


For now the scope is only the sample data generator. No database, no loader, no web page, no login, and no extra packages.


Before writing any files, tell me your plan: how you'll calculate the dates, and show the rows as a table with columns saying which test case each row covers. Wait for my approval before creating anything.


Create only scripts/data\_gen.py, data/good\_orders.csv, data/bad\_orders.csv (and the folders if missing). Do not create or edit anything else. Do not install packages. Do not run any git commands.

After writing the script, don't run it. Tell me the exact command to run and what I should check. When finished, list every file you created.

