CREATE UNIQUE PROPERTY INDEX ON forum ("id");
CREATE UNIQUE PROPERTY INDEX ON message      ("id");
CREATE UNIQUE PROPERTY INDEX ON post         ("id");
CREATE UNIQUE PROPERTY INDEX ON Comment    ("id");
CREATE UNIQUE PROPERTY INDEX ON organisation ("id");
CREATE UNIQUE PROPERTY INDEX ON person       ("id");
CREATE UNIQUE PROPERTY INDEX ON place        ("id");
CREATE UNIQUE PROPERTY INDEX ON tag          ("id");
CREATE UNIQUE PROPERTY INDEX ON tagclass     ("id");
CREATE PROPERTY INDEX ON message   ( "creationDate");
CREATE PROPERTY INDEX ON post      ( "creationDate");
CREATE PROPERTY INDEX ON Comment ( "creationDate");
CREATE PROPERTY INDEX ON hasmember ( "creationDate");
CREATE PROPERTY INDEX ON knows ( "creationDate");
CREATE PROPERTY INDEX ON hasCreator ( "creationDate");
CREATE PROPERTY INDEX ON hascreatorcomment ( "creationDate");
CREATE PROPERTY INDEX ON hascreatorpost ( "creationDate");



CREATE INDEX hascreatorcomment_start ON ldbc.hascreatorcomment ("start");
CREATE INDEX hascreatorcomment_end ON ldbc.hascreatorcomment ("end");

CREATE INDEX hascreatorpost_start ON ldbc.hascreatorpost ("start");
CREATE INDEX hascreatorpost_end ON ldbc.hascreatorpost ("end");


CREATE INDEX hascreator_start ON ldbc.hascreator ("start");
CREATE INDEX hascreator_end ON ldbc.hascreator ("end");
CREATE INDEX knows_start ON ldbc.knows ("start");
CREATE INDEX knows_end ON ldbc.knows ("end");

CREATE INDEX hastag_start ON ldbc.hastag ("start");
CREATE INDEX hastag_end ON ldbc.hastag ("end");

CREATE INDEX hastagpost_start ON ldbc.hastagpost ("start");
CREATE INDEX hastagpost_end ON ldbc.hastagpost ("end");

CREATE INDEX  hasInterest_start ON ldbc.hasInterest ("start");
CREATE INDEX  hasInterest_end ON ldbc.hasInterest ("end");

CREATE INDEX  hasMember_start ON ldbc.hasMember ("start");
CREATE INDEX  hasMember_end ON ldbc.hasMember ("end");

CREATE INDEX  containerOf_start ON ldbc.containerOf ("start");
CREATE INDEX  containerOf_end ON ldbc.containerOf ("end");

CREATE INDEX  studyAt_start ON ldbc.studyAt ("start");
CREATE INDEX  studyAt_end ON ldbc.studyAt ("end");

CREATE INDEX  workAt_start ON ldbc.workAt ("start");
CREATE INDEX  workAt_end ON ldbc.workAt ("end");

CREATE INDEX  isLocatedInOrgan_start ON ldbc.isLocatedInOrgan ("start");
CREATE INDEX  isLocatedInOrgan_end ON ldbc.isLocatedInOrgan ("end");

CREATE INDEX  isLocatedInPerson_start ON ldbc.isLocatedInPerson ("start");
CREATE INDEX  isLocatedInPerson_end ON ldbc.isLocatedInPerson ("end");

create index replyofpost_start  on ldbc.replyofpost ("start");
create index replyofpost_end  on ldbc.replyofpost ("end");
create index replyofcomment_start  on ldbc.replyofpost ("start");
create index replyofcomment_end  on ldbc.replyofpost ("end");

create index hasmoderator_start on ldbc.hasmoderator ("start");
create index hasmoderator_end on ldbc.hasmoderator ("end");

create index likespost_start  on ldbc.likespost ("start");
create index likespost_end  on ldbc.likespost ("end");
create index likescomment_start  on ldbc.likescomment ("start");
create index likescomment_end  on ldbc.likescomment ("end");