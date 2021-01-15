import os
import sys
import sqlite3
from time import strftime, gmtime
from itertools import repeat

from get_csv import db_to_csv
from paths import TABLES


def get_sheet_type(path):
    with open(path, encoding='utf8') as f:
        sheet_type = f.readline().strip().lower()
    if sheet_type.startswith('upd:'):
        sheet_type = sheet_type[4:]
    else:
        raise Exception("Expected a file of upd:XX type")
    return sheet_type


def update(filename, test=False):
    # md part
    sheet_type = get_sheet_type(filename)
    with open(filename, encoding='utf8', newline='\n') as f:
        # The part before the first '---' line is supposed to be file description
        # The part after the last '---' line is supposed to contain unfinished stuff
        (header, *blocks, footer) = f.read().split('\n---\n')
    cards = (block.strip().split('\n') for block in blocks)
    cards = ((note_id, front, '  \n'.join(back), tags)
             for note_id, front, *back, tags in cards if 1/len(back))
    # db part
    query_for_update = 'update {} set front=?, back=? where id=?'.format(TABLES[sheet_type])
    query_for_check = 'select * from {} where id=?'.format(TABLES[sheet_type])
    with sqlite3.connect('seraviere.db') as conn:
        note_ids = []
        for (note_id, front, back, tags) in cards:
            # There should be exactly one record for the id
            assert len(conn.execute(query_for_check, (note_id,)).fetchall()) == 1
            conn.execute(query_for_update, (front, back, note_id))
            # Remove and recreate tags
            conn.execute('delete from tags where note_id=?', (note_id,))
            tag_list = tags.split()
            conn.executemany('insert or replace into tags values (? ,?)',
                             zip(repeat(note_id), tag_list))
            note_ids.append(note_id)
            print('Card #', note_id, 'will be added to', TABLES[sheet_type], flush=True)
        if test:
            conn.rollback()
    return (header + '\n---\n' + footer), note_ids


if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
        # Expects an .md formatted file
        # Uses md_to_db to add the cards into the database
        # Moves old file to the past directory (to prevent duplication)
        # Creates a new file in place of the old header
        # Uses db_to_csv to produce ankifiable file
        old_header, note_ids = update(filepath)
        now = strftime('%Y%m%d%H%M%S', gmtime())
        os.rename(filepath,
                  os.path.join(os.path.dirname(filepath),
                               'past',
                               now + '.md'))
        with open(filepath, 'w', encoding='utf8', newline='\n') as f:
            f.write(old_header)
        sheet_type = get_sheet_type(filepath)
        db_to_csv(sheet_type, filepath, note_ids)
    except IndexError:
        print('Usage example:',
              'python ./ankify.py raws/raw_qa.md',
              sep='\n')
