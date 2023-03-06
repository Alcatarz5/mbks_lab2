create table access_marks(
    id integer primary key not null,

    description text not null
);

create table users(
    id integer primary key generated always as identity,

    access_mark integer references access_marks(id) on delete cascade,

	name text not null

);

create table objects(
    id integer primary key generated always as identity,

    user_id integer references users(id) on delete cascade,

    secure_mark integer not null,
    file_uri text not null
);

alter table objects
    add column name text not null