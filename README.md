#### This is a script that will import notes from your Colornote "notes.csv" file to Joplin

ColorNote used to allow exporting to a "coolornote.db" database, but this has possibly been removed. So this script supports the newer "notes.csv" file format.
If instead of a "notes.csv" file you have a "colornote.db" file, then use Ratchek's original import script at [https://github.com/ratchek/colornote_to_joplin] instead.

## The "Why?"
Colornote unfortunately doesn't allow you to export your data in any way (aside from exporting each note one by one). So if you aren't using it, **don't start now**. If you were and want to switch to a different app, this tool might be for you.
##### Why Joplin? Why not csv or markdown or another format?
Mainly because it's the app I intend on using. Also because it has an API that will enable me to keep the creation and modification dates intact in each note.
After you import this into Joplin, feel free to use its export options and get whatever format you'd like.
So, what will this tool preserve?
 * Title
 * Body
 * Creation date
 * Modification date

**Note**: this tool will *not* preserve the color category, creation date for folders, any geolocation data, tags, or anything besides what's listed above. So MAKE SURE YOU HAVE A BACKUP OF YOUR DATABASE.
### **I AM NOT RESPONSIBLE FOR ANY LOST DATA**

## The "How?"
##### Prerequisites:
 * You need python or python3 installed on your system.
 * You need to have the  *requests*, *sqlite3*, and *json* modules installed (but they come pre-installed with python 3, so try not to worry about it)

##### Prepping the CSV database
 * First you need to *get* the CSV database used by ColorNote. If you enabled online backups in ColorNote, you can get the CSV database by emailing "support@socialnmobile.com" and asking for the database as a CSV file, INCLUDING the last modified date. (Note: If you don't specifically ask for the last modified date to be included, they're likely to only include the note creation date. This script will still import your CSV file, but it won't be as useful as if your CSV includes the last modified date).
* Copy the CSV database file into the folder containing *colornote_to_joplin.py* and make sure it's named "notes.csv", which is typically the filename in the zip file from Social'N'Mobile.

##### Prepping Joplin
 * Open Joplin
 * Go to Tools -> Options -> Webclipper
 * Enable the webclipper service
 * Copy the API key (it's near the bottome of that page) and port number (it's near the top of the page. Above the "disable web clipper service" button. Default is 41184)

## Zhu Li, Do The Thing!
 * Open a terminal and navigate to the folder where the program and database are stored.
 * While Joplin is running on your PC, run this script by typing "./colornote_to_joplin.py" or "python3 colornote_to_joplin.py"
 * Paste the API key and port number from Joplin when prompted.
 * This may take a while, depending on the ammount of notes you have. Don't freak out.
 * You're done! Congrats.

## The Troubleshooting
 * .

## Thanks for Ratchek for the original importer script!
