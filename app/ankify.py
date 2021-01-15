import os
import sys
import sqlite3
from time import strftime, gmtime
from itertools import repeat

from numpy import base_repr

from get_csv import db_to_csv
from paths import TABLES, VIEWS


def next_id(current_id):
    return base_repr(int(current_id, 36) + 1, 36)


def get_sheet_type(path):
    with open(path, encoding='utf8') as f:
        sheet_type = f.readline().strip().lower()
    return sheet_type


def md_to_db(filename, test=False):
    # md part
    sheet_type = get_sheet_type(filename)
    with open(filename, encoding='utf8', newline='\n') as f:
        # The part before the first '---' line is supposed to be file description
        # The part after the last '---' line is supposed to contain unfinished stuff
        (header, *blocks, footer) = f.read().split('\n---\n')
    cards = (block.strip().split('\n') for block in blocks)
    cards = ((front, '  \n'.join(back), tags)
             for (front, *back, tags) in cards if 1/len(back))
    # db part
    query_for_note_id = 'select max("Id") from {}'.format(VIEWS[sheet_type])
    query_for_insert = 'insert into {} values (?, ?, ?)'.format(TABLES[sheet_type])
    with sqlite3.connect('seraviere.db') as conn:
        note_id, = conn.execute(query_for_note_id).fetchone()
        note_ids = []
        for (front, back, tags) in cards:
            note_id = next_id(note_id)
            (*row, tags) = (note_id, front, back, tags)
            conn.execute(query_for_insert, row)
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
        old_header, note_ids = md_to_db(filepath)
        now = strftime('%Y%m%d%H%M%S', gmtime())
        os.rename(filepath,
                  os.path.join(os.path.dirname(filepath),
                               'past',
                               now + '.md'))
        with open(filepath, 'w', encoding='utf8', newline='\n') as f:
            f.write(old_header)
        sheet_type = get_sheet_type(filepath)
        db_to_csv(sheet_type, filepath, max_cards=len(note_ids))
    except IndexError:
        print('Usage example:',
              'python ./ankify.py raws/raw_qa.md',
              sep='\n')
