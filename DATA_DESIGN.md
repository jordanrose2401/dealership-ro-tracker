Sketch of synthetic data

Stored Columns (type): Order No. (number) | Date Opened (date) | Date completed (date, blank if open) | Make/Model (text) | VIN (text, full and invented) | Reason (from the following list: Parts, Customer Approval, Technician, Warranty)
Calculated when the page loads: Days open, Stale check
Displayed to Mr. Smith: Order No. (number) | Days open (number) | Make/Model (text) | last 4 characters of VIN (text) | Reason (preselected text) | Flag ( either "STALE" or "OK")
Notes: Orders should be sorted by default by "Days open" with the oldest orders at the top. The source CSV (simulating the dealership feed) contains the full VIN. The loader validates the full VIN, then stores only the last 4 characters in the app’s database. The app displays those 4 characters.
Number of Rows: At least a dozen, a number that would feasibly fit on Mr. Smith's whiteboard
Test cases:
An order opened 6 calendar days ago which should not be marked as stale
An order opened exactly 7 calendar days ago which should not be marked as stale
An order opened today (0 days)
An order with a reason that isn't on the list (should be rejected)
An order missing a date (should be rejected)
An order opened 8 calendar days ago which should be marked as stale
A completed order with a completion date and a blank reason
An order with at least one of each of the preselected reasons why it's delayed (parts, customer approval, technician, warranty)
An open order with a blank reason
An order with a completion date earlier than the opened date
A duplicate order number

