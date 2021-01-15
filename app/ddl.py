# Two-sided notes
create_table_notes_ab = """
create table if not exists notes_ab
(
      id text,
   front text,
    back text,
    
 PRIMARY KEY(id)
)
"""

# One-sided notes
create_table_notes_qa = """
create table if not exists notes_qa
(
      id text,
   front text,
    back text,
    
 PRIMARY KEY(id)
)
"""

# The join table for notes/tags n:m relation
create_table_tags = """
create table if not exists tags
(
 note_id text,
     tag text,

 PRIMARY KEY(note_id, tag)
)
"""

