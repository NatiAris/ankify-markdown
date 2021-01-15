import sys
import sqlite3

from paths import VIEWS, FILES


def retrieve(sheet_type, target_file, note_ids=None, excluded_tags=()):
    if sheet_type not in VIEWS or sheet_type not in FILES:
        raise Exception('Didn\'t find the sheet type in lookups')
    # db part
    QUERY_TEMPLATE = """
    select s.*
      from {sheet} s
    except
    select s.*
      from {sheet} s
      join tags t on s.id = t.note_id
     where t.tag in ({tags_to_exclude})
    """
    query = QUERY_TEMPLATE.format(sheet=VIEWS[sheet_type],
                                  tags_to_exclude=','.join(map(lambda s: "'{}'".format(s), excluded_tags)))
    with sqlite3.connect('seraviere.db') as conn:
        cards = conn.execute(query).fetchall()
    cards_written = 0
    with open(target_file, 'w', encoding='utf8', newline='\n') as f:
        header = ('UPD:{0}\n'
                  'Temp file for notes of {0} type\n'
                  '\n---\n\n').format(sheet_type)
        f.write(header)
        for card in cards:
            if note_ids is None or card[0] in note_ids:
                note_id, front, back, tags = card
                front = front
                back = back.replace('<br>', '\n')
                card = note_id, front, back, tags
                f.write('\n'.join(card))
                f.write('\n\n---\n\n')
                cards_written += 1
    print('Retrieved {} cards of {} type'.format(cards_written, sheet_type.upper()))


def get_suspended_cards():
    from anki_location import anki_db
    conn = sqlite3.connect(anki_db)
    select_suspended = """
        select distinct sfld
          from notes n
          join cards c on n.id=c.nid
         where c.queue = -1
         order by sfld
    """
    cards = [x[0] for x in conn.execute(select_suspended).fetchall()]
    return cards


def retrieve_suspended(note_type, file, excluded_tags=['.obsolete', '.suspended']):
    cards = get_suspended_cards()
    print("Retrieved suspended card list from Anki")
    retrieve(note_type, file, cards, excluded_tags=excluded_tags)


if __name__ == '__main__':
    try:
        _,note_type,file,*cards = sys.argv
    except ValueError:
        print("Usage:\npython retrieve.py note_type destination_file list_of_cards\n")
        raise
    if cards == ['--suspended']:
        retrieve_suspended(note_type, file)
    elif cards == ['--all-suspended']:
        retrieve_suspended(note_type, file, excluded_tags=['.obsolete'])
    else:
        retrieve(note_type, file, cards if cards else None)
