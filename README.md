# RareishMCNameAvailabilityChecker
[Flask](https://flask.palletsprojects.com/en/stable/) program which cycles through all 3 and 4 letter accepted [Minecraft](https://www.minecraft.net) account usernames, checking their availability using [PlayerDB.co](https://playerdb.co/) and displaying the results on a localhost webpage. Made this because I wanted a "rare" Minecraft username. :)

# Usage

1. Install Python 3.12.7+ at https://www.python.org/downloads/.
2. [Download the source files for the program.](https://github.com/redbackspider77/RareishMCNameAvailabilityChecker/archive/refs/heads/main.zip)
3. Extract the zip file wherever you want.
4. Run `app.py` where you extracted the zip file.
5. Go to the development server link, typically http://127.0.0.1:5000/. <img src="/assets/link.png" align="right"/>
* Press `Start` to start cycling through 3 and 4 letter usernames.
* Press `Stop` to stop cycling.
* Press `Reset` to clear cache to be able to restart from `aaa`.
* You will be able to see available (status code `400`) and taken usernames (status code `200`) on the webpage.
* "Rate-limited usernames" include those who were hit with status code `429`.
* "Other usernames" encountered any other status code.
* "Error usernames" are those who encountered an exception in the program unexpectedly.
* Cache of all checked usernames is saved in `username_cache.json`.
