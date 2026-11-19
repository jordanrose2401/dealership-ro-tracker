\### Context

Read INTAKE.md and DATA\_DESIGN.md and scripts/load\_orders.py for context.



\### Goal

The goal is to create a Flask Board that displays the Repair Orders that are incomplete on a webpage. The database has completed orders in it, but this webpage should not display them to the user. Each row should show the order number ("Order Number" on the page, it's stored in the db as order\_no), days the order has been opened ("Days Open" on the page, calculated as today's date, read from the system clock, minus the date opened which is stored as date\_opened in the db), the make and model of the car ("Make \& Model" on the page, stored as make\_model in the db, in one column), the last 4 characters of the VIN ("VIN" on the page, stored as vin\_last4 in the db which only stores the last 4 characters of the VIN), the reason the order is open ("Reason" on the page, stored as reason in the db), and a flag with the word "STALE" (in red text) if the order is stale and "OK" (in green text) if the order is not stale. The staleness check is a small function that takes two dates (the opened date and today, check today's date with a simple get\_today() function that is the only place in the code where the clock is checked) and returns the days open (days\_open = today minus date\_opened, in caledary days) and whether it’s stale. Define STALE\_AFTER\_DAYS = 7, and an order is defined to be stale if days\_open > STALE\_AFTER\_DAYS. A summary line should be generated and put at the top of the table with the number of open orders that are stale out of the total number of open orders (ex: "2 of 9 open orders are stale").







\### Files

app.py at the project's root.

templates/board.html

test/test\_staleness.py

test/\_\_init\_\_.py



\### Rules

Only use the standard python library and the Flask package.

If the database is missing display "No data loaded, run the loader."

If the database exists but has no open orders, display "No open orders to display."

Any other errors should display a plain message, not traceback or a file path.

Run with Flask's debug mode off.

Open the database read-only.

Keep the app on my local machine for now (127.0.0.1)  

State the server settings explicitly in the code (127.0.0.1 and debug off), not as defaults.  

Create only app.py, templates/board.html, and test/test\_staleness.py

An order is open when date\_completed is empty (NULL in the db)

Sort orders by days opened, descending so that the stalest orders are at the top.

Plain HTML with a little inline CSS, no JavaScript, and no external fonts, scripts, or stylesheets.

Show the date the page was calculated on the web page (ex: As of November 18, 2026).

The page takes no forms and no query parameters.    

Importing app.py must not start the server or open the database.  

The function takes real date objects, so app.py converts the ISO text from the database first.  

Use render\_template with the HTML file, and don’t mark any database value as safe or build HTML by joining strings.  

Report any disagreement between the docs and the prompt, use short functions with plain-English comments, give a short outline of how the files are organized, and list every file created.  



\### Test Cases

The staleness check is a small function that takes two dates (the opened date and today) and returns the days open and whether it’s stale. It must not read the clock itself. Test it with fixed dates for the 0, 6, 7, and 8-day cases.



\### Do Not

No login.

No secrets.

No extra packages beyond Flask (Flask is already installed).

Do not create or edit any other files, including the loader, data\_gen.py, .gitignore, and requirements.txt.

Do not run git commands.

Do not run the app.

Do not run the tests.



\### Done When

Load good\_orders.csv first. This is done when all the rows are displayed as laid out above, with a message about what proportion of orders are stale, also as laid out above. In the case of running good\_orders.csv the expected output is 9 open orders at 0, 1, 2, 6, 7, 8, 12, 15, and 21 days, and three completed orders which stay hidden. Orders with 0, 1, 2, 6, and 7 days open should be marked as "OK" (with green text), and orders with 8, 12, 15, and 21 days open should be marked as "STALE" (with red text). 4 of 9 open orders are stale is expected, and the table should be ordered by days open 21. 15. 12. 8. 7. 6. 2. 1. 0.

The unit tests must pass with python -m unittest.  



\### Plan First

Create a plan first. Cover the route, the database query, how read-only works, the empty and error states, and a table with test cases and expected results. Confirm that a missing database file is not created as an empty one.  
Before writing any files, give me the plan and wait for my approval.  

