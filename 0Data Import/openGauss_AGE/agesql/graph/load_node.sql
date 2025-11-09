select * from load_labels_from_file('ldbc',   'forum',   '/data/dynamic/Forum.csv');
select * from load_labels_from_file('ldbc',   'post',   '/data/dynamic/Post.csv');
select * from load_labels_from_file('ldbc',   'comment',   '/data/dynamic/Comment.csv');
select * from load_labels_from_file('ldbc',   'organisation',   '/data/static/Organisation.csv');
select * from load_labels_from_file('ldbc',   'person',   '/data/dynamic/Person.csv');
select * from load_labels_from_file('ldbc',   'place',   '/data/static/Place.csv');
select * from load_labels_from_file('ldbc',   'tag',   '/data/static/Tag.csv');
select * from load_labels_from_file('ldbc',   'tagclass',   '/data/static/TagClass.csv');