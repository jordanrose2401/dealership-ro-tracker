\# Intake: Service RO Tracker



\## Imagined user

The primary user of this app is a service manager named Mr. Smith. Mr. Smith currently tracks his service repair orders on a whiteboard in his office. He updates his whiteboard as the orders are completed, and only tracks the dates the order was initiated, the order number, the make and model, and vin of the customer's vehicle, and a reason why the order has yet to be completed. He tends to use general statements as to why an order has not been completed, things like "parts", "approval", "technician", "warranty".



\## Problem today

Mr. Smith's main problem with his whiteboard system is that it doesn't track how long a customer's order has been waiting to be completed. He wants to be able to quickly consult a tool that tells him when an order has taken more than 7 calendar days to be completed.  We will also include all calendar days (including holidays) for the purposes of determining whether an order is stale. The main thing that these stale orders cost are customer satisfaction, this is why he cares about calendar rather than business days, to reflect how long the customer has actually been without their car. Mr. Smith will be the primary user of any tool and any login needed will be to ensure that only he can view the orders.



\## Smallest useful version

The smallest useful version of this app is a read-only version that is capable of flagging an order as "stale" if it has been more than 7 calendar days since the order was initiated. We will assume that the reason listed is only capable of being from a pre-selected list of options, the simple options that Mr. Smith already employs will do. To keep the "read-only" nature of the project, we will assume that synthetic data is loaded into the database via a small script and a csv. This simulates loading the data into the app via the dealership database that includes the more sensitive customer information that would happen in a real world scenario. Modifying the csv and then re-running the loading script is how this project simulates the app updating regularly for a real world Mr. Smith. Mr. Smith should be able to quickly see which orders have been open too long, and what issue needs to be resolved in order to finish the order.



\## Out of scope

For the purposes of this project the user will not be able to add new orders to the app. Also connecting to an existing dealership database (that is handled by the csv/script simulation), or being able to contact a customer directly through the app is not within the scope. We will also assume that Mr. Smith is the only user, so we will not need multiple roles.



\## Data and sensitivity
The app touches only the order number, the make and model and vin of the vehicle, and a reason why the order has not been completed yet. We will assume sensitive information such as customer name and contact information is not necessary for this app, as its primary focus is on tracking repair orders that have taken too long to be completed. Currently Mr. Smith does not track customer information on his whiteboard, the order numbers are linked to the customer information in a computer system used by the dealership. We will treat the customer's vin as semi-sensitive information by only displaying the last 4 characters of it to Mr. Smith.



\## Later, if time allows

If there is time we will include a login for Mr. Smith. By default orders will be sorted by days open, if time allows more sorting and filtering options may be added. The user's main issue is seeing stale orders, but in a real version of an app like this editing would be something that would be nice to add if the owner requested it.



\## Is this worth building?

The biggest thing the current whiteboard system lacks is a quick way to tell when an order has taken too long to complete. The app is worth building if it allows Mr. Smith to quickly identify orders that are stale, and what is causing them to be incomplete. Worth building only if a data feed from dealership system exists; otherwise recommend against.

