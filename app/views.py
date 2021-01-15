ab_sheet = """
  create view ab_sheet as
  select id                     AS "Id",
         front                  AS "Front",
         back                   AS "Back",
         group_concat(tag, ' ') AS "Tags"
    from notes_ab n
    left join tags t on n.id=t.note_id
   group by id
   order by id
"""

qa_sheet = """
  create view qa_sheet as
  select id                     AS "Id",
         front                  AS "Front",
         back                   AS "Back",
         group_concat(tag, ' ') AS "Tags"
    from notes_qa n
    left join tags t on n.id=t.note_id
   group by id
   order by id
"""

tag_desc = """
  create view tag_desc as
  select front AS tag,
         back  AS description
    from notes_ab ab
    join tags t on ab.id=t.note_id
   where t.tag = '.tag'
"""

tag_desc_and_counts = """
  create view tag_desc_and_counts as
    with all_tags as (
      select tag from tags
       union
      select tag from tag_desc
    ), counts as (
      select tag,
             count(1) as cards
        from tags
       group by tag
    )
  select all_tags.tag, d.description, counts.cards
    from all_tags
    left join tag_desc d on all_tags.tag=d.tag
    left join counts on all_tags.tag=counts.tag
"""

