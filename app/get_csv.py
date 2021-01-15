import os
import sys
import sqlite3

import pandas as pd
import pypandoc

from paths import VIEWS, FILES


def escape_latex(s):
    return s.replace('[$]', '&#91;$&#93;').replace('[$$]', '&#91;$$&#93;')


def unescape_latex(s):
    s = s.replace('&#91;$&#93;', '[$]').replace('&#91;$$&#93;', '[$$]')
    return s.replace('&#91;$&#93;', '[$]').replace('&#91;$$&#93;', '[$$]')


def md_to_html(str_md):
    str_md = escape_latex(str_md)
    str_html = pypandoc.convert_text(str_md, 'html', 'markdown_github', extra_args=['--eol=lf'])
    str_html = unescape_latex(str_html)
    return str_html.strip()


def db_to_csv(sheet_type, filename, cards=None, max_cards=None):
    if sheet_type not in VIEWS or sheet_type not in FILES:
        raise Exception('Didn\'t find the sheet type in lookups')
    # db part
    query = 'select * from {}'.format(VIEWS[sheet_type])
    with sqlite3.connect('seraviere.db') as conn:
        df = pd.read_sql(query, conn)
    # subsetting part
    if cards is not None:
        df = df[df.Id.isin(cards)]
    if max_cards is not None:
        df = df.tail(max_cards)
    # csv part
    df.Front = df.Front.apply(md_to_html)
    df.Back = df.Back.apply(md_to_html)
    sheet = os.path.join(os.path.dirname(filename), 'csv', FILES[sheet_type])
    print('DataFrame for {} sheet csv unload is prepared, {} lines included'.format(sheet_type, len(df)), flush=True)
    df.to_csv(sheet, index=False, encoding='utf8', header=False, line_terminator='\n')


if __name__ == '__main__':
    # Expects path where csv usually lie
    filepath = sys.argv[1]
    max_cards = sys.argv[2] if len(sys.argv) > 2 else None
    for sheet_type in VIEWS:
        db_to_csv(sheet_type, filepath, max_cards=max_cards)
