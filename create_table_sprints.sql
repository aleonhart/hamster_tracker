
/*
Connect to db:
$ sqlite3 hamstrometer.db
or
$ sqlite3
> attach "mydb.sqlite" as db1;

Show tables:
> .tables

describe tables:
> .schema sprints

insert syntax:
> INSERT INTO TABLE_NAME (column1, column2, column3,...columnN)]
VALUES (value1, value2, value3,...valueN);

*/


CREATE TABLE sprints(
    id INTEGER PRIMARY KEY,
    start_datetime DATETIME UNIQUE,
    end_datetime DATETIME UNIQUE,
    rotations INTEGER
);
