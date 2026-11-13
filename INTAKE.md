\# Intake: Service RO Tracker



\## Imagined user

The primary user of this app is a service manager named Mr. Smith. Mr. Smith currently tracks his service repair orders on a whiteboard in his office. He updates his whiteboard as the orders are completed, and only tracks the date the order was initiated, the order number, and the make and model, and vin of the customer's vehicle. 



\## Problem today

Mr. Smith's problem today is that he has to manually update his whiteboard and it doesn't track how long a customer's order has been waiting to be completed. He wants to be able to quickly consult a tool that tells him when an order has taken more than 7 days to be completed. The main thing that these stale orders cost are customer satisfaction, customers do not want to be without their cars for 7 days or more.



\## Smallest useful version

The smallest useful version of this app is a read-only version that is capable of flagging an order as "stale" if it has not been completed within 7 days. Mr. Smith should be able to quickly see which orders have been open too long, and what issue needs to be resolved in order to finish the order.



\## Out of scope

For the purposes of this project the user will not be able to add new orders to the app. Also connecting to an existing dealership database, or being able to contact a customer directly through the app is not within the scope. Things that will be included, if time allows, are the ability to filter orders, update statues of orders with notes, and have a login system for the role of a service manager and an advisor.



\## Data and sensitivity
The app touches only the order number, the make and model of vehicle, and vin of vehicle. Sensitive information such as customer name and contact information is not necessary for this app, as its primary focus is on tracking repair orders that have taken too long to be completed. Currently Mr. Smith does not track customer information on his whiteboard, the order numbers are linked to the customer information in a computer system used by the dealership.



\## Is this worth building?

The biggest thing the current whiteboard system lacks is a quick way to tell when an order has taken too long to complete. The whiteboard also has to be manually updated by Mr. Smith and copying down the information by hand has introduced errors in the past. If a more automated system was in play then an app might not be necessary, but the whiteboard system is not working well and an app that could automate at least a system to flag when an order has taken more than 7 days would be beneficial.

