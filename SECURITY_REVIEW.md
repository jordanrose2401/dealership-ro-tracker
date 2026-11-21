\### What data does the app hold, and what would happen if all of it leaked?  

My repair order tracker app only holds synthetic data of customer repair orders. This includes the order number, the number of days the order has been open, the make and model of the customer's vehicle, the last 4 characters of the vehicle's VIN, and the status of either "STALE" or "OK" depending on whether or not the number of days the order has been opened is greater than 7. The order number is the key to the customer's records in the dealership's other system, this order number is therefore harmless because the link to the actual customer information is out of reach.  

None of this data is sensitive for the customer, the only part would be the VIN, but the app never even has access to anymore than the last 4 characters of any given VIN, the loader doesn't even load that information.  



\### Who can reach it, and what can they do?  



Anyone with a link can reach this app, but as there is no user input allowed therefore they can't do anything beyond viewing what the app allows them to view. Trying to run a script on the app results in nothing happening, and viewing the page source only results in the last 4 characters of each VIN being accessible. Someone could send many requests if they wanted, but this is limited by the free hosting.  



\### Where does the app take in data from outside that it has to trust?  



This app takes no user input so the only outside data is from the imported synthetic data from the CSV.  



\### What does the app tell people when it fails?  



It depends on the failure, but in general it displays a plain-English error message about the specific type of failure. For example if the database exists but has no open orders the app displays "No open orders to display." If the database is missing it displays "No data loaded, run the loader."  



\### What outside code does it depend on?  

It depends on outside code from Flask, Jinja2, Werkzeug, and Gunicorn. As well as GitHub and Render as it uses those services.    



\### What would have to change before real data went in?  



A real data feed would need a login so only the right people have access to it, it would also be hosted by the company and not a public free host. A decision would be needed on how long to store the raw files and a security review.    



|**Issue**|**Risk if ignored**|**Decision**|**Why**|
|-|-|-|-|
|No login on a public URL|Anyone with the link sees backlog and delay reason|Accept for prototype|The data is synthetic and a real version would use a company sign-in.|
|Outside packages (Flask, Gunicorn, etc.) may have known vulnerabilities|A vulnerable library in a public app|Fix now |Run pip-audit (done with result: No known vulnerabilities found as of 11/20/2026), keep versions pinned|
|Anyone who can push to main changes the live site|A stolen GitHub login could deploy bad code|Fix now (already done)|Turn on 2FA. A real team would require code review|
|The CSV is the only outside input|A bad row could crash the page or display unsafe text|Fix now (already done)|Loader checks rows, database enforces rules again, and templates escape output|
|Real customer data would pass through the loader|A real feed could include sensitive customer data|Later/real version|The data is synthetic, and with a real data feed only certain columns could be selected and data could only be stored for a set period of time.|
|404 page and error logs|Error pages could reveal file paths, library versions, and lines of code|Fix now (already done)|Errors are general messages and actual error messages only go to logs. For example attempting to visit /anything results in just a 404 page, and no actual error messages.|
|Anyone has access to my public repository|Possible disclosure of personal information or secrets|Fix now (already done)|There are no secrets in this app, email privacy settings enabled on GitHub to hide personal information.|
|Dependency checks are manual|A new vulnerability in a library could go unnoticed between manual runs of pip-audit|Later/real version|A real version runs a scanner automatically on every change. GitHub also has a built-in dependency alert feature.|



