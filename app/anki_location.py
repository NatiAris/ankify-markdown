import os

# replace USERNAME and PROFILENAME or whatever else is needed to get a path to your .anki2 file
# you can list more than one location to make this thing work on different OS
location_candidates = [
    r"C:\Users\USERNAME\AppData\Roaming\Anki2\PROFILENAME\collection.anki2",
    r"/Users/USERNAME/Library/Application Support/Anki2/PROFILENAME/collection.anki2",
]

for location in location_candidates:
    if os.path.isfile(location):
        anki_db = location
        break
else:
    raise Exception("Couldn't find the collection")

