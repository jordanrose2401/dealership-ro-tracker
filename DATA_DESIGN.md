Sketch of synthetic data

Stored Columns (type): Order No. (number) | Date Opened (date) | Date completed (date, blank if open) | Make/Model (text) | VIN (text, full and invented) | Reason (preselected text option, blank if completed)
Calulated when the page loads: Days open, Is stale
Displayed to Mr. Smith: Order No. (number) | Days open (number) | Make/Model (text) | last 4 characters of VIN (text) | Reason (preselcted text) | Flag ( either "STALE" or "OK")
Notes: Orders should be sorted by default by "Days open" with the oldest orders at the top
Number of Rows: At least a dozen, a number that would feasibly fit on Mr. Smith's whiteboard
Test cases:
	An order opened 6 calendar days ago which should not be marked as stale
	An order opened exactly 7 calendar days ago which should not be marked as stale
	An order opened today (0 days)|
	An order with a reason that isn't on the list (should be rejected)
	An order missing a date (should be rejected)
	An order opened 8 calendar days ago which should be marked as stale
	A completed order with a complterion date and a blank reason
	An order with at least one of each of the preselected reasons why it's delayed (parts, customer approval, technician, warranty)