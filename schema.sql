drop table if exists problem;
create table problem (
	id integer primary key autoincrement,
	description string not null
);

drop table if exists idea;
create table idea (
	id integer primary key autoincrement,
	description string not null
);

drop table if exists problemidea;
create table problemidea (
	id integer primary key autoincrement,
	problem_id integer not null,
	idea_id integer not null
);
