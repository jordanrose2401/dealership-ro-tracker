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

