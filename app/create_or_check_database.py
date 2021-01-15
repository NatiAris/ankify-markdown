import sqlite3

import ddl
import views

conn = sqlite3.connect('./seraviere.db')

# Create if not exists, we're not ok with randomly dropping tables with data
conn.execute(ddl.create_table_notes_ab)
conn.execute(ddl.create_table_notes_qa)
conn.execute(ddl.create_table_tags)

# We're ok with dropping views, though
conn.execute('drop view if exists ab_sheet')
conn.execute(views.ab_sheet)
conn.execute('drop view if exists qa_sheet')
conn.execute(views.qa_sheet)
conn.execute('drop view if exists tag_desc')
conn.execute(views.tag_desc)

