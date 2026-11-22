I chose this project to practice building a simple internal app with Claude Code, using synthetic data, for the kind of work described in a role I’m applying for. The app focuses on handling customer information carefully: showing staff only what they need.  
A service repair-order tracker matches the job description closely but is small enough to finish and understand in a short time.

Accidently created a nested dealership-ro-tracker folder when attempting to clone it. Moved my git project to my C drive to avoid conflicts with OneDrive from my Documents folder.  
Checked with git status and git log to make sure that only an empty shell was being deleted when I deleted the dealership project in my OneDrive Documents folder.  
Learned about git pull, and how to tell where I am in my drive architecture when using the terminal.

Created INTAKE.md. Updated twice based on critique from Claude.

Created DATA\_DESIGN.md which lead to updating INTAKE.md to better reflect current design ideology.  
Updated DATA\_DESIGN.md to better reflect what information will be stored, calculated, and displayed to Mr. Smith. Also updated INTAKE.md to reflect these changes.  
Updated python to 3.15.2 for use on this project. Went with default options in the installer except I chose to add python to PATH. Created a virtual python environment so that nothing else would be interfered with on my machine. Checked that python was up to date and my virtual environment was working in my project terminal.

I created PROMPT\_DRAFT.md to determine what my first prompt using Claude Code should actually look like. I had several rounds of revision based on feedback from Claude Chat.  
Ran my first prompt in Claude Code, for now all it's done it create a script (using python) and a script folder that (when run) will generate seed data for the eventual app. I have instructed it to created a "good" set of data (one that follows all the rules I've laid out) and a "bad" set of data (one that breaks rules I've laid out to test cases that should be rejected by the loader later).

Gained an understanding of what a branch is in git. Ran my code in a separate branch from the main to maintain main branch integrity. Also came to understand the idea of hashing as a verb. A hash is basically just a unique code that tell you if two things are the same. Two things with the same characters will have the exact same hash and even if one character changes the hash changes completely. Very useful to quickly recognize if something has changed, but with no information about how big of a change occurred. The script I wrote generates data based on today's date, so that it is always up-to-date. When it generates orders it generates the dates opened by using today's date minus an integer number of days. The app will do the reverse. It will take the dates generated and calculate how many days the order has been open based on the current day.  
Merged the feature branch to the main after confirming that the script worked as intended. Finalized wording in INTAKE.md and DATA\_DESIGN.md documents.

Created a prompt for the loader, and went through several revisions per Claude recommendations.  
Ran loader prompt and modified the plan slightly before running and creating the loader script.

Decided that the CSVs would store the full VINs but the loader would only load in the last 4 characters, but only after checking that the VIN was valid first. This addresses a security concern, if the database the information is stored in is ever breached, it never held the full VINs to begin with.

Merged feature branch with main and deleted feature branch.

Created a prompt draft for the Flask board, then revised prompt.
Ran prompt, made slight revisions to plan before approving for Claude Code to build.
Tested board for expected behavior, 6 passed tests and "4 of 9 open orders are stale." Changed database name to test if the correct error would be displayed, which it was. Also tested that errors testing the staleness condition would trigger if I modified STALE\_AFTER\_DAYS variable from 7 to 6. Correct tests failed under these condition.
Finally merged board branch with main branch on GitHub, and deleted board branch locally.  
Setup hosting through Render and deployed v1 of the app. Set the time zone to Utah time in the settings on Render to agree with the idea that the app would be used by a user in Utah. Also did a test after 5 PM Utah time to make sure it still showed the correct date (November 19) which confirmed that it was using Utah time and not UTC. Also of note I'm use the free hosting option, so if the webpage is not in use for more than 15 minutes it needs around 50 seconds for the server to wake up when going back to the page. In this app the data\_gen.py script running first as part of the start command is simulating receiving a fresh feed of data from some dealership database every time the webpage is reloaded. If this were only run as part of the build command the "Days Open" would continually add a day for every day since the build was completed, this is the fix to simulate a real data feed. The database is similarly generated every time as part of the start command, but only if the data generation runs successfully. One limitation of this is that the webpage only updates on reload, so if it were kept open over a midnight threshold the page wouldn't be accurate until it was reloaded.

Also pinned gunicorn to an exact version in requirements.txt because it was the only package in requirements.txt that was not pinned to a specific version.

Created the feature/security-review-and-readme branch. Answered six security questions and revised answers based on Claude feedback.

Received note on compliance and tools like Snyk, so decided to run pip-audit to check for vulnerabilities (none found) and turned on 2FA on GitHub.

Confirmed Render's auto-deploy was set to "On-Commit" which means merging to main publishes the site.

Built the security findings table and learned to name specific bad scenarios, and what stops each.

Found my real email on GitHub was attached to branch merger commits, so changed the setting on GitHub. Chose to accept the risk of having my email visible on those commits.

Modified plan based on new information about time schedule, therefore cut login and documented it as a deliberate decision.

Drafted README and revised with input from Claude chat.  
Merged security branch to main which triggered a new deploy on Render, which it did. Everything worked as expected.  

Fixed markdown formatting on my markdown documents on GitHub, then pulled the fixed files. Since I committed these changes directly to main (which I know is generally a bad idea), each triggered a site deploy. These were very small aesthetic changes, which is why I was comfortable committing the directly to main.  

