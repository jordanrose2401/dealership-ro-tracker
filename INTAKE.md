\# Intake: Service RO Tracker



\## Imagined user

The primary user of this app is a service manager named Mr. Smith. Mr. Smith currently tracks his service repair orders on a whiteboard in his office. He updates his whiteboard as the orders are completed, and only tracks the date the order was initiated, the order number, the make and model, and vin of the customer's vehicle, and a reason why the order has yet to be completed.



\## Problem today

Mr. Smith's main problem with his whiteboard system is that it doesn't track how long a customer's order has been waiting to be completed. He wants to be able to quickly consult a tool that tells him when an order has taken more than 5 business days to be completed. The main thing that these stale orders cost are customer satisfaction, customers do not want to be without their cars for 5 business days or more. Mr. Smith will be the primary user of any tool and any login needed will be to ensure that only he can update the status of orders.



\## Smallest useful version

The smallest useful version of this app is a read-only version that is capable of flagging an order as "stale" if it has not been completed within 5 business days. We will assume that synthetic data is loaded via a script, so as to not contradict the "read-only" nature of this project. Mr. Smith should be able to quickly see which orders have been open too long, and what issue needs to be resolved in order to finish the order.



\## Out of scope

For the purposes of this project the user will not be able to add new orders to the app. Also connecting to an existing dealership database, or being able to contact a customer directly through the app is not within the scope. We will also assume that Mr. Smith is the only user, so we will not need multiple roles.



\## Data and sensitivity
The app touches only the order number, the make and model and vin of the vehicle, and a reason why the order has been delayed. Sensitive information such as customer name and contact information is not necessary for this app, as its primary focus is on tracking repair orders that have taken too long to be completed. Currently Mr. Smith does not track customer information on his whiteboard, the order numbers are linked to the customer information in a computer system used by the dealership. We will treat the customer's vin as semi-sensitive information.



\## Is this worth building?

The biggest thing the current whiteboard system lacks is a quick way to tell when an order has taken too long to complete. The app is worth building if it allows Mr. Smith to quickly identify orders that are stale, and what is causing them to be incomplete.

