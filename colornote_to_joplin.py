#!/usr/bin/env python3

# Joplin importer of ColorNote CSV file (obtained by emailing "support@socialnmobile.com").
# The ColorNote CSV file named "notes.csv" needs to already be saved in this folder, with 4 or 5 columns in it.
# By Shervin Emami (http://shervinemami.com or shervin.emami@gmail.com), 2023
# Based on Ratchek's Joplin importer of ColorNote SQL db ("https://github.com/ratchek/colornote_to_joplin").

import requests
import json
import pandas as pd
from datetime import datetime
from calendar import timegm

DATABASE_LOCATION = 'notes.csv'

class JoplinConnectionError(Exception):
    def __init__(self, api_call, response_code, response_body):
        """ Takes the method you were calling, the response code and the response body """
        self.response_code = response_code
        self.response_body = response_body
        self.message = "Joplin API '{}' call returned with code {} (should be 200). Here's the content of the response: \n _____ \n {} \n _____ \n ".format(api_call, response_code, response_body)
        super().__init__(self.message)

class Database:
    """Database connection manager"""
    def __init__(self, db_location):
        df = pd.read_csv(DATABASE_LOCATION)  # Import CSV file
        self.records = [tuple(x) for x in df.values]   # Convert to a list of 4 or 5 element tuples.

class JoplinApi:
    """Rudementary and very limited Joplin API abstraction"""
    def __init__(self, port, token ):
        """Sets the connection variables and checks if connection can be established"""
        self.token_string = "?token=" + token
        self.url = "http://127.0.0.1:{}/".format(port)
        r = requests.get(self.url + "folders" + self.token_string)
        if r.status_code != 200:
            raise JoplinConnectionError("test", r.status_code, r.text)

    def create_top_level_folder(self):
        """ Create a notebook in Joplin that will contain all the imported notes."""
        #TODO add try catch block to make sure you've created the folder and are returning the id
        r = requests.post(self.url+ "folders" + self.token_string, json={'title':"Imported from ColorNote"})
        if r.status_code != 200:
            raise JoplinConnectionError("Create Folder", r.status_code, r.text)
        self.top_level_folder_id = r.json()["id"]

    def create_subcategory_folder(self, name):
        """Creates folder in the top level folder and returns it's id"""
        #TODO add try catch block to make sure you've created the folder and are returning the id
        r = requests.post(self.url+ "folders" + self.token_string, json={'title':name, 'parent_id' : self.top_level_folder_id})
        if r.status_code != 200:
            raise JoplinConnectionError("Create Subfolder", r.status_code, r.text)
        return r.json()["id"]

    def create_note(self, title, folder_id, note_body, user_created_time, user_updated_time):
        """Creates folder in the top level folder and returns it's id"""
        #TODO add try catch block to make sure you've created the folder and are returning the id
        r = requests.post(self.url+ "notes" + self.token_string, json={
            'title':title,
            'parent_id' : folder_id,
            # Note - these two replacements in the body transform the checklists so they still work
            "body" : note_body.replace("[ ]", "- [ ]").replace("[V]", "- [x]"),
            "user_created_time": user_created_time,
            "user_updated_time" : user_updated_time,
            })
        if r.status_code != 200:
            raise JoplinConnectionError("Create Note", r.status_code, r.text)

def setup():
    """ Get token, port, initialize database and joplin api classes """
    print ("Hi. ")
    print ("Before we start, make sure you've backed up your database, then modified it according to the instructions in the README. ")
    print ("\nWhat's your authorization token?  ")
    auth_token = input()
    print("\nGreat! What port is the webclipper listening on?  ")
    port_number = input()
    print("Awesome! I'll get right to it. Please hold...")

    database = Database(DATABASE_LOCATION)
    joplin = JoplinApi(port_number, auth_token)

    return (database, joplin)


# Convert the datetime string into the number of milliseconds since UNIX epoch start date
def convertDateToMS(tm):
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    seconds = timegm(datetime.strptime(tm, fmt).utctimetuple())
    milliseconds = int(seconds * 1000)
    return milliseconds


def import_notes(database, joplin):
    """ Move all the notes to a seperate folder in joplin """
    print ("--- Creating notes in Joplin parent folder ---")
    # For each of the notes, import it into the folder we just created
    counter = 0
    for record in database.records:
        created_ms = updated_ms = color_id = 0
        title = note_body = ""
        # By default, ColorNote CSV database only shows the note creation date, hence the CSV file has 4 columns and we can't know the last modified date of any notes.
        # But if you ask them for it, they will include the note modification date too, hence the CSV file has 5 columns.
        if len(record) == 4:
            created_ms = convertDateToMS(record[0])
            updated_ms = created_ms
            color_id = record[1]
            title = record[2]
            note_body = record[3]
        elif len(record) == 5:
            created_ms = convertDateToMS(record[0])
            updated_ms = convertDateToMS(record[1])
            color_id = record[2]
            title = record[3]
            note_body = record[4]
        else:
            print("ERROR: Unknown number of columns in the ColorNote CSV file!")

        # Create the note, using the webclipper interface
        joplin.create_note(title=title, folder_id=joplin.top_level_folder_id, note_body=note_body, user_created_time=created_ms, user_updated_time=updated_ms)
        counter = counter + 1
        if counter > 10:
            counter = 0
            print(".", end="", flush=True)   # Print just a "." character without a newline.
    print("Done!")

# Main function
database, joplin = setup()

joplin.create_top_level_folder()
import_notes(database, joplin)

print ("Looks like we're all done! Thanks.")
